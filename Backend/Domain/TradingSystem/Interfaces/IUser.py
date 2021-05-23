from __future__ import annotations
from typing import Callable

from Backend.Domain.TradingSystem.offer import Offer
from Backend.Domain.TradingSystem.Interfaces.Subscriber import Subscriber
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.States.user_state import UserState


class IUser(Subscriber):

    # Used for testing purposes
    use_mock = False

    @staticmethod
    def create_user():
        from Backend.Tests.stubs.user_stub import UserStub
        from Backend.Domain.TradingSystem.user import User

        if IUser.use_mock:
            return UserStub()
        return User()

    def get_communicate(self) -> Callable[[list[str]], bool]:
        raise NotImplementedError

    # 2.3
    def register(self, username: str, password: str) -> Response[None]:
        raise NotImplementedError

    def connect(self, communicate: Callable[[list[str]], bool]) -> bool:
        raise NotImplementedError

    # 2.4
    def login(self, username: str, password: str) -> Response[None]:
        raise NotImplementedError

    # 2.7
    def add_to_cart(self, stor_id: str, product_id: str, quantity: int) -> Response[None]:
        raise NotImplementedError

    # 2.8
    def get_cart_details(self) -> Response[ShoppingCart]:
        raise NotImplementedError

    # 2.8
    def remove_product_from_cart(self, store_id: str, product_id: str) -> Response[None]:
        raise NotImplementedError

    # 2.8
    def change_product_quantity_in_cart(self, store_id, product_id, new_amount) -> Response[None]:
        raise NotImplementedError

    def get_discounted_current_cart_price(self):
        raise NotImplementedError

    # 2.9
    def purchase_cart(self, user_age: int) -> Response[PrimitiveParsable[float]]:
        raise NotImplementedError

    # 2.9
    def purchase_completed(self) -> Response[None]:
        raise NotImplementedError

    # 2.9
    def get_cart_price(self) -> Response[PrimitiveParsable[float]]:
        raise NotImplementedError

    # Member
    # ===============================

    # 3.2
    def create_store(self, name: str) -> Response[None]:
        raise NotImplementedError

    # 3.7
    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        raise NotImplementedError

    # Owner and manager
    # =======================

    # 4.1
    # Creating a new product a the store and setting its quantity to 0
    def create_product(
        self,
        store_id: str,
        name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str],
    ) -> Response[None]:
        raise NotImplementedError

    # 4.1
    def remove_product_from_store(self, store_id: str, product_id: str) -> Response[None]:
        raise NotImplementedError

    # 4.1
    def change_product_quantity_in_store(
        self, store_id: str, product_id: str, new_quantity: int
    ) -> Response[None]:
        raise NotImplementedError

    # 4.1
    def edit_product_details(
        self,
        store_id: str,
        product_id: str,
        new_name: str,
        new_category: str,
        new_price: float,
        keywords: list[str],
    ) -> Response[None]:
        raise NotImplementedError

    # 4.3
    def appoint_owner(self, store_id: str, user: IUser) -> Response[None]:
        raise NotImplementedError

    # 4.5
    def appoint_manager(self, store_id: str, user: IUser) -> Response[None]:
        raise NotImplementedError

    # 4.6
    def add_manager_permission(self, store_id: str, username: str, permission) -> Response[None]:
        raise NotImplementedError

    # 4.6
    def remove_manager_permission(self, store_id: str, username: str, permission) -> Response[None]:
        raise NotImplementedError

    # 4.4, 4.7
    def remove_appointment(self, store_id: str, username: str) -> Response[None]:
        raise NotImplementedError

    # 4.9
    def get_store_appointments(self, store_id: str) -> Response:
        raise NotImplementedError

    # 4.11
    def get_store_purchase_history(self, store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        raise NotImplementedError

    # System Manager
    # ====================

    # 6.4
    def get_any_user_purchase_history_admin(
        self, username: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        raise NotImplementedError

    # 6.4
    def get_any_store_purchase_history_admin(
        self, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        raise NotImplementedError

    # Inter component functions
    # ====================

    def is_appointed(self, store_id: str) -> Response[bool]:
        raise NotImplementedError

    def get_username(self) -> Response[PrimitiveParsable[str]]:
        raise NotImplementedError

    def change_state(self, new_state: UserState) -> None:
        raise NotImplementedError

    def get_appointment_lock(self):
        raise NotImplementedError

    def notify(self, message: str) -> bool:
        raise NotImplementedError

    # Offers
    # ==================

    def get_user_offers(self) -> Response[ParsableList[Offer]]:
        raise NotImplementedError

    def get_store_offers(self, store_id) -> Response[ParsableList[Offer]]:
        raise NotImplementedError

    def create_offer(self, store_id, product_id) -> Response[None]:
        raise NotImplementedError

    def declare_price(self, offer_id, price) -> Response[None]:
        raise NotImplementedError

    def suggest_counter_offer(self, store_id, product_id, offer_id, price) -> Response[None]:
        raise NotImplementedError

    def approve_manager_offer(self, offer_id) -> Response[None]:
        raise NotImplementedError

    def approve_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        raise NotImplementedError

    def reject_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        raise NotImplementedError

    def cancel_offer(self, offer_id) -> Response[None]:
        raise NotImplementedError
