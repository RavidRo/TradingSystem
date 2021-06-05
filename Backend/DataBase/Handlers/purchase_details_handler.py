from threading import Lock

from sqlalchemy import Table, Column, String, Boolean, insert, ForeignKey, Date, Float, ARRAY
from sqlalchemy.orm import mapper

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, session
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock


class PurchaseDetailsHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        self.__purchase_details = Table('purchase_details', Base.metadata,
                                        Column('username', String(50), ForeignKey('members.username'),
                                               primary_key=True),
                                        Column('store_id', String(50), ForeignKey('stores.store_id'), primary_key=True),
                                        Column('store_name', String(50)),
                                        Column('product_names', ARRAY(String)),
                                        Column('date', Date, primary_key=True),
                                        Column('total_price', Float),
                                        )

        mapper(PurchaseDetails, self.__purchase_details, properties={
            'username': self.__purchase_details.c.username,
            'store_name': self.__purchase_details.c.store_name,
            'store_id': self.__purchase_details.c.store_id,
            'product_names': self.__purchase_details.c.product_names,
            'date': self.__purchase_details.c.date,
            'total_price': self.__purchase_details.c.total_price,
        })

    @staticmethod
    def get_instance():
        with PurchaseDetailsHandler._lock:
            if PurchaseDetailsHandler._instance is None:
                PurchaseDetailsHandler._instance = PurchaseDetailsHandler()
        return PurchaseDetailsHandler._instance

    # region save

    # def save(self, obj: PurchaseDetails, **kwargs) -> Response[None]:
    #     self._rwlock.acquire_write()
    #     session = Session(expire_on_commit=False)
    #     res = Response(True)
    #     try:
    #         stmt = insert(self.__purchase_details).values(username=obj.username,
    #                                                       store_id=obj.store_id,
    #                                                       store_name=obj.store_name,
    #                                                       product_names=obj.product_names,
    #                                                       date=obj.date,
    #                                                       total_price=obj.total_price)
    #         session.execute(stmt)
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         session.close()
    #         self._rwlock.release_write()
    #         return res

    # endregion

    # region load

    """This will be used by User to load all of his purchases"""
    def load_by_username(self, user_name: str):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            user = session.query(PurchaseDetails).filter(PurchaseDetails.username == user_name).all()
            session.commit()
            res = Response(True, user)
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            self._rwlock.release_write()
            return res

    """This will be used by Store to load all its purchases"""
    def load_by_store_id(self, store_id: str):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            user = session.query(PurchaseDetails).filter(PurchaseDetails.store_id == store_id).all()
            session.commit()
            res = Response(True, user)
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            self._rwlock.release_write()
            return res

    def update(self, id, update_dict):
        pass

    """This function is not needed since only store and member will load"""
    def load(self, id):
        pass

    def load_all(self):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            user = session.query(PurchaseDetails).all()
            session.commit()
            res = Response(True, user)
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            self._rwlock.release_write()
            return res