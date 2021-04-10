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

    # 2.6
    # kwargs = You can search for a product by additional key words
    @staticmethod
    def search_products(
        *keywords, product_name, category, min_price, max_price
    ) -> Response[ParsableList[ProductData]]:
        return SearchEngine.search_products(
            product_name, category, min_price, max_price, *keywords
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
        self, store_id: str, product_id: str, new_quantity: int
    ) -> Response[None]:
        return UserManager.change_product_quantity_in_cart(store_id, product_id, new_quantity)

    # 2.9
    @staticmethod
    def purchase_cart(cookie: str) -> Response[PrimitiveParsable[float]]:
        return UserManager.purchase_cart(cookie).parse()

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
    def create_store(cookie: str, name: str) -> Response[None]:
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
    # Creating a new product a the store and setting its quantity to 0
    @staticmethod
    def create_product(
        cookie: str, store_id: str, name: str, price: float, quantity: int
    ) -> Response[None]:
        return UserManager.create_product(cookie, store_id, name, price, quantity)

    # 4.1
    @staticmethod
    def remove_product_from_store(cookie: str, store_id: str, product_id: str) -> Response[None]:
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
        cookie: str, store_id: str, product_id: str, new_name: str, new_price: float
    ) -> Response[None]:
        return UserManager.edit_product_details(cookie, store_id, product_id, new_name, new_price)

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
        return UserManager.add_manager_permission(
            cookie, store_id, username, name_to_permission[permission]
        )

    # 4.6
    @staticmethod
    def remove_manager_permission(
        cookie: str, store_id: str, username: str, permission: str
    ) -> Response[None]:
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
