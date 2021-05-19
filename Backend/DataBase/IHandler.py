from abc import ABC, abstractmethod

from Backend.DataBase.database import Session
from Backend.response import Response, PrimitiveParsable


class IHandler(ABC):

    def __init__(self, rwlock):
        self._rwlock = rwlock

    def save(self, obj, **kwargs) -> Response[None]:
        session = Session()
        res = Response(True)
        try:
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            return res

    def remove(self, obj) -> Response[None]:
        session = Session()
        res = Response(True)
        try:
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
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

