from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint, insert
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response, PrimitiveParsable


class ProductHandler(IHandler):
    class Keyword(Base):
        __tablename__ = 'products_keywords'
        product_id = Column(String(50), ForeignKey('products.product_id'), primary_key=True),
        keyword = Column(String(50), primary_key=True)

    products = Table('products', Base.metadata,
                     Column('product_id', String(50), primary_key=True),
                     Column('product_name', String(50)),
                     Column('category', String(50)),
                     Column('price', Float),
                     Column('store_id', String(50), ForeignKey('stores.store_id')),
                     Column('quantity', Integer, CheckConstraint('quantity > 0'))
                     )

    mapper(Product, products, properties={
        '_Product__id': products.c.product_id,
        '_Product__product_name': products.c.product_name,
        '_Product__category': products.c.category,
        '_Product__price': products.c.price,
        '_Product__keywords': relationship(Keyword)
    })

    @staticmethod
    def save(obj, **kwargs) -> Response[None]:
        session = Session()
        res = Response(True)
        try:
            stmt = insert(ProductHandler.products).values(product_id=obj.get_id(),
                                                          product_name=obj.get_name(),
                                                          category=obj.get_category(),
                                                          price=obj.get_price(),
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
        pass

    def load(self, id):
        pass

    def load_all(self):
        pass
