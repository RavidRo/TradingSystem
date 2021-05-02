from typing import Callable

from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.user_manager import UserManager
from Backend.Domain.TradingSystem.search_engine import SearchEngine
from Backend.Domain.TradingSystem.Responsibilities.responsibility import name_to_permission
from Backend.Service.DataObjects.product_data import ProductData
from Backend.Service.DataObjects.store_data import StoreData
from Backend.Service.DataObjects.shopping_cart_data import ShoppingCartData
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Service.DataObjects.responsibilities_data import ResponsibilitiesData

from Backend.response import Response, ParsableList, PrimitiveParsable


class TradingSystemManager:

    # 2.1
    # returns the guest newly created cookie
    @staticmethod
    def enter_system() -> str:
        return UserManager.enter_system()

    @staticmethod
    def connect(cookie: str, communicate: Callable[[list[str]], bool]) -> Response[None]:
        return UserManager.connect(cookie, communicate)

    # 2.3
    @staticmethod
    def register(username: str, password: str, cookie: str) -> Response[None]:
        return UserManager.register(username, password, cookie)

    # 2.4
    @staticmethod
    def login(username: str, password: str, cookie: str) -> Response[None]:
        return UserManager.login(username, password, cookie)

    # 2.5
    @staticmethod
    def get_stores_details() -> Response[ParsableList[StoreData]]:
        return StoresManager.get_stores_details().parse()

    # 2.5
    @staticmethod
    def get_products_by_store(store_id: str) -> Response[ParsableList[ProductData]]:
        return StoresManager.get_products_by_store(store_id).parse()

    @staticmethod
    def get_store(store_id: str) -> Response[StoreData]:
        return StoresManager.get_store(store_id).parse()

    # 2.6
    # kwargs = You can search for a product by additional key words
    @staticmethod
    def search_products(
        product_name: str, product_category: str, min_price, max_price, keywords
    ) -> Response[ParsableList[ProductData]]:
        return SearchEngine.search_products(
            product_name, product_category, min_price, max_price, keywords
        ).parse()

    # 2.7
    @staticmethod
    def save_product_in_cart(
        cookie: str, store_id: str, product_id: str, quantity
    ) -> Response[None]:
        return UserManager.add_to_cart(cookie, store_id, product_id, quantity)

    # 2.8
    @staticmethod
    def get_cart_details(cookie: str) -> Response[ShoppingCartData]:
        return UserManager.get_cart_details(cookie).parse()

    # 2.8
    @staticmethod
    def remove_product_from_cart(cookie: str, store_id: str, product_id: str) -> Response[None]:
        return UserManager.remove_product_from_cart(cookie, store_id, product_id)

    # 2.8
    @staticmethod
    def change_product_quantity_in_cart(
        cookie: str, store_id: str, product_id: str, new_quantity: int
    ) -> Response[None]:
        return UserManager.change_product_quantity_in_cart(
            cookie, store_id, product_id, new_quantity
        )

    # 2.9
    @staticmethod
    def purchase_cart(cookie: str, user_age: int) -> Response[PrimitiveParsable[float]]:
        return UserManager.purchase_cart(cookie, user_age)

    # 2.9
    @staticmethod
    def purchase_completed(cookie: str) -> Response[None]:
        return UserManager.purchase_completed(cookie)

    @staticmethod
    def get_cart_price(cookie: str) -> Response[PrimitiveParsable[float]]:
        return UserManager.get_cart_price(cookie)

    # Member
    # ===============================

    # 3.2
    @staticmethod
    def create_store(cookie: str, name: str) -> Response[str]:
        Response = UserManager.create_store(cookie, name)
        if Response.succeeded():
            return StoresManager.create_store(Response.get_obj())
        return Response

    # 3.7
    @staticmethod
    def get_purchase_history(cookie: str) -> Response[ParsableList[PurchaseDetails]]:
        return UserManager.get_purchase_history(cookie)

    # Owner and manager
    # =======================

    # 4.1
    # Creating a new product and returns its id
    @staticmethod
    def create_product(
        cookie: str,
        store_id: str,
        name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str] = None,
    ) -> Response[str]:
        return UserManager.create_product(
            cookie, store_id, name, category, price, quantity, keywords
        )

    # 4.1
    @staticmethod
    def remove_product_from_store(
        cookie: str, store_id: str, product_id: str
    ) -> Response[PrimitiveParsable[int]]:
        return UserManager.remove_product_from_store(cookie, store_id, product_id)

    # 4.1
    @staticmethod
    def change_product_quantity_in_store(
        cookie: str, store_id: str, product_id: str, quantity: int
    ) -> Response[None]:
        return UserManager.change_product_quantity_in_store(cookie, store_id, product_id, quantity)

    # 4.1
    @staticmethod
    def edit_product_details(
        cookie: str,
        store_id: str,
        product_id: str,
        new_name: str,
        new_category,
        new_price: float,
        keywords: list[str] = None,
    ) -> Response[None]:
        return UserManager.edit_product_details(
            cookie, store_id, product_id, new_name, new_category, new_price, keywords
        )

    # 4.2
    @staticmethod
    def add_discount(
        cookie: str, store_id: str, discount_data: dict, exist_id: str, condition_type: str = None
    ):
        return UserManager.add_discount(cookie, store_id, discount_data, exist_id, condition_type)

    @staticmethod
    def move_discount(cookie: str, store_id: str, src_id: str, dest_id: str):
        return UserManager.move_discount(cookie, store_id, src_id, dest_id)

    @staticmethod
    def get_discounts(cookie: str, store_id: str):
        return UserManager.get_discounts(cookie, store_id)

    @staticmethod
    def remove_discount(cookie: str, store_id: str, discount_id: str):
        return UserManager.remove_discount(cookie, store_id, discount_id)

    @staticmethod
    def edit_simple_discount(
        cookie: str,
        store_id: str,
        discount_id: str,
        percentage: float = None,
        context: dict = None,
        duration=None,
    ):
        return UserManager.edit_simple_discount(
            cookie, store_id, discount_id, percentage, context, duration
        )

    @staticmethod
    def edit_complex_discount(
        cookie: str,
        store_id: str,
        discount_id: str,
        complex_type: str = None,
        decision_rule: str = None,
    ):
        return UserManager.edit_complex_discount(
            cookie, store_id, discount_id, complex_type, decision_rule
        )

    # 4.2
    @staticmethod
    def add_purchase_rule(
        cookie: str,
        store_id: str,
        rule_details: dict,
        rule_type: str,
        parent_id: str,
        clause: str = None,
    ) -> Response[None]:
        return UserManager.add_purchase_rule(
            cookie, store_id, rule_details, rule_type, parent_id, clause
        )

    # 4.2
    @staticmethod
    def remove_purchase_rule(cookie: str, store_id: str, rule_id: str) -> Response[None]:
        return UserManager.remove_purchase_rule(cookie, store_id, rule_id)

    # 4.2
    @staticmethod
    def edit_purchase_rule(
        cookie: str, store_id: str, rule_details: dict, rule_id: str, rule_type: str
    ) -> Response[None]:
        return UserManager.edit_purchase_rule(cookie, store_id, rule_details, rule_id, rule_type)

    # 4.2
    @staticmethod
    def move_purchase_rule(
        cookie: str, store_id: str, rule_id: str, new_parent_id: str
    ) -> Response[None]:
        return UserManager.move_purchase_rule(cookie, store_id, rule_id, new_parent_id)

    # 4.2
    @staticmethod
    def get_purchase_policy(cookie: str, store_id: str):
        return UserManager.get_purchase_policy(cookie, store_id).parse()

    # 4.3
    @staticmethod
    def appoint_owner(cookie: str, store_id: str, username: str) -> Response[None]:
        return UserManager.appoint_owner(cookie, store_id, username)

    # 4.5
    @staticmethod
    def appoint_manager(cookie: str, store_id: str, username: str) -> Response[None]:
        return UserManager.appoint_manager(cookie, store_id, username)

    # 4.6
    @staticmethod
    def add_manager_permission(
        cookie: str, store_id: str, username: str, permission: str
    ) -> Response[None]:
        if permission not in name_to_permission:
            return Response(False, msg="Invalid permission was given")
        return UserManager.add_manager_permission(
            cookie, store_id, username, name_to_permission[permission]
        )

    # 4.6
    @staticmethod
    def remove_manager_permission(
        cookie: str, store_id: str, username: str, permission: str
    ) -> Response[None]:
        if permission not in name_to_permission:
            return Response(False, msg="Invalid permission was given")
        return UserManager.remove_manager_permission(
            cookie, store_id, username, name_to_permission[permission]
        )

    # 4.4, 4.7
    @staticmethod
    def remove_appointment(cookie: str, store_id: str, username: str) -> Response[None]:
        return UserManager.remove_appointment(cookie, store_id, username)

    # 4.9
    @staticmethod
    def get_store_appointments(cookie: str, store_id: str) -> Response[ResponsibilitiesData]:
        return UserManager.get_store_appointments(cookie, store_id).parse()

    @staticmethod
    def get_my_appointments(cookie: str) -> Response[ParsableList[ResponsibilitiesData]]:
        return UserManager.get_my_appointments(cookie).parse()

    # 4.11
    @staticmethod
    def get_store_purchase_history(
        cookie: str, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        return UserManager.get_store_purchase_history(cookie, store_id)

    # System Manager
    # ====================

    # 6.4
    @staticmethod
    def get_any_user_purchase_history_admin(
        cookie: str, username: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        return UserManager.get_any_user_purchase_history_admin(cookie, username)

    # 6.4
    @staticmethod
    def get_any_store_purchase_history_admin(
        cookie: str, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        return UserManager.get_any_store_purchase_history_admin(cookie, store_id)

    # Inter component functions
    # ============================
    # 6.4
    @staticmethod
    def get_any_user_purchase_history(username: str) -> Response[ParsableList[PurchaseDetails]]:
        return UserManager.get_any_user_purchase_history(username)

    # 6.4
    @staticmethod
    def get_any_store_purchase_history(store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        return StoresManager.get_any_store_purchase_history(store_id)

    @staticmethod
    def lock_cart(cookie):
        return UserManager.lock_cart(cookie)

    @staticmethod
    def release_cart(cookie):
        return UserManager.release_cart(cookie)

    @staticmethod
    def cancel_purchase(cookie):
        return UserManager.cancel_purchase(cookie)

    @staticmethod
    def empty_notifications(cookie):
        return UserManager.empty_notifications(cookie)
