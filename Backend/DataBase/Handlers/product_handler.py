from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint, insert
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session, engine
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response, PrimitiveParsable, ParsableList

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class Keyword(Base):
    __tablename__ = 'products_keywords'
    product_id = Column(String(50), ForeignKey('products.product_id'), primary_key=True)
    keyword = Column(String(50), primary_key=True)

    def __init__(self, product_id, keyword):
        self.product_id = product_id
        self.keyword = keyword


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
                                Column('store_id', String(50), ForeignKey('stores.store_id')),
                                Column('quantity', Integer, CheckConstraint('quantity > 0'))
                                )

        mapper(Product, self.__products, properties={
            '_Product__id': self.__products.c.product_id,
            '_Product__product_name': self.__products.c.product_name,
            '_Product__category': self.__products.c.category,
            '_Product__price': self.__products.c.price,
            '_Product__keywords': relationship(Keyword, cascade="all, delete", passive_deletes=True, lazy='joined')
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
                                                  quantity=kwargs['quantity'])
            session.execute(stmt)

            for keyword in obj.get_keywords():
                stmt = insert(Base.metadata.tables['products_keywords']).values(product_id=obj.get_id(),
                                                                                keyword=keyword)
                session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            Session.remove()
            self._rwlock.release_write()
            return res

    def update(self, id, update_dict):
        keywords = update_dict.pop('keywords', None)
        self._rwlock.acquire_write()
        session = Session()
        res = Response(True)
        try:
            session.query(Product).filter_by(product_id=id).update(update_dict)

            if keywords is not None:
                session.query(Keyword).filter_by(product_id=id).delete()

                for keyword in keywords:
                    stmt = insert(Base.metadata.tables['products_keywords']).values(product_id=id,
                                                                                    keyword=keyword)
                    session.execute(stmt)
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
        session = Session()
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
        session = Session()
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
        session = Session()
        self._rwlock.acquire_read()
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


if __name__ == "__main__":
    product_handler = ProductHandler.get_instance()
    object1 = Product("inon", "katz", 0.1)
    res = product_handler.save(object1, quantity=3, store_id="1")
    if not res.succeeded():
        print(res.get_msg())
