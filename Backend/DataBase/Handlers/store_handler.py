from datetime import date

from sqlalchemy import Table, Column, String, insert
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.Handlers.member_handler import MemberHandler
from Backend.DataBase.Handlers.product_handler import ProductHandler
from Backend.DataBase.Handlers.purchase_details_handler import PurchaseDetailsHandler
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session, engine
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class StoreHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        self.__stores = Table("stores", Base.metadata,
                              Column("store_id", String(50), primary_key=True),
                              Column("store_name", String(30)))

        mapper(Store, self.__stores, properties={
            "_Store__id": self.__stores.c.store_id,
            "_Store__name": self.__stores.c.store_name,
            "_Store__purchase_history": relationship(PurchaseDetails, lazy='joined')
        })

        self.__product_handler = ProductHandler.get_instance()

    @staticmethod
    def get_instance():
        with StoreHandler._lock:
            if StoreHandler._instance is None:
                StoreHandler._instance = StoreHandler()
        return StoreHandler._instance

    def save(self, obj: Store, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        session = Session()
        res = Response(True)
        try:
            session.add(obj)

            # stmt = insert(Base.metadata.tables['responsibilities']).values(
            #     username=obj.get_responsibility().get_user_state().get_username().get_obj(),
            #     store_id=obj.get_id(),
            #     parent_id=None,
            #     responsibility_type="F")
            # session.execute(stmt)

            # TODO: save discount using discounts_handler

            # TODO: save purchase_rule using purchase_rule_handler

            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_write()
            return res

    def remove(self, obj, **kwargs) -> Response[None]:
        pass

    def update(self, id, update_dict):
        pass

    def load(self, id):
        self._rwlock.acquire_read()
        session = Session(expire_on_commit=False)
        res = Response(True)
        try:
            store = session.query(Store).get(id)

            # TODO: load responsibility using responsibility_handler.load_by_store_id(), add it to store

            # TODO: load root discount using discount_handler.load(), add it to store

            # TODO: load root rule using purchase_rule_handler.load(), add it to store

            session.commit()
            res = Response(True, store)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            session.close()
            self._rwlock.release_read()
            return res

    def load_all(self):
        pass


if __name__ == "__main__":
    store_handler = StoreHandler.get_instance()
    purchase_details_handler = PurchaseDetailsHandler.get_instance()
    member_handler = MemberHandler.get_instance()
    Base.metadata.create_all(engine)
    # store = Store("store")
    # store._Store__purchase_history = [
    #     PurchaseDetails("Sean", "store", "abc", ["Banana", "Melon"], date(2000, 4, 13), 22),
    #     PurchaseDetails("Inon", "store", "abc", ["PineApple", "Grapes"], date(2000, 4, 14), 25)]
    #
    # store.add_product("Oranges", "Fruit", 5, 8, ["Yummy", "Orange"])
    # res = store_handler.save(store)

    res = store_handler.load("c6ba8b7c-c284-4334-baa1-346827534068")
    if not res.succeeded():
        print(res.get_msg())
    else:
        print(res.get_obj())

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
