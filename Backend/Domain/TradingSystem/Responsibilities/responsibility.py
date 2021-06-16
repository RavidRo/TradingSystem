from __future__ import annotations
import enum
import uuid

from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.offer import Offer
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
        ("manage purchase policy", 6),
        ("MANAGE_PURCHASE_POLICY", 6),
        ("manage discount policy", 7),
        ("MANAGE_DISCOUNT_POLICY", 7),
    ],
)

name_to_permission: dict[str, Permission] = {
    "manage products": Permission.MANAGE_PRODUCTS,
    "get appointments": Permission.GET_APPOINTMENTS,
    "appoint manager": Permission.APPOINT_MANAGER,
    "remove manager": Permission.REMOVE_MANAGER,
    "get history": Permission.GET_HISTORY,
    "manage purchase policy": Permission.MANAGE_PURCHASE_POLICY,
    "manage discount policy": Permission.MANAGE_DISCOUNT_POLICY,
}


class Responsibility(Parsable):
    ERROR_MESSAGE = "Responsibility is an interface, function not implemented"

    def __init__(self, user_state, store, subscriber=None) -> None:
        from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
        self._store_id = store.get_id()
        self._user_state = user_state
        self._store = store
        self.__subscriber = subscriber
        if subscriber:
            self._store.subscribe(subscriber)
            subscriber.notify(
                {
                    "subject": "message",
                    "data": f"You have been appointed to {store.get_name()} as {self.__class__.__name__}",
                }
            )
        self._appointed = []

        if self._user_state is not None:
            self._username = user_state.get_username().get_obj().get_val()
            store.add_owner(user_state.get_username().get_obj().value)
        else:
            self._username = None
        self._responsibilities_handler = ResponsibilitiesHandler.get_instance()
        self._responsibility_dal = None
        self._responsibility_dal_id = None

    def set_subscriber(self, subscriber):
        self.__subscriber = subscriber
        self._store.subscribe(subscriber)

    def set_user_state(self, user_state):
        self._user_state = user_state
        self._username = user_state.get_username().get_obj().get_val()

    def get_user_state(self):
        from Backend.Domain.TradingSystem.user_manager import UserManager
        if self._user_state is None:
            response_member = UserManager.get_member(self._responsibility_dal_id)
            if response_member.succeeded():
                response_member.get_obj().add_responsibility(self, self._store_id)
                self._user_state = response_member.get_obj()
                self._username = self._user_state.get_username()
                self._store.add_owner(self._user_state.get_username().get_obj().value)
                self.set_subscriber(self._user_state._user)
            else:
                return response_member
        for appointed in self._appointed:
            res = appointed.get_user_state()
            if not res.succeeded():
                return res
        return Response(True, self._user_state)

    def get_store_id(self):
        return self._store.get_id()

    def set_username(self, username):
        self._username = username

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
    def add_discount(self, discount_data: dict, exist_id: str, condition_type: str = None):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def move_discount(self, src_id: str, dest_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def get_discounts(self):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def remove_discount(self, discount_id: str):
        raise Exception(Responsibility.ERROR_MESSAGE)

    def edit_simple_discount(
        self, discount_id: str, percentage: float = None, context: dict = None, duration=None
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

    # 4.11
    def get_store_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def is_owner(self) -> bool:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def _add_permission(self, username: str, permission: Permission) -> Response[None]:
        if not self._appointed:
            # if self.user never appointed anyone
            return Response(False, msg=f"{self._username} is not appointed to store: {self._store.get_name()}!")

        def add_appointee_permission(appointee: Responsibility):
            return appointee._add_permission(username, permission)

        # returns true if any one of the children returns true
        for appointee in self._appointed:
            response = add_appointee_permission(appointee)
            if response.succeeded():
                return response
            elif response.get_obj().parse() == -1:
                return db_fail_response

        return Response(False, msg=f"Didn't find appointee with username: {username}")

        # return any(map(add_appointee_permission, self._appointed))

    def _remove_permission(self, username: str, permission: Permission) -> Response[None]:
        if not self._appointed:
            # if self.user never appointed anyone
            return Response(False, msg=f"{self._username} is not appointed to store: {self._store.get_name()}!")

        def remove_appointee_permission(appointee: Responsibility):
            return appointee._remove_permission(username, permission)

        for appointee in self._appointed:
            response = remove_appointee_permission(appointee)
            if response.succeeded():
                return response
            elif response.get_obj().parse() == -1:
                return db_fail_response

        return Response(False, msg=f"Didn't find appointee with username: {username}")
        # returns true if any one of the children returns true
        # return any(map(remove_appointee_permission, self._appointed))

    def _remove_appointment(self, username: str) -> bool:
        if not self._appointed:
            # if self.user never appointed anyone
            return False

        for appointment in self._appointed:
            if appointment._user_state.get_username().get_obj().get_val() == username:
                res = self._responsibilities_handler.remove_res(appointment)

                if res.succeeded():
                    res = appointment.__dismiss_from_store_db()
                    if res.succeeded():
                        res_commit = self._responsibilities_handler.commit_changes()
                        if res_commit.succeeded():
                            self._appointed.remove(appointment)
                            appointment.__dismiss_from_store(self._store.get_id())

                        return True
                    return False

        return any(map(lambda worker: worker._remove_appointment(username), self._appointed))

    def __dismiss_from_store(self, store_id: str) -> None:
        for appointment in self._appointed:
            appointment.__dismiss_from_store(store_id)

        message = f'You have been dismissed from store "{self._store.get_name()}"'
        self.get_user_state()
        if self.__subscriber:
            self.__subscriber.notify(message)
            self._store.unsubscribe(self.__subscriber)
        self._store.remove_owner(self._user_state.get_username().get_obj().value)
        self._user_state.dismiss_from_store(store_id)

    def __dismiss_from_store_db(self) -> Response[None]:
        for appointment in self._appointed:
            response = appointment.__dismiss_from_store_db()
            if not response.succeeded():
                return response

        member_response = self.get_user_state()
        if member_response.succeeded():
            member_response.get_obj().dismiss_from_store_db(self)
        return member_response

    # Parsing the object for user representation
    def parse(self) -> ResponsibilitiesData:
        return ResponsibilitiesData(
            self._store.get_id(),
            self._store.get_name(),
            self._is_manager(),
            self.__class__.__name__,
            [appointee.parse() for appointee in self._appointed],
            self._permissions(),
            self.get_user_state().get_obj().get_username().object.value,
        )

    def _is_manager(self) -> bool:
        return False

    def _permissions(self) -> list[str]:
        return [per.name for per in Permission]

    def save_self(self):
        from Backend.DataBase.Handlers.responsibilities_handler import Founder_Responsibility_DAL
        dal_responsibility_res = self._responsibilities_handler.save_res(Founder_Responsibility_DAL)
        if dal_responsibility_res.succeeded():
            self._responsibility_dal = dal_responsibility_res.get_obj()
            self._responsibility_dal_id = dal_responsibility_res.get_obj().id
            return Response(True)
        return db_fail_response
    # Offers
    # ======================

    def get_store_offers(self) -> Response[ParsableList[Offer]]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def suggest_counter_offer(self, product_id, offer_id, price) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def approve_user_offer(self, product_id, offer_id, username) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def reject_user_offer(self, product_id, offer_id) -> Response[None]:
        raise Exception(Responsibility.ERROR_MESSAGE)

    def get_owners_names(self) -> list[str]:

        import itertools

        self.get_user_state()
        my_username = self._user_state.get_username().object.value
        nested_names = [appointee.get_owners_names() for appointee in self._appointed]
        List_flat = list(itertools.chain(*nested_names))
        return List_flat + [my_username]

    def get_dal_responsibility_id(self):
        return self._responsibility_dal_id

    def get_dal_responsibility(self):
        return self._responsibility_dal

    def set_appointments(self, appointments):
        self._appointed = appointments

    def set_dal_responsibility_and_id(self, res_root):
        self._responsibility_dal = res_root
        self._responsibility_dal_id = res_root.id

    def get_res_if_exists(self, responsibility_ids):
        if str(self._responsibility_dal_id) in responsibility_ids:
            return Response(True, obj=self)
        if self._appointed is None:
            return Response(False)
        for child in self._appointed:
            res = child.get_res_if_exists(responsibility_ids)
            if res.succeeded():
                return res

    def set_store(self, store):
        self._store = store