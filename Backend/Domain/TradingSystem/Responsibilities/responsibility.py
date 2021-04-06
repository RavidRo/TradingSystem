from __future__ import annotations

from Backend.Domain.TradingSystem.member import Member
from Backend.Domain.TradingSystem.IUser import IUser
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response, ParsableList

import enum

Permission = enum.Enum(
    value="Permission",
    names=[
        ("MANAGE_PRODUCTS", 1),
        ("manage products", 1),
        ("GET_APPOINTMENTS", 2),
        ("get appointments", 2),
        ("APPOINT_MANAGER", 3),
        ("appoint mannager", 3),
        ("REMOVE_MANAGER", 4),
        ("remove manager", 4),
        ("GET_HISTORY", 5),
        ("get history", 5),
    ],
)


class Permission(enum.Enum):
    MANAGE_PRODUCTS = 1
    GET_APPOINTMENTS = 2
    APPOINT_MANAGER = 3
    REMOVE_MANAGER = 4
    GET_HISTORY = 5


class Responsibility:
    ERROR_MESSAGE = "Responsibility is an interface, function not implemented"

    def __init__(self, user_state: Member, store: Store) -> None:
        self.user_state = user_state
        user_state.add_responsibility(self, store.get_id())
        self.store = store
        self.appointed: list[Responsibility] = []

    # 4.1
    # Creating a new product a the store
    def add_product(self, name: str, price: float, quantity: int) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.1
    def remove_product(self, product_id: str) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.1
    def change_product_quantity(self, product_id: str, quantity: int) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    # 4.1
    def edit_product_details(
        self, product_id: str, new_name: str, new_price: float
    ) -> Response[None]:
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

    # 4.11
    def get_store_purchases_history(self) -> Response[ParsableList[PurchaseDetails]]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def _add_permission(self, username: str, permission: Permission) -> bool:
        if not self.appointed:
            # if self.user never appointed anyone
            return False

        def add_appointee_permission(appointee: Responsibility):
            return appointee._add_permission(username, permission)

        # returns true if any one of the children returns true
        return any(map(add_appointee_permission, self.appointed))

    def _remove_permission(self, username: str, permission: Permission) -> bool:
        if not self.appointed:
            # if self.user never appointed anyone
            return False

        def remove_appointee_permission(appointee: Responsibility):
            return appointee._remove_permission(username, permission)

        # returns true if any one of the children returns true
        return any(map(remove_appointee_permission, self.appointed))

    def _remove_appointment(self, username: str) -> bool:
        if not self.appointed:
            # if self.user never appointed anyone
            return False

        for appointment in self.appointed:
            if appointment.user_state.get_username() == username:
                self.appointed.remove(appointment)
                appointment.__dismiss_from_store(self.store.get_id())
                return True

        return any(map(lambda worker: worker._remove_appointment(username), self.appointed))

    def __dismiss_from_store(self, store_id: str) -> None:
        for appointment in self.appointed:
            appointment.__dismiss_from_store(store_id)
        self.user_state.dismiss_from_store(store_id)
