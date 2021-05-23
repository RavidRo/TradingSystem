import threading
from typing import Callable

from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.response import ParsableList, PrimitiveParsable, Response
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.States.user_state import UserState

from .member_stub import MemberStub


class UserStub(IUser):
    def __init__(self, state=None) -> None:
        if state is None:
            state = MemberStub()
        self.state = state
        self.registered = False
        self.can_register = True
        self.can_login = True
        self._add_to_cart = False
        self._get_cart_details = False
        self._remove_product_from_cart = False
        self._change_product_quantity_in_cart = False
        self._change_product_quantity_in_store = False
        self._purchase_cart = False
        self._purchase_completed = False
        self._get_cart_price = False
        self._create_store = False
        self._get_purchase_history = False
        self._create_store = False
        self._remove_product_from_store = False
        self._edit_product_details = False
        self._appoint_owner = False
        self._appoint_manager = False
        self._add_manager_permission = False
        self._remove_appointment = False
        self._get_store_appointments = False
        self._get_any_store_purchase_history = False
        self._get_any_user_purchase_history = False
        self._create_product = False
        self._remove_manager_permission = False
        self._get_store_purchase_history = False
        self.notified = False

    def is_appointed(self, store_id):
        return Response(True, self.state.is_appointed(store_id))

    def appoint(self, store_id):
        return self.state.appoint(store_id)

    def get_username(self) -> str:
        return self.state.get_username()

    def set_username(self, username):
        self.state.username = username

    def register(self, username, password):
        self.registered = True
        return Response(self.can_register)

    def login(self, username: str, password: str) -> Response[None]:
        if not self.registered:
            return Response(False)
        return Response(self.can_login)

    def add_to_cart(self, stor_id: str, product_id: str, quantity: int) -> Response[None]:
        self._add_to_cart = True
        return Response(True)

    def get_cart_details(self) -> Response[ShoppingCart]:
        self._get_cart_details = True
        return Response(True)

    def remove_product_from_cart(self, store_id: str, product_id: str) -> Response[None]:
        self._remove_product_from_cart = True
        return Response(True)

    def change_product_quantity_in_cart(
        self, store_id: str, product_id: str, new_quantity: int
    ) -> Response[None]:
        self._change_product_quantity_in_cart = True
        return Response(True)

    def purchase_cart(self, age: int) -> Response[PrimitiveParsable[float]]:
        self._purchase_cart = True
        return Response(True)

    def purchase_completed(self) -> Response[None]:
        self._purchase_completed = True
        return Response(True)

    def get_cart_price(self) -> Response[PrimitiveParsable[float]]:
        self._get_cart_price = True
        return Response(True)

    def create_store(self, name: str) -> Response[None]:
        self._create_store = True
        return Response(True)

    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        self._get_purchase_history = True
        return Response(True)

    def remove_product_from_store(self, store_id: str, product_id: str) -> Response[None]:
        self._remove_product_from_store = True
        return Response(True)

    def create_product(
        self,
        store_id: str,
        name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str],
    ) -> Response[None]:
        self._create_product = True
        return Response(True)

    def change_product_quantity_in_store(
        self, store_id: str, product_id: str, new_quantity: int
    ) -> Response[None]:
        self._change_product_quantity_in_store = True
        return Response(True)

    def edit_product_details(
        self,
        store_id: str,
        product_id: str,
        new_name: str,
        category: str,
        new_price: float,
        keywords: list[str],
    ) -> Response[None]:
        self._edit_product_details = True
        return Response(True)

    def appoint_owner(self, store_id: str, user: IUser) -> Response[None]:
        self._appoint_owner = True
        return Response(True)

    def get_communicate(self) -> Callable[[list[str]], bool]:
        self._get_communicate = True
        return lambda _: True

    def connect(self, communicate: Callable[[list[str]], bool]) -> bool:
        self._connect = True
        return lambda _: True

    def appoint_manager(self, store_id: str, user: IUser) -> Response[None]:
        self._appoint_manager = True
        return Response(True)

    def add_manager_permission(self, store_id: str, username: str, permission) -> Response[None]:
        self._add_manager_permission = True
        return Response(True)

    def remove_manager_permission(self, store_id: str, username: str, permission) -> Response[None]:
        self._remove_manager_permission = True
        return Response(True)

    def remove_appointment(self, store_id: str, username: str) -> Response[None]:
        self._remove_appointment = True
        return Response(True)

    def get_store_appointments(self, store_id: str) -> Response:
        self._get_store_appointments = True
        return Response(True)

    def get_store_purchase_history(self, store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        self._get_store_purchase_history = True
        return Response(True)

    def get_any_store_purchase_history_admin(
        self, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        self._get_any_store_purchase_history = True
        return Response(True)

    def get_any_user_purchase_history_admin(
        self, username: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        self._get_any_user_purchase_history = True
        return Response(True)

    def get_appointment_lock(self):
        return threading.Lock()

    def change_state(self, new_state: UserState) -> None:
        self.state = new_state

    def notify(self, message: str) -> bool:
        self.notified = True
        return True
