from Backend.response import Response
from Backend.response import ParsableList
from Backend.Domain.TradingSystem.Interfaces.IStore import IStore as store
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class StoresManager:
    stores: list[store] = []

    # 2.5
    def get_stores_details(self) -> Response[ParsableList[store]]:
        return Response(True, ParsableList(StoresManager.stores))

    # 2.5
    def get_products_by_store(store_id: str) -> Response[ParsableList[product]]:
        for store in StoresManager.stores:
            if store.get_id():
                return store.show_store_data()
        return Response(False, msg=f"No store with the ID {store_id} exists")

    # 2.6
    def get_products(self) -> list[product]:
        products_per_store = map(lambda store: store.show_store_data(), StoresManager.stores)
        products = []
        # iterating over the data
        for product_list in products_per_store:
            # appending elements to the flat_list
            products += product_list

        return products

    # Inter component functions
    # used in 3.2
    def create_store(store: store) -> None:
        StoresManager.stores.append(store)

    def get_store(store_id):
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
