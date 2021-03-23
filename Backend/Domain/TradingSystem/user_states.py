from abc import ABC, abstractmethod
from Backend.Domain.Authentication.authentication import Authentication
from Backend.Domain.TradingSystem.responsibility import Responsibility
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager


class UserState(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def register(self, username, password):
        pass

    @abstractmethod
    def open_store(self, store_id, store_parameters):  # TODO: Change the parameters according to actual store's data
        pass

    # TODO: Check if cart actions should be here (e.g: member's cart needs to be saved)

    @abstractmethod
    def add_new_product(self, store_id, product_information,
                        quantity):  # TODO: Change the parameters according to actual product's data
        pass

    @abstractmethod
    def remove_product(self, store_id, product_id):
        pass

    @abstractmethod
    def change_product_quantity(self, store_id, product_id, new_quantity):
        pass

    @abstractmethod
    def edit_product_details(self, store_id, product_id,
                             new_details):  # TODO: Change the parameters according to actual product's data
        pass

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner_id):
        pass

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager_id):
        pass

    @abstractmethod
    def edit_managers_responsibilities(self, store_id, manager_id,
                                       responsibilities):  # TODO: Change the parameters according to responsibility's representation
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


class Guest(UserState):

    def __init__(self):
        super().__init__()
        self.authentication = Authentication.get_instance()

    def login(self, username, password):
        msg = self.authentication.login(username, password)
        # TODO: need to induce if an admin was logged in - ask Sunshine
        return msg

    def register(self, username, password):
        return self.authentication.register(username, password)

    def open_store(self, store_id, store_parameters):  # TODO: Change the parameters according to actual store's data
        raise RuntimeError('A store cannot be opened by a guest')

    # In contrary to the requirements, guests can see their RAM history (can be complex because all store's history
    # is saved in DB and we need to ignore if the buyer was a guest).

    # TODO: Check if cart actions should be here (e.g: member's cart needs to be saved)

    def add_new_product(self, store_id, product_information,
                        quantity):  # TODO: Change the parameters according to actual product's data
        raise RuntimeError('Guests cannot add products to stores')

    def remove_product(self, store_id, product_id):
        raise RuntimeError('Guests cannot remove products from stores')

    def change_product_quantity(self, store_id, product_id, new_quantity):
        raise RuntimeError("Guests cannot change store product's quantity")

    def edit_product_details(self, store_id, product_id,
                             new_details):  # TODO: Change the parameters according to actual product's data
        raise RuntimeError("Guests cannot edit store product's details")

    def appoint_new_store_owner(self, store_id, new_owner_id):
        raise RuntimeError("Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager_id):
        raise RuntimeError("Guests cannot appoint new store managers")

    def edit_managers_responsibilities(self, store_id, manager_id,
                                       responsibilities):  # TODO: Change the parameters according to responsibilities representation
        raise RuntimeError("Guests cannot edit a stores manager's responsibilities")

    def dismiss_manager(self, store_id, manager_id):
        raise RuntimeError("Guests cannot dismiss managers")

    def get_store_personnel_info(self, store_id):
        raise RuntimeError("Guests cannot get store personnel information")

    def get_store_purchase_history(self, store_id):
        raise RuntimeError("Guests cannot get store's purchase history")

    def get_any_store_purchase_history(self, store_id):
        raise RuntimeError("Guests cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        raise RuntimeError("Guests cannot get any user's purchase history")


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
        if store_id in self.responsibilities:
            raise RuntimeError("Store cannot be re-opened")
        self.responsibilities[store_id] = Responsibility(store_id,
                                                         store_parameters)  # TODO: change call according to actual store parameters

    def add_new_product(self, store_id, product_information,
                        quantity):  # TODO: Change the parameters according to actual product's data
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].add_new_product(product_information, quantity)

    def remove_product(self, store_id, product_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].remove_product(product_id)

    def change_product_quantity(self, store_id, product_id, new_quantity):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].change_product_quantity(product_id, new_quantity)

    def edit_product_details(self, store_id, product_id,
                             new_details):  # TODO: Change the parameters according to actual product's data
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].edit_product_details(product_id, new_details)

    def appoint_new_store_owner(self, store_id, new_owner_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].appoint_new_store_owner(new_owner_id)

    def appoint_new_store_manager(self, store_id, new_manager_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].appoint_new_store_manager(new_manager_id)

    def edit_managers_responsibilities(self, store_id, manager_id,
                                       responsibilities):  # TODO: Change the parameters according to responsibilities representation
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].edit_managers_responsibilities(manager_id, responsibilities)

    def dismiss_manager(self, store_id, manager_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].dismiss_manager(manager_id)

    def get_store_personnel_info(self, store_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].get_store_personnel_info()

    def get_store_purchase_history(self, store_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        self.responsibilities[store_id].get_store_purchase_history()

    def get_any_store_purchase_history(self, store_id):
        raise RuntimeError("Members cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        raise RuntimeError("Members cannot get any user's purchase history")


class Admin(Member):

    def __init__(self, username, responsibilities=dict()):
        super().__init__(username, responsibilities)
        self.trading_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        self.trading_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        self.trading_system_manager.get_user_purchase_history(user_id)
