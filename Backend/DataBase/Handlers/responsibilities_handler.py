import json

import sqlalchemy
from sqlalchemy.orm.collections import attribute_mapped_collection

from Backend.DataBase.IHandler import IHandler
from threading import Lock
from Backend.DataBase.database import Base, Session
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.store import Store
from sqlalchemy.types import TypeDecorator

from Backend.response import Response
from Backend.rw_lock import ReadWriteLock
from sqlalchemy import Table, Column, String, Boolean, insert, ForeignKey, Date, Float, ARRAY, ForeignKeyConstraint, \
    join
from sqlalchemy.orm import mapper, relationship, backref


class ResponsibilitiesHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        self.__responsibilities = Table('responsibilities', Base.metadata,
                                        Column('username', String(50), ForeignKey('members.username'),
                                               primary_key=True),
                                        Column('store_id', String(50), ForeignKey('stores.store_id'), primary_key=True),
                                        Column('parent_username', String(50)),
                                        Column('responsibility_type', String(10), nullable=False, default='R'),
                                        ForeignKeyConstraint(('parent_username', 'store_id'),
                                                             ['responsibilities.username',
                                                              'responsibilities.store_id'], name="fk_self_reference"))

        self.__manager_permissions = Table('manager_permissions', Base.metadata,
                                           Column('manager_store_id', String(50), primary_key=True),
                                           Column('manager_username', String(50), primary_key=True),
                                           Column('permissions', PermissionType()),
                                           ForeignKeyConstraint(('manager_username', 'manager_store_id'),
                                                                ['responsibilities.username',
                                                                 'responsibilities.store_id']))

        responsibility_mapper = mapper(Responsibility, self.__responsibilities, properties={
            '_appointed': relationship(Responsibility, uselist=True, cascade="all",
                                       passive_deletes=True,
                                       remote_side=[self.__responsibilities.c.username,
                                                    self.__responsibilities.c.store_id], overlaps="_store"),
            '_user_state': relationship(Member, uselist=False, lazy='joined',
                                        backref=backref("_Member__responsibilities", cascade="all, delete, delete-orphan",
                                                        collection_class=attribute_mapped_collection('_store_id'),
                                                        passive_deletes=True)),
            '_store': relationship(Store, uselist=False, backref=backref("_Store__responsibility", uselist=False, overlaps="_appointed")),
        }, polymorphic_on=self.__responsibilities.c.responsibility_type, polymorphic_identity='R')

        mapper(Founder, self.__responsibilities, inherits=responsibility_mapper, polymorphic_identity='F')
        mapper(Owner, self.__responsibilities, inherits=responsibility_mapper, polymorphic_identity='O')
        mapper(Manager, join(self.__responsibilities, self.__manager_permissions), polymorphic_identity='M',
               properties={
                   '_Manager__permissions': self.__manager_permissions.c.permissions
               })

    @staticmethod
    def get_instance():
        with ResponsibilitiesHandler._lock:
            if ResponsibilitiesHandler._instance is None:
                ResponsibilitiesHandler._instance = ResponsibilitiesHandler()
        return ResponsibilitiesHandler._instance

    def update(self, id, update_dict):
        pass

    def update_child(self, appointer_username, store_id, responsibility):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            appointer: Responsibility = session.query(Responsibility).filter_by(username=appointer_username, store_id=store_id).one()
            appointer._appointed.append(responsibility)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_write()
            return res

    def load(self, id):
        pass

    def load_all(self):
        pass


class PermissionType(TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        pass

    impl = sqlalchemy.Text()

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


if __name__ == '__main__':
    stam1 = 1
