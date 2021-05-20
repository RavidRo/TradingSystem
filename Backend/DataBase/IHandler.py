from abc import ABC, abstractmethod

from Backend.DataBase.database import Session
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock


class IHandler(ABC):

    def __init__(self, rwlock: ReadWriteLock):
        self._rwlock = rwlock

    def save(self, obj, **kwargs) -> Response[None]:
        session = Session()
        res = Response(True)
        try:
            self._rwlock.acquire_write()
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            self._rwlock.release_write()
            Session.remove()
            return res

    def remove(self, obj) -> Response[None]:
        session = Session()
        res = Response(True)
        try:
            self._rwlock.acquire_write()
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            self._rwlock.release_write()
            Session.remove()
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

