from abc import ABC, abstractmethod
from Backend.Domain.Authentication.authentication import Authentication
from Backend.Domain.TradingSystem.responsibility import Responsibility
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.store import Store


class UserState(ABC):

    def __init__(self):
        self.cart = ShoppingCart()

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def register(self, username, password):
        pass

    def save_product_in_cart(self, store_id, product_id):   # TODO: talk to sean about quantity in save_product
        return self.cart.add_product(store_id, product_id)

    def show_cart(self):
        return self.cart.show_cart()

    def delete_from_cart(self, store_id, product_id):
        return self.cart.remove_product(store_id, product_id)   # TODO: talk to sean about quantity in remove_product

    @abstractmethod
    def open_store(self, store_id, store_parameters):
        pass

    @abstractmethod
    def add_new_product(self, store_id, product_information,
                        quantity):
        pass

    @abstractmethod
    def remove_product(self, store_id, product_id):
        pass

    @abstractmethod
    def change_product_quantity(self, store_id, product_id, new_quantity):
        pass

    @abstractmethod
    def edit_product_details(self, store_id, product_id,
                             new_details):
        pass

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner_id):
        pass

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager_id):
        pass

    @abstractmethod
    def edit_managers_responsibilities(self, store_id, manager_id,
                                       responsibilities):
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

    def open_store(self, store_id, store_parameters):
        raise RuntimeError('A store cannot be opened by a guest')

    # In contrary to the requirements, guests can see their RAM history (can be complex because all store's history
    # is saved in DB and we need to ignore if the buyer was a guest).

    def add_new_product(self, store_id, product_information,
                        quantity):
        raise RuntimeError('Guests cannot add products to stores')

    def remove_product(self, store_id, product_id):
        raise RuntimeError('Guests cannot remove products from stores')

    def change_product_quantity(self, store_id, product_id, new_quantity):
        raise RuntimeError("Guests cannot change store product's quantity")

    def edit_product_details(self, store_id, product_id,
                             new_details):
        raise RuntimeError("Guests cannot edit store product's details")

    def appoint_new_store_owner(self, store_id, new_owner_id):
        raise RuntimeError("Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager_id):
        raise RuntimeError("Guests cannot appoint new store managers")

    def edit_managers_responsibilities(self, store_id, manager_id,
                                       responsibilities):
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

    def __init__(self, username, responsibilities=None):  # for DB initialization
        super().__init__()
        if responsibilities is None:
            responsibilities = dict()
        self.username = username
        self.responsibilities = responsibilities
        # get cart data from DB

    def login(self, username, password):
        raise RuntimeError("Members cannot re-login")

    def register(self, username, password):
        raise RuntimeError("Members cannot re-register")

    def delete_from_cart(self, store_id, product_id):
        response = super().delete_from_cart(store_id, product_id)
        # update data in DB in later milestones
        return response

    def save_product_in_cart(self, store_id, product_id):
        response = super().save_product_in_cart(store_id, product_id)
        # update data in DB in later milestones
        return response

    def open_store(self, store_id, store_parameters):
        if store_id in self.responsibilities:
            raise RuntimeError("Store cannot be re-opened")
        store = Store(store_id, store_parameters)
        self.responsibilities[store_id] = Responsibility(self,
                                                         store)
        return store

    def add_new_product(self, store_id, product_information,
                        quantity):
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
                             new_details):
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
                                       responsibilities):
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

    def __init__(self, username, responsibilities=None):
        super().__init__(username, responsibilities)
        if responsibilities is None:
            responsibilities = dict()
        self.trading_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        self.trading_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        self.trading_system_manager.get_user_purchase_history(user_id)
