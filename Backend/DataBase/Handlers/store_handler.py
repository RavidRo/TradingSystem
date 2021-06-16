from sqlalchemy import Table, Column, String, insert, ForeignKey, CheckConstraint, Integer, PrimaryKeyConstraint, select
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection, collection
from Backend.DataBase.Handlers.product_handler import ProductHandler
from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import mapper_registry, session, db_fail_response
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock
from threading import Lock


class ProductsOfStores:
    def __init__(self, store_id, product_id, quantity):
        self.store_id = store_id
        self.product_id = product_id
        self.quantity = quantity


class StoreHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Store)

        self.__products_of_stores = Table("products_of_stores", mapper_registry.metadata,
                                          Column("store_id", String(50), ForeignKey("stores.store_id"),
                                                 primary_key=True),
                                          Column("product_id", String(50),
                                                 ForeignKey("products.product_id", ondelete="CASCADE",
                                                            onupdate="CASCADE"),
                                                 primary_key=True),
                                          Column("quantity", Integer, CheckConstraint('quantity > 0')))

        self.__stores = Table("stores", mapper_registry.metadata,
                              Column("store_id", String(50), primary_key=True),
                              Column("store_name", String(30)),
                              Column("responsibility_id", Integer),
                              Column("purchase_policy_root_id", String(30)))

        mapper_registry.map_imperatively(ProductsOfStores, self.__products_of_stores, properties={
            "store_id": self.__products_of_stores.c.store_id,
            "product_id": self.__products_of_stores.c.product_id,
            "quantity": self.__products_of_stores.c.quantity,
            "product": relationship(Product, cascade="all", uselist=False)
        })

        mapper_registry.map_imperatively(Store, self.__stores, properties={
            "_Store__purchase_policy_root_id": self.__stores.c.purchase_policy_root_id,
            "_Store__id": self.__stores.c.store_id,
            "_Store__name": self.__stores.c.store_name,
            "_Store__responsibility_id": self.__stores.c.responsibility_id,
            "_Store__purchase_history": relationship(PurchaseDetails),
            "products": relationship(ProductsOfStores, uselist=True,
                                     collection_class=attribute_mapped_collection("product_id"))
        })
        self.__product_handler = ProductHandler.get_instance()
        from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
        self.__responsibility_hadnler = ResponsibilitiesHandler.get_instance()
        self.__purchase_rules_handler = PurchaseRulesHandler.get_instance()

    @staticmethod
    def get_instance():
        with StoreHandler._lock:
            if StoreHandler._instance is None:
                StoreHandler._instance = StoreHandler()
        return StoreHandler._instance

    # def save(self, obj: Store, **kwargs) -> Response[None]:
    #     self._rwlock.acquire_write()
    #     session = Session(expire_on_commit=False)
    #     res = Response(True)
    #     try:
    #         session.add(obj)
    #         # stmt = insert(Base.metadata.tables['responsibilities']).values(
    #         #     username=obj.get_responsibility().get_user_state().get_username().get_obj().get_val(),
    #         #     store_id=obj.get_id(),
    #         #     parent_id=None,
    #         #     responsibility_type="F")
    #         # session.execute(stmt)
    #
    #         # TODO: save discount using discounts_handler
    #
    #         # TODO: save purchase_rule using purchase_rule_handler
    #
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         session.close()
    #         self._rwlock.release_write()
    #         return res

    def remove_product(self, product):
        return self.__product_handler.remove(product)

    def add_product(self, store, product, quantity):
        self.__product_handler.save(product)
        store.products.update({product.get_id(): ProductsOfStores(store.get_id(), product.get_id(), quantity)})

    def update_product_quantity(self, store, product, quantity):
        product_in_bag = session.query(ProductsOfStores).filter_by(store_id=store.get_id(),
                                                                   product_id=product.get_id()).one()
        product_in_bag.quantity = quantity

    def save_purchase_rule(self, root_rule):
        return self.__purchase_rules_handler.save(root_rule)

    def load(self, id):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            store = session.query(Store).get(id)

            # TODO: load responsibility using responsibility_handler.load_by_store_id(), add it to store

            # TODO: load root discount using discount_handler.load(), add it to store

            # TODO: load root rule using purchase_rule_handler.load(), add it to store

            loaded_products = self.__product_handler.load_products_by_store(id)
            if type(loaded_products) != str:
                store.set_products(loaded_products)
                res = Response(True, store)
                session.commit()

            else:
                res = Response(False, msg=loaded_products)
                session.rollback()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_store(self, store_id):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            store = session.query(Store).get(store_id)
            store.set_products({prod_id: (store_product.product, store_product.quantity) for prod_id, store_product in store.products.items()})
            store.init_fields()
            res.object = store
            session.commit()
        except DisconnectionError as e:
            session.rollback()
            res = Response(False, PrimitiveParsable(0), msg=str(e))
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_res_of_store(self, res_id, store):
        return self.__responsibility_hadnler.load_res_and_appointments(res_id, store)

    def load_purchase_rules_of_store(self, purchase_policy_root_id):
        res = self.__purchase_rules_handler.load(purchase_policy_root_id)
        if res.succeeded():
            return res
        else:
            return db_fail_response
    # def load_store_founder(self, store):
    #     self._rwlock.acquire_read()
    #     res = Response(True)
    #     try:
    #         store = session.query(Store).get(store_id)
    #         res_id = store.responsibility_id
    #         from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
    #         ResponsibilitiesHandler.get_instance().load_res(res_id, store_id)
    #     except DisconnectionError as e:
    #         session.rollback()
    #         res = Response(False, PrimitiveParsable(0), msg=str(e))
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         self._rwlock.release_read()
    #         return res
    #

    def load_ids(self):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            stmt = select(self.__stores.c.store_id)
            store_ids = session.execute(stmt).all()
            store_ids = map(lambda id_tuple: id_tuple[0], store_ids)
            res.object = store_ids
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res

    def load_all(self):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            stores = session.query(Store).all()
            succesfully_loaded = True
            for store in stores:
                # TODO: load responsibility using responsibility_handler.load_by_store_id(), add it to store

                # TODO: load root discount using discount_handler.load(), add it to store

                # TODO: load root rule using purchase_rule_handler.load(), add it to store

                loaded_products = self.__product_handler.load_products_by_store(store.get_id())
                if type(loaded_products) != str:
                    store.set_products(loaded_products)

                else:
                    session.rollback()
                    succesfully_loaded = False
                    res = Response(False, msg=loaded_products)
                    break
            if succesfully_loaded:
                res = Response(True, obj=ParsableList(stores))
                session.commit()

            else:
                session.rollback()

        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res


if __name__ == "__main__":
    pass

#     # store._Store__purchase_history = [
#     #     PurchaseDetails("Sean", "store", "abc", ["Banana", "Melon"], date(2000, 4, 13), 22),
#     #     PurchaseDetails("Inon", "store", "abc", ["PineApple", "Grapes"], date(2000, 4, 14), 25)]
#     #
#     # store.add_product("Oranges", "Fruit", 5, 8, ["Yummy", "Orange"])
#
#     res = store_handler.load("c6ba8b7c-c284-4334-baa1-346827534068")
#     if not res.succeeded():
#         print(res.get_msg())
#     else:
#         print(res.get_obj())

# purchase_details_hadnler = PurchaseDetailsHandler()
# member_handler = MemberHandler.get_instance()
# Base.metadata.create_all(engine)
# member_handler.save_user("Sean", "Pikulin")
# user = member_handler.load("Sean").get_obj()
# det = PurchaseDetails("Sean", "store", "abc", ["Banana", "Melon"], date(2000, 4, 13), 22)
# user.add_purchase_rule_history(det)
# purchase_details_hadnler.save(det)
# user_after = member_handler.load("Sean").get_obj()
# print("sfa")
