from abc import ABC, abstractmethod

from Backend.DataBase.database import Session
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock


class IHandler(ABC):

    def __init__(self, rwlock: ReadWriteLock):
        self._rwlock = rwlock

    def save(self, obj, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_write()
            return res

    def remove(self, obj, **kwargs) -> Response[None]:
        session = Session(expire_on_commit=False)
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_write()
            return res

    @abstractmethod
    def update(self, id, update_dict):
        pass

    @abstractmethod
    def load(self, id):
        pass

    @abstractmethod
    def load_all(self):
        pass

