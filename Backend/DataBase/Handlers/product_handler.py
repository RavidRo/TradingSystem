from sqlalchemy import Table, Column, String, Float, Integer, CheckConstraint, insert, ARRAY
from sqlalchemy.orm import mapper

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response, ParsableList

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class ProductHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        self.__products = Table('products', Base.metadata,
                                Column('product_id', String(50), primary_key=True),
                                Column('product_name', String(50)),
                                Column('category', String(50)),
                                Column('price', Float),
                                Column('store_id', String(50)),     # add foreign key to stores when it will be created
                                Column('quantity', Integer, CheckConstraint('quantity>0')),
                                Column('keywords', ARRAY(String(30)))
                                )

        mapper(Product, self.__products, properties={
            '_Product__id': self.__products.c.product_id,
            '_Product__product_name': self.__products.c.product_name,
            '_Product__category': self.__products.c.category,
            '_Product__price': self.__products.c.price,
            '_Product__keywords': self.__products.c.keywords
        })

    @staticmethod
    def get_instance():
        with ProductHandler._lock:
            if ProductHandler._instance is None:
                ProductHandler._instance = ProductHandler()
        return ProductHandler._instance

    def save(self, obj: Product, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        session = Session()
        res = Response(True)
        try:
            stmt = insert(self.__products).values(product_id=obj.get_id(),
                                                  product_name=obj.get_name(),
                                                  category=obj.get_category(),
                                                  price=obj.get_price(),
                                                  store_id=kwargs['store_id'],
                                                  quantity=kwargs['quantity'],
                                                  keywords=obj.get_keywords())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    def remove(self, obj, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        session = Session()
        res = Response(True)
        try:
            session.query(Product).filter_by(_Product__id=obj.get_id()).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    def update(self, id, update_dict):
        self._rwlock.acquire_write()
        session = Session()
        res = Response(True)
        try:
            session.query(Product).filter_by(_Product__id=id).update(update_dict)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    def load(self, id):
        self._rwlock.acquire_read()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            product = session.query(Product).get(id)
            session.commit()
            res = Response(True, product)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_read()
            return res

    def load_all(self):
        self._rwlock.acquire_read()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            products = session.query(Product).all()
            session.commit()
            res = Response(True, ParsableList(products))
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_read()
            return res

    def load_products_by_store(self, store_id):
        self._rwlock.acquire_read()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            products = session.query(Product).filter_by(store_id=store_id).all()
            session.commit()
            res = Response(True, ParsableList(products))
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_read()
            return res
