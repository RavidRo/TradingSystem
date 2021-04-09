from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response
from Backend.response import ParsableList
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class StoresManager:
    stores: list[Store] = []

    # 2.5
    def get_stores_details(self) -> Response[ParsableList[Store]]:
        return Response(True, ParsableList(StoresManager.stores))

    # 2.5
    def get_products_by_store(store_id: str) -> Response[ParsableList[Product]]:
        for store in StoresManager.stores:
            if store.get_id():
                return store.get_products()
        return Response(False, msg=f"No store with the ID {store_id} exists")

    # 2.6
    def get_products(self) -> Response[list[Product]]:
        products_per_store = map(lambda store: store.get_p(), StoresManager.stores)
        products = []
        # iterating over the data
        for product_list in products_per_store:
            # appending elements to the flat_list
            products += product_list

        return products

    # Inter component functions
    # used in 3.2
    def create_store(store: Store) -> None:
        StoresManager.stores.append(store)

    def get_store(store_id: str):
        for store in StoresManager.stores:
            if store.get_id():
                return Response(True, store)
        return Response(False, msg=f"No store with the ID {store_id} exists")

    # 6.4
    def get_any_store_purchase_history(store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        for store in StoresManager.stores:
            if store.get_id():
                return store.get_purchase_history()
        return Response(False, msg=f"No store with the ID {store_id} exists")
