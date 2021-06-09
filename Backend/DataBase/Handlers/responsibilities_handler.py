import json

import sqlalchemy
from sqlalchemy.orm.collections import attribute_mapped_collection

from Backend.DataBase.IHandler import IHandler
from threading import Lock
from Backend.DataBase.database import mapper_registry, session
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
    join, and_
from sqlalchemy.orm import mapper, relationship, backref


# class ManagerPermission:
#     def __init__(self, username, store_id):
#         self.username = username
#         self.store_id =


class ResponsibilitiesHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Responsibility)

        self.__responsibilities = Table('responsibilities', mapper_registry.metadata,
                                        Column('username', String(50), ForeignKey('members.username'),
                                               primary_key=True),
                                        Column('store_id', String(50), ForeignKey('stores.store_id'), primary_key=True),
                                        Column('parent_username', String(50)),
                                        Column('responsibility_type', String(10)),
                                        Column('manager_permissions', PermissionType()),
                                        ForeignKeyConstraint(('parent_username', 'store_id'),
                                                             ['responsibilities.username',
                                                              'responsibilities.store_id'], name="fk_self_reference"))

        # self.__manager_permissions = Table('manager_permissions', mapper_registry.metadata,
        #                                    Column('manager_store_id', String(50), primary_key=True),
        #                                    Column('manager_username', String(50), primary_key=True),
        #                                    Column('permissions', PermissionType()),
        #                                    ForeignKeyConstraint(('manager_username', 'manager_store_id'),
        #                                                         ['responsibilities.username',
        #                                                          'responsibilities.store_id']))

        mapper_registry.map_imperatively(Responsibility, self.__responsibilities, properties={
            '_username': self.__responsibilities.c.username,
            '_appointed': relationship(Responsibility, cascade="all", overlaps="_store", remote_side=[self.__responsibilities.c.username, self.__responsibilities.c.store_id],
                                       primaryjoin=(and_(self.__responsibilities.c.username == self.__responsibilities.c.parent_username, self.__responsibilities.c.store_id == self.__responsibilities.c.store_id))),
            '_Manager__permissions': self.__responsibilities.c.manager_permissions

        }, polymorphic_on=self.__responsibilities.c.responsibility_type, polymorphic_identity='R',
                                         exclude_properties={'permissions'})

        mapper_registry.map_imperatively(Founder, self.__responsibilities, inherits=Responsibility,
                                         polymorphic_identity='F', exclude_properties={'permissions'})
        mapper_registry.map_imperatively(Owner, self.__responsibilities, inherits=Responsibility,
                                         polymorphic_identity='O', exclude_properties={'permissions'})
        mapper_registry.map_imperatively(Manager, self.__responsibilities,
                                         inherits=Responsibility, polymorphic_identity='M',
                                         # Maybe replace self.__manager_permissions with join(self.__responsibilities, self.__manager_permissions) below
                                         # properties={
                                         #     '_Manager__permissions': relationship()
                                         # }
                                         )

    @staticmethod
    def get_instance():
        with ResponsibilitiesHandler._lock:
            if ResponsibilitiesHandler._instance is None:
                ResponsibilitiesHandler._instance = ResponsibilitiesHandler()
        return ResponsibilitiesHandler._instance

    def update_child(self, appointer_username, store_id, responsibility):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            appointer: Responsibility = session.query(Responsibility).filter_by(username=appointer_username,
                                                                                store_id=store_id).one()
            appointer._appointed.append(responsibility)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

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
