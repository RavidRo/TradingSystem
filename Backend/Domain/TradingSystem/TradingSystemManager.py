from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.user_manager import UserManager
from Backend.Domain.TradingSystem.search_engine import SearchEngine
from Backend.Domain.TradingSystem.Responsibilities.responsibility import permissions
from Backend.Domain.TradingSystem.product_data import product_data
from Backend.Domain.TradingSystem.store_data import store_data
from Backend.Domain.TradingSystem.shopping_cart_data import shopping_cart_data
from Backend.Domain.TradingSystem.purchase_details_data import purchase_details_data
from Backend.Domain.TradingSystem.purchase_details import purchase_details
from Backend.Domain.TradingSystem.responsibility_data import responsibility_data
from Backend.Domain.TradingSystem.ITradingSystemManager import ITradingSystem
from Backend.response import Response, ParsableList, PrimitiveParsable

class TradingSystem(ITradingSystem):

    # 2.1
    # returns the guest newly created cookie
    def enter_system() -> str:
        return UserManager.enter_system()

    # 2.3
    def register(username: str, password: str, cookie: str) -> Response[None]:
        return UserManager.register(username, password, cookie)

    # 2.4
    def login(username: str, password: str, cookie: str) -> Response[None]:
        return UserManager.login(username, password, cookie)

    # 2.5
    def get_stores_details() -> Response[ParsableList[store_data]]:
        return StoresManager.get_stores_details().parse()

    # 2.5
    def get_products_by_store(store_id: str) -> Response[ParsableList[product_data]]:
        return StoresManager.get_products_by_store(store_id).parse()

    # 2.6
    # kwargs = You can search for a product by additional key words
    def search_products(
        product_name="", category=None, min_price=None, max_price=None, *keywords: tuple[str]
    ) -> Response[ParsableList[product_data]]:
        return SearchEngine.search_products(product_name, category, min_price, max_price, *keywords).parse()

    # 2.7
    def save_product_in_cart(cookie: str, store_id: str, product_id: str, quantity=1) -> Response[None]:
        return UserManager.add_to_cart(cookie, store_id, product_id, quantity)

    # 2.8
    def get_cart_details(cookie: str) -> Response[shopping_cart_data]:
        return UserManager.get_cart_details(cookie).parse()

    # 2.8
    def remove_product_from_cart(cookie: str, product_id: str) -> Response[None]:
        return UserManager.remove_product_from_cart(cookie, product_id)

    # 2.8
    def change_product_quantity_in_cart(self, store_id: str, product_id: str, new_quantity: int) -> Response[None]:
        return UserManager.change_product_quantity_in_cart(store_id, product_id, new_quantity)

    # 2.9
    def purchase_cart(cookie: str) -> Response[PrimitiveParsable[float]]:
        return UserManager.purchase_cart(cookie).parse()

    # 2.9
    def purchase_completed(cookie: str) -> Response[None]:
        return UserManager.purchase_completed(cookie)

    def get_cart_price(cookie: str) -> Response[PrimitiveParsable[float]]:
        return UserManager.get_cart_price(cookie)

    # Member
    # ===============================

    # 3.2
    def create_store(cookie: str, name: str) -> Response[None]:
        Response = UserManager.create_store(cookie, name)
        if Response.success:
            return StoresManager.create_store(Response.data)
        return Response

    # 3.7
    def ger_purchase_history(cookie: str) -> Response[ParsableList[purchase_details_data]]:
        return UserManager.ger_purchase_history(cookie).parse()

    # Owner and manager
    # =======================

    # 4.1
    # Creating a new product a the store and setting its quantity to 0
    def create_product(cookie: str, store_id: str, name: str, price: float, quantity: int) -> Response[None]:
        return UserManager.create_product(cookie, store_id, name, price, quantity)

    # 4.1
    def remove_products(cookie: str, store_id: str, product_id: str) -> Response[None]:
        return UserManager.remove_products(cookie, store_id, product_id)

    # 4.1
    def change_product_quantity(cookie: str, store_id: str, product_id: str, quantity: int) -> Response[None]:
        return UserManager.change_product_quantity(cookie, store_id, product_id, quantity)

    # 4.1
    def edit_product_details(cookie: str, store_id: str, product_id: str, new_name: str, new_price: float) -> Response[None]:
        return UserManager.set_product_price(cookie, store_id, product_id, new_name, new_price)

    # 4.3
    def appoint_owner(cookie: str, store_id: str, username: str) -> Response[None]:
        return UserManager.appoint_owner(cookie, store_id, username)

    # 4.5
    def appoint_manager(cookie: str, store_id: str, username: str) -> Response[None]:
        return UserManager.appoint_manager(cookie, store_id, username)

    # 4.6
    def add_manager_permission(cookie: str, store_id: str, username: str, permission_number: int) -> Response[None]:
        return UserManager.add_manager_permission(cookie, store_id, username, permissions(permission_number))

    # 4.6
    def remove_manager_permission(cookie: str, store_id: str, username: str, permission_number: int) -> Response[None]:
        return UserManager.remove_manager_permission(cookie, store_id, username, permissions(permission_number))

    # 4.4, 4.7
    def remove_appointment(cookie: str, store_id: str, username: str) -> Response[None]:
        return UserManager.remove_appointment(cookie, store_id, username)

    # 4.9
    def get_store_appointments(cookie: str, store_id: str) -> Response[responsibility_data]:
        return UserManager.get_store_appointments(cookie, store_id).parse()

    # 4.11
    def get_store_purchases_history(cookie: str, store_id: str) -> Response[ParsableList[purchase_details_data]]:
        return UserManager.get_store_purchases_history(cookie, store_id).parse()

    # System Manager
    # ====================

    # 6.4
    def get_any_user_purchase_history(cookie: str, username: str) -> Response[ParsableList[purchase_details_data]]:
        return UserManager.get_any_user_purchase_history(cookie, username).parse()

    # 6.4
    def get_any_store_purchase_history(cookie: str, store_id: str) -> Response[ParsableList[purchase_details_data]]:
        return UserManager.get_any_store_purchase_history(cookie, store_id).parse()

    # Inter component functions
    # ============================
    # 6.4
    def get_any_user_purchase_history(username: str) -> Response[ParsableList[purchase_details]]:
        return UserManager.get_any_user_purchase_history(username).parse()

    # 6.4
    def get_any_store_purchase_history(store_id: str) -> Response[ParsableList[purchase_details]]:
        return StoresManager.get_any_store_purchase_history(store_id).parse()
