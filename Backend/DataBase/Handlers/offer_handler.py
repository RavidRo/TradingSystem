from msilib import Table
from threading import Lock

from sqlalchemy import Column, String, Float

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import mapper_registry
from Backend.Domain.TradingSystem.offer import Offer
from Backend.rw_lock import ReadWriteLock


class OfferHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Offer)

        self.__offers = Table('offers', mapper_registry.metadata,
                                Column('offer_id', String(50), primary_key=True),
                                Column('price', Float(50)),
                                Column('status', String(1)),
                                Column('price', Float),
                                Column('keywords', ARRAY(String(30)))
                                )

        mapper_registry.map_imperatively(Product, self.__products, properties={
            '_Product__id': self.__products.c.product_id,
            '_Product__product_name': self.__products.c.product_name,
            '_Product__category': self.__products.c.category,
            '_Product__price': self.__products.c.price,
            '_Product__keywords': self.__products.c.keywords,
        })

    @staticmethod
    def get_instance():
        with ProductHandler._lock:
            if ProductHandler._instance is None:
                ProductHandler._instance = ProductHandler()
        return ProductHandler._instance