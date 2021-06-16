import json
import threading
from threading import Lock
from sqlalchemy import Table, Column, String, Boolean, insert, ForeignKey, select, TypeDecorator, VARCHAR, Integer
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.ext.mutable import Mutable, MutableDict
from sqlalchemy.orm import mapper, relationship, backref, with_polymorphic
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import mapper_registry, session
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.offer import Offer
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock
from sqlalchemy.orm.collections import attribute_mapped_collection, column_mapped_collection


class MemberHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        from Backend.Domain.TradingSystem.States.admin import Admin
        from Backend.DataBase.Handlers.shopping_bag_handler import ShoppingBagHandler
        super().__init__(ReadWriteLock(), Member)
        self.__credentials = Table("credentials", mapper_registry.metadata,
                                   Column('username', String(50), primary_key=True),
                                   Column('password', String(256)))

        self.__members = Table('members', mapper_registry.metadata,
                               Column('username', String(50), ForeignKey("credentials.username"), primary_key=True),
                               Column('notifications', ARRAY(String(50))),
                               Column('member_type', String(10), nullable=False),
                               Column('responsibilities_ids', ARRAY(Integer)))

        mapper_registry.map_imperatively(Member, self.__members, properties={
            '_notifications': self.__members.c.notifications,
            "_responsibilities_ids": self.__members.c.responsibilities_ids,
            '_username': self.__members.c.username,
            '_purchase_details': relationship(PurchaseDetails, cascade="all, delete-orphan"),
            '_offers': relationship(Offer, collection_class=attribute_mapped_collection('_Offer__id'))

        }, polymorphic_on=self.__members.c.member_type, polymorphic_identity='M')

        mapper_registry.map_imperatively(Admin, self.__members, inherits=Member, polymorphic_identity='A')

        self.__shopping_bag_handler = ShoppingBagHandler.get_instance()

    @staticmethod
    def get_instance():
        with MemberHandler._lock:
            if MemberHandler._instance is None:
                MemberHandler._instance = MemberHandler()
        return MemberHandler._instance

    # region save
    def save_user_credentials(self, username: str, password: str):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            stmt = insert(self.__credentials).values(username=username,
                                                     password=password)
            session.execute(stmt)
            session.flush()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    # endregion

    # region remove

    # TODO: don't know if it's a use_case but need to check
    def remove_user(self, username):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.query(self.__members).filter(self.__members.c.username == username).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    # def remove_responsibility(self, username: str, responsibility: Responsibility):
    #     self._rwlock.acquire_write()
    #     res = Response(True)
    #     try:
    #         member = session.query(Member).filter_by(_username=username).one()
    #         member.get_responsibilities().append(responsibility)
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         self._rwlock.release_write()
    #         return res
    #

    # # TODO: check if append here is on same object as in the domain!
    # def update_responsibility(self, username: str, responsibility: Responsibility):
    #     self._rwlock.acquire_write()
    #     res = Response(True)
    #     try:
    #         member = session.query(Member).filter_by(_username=username).one()
    #         responsibilities = member.get_responsibilities()
    #         responsibilities[responsibility.get_store_id()] = responsibility
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         self._rwlock.release_write()
    #         return res

    def update_responsibilities_ids(self, username: str, responsibilities_ids: list):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            member = session.query(Member).filter_by(_username=username).one()
            member.responsibilities_ids = None
            member._responsibilities_ids = responsibilities_ids
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def update_notifications(self, username: str, notifications: list[str]):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            member = session.query(Member).filter_by(_username=username).one()
            member.notifications = notifications
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    # endregion

    # region load

    def load_credentials(self, username):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            stmt = select([self.__credentials.c.username, self.__credentials.c.password]).where(
                self.__credentials.c.username == username)
            res = session.execute(stmt).one()
            session.commit()
            res = Response(True, res)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_cart(self, username):
        return self.__shopping_bag_handler.load_cart(username)

    def load_all(self):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            user = session.query(self.__members).all()
            session.commit()
            res = Response(True, user)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_user_with_res(self, res_id):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            user = session.query(Member).filter(self.__members.c.responsibilities_ids.contains([res_id])).one()
            user._responsibilities = dict()
            user.notifications_lock = threading.Lock()
            res = Response(True, user)
            # session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    # def load_res_ids(self, username):
    #     self._rwlock.acquire_read()
    #     res = Response(True)
    #     try:
    #         stmt = select([self.__members.c.responsibilities_ids]).where(
    #             self.__members.c.username == username)
    #         reses = session.execute(stmt).one()
    #         session.commit()
    #         res = list([Founder(None, None) if res.type == 'founder'
    #                      else Owner(None, None) if res.type == 'owner'
    #                      else Manager(None, None) for res in reses])
    #         res = Response(True, res)
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         self._rwlock.release_read()
    #         return res
