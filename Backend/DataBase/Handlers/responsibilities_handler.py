import json

import sqlalchemy

from Backend.DataBase.IHandler import IHandler
from threading import Lock
from Backend.DataBase.database import Base
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.store import Store
from sqlalchemy.types import TypeDecorator
from Backend.rw_lock import ReadWriteLock
from sqlalchemy import Table, Column, String, Boolean, insert, ForeignKey, Date, Float, ARRAY, ForeignKeyConstraint, \
    join
from sqlalchemy.orm import mapper, relationship


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
            '_appointed': relationship(Responsibility, uselist=True, cascade="all, delete",
                                       passive_deletes=True,
                                       remote_side=[self.__responsibilities.c.username,
                                                    self.__responsibilities.c.store_id], overlaps="_store"),
            # '_user_state': relationship(Member, uselist=False, lazy='joined',
            #                             back_populates="_Member__responsibilities"),
            # '_store': relationship(Store, uselist=False, lazy='joined', overlaps="_appointed"),
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
