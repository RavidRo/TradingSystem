from .user_state import UserState
from .member import Member
from .admin import Admin
from Backend.Domain.Authentication.authentication import Authentication
from Backend.response import Response


class Guest(UserState):
    def get_username(self):
        return Response(False, msg="Guests don't have username")

    def __init__(self, user):
        super().__init__(user)
        self.authentication = Authentication.get_instance()

    def login(self, username, password):
        response = self.authentication.login(username, password)
        if response.succeeded():
            if response.object.value:
                self.user.change_state(
                    Admin(self.user, username)
                )  # in later milestones, fetch data from DB
            else:
                self.user.change_state(Member(self.user, username))
        return response

    def register(self, username, password):
        return self.authentication.register(username, password)

    def open_store(self, store_name):
        return Response(False, msg="A store cannot be opened by a guest")

    def get_purchase_history(self):
        return Response(False, msg="Guests don't have purchase history")

    def add_new_product(self, store_id, product_name, product_price, quantity):
        return Response(False, msg="Guests cannot add products to stores")

    def remove_product(self, store_id, product_id):
        return Response(False, msg="Guests cannot remove products from stores")

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        return Response(False, msg="Guests cannot change store product's quantity")

    def edit_product_details(self, store_id, product_id, new_name, new_price):
        return Response(False, msg="Guests cannot edit store product's details")

    def appoint_new_store_owner(self, store_id, new_owner):
        return Response(False, msg="Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager):
        return Response(False, msg="Guests cannot appoint new store managers")

    def add_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Guests cannot edit a stores manager's responsibilities")

    def remove_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Guests cannot edit a stores manager's responsibilities")

    def dismiss_manager(self, store_id, manager):
        return Response(False, msg="Guests cannot dismiss managers")

    def get_store_personnel_info(self, store_id):
        return Response(False, msg="Guests cannot get store personnel information")

    def get_store_purchase_history(self, store_id):
        return Response(False, msg="Guests cannot get store's purchase history")

    def get_any_store_purchase_history(self, store_id):
        return Response(False, msg="Guests cannot get any store's purchase history")

    def get_user_purchase_history(self, username):
        return Response(False, msg="Guests cannot get any user's purchase history")
