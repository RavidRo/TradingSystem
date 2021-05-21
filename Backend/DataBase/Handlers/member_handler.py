from threading import Lock
from sqlalchemy import Table, Column, String, Boolean, insert, ARRAY
from sqlalchemy.orm import mapper, relationship
from Backend.DataBase.Handlers.purchase_details_handler import PurchaseDetailsHandler
from Backend.DataBase.Handlers.store_handler import StoreHandler
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
        self.__members = Table('members', Base.metadata,
                               Column('username', String(50), primary_key=True),
                               Column('password', String(50)),
                               Column('is_admin', Boolean(20)),
                               Column('notifications', ARRAY(String(256)))
                               )

        mapper(Member, self.__members, properties={
            '_username': self.__members.c.username,
            # '_Member__responsibilities': relationship(Base.metadata.tables['responsibilities'], cascade="all, delete",
            #                                           passive_deletes=True, lazy='joined'),
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
    def save_user(self, username: str, password: str, is_admin=False):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            stmt = insert(self.__members).values(username=username,
                                                 password=password,
                                                 is_admin=is_admin,
                                                 notifications=[])
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
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
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_write()
            return res

    """remove notifications will remove"""

    def update(self, id, update_dict):
        pass

    def update_notifications(self, username: str, notifications: list[str]):
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            member = session.query(Member).filter_by(_username=username).one()
            member.notifications = notifications
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
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
            res = Response(False, msg=str(e))
        finally:
            session.close()
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
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_write()
            return res


# if __name__ == '__main__':
#     print("asfsa")
#     purchase_details_handler = PurchaseDetailsHandler.get_instance()
#     member_handler = MemberHandler.get_instance()
#     stores_handler = StoreHandler.get_instance()
#     Base.metadata.create_all(engine)
#     # member_handler.save_user("Sean", "Pikulin")
#     member_handler.update_notifications("Sean", ["saasf", "afasfsafasfas"])