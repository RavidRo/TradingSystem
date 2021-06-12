from threading import Lock

from sqlalchemy import Column, Integer, Sequence, Index, String, ForeignKey, Table
from sqlalchemy import func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, mapper_registry, db_fail_response
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock

id_seq = Sequence('nodes_id_seq')


class Responsibility_DAL:

    def __init__(self, parent=None):
        _id = engine.execute(id_seq)
        self.id = _id
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id


class Manager_Responsibility_DAL(Responsibility_DAL):
    pass


class Owner_Responsibility_DAL(Responsibility_DAL):
    pass


class Founder_Responsibility_DAL(Responsibility_DAL):
    pass


class ResponsibilitiesHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Responsibility)
        from Backend.DataBase.Handlers.member_handler import MemberHandler
        self.__member_handler = MemberHandler.get_instance()
        self.__responsibilities = dict()  # responsibilities cache

        self.__responsibilities_table = Table('responsibilities', mapper_registry.metadata,
                                              Column('id', Integer, id_seq, primary_key=True),
                                              Column('path', LtreeType, nullable=False),
                                              Column('type', String(10)),
                                              Index('ix_nodes_path', 'path', postgresql_using='gist'))

        mapper_registry.map_imperatively(Responsibility_DAL, self.__responsibilities_table, properties={
            'id': self.__responsibilities_table.c.id,
            'path': self.__responsibilities_table.c.path,
            'parent': relationship(
                'Responsibility_DAL',
                primaryjoin=(remote(self.__responsibilities_table.c.path) == foreign(
                    func.subpath(self.__responsibilities_table.c.path, 0, -1))),
                backref='appointed',
                viewonly=True
            )
        }, polymorphic_on=self.__responsibilities_table.c.type)

        mapper_registry.map_imperatively(Founder_Responsibility_DAL, self.__responsibilities_table, inherits=Responsibility_DAL,
                                         polymorphic_identity='founder')

        mapper_registry.map_imperatively(Owner_Responsibility_DAL, self.__responsibilities_table, inherits=Responsibility_DAL,
                                         polymorphic_identity='owner')

        mapper_registry.map_imperatively(Manager_Responsibility_DAL, self.__responsibilities_table, inherits=Responsibility_DAL,
                                         polymorphic_identity='manager')

    @staticmethod
    def get_instance():
        with ResponsibilitiesHandler._lock:
            if ResponsibilitiesHandler._instance is None:
                ResponsibilitiesHandler._instance = ResponsibilitiesHandler()
        return ResponsibilitiesHandler._instance

    def save_res(self, class_type, parent=None):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            responsibility_dal = class_type(parent)
            session.add(responsibility_dal)
            res = Response(True, obj=responsibility_dal)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def load_res_and_appointments(self, res_id, store):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            if self.__responsibilities.get(res_id) is None:
                res_root = session.query(Responsibility_DAL).filter(Responsibility_DAL.id == res_id).one()
                responsibility_res = self.create_responsibilities(res_root, store)
                if responsibility_res.succeeded():
                    self.__responsibilities[res_id] = responsibility_res.get_obj()
                res = responsibility_res
            else:
                res = Response(True, obj=self.__responsibilities[res_id])
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def remove_res(self, responsibility):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            responsibility_dal = responsibility.get_dal_responsibility()
            # I think this isn't removing the subtree like it suppose to do...
            session.delete(responsibility_dal)
            res = Response(True)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def create_responsibilities(self, res_root, store):
        member_of_res = self.__member_handler.load_user_with_res(res_root.id)
        if not member_of_res.succeeded():
            return member_of_res
        res = self.__create_responsibility_from_type(res_root.type, store)
        res.set_dal_responsibility_and_id(res_root)
        res.set_username(member_of_res.get_obj().get_username().get_obj().get_val())
        appointments = [self.create_responsibilities(child, store) for child in res_root.appointed]
        if any([not appointment.succeeded() for appointment in appointments]):
            return db_fail_response
        res.set_appointments([appointment.get_obj() for appointment in appointments])
        return Response(True, res)

    def __create_responsibility_from_type(self, responsibility_type, store):
        if responsibility_type == "founder":
            from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
            return Founder(None, store)
        elif responsibility_type == "owner":
            from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
            return Owner(None, store)
        else:
            from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
            return Manager(None, store)
