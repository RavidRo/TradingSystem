from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint, insert, update
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response, PrimitiveParsable, ParsableList

from Backend.rw_lock import ReadWriteLock
from threading import Lock

class Keyword(Base):
    __tablename__ = 'products_keywords'
    product_id = Column(String(50), ForeignKey('products.product_id'), primary_key=True),
    keyword = Column(String(50), primary_key=True)

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
            '_Product__keywords': relationship(Keyword, cascade="all, delete", passive_deletes=True)
        })

    @staticmethod
    def get_instance():
        with ProductHandler._lock:
            if ProductHandler._instance is None:
                ProductHandler._instance = ProductHandler()
        return ProductHandler._instance

    def save(self, obj, **kwargs) -> Response[None]:
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
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            return res

    def update(self, id, update_dict):
        keywords = update_dict.pop('keywords', None)
        session = Session()
        res = Response(True)
        try:
            session.query(self.__products).filter_by(product_id=id).update(update_dict)

            if keywords is not None:
                session.query(Base.metadata.tables['products_keywords']).filter_by(product_id=id).delete()

                for keyword in keywords:
                    stmt = insert(Base.metadata.tables['products_keywords']).values(product_id=id,
                                                                                    keyword=keyword)
                    session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            return res

    def load(self, id):
        session = Session()
        res = Response(True)
        try:
            product = session.query(self.__products).get(id)

            keywords = session.query(Base.metadata.tables['products_keywords']).filter_by(product_id=id).all()
            product.set_keywords(keywords)
            session.commit()
            res = Response(True, product)
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            return res

    def load_all(self):
        session = Session()
        res = Response(True)
        try:
            products = session.query(self.__products).all()

            for product in products:
                keywords = session.query(Base.metadata.tables['products_keywords']).filter_by(product_id=product.get_id()).all()
                product.set_keywords(keywords)
            session.commit()
            res = Response(True, ParsableList(products))
        except Exception as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(str(e)))
        finally:
            Session.remove()
            return res

    # def load_products_by_store(self, store_id):
