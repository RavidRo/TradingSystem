from threading import Lock

from sqlalchemy import Column, Integer, Sequence, Index, String, ForeignKey
from sqlalchemy import func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, Base
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock

id_seq = Sequence('nodes_id_seq')


class Responsibility_DAL(Base):
    __tablename__ = 'responsibilities'

    id = Column(Integer, id_seq, primary_key=True)
    path = Column(LtreeType, nullable=False)
    responsibility_type = Column('type', String(50))
    parent = relationship(
        'Responsibility_DAL',
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref='appointed',
        viewonly=True
    )
    __mapper_args__ = {'polymorphic_on': responsibility_type}

    __table_args__ = (
        Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __init__(self, parent=None):
        _id = engine.execute(id_seq)
        self.id = _id
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id


class Manager_Responsibility_DAL(Responsibility_DAL):
    __mapper_args__ = {'polymorphic_identity': 'manager'}


class Owner_Responsibility_DAL(Responsibility_DAL):
    __mapper_args__ = {'polymorphic_identity': 'owner'}


class Founder_Responsibility_DAL(Responsibility_DAL):
    __mapper_args__ = {'polymorphic_identity': 'founder'}


Base.metadata.create_all(engine)


class ResponsibilitiesHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Responsibility)
        from Backend.DataBase.Handlers.member_handler import MemberHandler
        self.__member_handler = MemberHandler.get_instance()

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
            res_root = session.query(Responsibility_DAL).filter(Responsibility_DAL.id == res_id).one()
            responsibilities = self.create_responsibilities(res_root, store)
            res = Response(True, obj=responsibilities)

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
            session.delete(responsibility_dal)
            res = Response(True)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def create_responsibilities(self, res_root, store):
        from Backend.Domain.TradingSystem.user_manager import UserManager
        from Backend.Domain.TradingSystem.States.member import Member
        from Backend.Domain.TradingSystem.stores_manager import StoresManager
        member_of_res: Member = UserManager.get_member(res_root.id).get_obj()
        ids = self.__member_handler.load_res_ids(member_of_res.get_username().get_obj().get_val()).get_obj()
        member_of_res.set_responsibility_ids(ids)
        store_id_to_res = StoresManager.get_store_id_to_responsibilities(ids)
        member_of_res.set_responsibilities(store_id_to_res)

        res = self.__create_responsibility_from_type(res_root.responsibility_type, member_of_res, store)
        res.set_dal_responsibility_and_id(res_root)
        res.set_appointments([self.create_responsibilities(child, store) for child in res_root.appointed])
        return res


    def __create_responsibility_from_type(self, responsibility_type, member_of_res, store):
        if responsibility_type == "founder":
            from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
            return Founder(member_of_res, store)
        elif responsibility_type == "owner":
            from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
            return Owner(member_of_res, store)
        else:
            from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
            return Manager(member_of_res, store)