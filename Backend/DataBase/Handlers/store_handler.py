from threading import Lock

from sqlalchemy import Table, Column, String, ForeignKey, Date, Float, ARRAY
from sqlalchemy.orm import mapper

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.rw_lock import ReadWriteLock


class StoreHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        self.__stores = Table('stores', Base.metadata,
                                        Column('store_id', String(50), ForeignKey('members.username'),
                                               primary_key=True),
                                        Column('store_id', String(50), ForeignKey('stores.store_id'), primary_key=True),
                                        Column('store_name', String(50)),
                                        Column('product_names', ARRAY(String)),
                                        Column('date', Date, primary_key=True),
                                        Column('total_price', Float),
                                        )

        mapper(PurchaseDetails, self.__purchase_details, properties={
            'user_name': self.__purchase_details.c.user_name,
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
