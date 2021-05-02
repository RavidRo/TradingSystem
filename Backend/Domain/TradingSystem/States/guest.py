from Backend.Domain.Authentication import authentication
from Backend.Domain.TradingSystem.States.user_state import UserState
from Backend.response import Response
import json

admins = []


def register_admins() -> None:
    with open("config.json", "r") as read_file:
        data = json.load(read_file)
        for username in data["admins"]:
            authentication.register(username, data["admin-password"])
            admins.append(username)


register_admins()


def is_username_admin(username) -> bool:
    return username in admins


class Guest(UserState):

    def get_username(self):
        return Response(False, msg="Guests don't have username")

    def __init__(self, user, cart=None):
        super().__init__(user, cart)

    def login(self, username, password):
        from Backend.Domain.TradingSystem.States.member import Member
        from Backend.Domain.TradingSystem.States.admin import Admin

        response = authentication.login(username, password)
        if response.succeeded():
            if is_username_admin(username):
                self._user.change_state(
                    Admin(self._user, username)
                )  # in later milestones, fetch data from DB
            else:
                self._user.change_state(Member(self._user, username))
        return response

    def register(self, username, password):
        return authentication.register(username, password)

    def delete_products_after_purchase(self):
        return self._cart.delete_products_after_purchase("guest")

    def open_store(self, store_name):
        return Response(False, msg="A store cannot be opened by a guest")

    def get_purchase_history(self):
        return Response(False, msg="Guests don't have purchase history")

    def add_new_product(self, store_id, product_name, category, product_price, quantity, keywords=None):
        return Response(False, msg="Guests cannot add products to stores")

    def remove_product(self, store_id, product_id):
        return Response(False, msg="Guests cannot remove products from stores")

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        return Response(False, msg="Guests cannot change store product's quantity")

    def edit_product_details(self, store_id, product_id, new_name, new_category, new_price, keywords=None):
        return Response(False, msg="Guests cannot edit store product's details")

    def add_discount(self, store_id: str, discount_data: dict, exist_id: str):
        return Response(False, msg="Guests cannot add new discount to store")

    def move_discount(self, store_id: str, src_id: str, dest_id: str):
        return Response(False, msg="Guests cannot modify store's discount tree")

    def get_discounts(self, store_id: str):
        return Response(False, msg="Guests cannot get store's discount tree")

    def remove_discount(self, store_id: str, discount_id: str):
        return Response(False, msg="Guests cannot remove discount from store's discount tree")

    def edit_simple_discount(self, store_id: str, discount_id: str, percentage: float = None,
                             condition: dict = None, context: dict = None, duration=None):
        return Response(False, msg="Guests cannot edit discounts")

    def edit_complex_discount(self, store_id: str, discount_id: str, complex_type: str = None,
                              decision_rule: str = None):
        return Response(False, msg="Guests cannot edit discounts")

    def appoint_new_store_owner(self, store_id, new_owner):
        return Response(False, msg="Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager):
        return Response(False, msg="Guests cannot appoint new store managers")

    def add_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Guests cannot edit a stores manager's responsibilities")

    def remove_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Guests cannot edit a stores manager's responsibilities")

    def remove_appointment(self, store_id, username):
        return Response(False, msg="Guests cannot dismiss managers")

    def get_store_personnel_info(self, store_id):
        return Response(False, msg="Guests cannot get store personnel information")

    def get_my_appointees(self, store_id):
        return Response(False, msg="Guests cannot get store personnel information")

    def get_store_purchase_history(self, store_id):
        return Response(False, msg="Guests cannot get store's purchase history")

    def get_any_store_purchase_history_admin(self, store_id):
        return Response(False, msg="Guests cannot get any store's purchase history")

    def get_user_purchase_history_admin(self, username):
        return Response(False, msg="Guests cannot get any user's purchase history")

    def is_appointed(self, store_id):
        return Response(False, msg="Can't appoint guests to stores")

    # 4.2
    def add_purchase_rule(self, store_id: str, rule_details: dict, rule_type: str, parent_id: str, clause: str = None):
        return Response(False, msg="Guests cannot add purchase rules")

    # 4.2
    def remove_purchase_rule(self, store_id: str, rule_id: str):
        return Response(False, msg="Guests cannot remove purchase rules")

    # 4.2
    def edit_purchase_rule(self, store_id: str, rule_details: dict, rule_id: str, rule_type: str):
        return Response(False, msg="Guests cannot edit purchase rules")

    # 4.2
    def move_purchase_rule(self, store_id: str, rule_id: str, new_parent_id: str):
        return Response(False, msg="Guests cannot move purchase rule")

    # 4.2
    def get_purchase_policy(self, store_id):
        return self.__responsibilities[store_id].get_purchase_policy()
