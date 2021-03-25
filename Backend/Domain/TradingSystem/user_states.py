from abc import ABC, abstractmethod
from Backend.Domain.Authentication.authentication import Authentication
from Backend.Domain.TradingSystem.responsibility import Responsibility
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.store import Store

# TODO: Change return types to Response

class UserState(ABC):

    def __init__(self, user):
        self.cart = ShoppingCart()
        self.user = user

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def register(self, username, password):
        pass

    def save_product_in_cart(self, store_id, product_id, quantity):
        return self.cart.add_product(store_id, product_id, quantity)

    def show_cart(self):
        return self.cart.show_cart()

    def delete_from_cart(self, store_id, product_id):
        return self.cart.remove_product(store_id, product_id)

    def change_product_quantity(self, store_id, product_id, new_amount):
        return self.cart.change_product_qunatity(store_id, product_id, new_amount)

    def buy_cart(self, product_purchase_info, current_user):
        return self.cart.buy_products(product_purchase_info, current_user)

    def delete_products_after_purchase(self):
        return self.cart.delete_pruducts_after_purchase()

    @abstractmethod
    def open_store(self, store_id, store_parameters):
        pass

    @abstractmethod
    def get_purchase_history(self):
        pass

    @abstractmethod
    def add_new_product(self, store_id, product_information,
                        quantity):
        pass

    @abstractmethod
    def remove_product(self, store_id, product_id):
        pass

    @abstractmethod
    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        pass

    @abstractmethod
    def set_product_price(self, store_id, product_id,
                          new_price):
        pass

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner):
        pass

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager):
        pass

    @abstractmethod
    def add_manager_permission(self, store_id, member, permission):
        pass

    @abstractmethod
    def remove_manager_permission(self, store_id, member, permission):
        pass

    @abstractmethod
    def dismiss_manager(self, store_id, manager):
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

    def __init__(self, user):
        super().__init__(user)
        self.authentication = Authentication.get_instance()

    def login(self, username, password):
        msg = self.authentication.login(username, password)
        if msg == "login succeeded":
            self.user.change_state(Member(username))    # in later milestones, fetch data from DB
        # TODO: need to induce if an admin was logged in - ask Sunshine
        return msg

    def register(self, username, password):
        return self.authentication.register(username, password)

    def open_store(self, store_id, store_parameters):
        raise RuntimeError('A store cannot be opened by a guest')

    def get_purchase_history(self):
        raise RuntimeError("Guests don't have purchase history")

    def add_new_product(self, store_id, product_information,
                        quantity):
        raise RuntimeError('Guests cannot add products to stores')

    def remove_product(self, store_id, product_id):
        raise RuntimeError('Guests cannot remove products from stores')

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        raise RuntimeError("Guests cannot change store product's quantity")

    def set_product_price(self, store_id, product_id,
                          new_price):
        raise RuntimeError("Guests cannot edit store product's details")

    def appoint_new_store_owner(self, store_id, new_owner):
        raise RuntimeError("Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager):
        raise RuntimeError("Guests cannot appoint new store managers")

    def add_manager_permission(self, store_id, member, permission):
        raise RuntimeError("Guests cannot edit a stores manager's responsibilities")

    def remove_manager_permission(self, store_id, member, permission):
        raise RuntimeError("Guests cannot edit a stores manager's responsibilities")

    def dismiss_manager(self, store_id, manager):
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

    def __init__(self, user, username, responsibilities=None, purchase_details=[]):  # for DB initialization
        super().__init__(user)
        if responsibilities is None:
            responsibilities = dict()
        self.username = username
        self.responsibilities = responsibilities
        self.purchase_details = purchase_details
        # get cart data from DB

    def login(self, username, password):
        raise RuntimeError("Members cannot re-login")

    def register(self, username, password):
        raise RuntimeError("Members cannot re-register")

    def save_product_in_cart(self, store_id, product_id, quantity):
        response = super().save_product_in_cart(store_id, product_id, quantity)
        # update data in DB in later milestones
        return response

    def delete_from_cart(self, store_id, product_id):
        response = super().delete_from_cart(store_id, product_id)
        # update data in DB in later milestones
        return response

    def change_product_quantity(self, store_id, product_id, new_quantity):
        response = super().change_product_quantity(store_id, product_id, new_quantity)
        # update data in DB in later milestones
        return response

    def buy_cart(self, user, product_purchase_info):
        response = super().buy_cart(user, product_purchase_info)
        # update data in DB in later milestones
        return response

    def delete_products_after_purchase(self):
        response = super().delete_products_after_purchase()
        # update data in DB in later milestones
        return response

    def open_store(self, store_id, store_parameters):
        if store_id in self.responsibilities:
            raise RuntimeError("Store cannot be re-opened")
        store = Store(store_id, store_parameters)
        self.responsibilities[store_id] = Responsibility(self,
                                                         store)
        return store

    def get_purchase_history(self):
        return self.purchase_details

    def add_new_product(self, store_id, product_id,
                        quantity):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].add_product(product_id, quantity)

    def remove_product(self, store_id, product_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_product(product_id)

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].change_product_quantity(product_id, new_quantity)

    def set_product_price(self, store_id, product_id,
                          new_price):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].set_product_price(product_id, new_price)

    def appoint_new_store_owner(self, store_id, new_owner):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].appoint_owner(new_owner)

    def appoint_new_store_manager(self, store_id, new_manager):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].appoint_manager(new_manager)

    def add_manager_permission(self, store_id, member, permission):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].add_manager_permission(member, permission)

    def remove_manager_permission(self, store_id, member, permission):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_manager_permission(member, permission)

    def dismiss_manager(self, store_id, manager):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_appointment(manager)

    def get_store_personnel_info(self, store_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].get_store_appointments()

    def get_store_purchase_history(self, store_id):
        if store_id not in self.responsibilities:
            raise RuntimeError(f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].get_store_purchases_history()

    def get_any_store_purchase_history(self, store_id):
        raise RuntimeError("Members cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        raise RuntimeError("Members cannot get any user's purchase history")


class Admin(Member):

    def __init__(self, user, username, responsibilities=None):
        super().__init__(user, username, responsibilities)
        self.trading_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        self.trading_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        self.trading_system_manager.get_user_purchase_history(user_id)
