from Backend.DataBase.Handlers.store_handler import StoreHandler
from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response
from Backend.response import ParsableList
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class StoresManager:
    __store_handler = StoreHandler.get_instance()
    __stores: list[Store] = []

    # 2.5
    @staticmethod
    def get_stores_details() -> Response[ParsableList[Store]]:
        store_ids_res = StoresManager.__store_handler.load_ids()
        if store_ids_res.succeeded():
            for id in store_ids_res.get_obj():
                StoresManager.get_store(id)
            return Response(True, ParsableList(StoresManager.__stores))
        return store_ids_res

    # 2.5
    @staticmethod
    def get_products_by_store(store_id: str) -> Response[ParsableList[Product]]:
        StoresManager.get_store(store_id)
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
        store_res = StoresManager.__store_handler.load_store(store_id)
        if not store_res.succeeded():
            if store_res.get_obj() is None:
                return Response(False, msg=f"No store with the ID {store_id} exists")
            return db_fail_response

        store = store_res.get_obj()
        root_purchase_rule_res = StoresManager.__store_handler.load_purchase_rules(store.get_purchase_policy_root_id())
        root_discount_rule_res = StoresManager.__store_handler.load_discounts_rules_of_store(store.get_discounts_policy_root_id())

        if not root_purchase_rule_res.succeeded():
            return root_purchase_rule_res
        if not root_discount_rule_res.succeeded():
            return root_discount_rule_res

        
        store.set_root_purchase_rule(root_purchase_rule_res.get_obj())
        store.set_root_discounts_rule(root_discount_rule_res.get_obj())

        StoresManager.__stores.append(store)

        return Response[Store](True, obj=store)

    @staticmethod
    def get_product(store_id: str, product_id: str) -> Response:
        store_res = StoresManager.get_store(store_id)
        if store_res.succeeded():
            prod = store_res.get_obj().get_product(product_id)
            if prod is None:
                return Response(False, msg="The product does not exist!")
            return Response(True, prod)
        return store_res

    # used in 4.1
    @staticmethod
    def get_product_with_price(store_id: str, product_id: str, username: str) -> Response:
        response = StoresManager.get_product(store_id, product_id)
        if not response.succeeded():
            return response
        return Response(True, response.get_obj().parse_with_price(username))

    # 6.4
    @staticmethod
    def get_any_store_purchase_history(store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        for store in StoresManager.__stores:
            if store.get_id() == store_id:
                return store.get_purchase_history()
        return Response(False, msg=f"No store with the ID {store_id} exists")

