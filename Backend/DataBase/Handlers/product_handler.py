from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response


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
    def save(obj, **args) -> Response[None]:
        pass

    def update(self, id, update_dict):
        pass

    def load(self, id):
        pass

    def load_all(self):
        pass

