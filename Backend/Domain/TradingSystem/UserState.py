from abc import ABC, abstractmethod
import User

class UserState(ABC):

    def __init__(self, user):
        self.user = user

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def register(self, username, password):
        pass

    @abstractmethod
    def open_store(self, store_id, store_parameters): # TODO: Change the parameters according to actual store's data
        pass

    # TODO: Check if cart actions should be here (e.g: member's cart needs to be saved)

    @abstractmethod
    def add_new_product(self, store_id, product_information, quantity): # TODO: Change the parameters according to actual product's data
        pass

    @abstractmethod
    def remove_product(self, store_id, product_id):
        pass

    @abstractmethod
    def change_product_quantity(self, store_id, product_id, new_quantity):
        pass

    @abstractmethod
    def edit_product_details(self, store_id, product_id, new_details): # TODO: Change the parameters according to actual product's data
        pass

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner_id):
        pass

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager_id):
        pass

    @abstractmethod
    def edit_managers_responsibilities(self, store_id, manager_id, responsibilities): # TODO: Change the parameters according to responsibilities representation
        pass

    @abstractmethod
    def dismiss_manager(self, store_id, manager_id):
        pass

    @abstractmethod
    def get_store_personnel_info(self, store_id):
        pass

    @abstractmethod
    def get_store_purchase_history(self, store_id):
        pass

    @abstractmethod
    def get_any_store_purchase_history(self, store_id):
        pass

    @abstractmethod
    def get_user_purchase_history(self, user_id):
        pass