from Backend.Domain.TradingSystem.user_state import UserState
from Backend.Domain.TradingSystem.responsibility import Responsibility


class Member(UserState):

    def __init__(self, username, responsibilities=dict()):  # for DB initialization
        super().__init__()
        self.username = username
        self.responsibilities = responsibilities

    def login(self, username, password):
        raise RuntimeError("Members cannot re-login")

    def register(self, username, password):
        raise RuntimeError("Members cannot re-register")

    def open_store(self, store_id, store_parameters):  # TODO: Change the parameters according to actual store's data
        if self.responsibilities.has_key(store_id):
            raise RuntimeError("Store cannot be re-opened")
        self.responsibilities[store_id] = Responsibility(store_id,
                                                         store_parameters)  # TODO: change call according to actual store parameters

    def add_new_product(self, store_id, product_information,
                        quantity):  # TODO: Change the parameters according to actual product's data
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].add_new_product(product_information, quantity)

    def remove_product(self, store_id, product_id):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].remove_product(product_id)

    def change_product_quantity(self, store_id, product_id, new_quantity):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].change_product_quantity(product_id, quantity)

    def edit_product_details(self, store_id, product_id,
                             new_details):  # TODO: Change the parameters according to actual product's data
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].edit_product_details(product_id, new_details)

    def appoint_new_store_owner(self, store_id, new_owner_id):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].appoint_new_store_owner(new_owner_id)

    def appoint_new_store_manager(self, store_id, new_manager_id):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].appoint_new_store_manager(new_manager_id)

    def edit_managers_responsibilities(self, store_id, manager_id,
                                       responsibilities):  # TODO: Change the parameters according to responsibilities representation
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].edit_managers_responsibilities(manager_id, responsibilities)

    def dismiss_manager(self, store_id, manager_id):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].dismiss_manager(manager_id)

    def get_store_personnel_info(self, store_id):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].get_store_personnel_info()

    def get_store_purchase_history(self, store_id):
        if not self.responsibilities.has_key(store_id):
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].get_store_purchase_history()

    def get_any_store_purchase_history(self, store_id):
        raise RuntimeError("Members cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        raise RuntimeError("Members cannot get any user's purchase history")
