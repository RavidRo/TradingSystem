# from Backend.DataBase.IHandler import IHandler
# from threading import Lock
# from Backend.DataBase.database import Base
# from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
# from Backend.rw_lock import ReadWriteLock
# from sqlalchemy import Table, Column, String, Boolean, insert, ForeignKey, Date, Float, ARRAY, ForeignKeyConstraint
# from sqlalchemy.orm import mapper, relationship
#
#
# class ResponsibilitiesHandler(IHandler):
#     _lock = Lock()
#     _instance = None
#
#     def __init__(self):
#         super().__init__(ReadWriteLock())
#
#         self.__responsibilities = Table('responsibilities', Base.metadata,
#                                         Column('username', String(50), ForeignKey('members.username'),
#                                                primary_key=True),
#                                         Column('store_id', String(50), ForeignKey('stores.store_id'), primary_key=True),
#                                         Column('parent_user_name', String(50)),
#                                         Column('parent_store_id', String(50)),
#                                         Column('responsibility_type', String(10), nullable=False),
#                                         __table_args__=(ForeignKeyConstraint(['parent_user_name', 'parent_store_id'],
#                                                                              ['responsibilities.parent_user_name',
#                                                                               'responsibilities.parent_store_id'])
#                                                         ))
#
#         mapper(Responsibility, self.__responsibilities, properties={
#             'Responsibility_appointed': relationship(Responsibility, cascade="all, delete",
#                                                      passive_deletes=True, lazy='joined'),
#         }, polymporphic_on=self.__responsibilities.responsibility_type, polymporphic_identity='R')
#
#     @staticmethod
#     def get_instance():
#         with ResponsibilitiesHandler._lock:
#             if ResponsibilitiesHandler._instance is None:
#                 ResponsibilitiesHandler._instance = ResponsibilitiesHandler()
#         return ResponsibilitiesHandler._instance
#
#
#     def update(self, id, update_dict):
#         pass
#
#     def load(self, id):
#         pass
#
#     def load_all(self):
#         pass
#
#
# if __name__ == '__main__':
#     stam = ResponsibilitiesHandler.get_instance()
#     stam1 = 1