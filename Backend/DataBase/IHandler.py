from abc import ABC, abstractmethod

from Backend.DataBase.database import Session
from Backend.response import Response, PrimitiveParsable, ParsableList


class IHandler(ABC):

    def __init__(self, table, classname):
        self._table = table
        self._classname = classname

    @staticmethod
    def save(obj, **kwargs) -> Response[None]:
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

    @staticmethod
    def remove(obj) -> Response[None]:
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
        session = Session()
        res = Response(True)
        try:
            objects = session.query(self._classname).all()
            session.commit()
            res = Response(True, ParsableList(objects))
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            return res

