from sqlalchemy import Table, Column, String, Integer, ForeignKey, CheckConstraint, insert, Boolean, \
    ForeignKeyConstraint, delete, update, and_, select
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection, column_mapped_collection

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import mapper_registry, session
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.response import Response

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class ProductInShoppingBag:
    def __init__(self, store_id, product_id, username, quantity):
        self.store_id = store_id
        self.product_id = product_id
        self.username = username
        self.quantity = quantity


class ShoppingBagHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), ShoppingBag)

        self.__products_in_shopping_bags = Table("products_in_shopping_bags", mapper_registry.metadata,
                                                 Column("product_id", String(50),
                                                        ForeignKey("products.product_id", ondelete="CASCADE"),
                                                        primary_key=True),
                                                 Column("store_id", String(50), primary_key=True),
                                                 Column("username", String(50), primary_key=True),
                                                 Column("quantity", Integer, CheckConstraint('quantity>0')),
                                                 ForeignKeyConstraint(('store_id', 'username'),
                                                                      ['shopping_bags.store_id',
                                                                       'shopping_bags.username'])
                                                 )

        self.__shopping_bags = Table("shopping_bags", mapper_registry.metadata,
                                     Column("store_id", String(50), ForeignKey("stores.store_id"), primary_key=True),
                                     Column("username", String(50), ForeignKey("members.username"), primary_key=True))

        mapper_registry.map_imperatively(ProductInShoppingBag, self.__products_in_shopping_bags, properties={
            "store_id": self.__products_in_shopping_bags.c.store_id,
            "product_id": self.__products_in_shopping_bags.c.product_id,
            "username": self.__products_in_shopping_bags.c.username,
            "quantity": self.__products_in_shopping_bags.c.quantity,
            "product": relationship(Product, cascade="all", uselist=False),
        })

        # mapper_registry.map_imperatively(ShoppingBag, self.__shopping_bags, properties={
        #     # "_ShoppingBag__store": relationship(Store, passive_deletes=True),
        #     "products": relationship(ProductInShoppingBag, uselist=True,
        #                              collection_class=attribute_mapped_collection("product_id"))
        # })

    @staticmethod
    def get_instance():
        with ShoppingBagHandler._lock:
            if ShoppingBagHandler._instance is None:
                ShoppingBagHandler._instance = ShoppingBagHandler()
        return ShoppingBagHandler._instance

    def save_bag(self, user_name, store_id):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            stmt = insert(self.__shopping_bags).values(store_id=store_id,
                                                       username=user_name)
            session.execute(stmt)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def add_product_to_bag(self, store, product, username, quantity):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            stmt = insert(self.__products_in_shopping_bags).values(store_id=store.get_id(),
                                                                   username=username,
                                                                   product_id=product.get_id(),
                                                                   quantity=quantity)
            session.execute(stmt)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def remove_product_from_bag(self, store, product_id, user_name):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            d = delete(self.__products_in_shopping_bags).where(
                self.__products_in_shopping_bags.c.store_id == store.get_id()).where(
                self.__products_in_shopping_bags.c.product_id == product_id).where(
                self.__products_in_shopping_bags.c.username == user_name)
            session.execute(d)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def change_product_quantity_in_bag(self, store, product_id, user_name, amount):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            stmt = update(self.__products_in_shopping_bags).where(
                and_(self.__products_in_shopping_bags.c.store_id == store.get_id(),
                     self.__products_in_shopping_bags.c.product_id == product_id,
                     self.__products_in_shopping_bags.c.username == user_name)).values(quantity=amount)
            session.execute(stmt)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res



        # shopping_bag.products.update(
        #     {product.get_id(): ProductInShoppingBag(store.get_id(), product.get_id(), username, quantity)})

    # def save(self, obj: ShoppingBag, **kwargs) -> Response[None]:
    #     self._rwlock.acquire_write()
    #     res = Response(True)
    #     try:
    #         stmt = insert(self.__shopping_bags).values(store_id=obj.get_store_ID(),
    #                                                    username=kwargs['username'])
    #         session.execute(stmt)
    #
    #         for prod_id, product_to_quantity in obj.get_products_to_quantity().items():
    #             stmt = insert(Base.metadata.tables[ProductInShoppingBag.__tablename__]).values(
    #                 store_id=obj.get_store_ID(),
    #                 username=kwargs['username'],
    #                 product_id=prod_id,
    #                 quantity=product_to_quantity[1])
    #             session.execute(stmt)
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         self._rwlock.release_write()
    #         return res

    def remove(self, obj: ShoppingBag, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.query(ProductInShoppingBag).filter_by(store_id=obj.get_store_ID(),
                                                          username=kwargs['username']).delete()
            session.query(ShoppingBag).filter_by(store_id=obj.get_store_ID(), username=kwargs['username']).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def load_all(self):
        pass

    def load_cart(self, username):
        res = Response(True)
        try:
            cart = ShoppingCart()
            stmt = select(self.__shopping_bags.c.store_id).where(self.__shopping_bags.c.username == username)
            bags_store_ids = session.execute(stmt).all()
            store_id_to_bag = dict()
            for bag_store_id in bags_store_ids:
                store = StoresManager.get_store(bag_store_id[0])
                bag = ShoppingBag(store)
                products_in_bag: list[ProductInShoppingBag] = session.query(ProductInShoppingBag).filter_by(username=username,
                                                                                                            store_id=bag_store_id[0]).all()
                bag.set_products({product_in_bag.product_id: (product_in_bag.product, product_in_bag.quantity) for product_in_bag in products_in_bag})
                store_id_to_bag.update({bag_store_id[0]: bag})

            cart.add_bags(store_id_to_bag)
            res = Response(True, cart)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            return res

# if __name__ == "__main__":
#     bags_handler = ShoppingBagHandler.get_instance()
#     product_handler = ProductHandler.get_instance()
#     members = Table('members', Base.metadata,
#                     Column('username', String(50), primary_key=True),
#                     Column('password', String(50)),
#                     Column('is_admin', Boolean(20)),
#                     )
#     Base.metadata.create_all(engine)
# bag = ShoppingBag(Store("store"))
# object1 = Product("inoninoni", "katz", 2, ["Cat", "Dog"])
# res = product_handler.save(object1, quantity=3, store_id="1")
# if not res.succeeded():
#     print(res.get_msg())
# bag._products_to_quantity = {object1.get_id(): (object1, 3)}
# res = bags_handler.save(bag, username="Me")
# if not res.succeeded():
#     print(res.get_msg())
# res = bags_handler.remove(bag, username="Me")
# if not res.succeeded():
#     print(res.get_msg())

# res = bags_handler.load_cart("Me")
# if not res.succeeded():
#     print(res.get_msg())
