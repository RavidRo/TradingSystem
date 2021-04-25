from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response
from Backend.response import ParsableList
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class StoresManager:
    __stores: list[Store] = []

    # 2.5
    @staticmethod
    def get_stores_details() -> Response[ParsableList[Store]]:
        return Response(True, ParsableList(StoresManager.__stores))

    # 2.5
    @staticmethod
    def get_products_by_store(store_id: str) -> Response[ParsableList[Product]]:
        for store in StoresManager.__stores:
            if store.get_id() == store_id:
                return store.get_products()
        return Response(False, msg=f"No store with the ID {store_id} exists")

    # 2.6
    @staticmethod
    def get_products() -> Response[list[Product]]:
        products_per_store = map(
            lambda store: store.get_products().object.values, StoresManager.__stores
        )
        products = []
        # iterating over the data
        for product_list in products_per_store:
            # appending elements to the flat_list
            products += product_list

        return Response(True, ParsableList(products))

    # Inter component functions
    # used in 3.2
    @staticmethod
    def create_store(store: Store) -> Response[str]:
        StoresManager.__stores.append(store)
        return Response(True, store.get_id())

    @staticmethod
    def get_store(store_id: str) -> Response[Store]:
        for store in StoresManager.__stores:
            if store.get_id() == store_id:
                return Response[Store](True, obj=store)
        return Response(False, msg=f"No store with the ID {store_id} exists")

    # 6.4
    @staticmethod
    def get_any_store_purchase_history(store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        for store in StoresManager.__stores:
            if store.get_id() == store_id:
                return store.get_purchase_history()
        return Response(False, msg=f"No store with the ID {store_id} exists")
