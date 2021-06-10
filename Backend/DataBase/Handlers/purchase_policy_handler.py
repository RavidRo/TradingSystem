from threading import Lock

from sqlalchemy import Table, Column

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import mapper_registry
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseRule
from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import PurchasePolicy
from Backend.rw_lock import ReadWriteLock


class PurchasePolicyHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), PurchaseRule)

        self.__purchase_rules = Table("stores", mapper_registry.metadata,
                              Column("store_id", String(50), primary_key=True),
                              Column("store_name", String(30)),
                              Column("responsibility_id", String(30), ForeignKey('responsibilities.responsibility_id')))

        mapper_registry.map_imperatively(ProductsOfStores, self.__products_of_stores, properties={
            "store_id": self.__products_of_stores.c.store_id,
            "product_id": self.__products_of_stores.c.product_id,
            "quantity": self.__products_of_stores.c.quantity,
            "product": relationship(Product, cascade="all", uselist=False)
        })

        mapper_registry.map_imperatively(Store, self.__stores, properties={
            "_Store__id": self.__stores.c.store_id,
            "_Store__name": self.__stores.c.store_name,
            "_Store__responsibility_id": self.__stores.c.responsibility_id,
            "_Store__purchase_history": relationship(PurchaseDetails),
            "products": relationship(ProductsOfStores, uselist=True,
                                     collection_class=attribute_mapped_collection("product_id"))
        })

        self.__product_handler = ProductHandler.get_instance()

    @staticmethod
    def get_instance():
        with StoreHandler._lock:
            if StoreHandler._instance is None:
                StoreHandler._instance = StoreHandler()
        return StoreHandler._instance