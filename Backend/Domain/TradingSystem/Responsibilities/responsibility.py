from __future__ import annotations
import enum

from Backend.Service.DataObjects.responsibilities_data import ResponsibilitiesData
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Parsable, Response, ParsableList


Permission = enum.Enum(
    value="Permission",
    names=[
        ("manage products", 1),
        ("MANAGE_PRODUCTS", 1),
        ("get appointments", 2),
        ("GET_APPOINTMENTS", 2),
        ("appoint manager", 3),
        ("APPOINT_MANAGER", 3),
        ("remove manager", 4),
        ("REMOVE_MANAGER", 4),
        ("get history", 5),
        ("GET_HISTORY", 5),
        ("manage_purchase_policy", 6),
        ("MANAGE_PURCHASE_POLICY", 6),
        ("manage_discount_policy", 7),
        ("MANAGE_DISCOUNT_POLICY", 7),
    ],
)

name_to_permission: dict[str, Permission] = {
    "manage_products": Permission.MANAGE_PRODUCTS,
    "get_appointments": Permission.GET_APPOINTMENTS,
    "appoint_manager": Permission.APPOINT_MANAGER,
    "remove_manager": Permission.REMOVE_MANAGER,
    "get_history": Permission.GET_HISTORY,
    "manage_purchase_policy": Permission.MANAGE_PURCHASE_POLICY,
    "manage_discount_policy": Permission.MANAGE_DISCOUNT_POLICY,
}


class Responsibility(Parsable):
    ERROR_MESSAGE = "Responsibility is an interface, function not implemented"

    def __init__(self, user_state, store, subscriber=None) -> None:
        self._user_state = user_state
        user_state.add_responsibility(self, store.get_id())
        self._store = store
        self.__subscriber = subscriber
        if subscriber:
            self._store.subscribe(subscriber)
        self._appointed: list[Responsibility] = []

    # 4.1
    # Creating a new product a the store
    def add_product(
        self, name: str, category: str, price: float, quantity: int, keywords: list[str] = None
    ) -> Response[str]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.1
    def remove_product(self, product_id: str) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.1
    def change_product_quantity_in_store(self, product_id: str, quantity: int) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.1
    def edit_product_details(
        self,
        product_id: str,
        new_name: str,
        new_category: str,
        new_price: float,
        keywords: list[str] = None,
    ) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.2
    def add_discount(self, discount_data: dict, exist_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def move_discount(self, src_id: str, dest_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def get_discounts(self):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def remove_discount(self, discount_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def edit_simple_discount(
        self,
        discount_id: str,
        percentage: float = None,
        condition: dict = None,
        context: dict = None,
        duration=None,
    ):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def edit_complex_discount(
        self, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.2
    def add_purchase_rule(
        self, rule_details: dict, rule_type: str, parent_id: str, clause: str = None
    ):
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.2
    def remove_purchase_rule(self, rule_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.2
    def edit_purchase_rule(self, rule_details: dict, rule_id: str, rule_type: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.2
    def move_purchase_rule(self, rule_id: str, new_parent_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.2
    def get_purchase_policy(self):
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.3
    def appoint_owner(self, user: IUser) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.5
    def appoint_manager(self, user: IUser) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.6
    # Returns true if and only if self.user appointed user and user is a manager
    def add_manager_permission(self, username: str, permission: Permission) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.6
    def remove_manager_permission(self, username: str, permission: Permission) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.4, 4.7
    def remove_appointment(self, username: str) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.9
    def get_store_appointments(self) -> Response[Responsibility]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def get_my_appointees(self) -> Response[ParsableList[Responsibility]]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.11
    def get_store_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def _add_permission(self, username: str, permission: Permission) -> bool:
        if not self._appointed:
            # if self.user never appointed anyone
            return False

        def add_appointee_permission(appointee: Responsibility):
            return appointee._add_permission(username, permission)

        # returns true if any one of the children returns true
        return any(map(add_appointee_permission, self._appointed))

    def _remove_permission(self, username: str, permission: Permission) -> bool:
        if not self._appointed:
            # if self.user never appointed anyone
            return False

        def remove_appointee_permission(appointee: Responsibility):
            return appointee._remove_permission(username, permission)

        # returns true if any one of the children returns true
        return any(map(remove_appointee_permission, self._appointed))

    def _remove_appointment(self, username: str) -> bool:
        if not self._appointed:
            # if self.user never appointed anyone
            return False

        for appointment in self._appointed:
            if appointment._user_state.get_username().get_obj().get_val() == username:
                self._appointed.remove(appointment)
                appointment.__dismiss_from_store(self._store.get_id())
                return True

        return any(map(lambda worker: worker._remove_appointment(username), self._appointed))

    def __dismiss_from_store(self, store_id: str) -> None:
        for appointment in self._appointed:
            appointment.__dismiss_from_store(store_id)
        message = f'You have been dismissed from store "{self._store.get_name()}"'
        if self.__subscriber:
            self.__subscriber.notify(message)
        self._user_state.dismiss_from_store(store_id)

    # Parsing the object for user representation
    def parse(self) -> ResponsibilitiesData:
        return ResponsibilitiesData(
            self._store.get_id(),
            self._store.get_name(),
            self._is_manager(),
            self.__class__.__name__,
            [appointee.parse() for appointee in self._appointed],
            self._permissions(),
            self._user_state.get_username().object.value,
        )

    def _is_manager(self) -> bool:
        return False

    def _permissions(self) -> list[str]:
        return [per.name for per in Permission]
