import enum
from threading import Lock

from sqlalchemy import Column, Integer, Sequence, Index, String, Table, select
from sqlalchemy import func, create_engine
from sqlalchemy import TypeDecorator, cast
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import relationship, remote, foreign, column_property
from sqlalchemy_utils import LtreeType, Ltree
import re
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, mapper_registry, db_fail_response
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility, Permission
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock

id_seq = Sequence('nodes_id_seq')

class ArrayOfEnum(TypeDecorator):

    impl = ARRAY

    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)

            return inner.split(",") if inner else []

        def process(value):
            if value is None:
                return None

            return super_rp(handle_raw_string(value))

        return process


class Responsibility_DAL:

    def __init__(self, username, store_id, parent=None):
        _id = engine.execute(id_seq)
        self.id = _id
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id
        self.permissions = []
        self.username = username
        self.store_id = store_id


class Manager_Responsibility_DAL(Responsibility_DAL):
    def __init__(self, username, store_id, parent=None):
        super().__init__(username, store_id, parent)
        self.permissions = [Permission.GET_APPOINTMENTS.value]


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
                                              Column('manager_permissions', ARRAY(Integer)),
                                              Column('username', String(30)),
                                              Column('store_id', String(50)),
                                              Index('ix_nodes_path', 'path', postgresql_using='gist'))

        mapper_registry.map_imperatively(Responsibility_DAL, self.__responsibilities_table, properties={
            'id': self.__responsibilities_table.c.id,
            'path': self.__responsibilities_table.c.path,
            'username': self.__responsibilities_table.c.username,
            'store_id': self.__responsibilities_table.c.store_id,
            'parent': relationship(
                'Responsibility_DAL',
                primaryjoin=(remote(self.__responsibilities_table.c.path) == foreign(
                    func.subpath(self.__responsibilities_table.c.path, 0, -1))),
                backref='appointed',
                viewonly=True
            ),
            "permissions": column_property(self.__responsibilities_table.c.manager_permissions),
        }, polymorphic_on=self.__responsibilities_table.c.type)

        mapper_registry.map_imperatively(Founder_Responsibility_DAL, self.__responsibilities_table, inherits=Responsibility_DAL,
                                         polymorphic_identity='founder')

        mapper_registry.map_imperatively(Owner_Responsibility_DAL, self.__responsibilities_table, inherits=Responsibility_DAL,
                                         polymorphic_identity='owner')

        mapper_registry.map_imperatively(Manager_Responsibility_DAL, self.__responsibilities_table,
                                         inherits=Responsibility_DAL,
                                         polymorphic_identity='manager')

    @staticmethod
    def get_instance():
        with ResponsibilitiesHandler._lock:
            if ResponsibilitiesHandler._instance is None:
                ResponsibilitiesHandler._instance = ResponsibilitiesHandler()
        return ResponsibilitiesHandler._instance

    def save_res(self, class_type, username, store_id, parent=None):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            responsibility_dal = class_type(username, store_id, parent)
            session.add(responsibility_dal)
            res = Response(True, obj=responsibility_dal)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def __save_children(self, responsibility):
        for appointed in responsibility._appointed:
            # self.__responsibilities[appointed.get_dal_responsibility_id()] = appointed
            self.__save_children(appointed)

    def load_res_and_appointments(self, res_id, store):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            if self.__responsibilities.get(res_id) is None:
                res_root = session.query(Responsibility_DAL).filter(Responsibility_DAL.id == res_id).one()
                responsibility_res = self.create_responsibilities(res_root, store)
                if responsibility_res.succeeded():
                    # self.__responsibilities[res_id] = responsibility_res.get_obj()
                    self.__save_children(responsibility_res.get_obj())
                res = responsibility_res
            else:
                res = Response(True, obj=self.__responsibilities[res_id])
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_responsibilities_by_username(self, username):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            reses = session.query(Responsibility_DAL).filter_by(username=username).all()
            session.commit()
            responsibilities = []

            from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
            from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
            from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
            for responsibility_dal in reses:
                responsibility = Founder(None, None) if responsibility_dal.type == 'founder' else Owner(None, None) if responsibility_dal.type == 'owner' else Manager(None, None)
                responsibility.set_username(username)
                responsibility.set_store_id(responsibility_dal.store_id)
                responsibilities.append(responsibility)
            res = Response(True, responsibilities)
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
            whole_subtree = session.query(Responsibility_DAL).filter(Responsibility_DAL.path.descendant_of(responsibility_dal.path)).all()
            session.delete(responsibility_dal)
            for responsibility in whole_subtree:
                session.delete(responsibility)
            res = Response(True)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def create_responsibilities(self, res_root, store):
        # member_of_res = self.__member_handler.load_user_with_res(res_root.id)
        # if not member_of_res.succeeded():
        #     return member_of_res
        res = self.__create_responsibility_from_type(res_root, store)
        res.set_dal_responsibility_and_id(res_root)
        # res.set_username(member_of_res.get_obj().get_username().get_obj().get_val())
        appointments = [self.create_responsibilities(child, store) for child in res_root.appointed]
        if any([not appointment.succeeded() for appointment in appointments]):
            return db_fail_response
        res.set_appointments([appointment.get_obj() for appointment in appointments])
        return Response(True, res)

    def __create_responsibility_from_type(self, responsibility_dal, store):
        if responsibility_dal.type == "founder":
            from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
            return Founder(None, store)
        elif responsibility_dal.type == "owner":
            from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
            return Owner(None, store)
        else:
            from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
            manager = Manager(None, store)
            manager.set_permissions(responsibility_dal.permissions)
            return manager

    def add_permission(self, res_id, permission):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            manager_dal = session.query(Responsibility_DAL).filter(Responsibility_DAL.id == res_id).one()
            perms = manager_dal.permissions
            manager_dal.manager_permissions = None
            manager_dal.permissions = perms + [permission.value]
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def remove_permission(self, res_id, permission):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            manager_dal = session.query(Responsibility_DAL).filter(Responsibility_DAL.id == res_id).one()
            perms = manager_dal.permissions
            manager_dal.manager_permissions = None
            manager_dal.permissions = list(set(perms) - {permission.value})
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res