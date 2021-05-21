from threading import Lock

from sqlalchemy import Table, Column, String, Boolean, insert, ForeignKey, ARRAY
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session, engine
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock


class MemberHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        # self.__notifications = Table('notifications', Base.metadata,
        #                              Column('id', String(50), primary_key=True, autoincrement=True),
        #                              Column('receiver_username', String(50), ForeignKey('members.username')),
        #                              Column('msg', String(50))
        #                              )

        self.__members = Table('members', Base.metadata,
                               Column('username', String(50), primary_key=True),
                               Column('password', String(50)),
                               Column('is_admin', Boolean(20)),
                               Column('notifications', ARRAY(String(256)))
                               )

        mapper(Member, self.__members, properties={
            '_Member__username': self.__members.c.username,
            # '_Member__responsibilities': relationship(Base.metadata.tables['responsibilities'], cascade="all, delete",
            #                                           passive_deletes=True, lazy='joined'),
            # '_Member__notifications': relationship(Base.metadata.tables['notifications'], cascade="all, delete",
            #                                        passive_deletes=True, lazy='joined'),
            '_Member__purchase_details': relationship(PurchaseDetails, cascade="all, delete",
                                                      passive_deletes=True, lazy='joined'),
        })

    @staticmethod
    def get_instance():
        with MemberHandler._lock:
            if MemberHandler._instance is None:
                MemberHandler._instance = MemberHandler()
        return MemberHandler._instance

    """Note: member is saved in db in register so all of his lists are empty and not the object is saved"""

    # region save
    def save_user(self, username: str, password: str):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            stmt = insert(self.__members).values(username=username,
                                                 password=password,
                                                 is_admin=False)
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    def save_notification(self, username: str, notification_msg: str):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            stmt = insert(self.__notifications).values(receiver_username=username,
                                                       msg=notification_msg)
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    # endregion

    # region remove

    # TODO: don't know if it's a use_case but need to check
    def remove_user(self, username):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            session.query(self.__members).filter(self.__members.c.username == username).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    """remove notifications will remove"""

    def update(self, id, update_dict):
        pass

    def remove_notifications(self, username):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            session.query(self.__notifications).filter_by(username=username).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    # endregion

    # region load

    def load(self, username):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            user = session.query(Member).get(username)
            session.commit()
            res = Response(True, user)
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    def load_all(self):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            user = session.query(self.__members).all()
            session.commit()
            res = Response(True, user)
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res
