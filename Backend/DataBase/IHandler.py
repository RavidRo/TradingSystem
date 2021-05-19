from abc import ABC, abstractmethod

from Backend.response import Response, PrimitiveParsable, ParsableList
from database import Session


class IHandler(ABC):

    def __init__(self, table, classname):
        self._table = table
        self._classname = classname

    @staticmethod
    def save(obj, **args) -> Response[None]:
        session = Session()
        res = Response(True)
        try:
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            session.close()
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
            session.close()
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
            session.close()
            return res

