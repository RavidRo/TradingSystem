from sqlalchemy import Table, Column, String, Float, Integer, CheckConstraint, insert, ARRAY, ForeignKey
from sqlalchemy.orm import mapper

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, session
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response, ParsableList

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class ProductHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Product)

        self.__products = Table('products', Base.metadata,
                                Column('product_id', String(50), primary_key=True),
                                Column('product_name', String(50)),
                                Column('category', String(50)),
                                Column('price', Float),
                                Column('keywords', ARRAY(String(30)))
                                )

        mapper(Product, self.__products, properties={
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

    def load_all(self):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            products = session.query(Product).all()
            session.commit()
            res = Response(True, ParsableList(products))
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_products_by_store(self, store_id):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            products = session.query(Product).filter_by(store_id=store_id).all()
            session.commit()
            res = {product.get_id(): (product, product.quantity) for product in products}
        except Exception as e:
            session.rollback()
            res = str(e)
        finally:
            self._rwlock.release_read()
            return res


# if __name__ == '__main__':
#     product_handler = ProductHandler.get_instance()
#     # product_handler.save(Product("Watermelon", "Fruit", 5, ["Watery"]), quantity=8, store_id="c6ba8b7c-c284-4334-baa1-346827534068")
#     res = product_handler.load_products_by_store("c6ba8b7c-c284-4334-baa1-346827534068")
#     if not res.succeeded():
#         print(res.get_msg())
