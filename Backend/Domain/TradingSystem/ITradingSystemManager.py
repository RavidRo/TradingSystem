from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem.product_data import product_data
from Backend.Domain.TradingSystem.store_data import store_data
from Backend.Domain.TradingSystem.shopping_cart_data import shopping_cart_data
from Backend.Domain.TradingSystem.purchase_details_data import purchase_details_data
from Backend.Domain.TradingSystem.responsibility_data import responsibility_data
from Backend.response import Response, ParsableList, PrimitiveParsable


class ITradingSystem(metaclass=ABC):

    # 2.1
    # returns the guest newly created cookie
    @abstractmethod
    def enter_system() -> str:
        raise NotImplementedError

    # 2.3
    @abstractmethod
    def register(username: str, password: str, cookie: str) -> Response[None]:
        raise NotImplementedError

    # 2.4
    @abstractmethod
    def login(username: str, password: str, cookie: str) -> Response[None]:
        raise NotImplementedError

    # 2.5
    @abstractmethod
    def get_stores_details() -> Response[ParsableList[store_data]]:
        raise NotImplementedError

    # 2.5
    @abstractmethod
    def get_products_by_store(store_id: str) -> Response[ParsableList[product_data]]:
        raise NotImplementedError

    # 2.6
    # kwargs = You can search for a product by additional key words
    @abstractmethod
    def search_products(
        product_name: str, *keywords: tuple[str], category: str, min_price: float, max_price: float
    ) -> Response[ParsableList[product_data]]:
        raise NotImplementedError

    # 2.7
    @abstractmethod
    def save_product_in_cart(
        cookie: str, store_id: str, product_id: str, quantity: int
    ) -> Response[None]:
        raise NotImplementedError

    # 2.8
    @abstractmethod
    def get_cart_details(cookie: str) -> Response[shopping_cart_data]:
        raise NotImplementedError

    # 2.8
    @abstractmethod
    def remove_product_from_cart(cookie: str, product_id: str) -> Response[None]:
        raise NotImplementedError

    # 2.8
    @abstractmethod
    def change_product_quantity_in_cart(cookie, store_id: str, product_id: str, new_quantity: int):
        raise NotImplementedError

    # 2.9
    @abstractmethod
    def purchase_cart(cookie: str) -> Response[PrimitiveParsable[float]]:
        raise NotImplementedError

    # 2.9
    @abstractmethod
    def purchase_completed(cookie: str) -> Response[None]:
        raise NotImplementedError

    @abstractmethod
    def get_cart_price(cookie: str) -> Response[PrimitiveParsable[float]]:
        raise NotImplementedError

    # Member
    # ===============================

    # 3.2
    @abstractmethod
    def create_store(cookie: str, name: str) -> Response[None]:
        raise NotImplementedError

    # 3.7
    @abstractmethod
    def ger_purchase_history(cookie: str) -> Response[ParsableList[purchase_details_data]]:
        raise NotImplementedError

    # Owner and manager
    # =======================

    # 4.1
    # Creating a new product a the store and setting its quantity to 0
    @abstractmethod
    def create_product(
        cookie: str, store_id: str, name: str, price: float, quantity: int
    ) -> Response[None]:
        raise NotImplementedError

    # 4.1
    @abstractmethod
    def remove_products(cookie: str, store_id: str, product_id: str) -> Response[None]:
        raise NotImplementedError

    # 4.1
    @abstractmethod
    def change_product_quantity(
        cookie: str, store_id: str, product_id: str, quantity: int
    ) -> Response[None]:
        raise NotImplementedError

    # 4.1
    @abstractmethod
    def edit_product_details(
        cookie: str, store_id: str, product_id: str, new_name: str, new_price: float
    ) -> Response[None]:
        raise NotImplementedError

    # 4.3
    def appoint_owner(cookie: str, store_id: str, username: str) -> Response[None]:
        raise NotImplementedError

    # 4.5
    @abstractmethod
    def appoint_manager(cookie: str, store_id: str, username: str) -> Response[None]:
        raise NotImplementedError

    # 4.6
    @abstractmethod
    def add_manager_permission(
        cookie: str, store_id: str, username: str, permission_number: int
    ) -> Response[None]:
        raise NotImplementedError

    # 4.6
    @abstractmethod
    def remove_manager_permission(
        cookie: str, store_id: str, username: str, permission_number: int
    ) -> Response[None]:
        raise NotImplementedError

    # 4.4, 4.7
    @abstractmethod
    def remove_appointment(cookie: str, store_id: str, username: str) -> Response[None]:
        raise NotImplementedError

    # 4.9
    @abstractmethod
    def get_store_appointments(cookie: str, store_id: str) -> Response[responsibility_data]:
        raise NotImplementedError

    # 4.11
    @abstractmethod
    def get_store_purchases_history(
        cookie: str, store_id: str
    ) -> Response[ParsableList[purchase_details_data]]:
        raise NotImplementedError

    # System Manager
    # ====================

    # 6.4
    @abstractmethod
    def get_user_purchase_history(
        cookie: str, username: str
    ) -> Response[ParsableList[purchase_details_data]]:
        raise NotImplementedError

    # 6.4
    @abstractmethod
    def get_any_store_purchase_history(
        cookie: str, store_id: str
    ) -> Response[ParsableList[purchase_details_data]]:
        raise NotImplementedError
