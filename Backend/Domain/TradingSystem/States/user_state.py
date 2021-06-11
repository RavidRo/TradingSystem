from Backend.Domain.TradingSystem.offer import Offer
from abc import ABC, abstractmethod
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.response import ParsableList, Response


class UserState(ABC):
    def __init__(self, user, cart=None):
        from Backend.DataBase.Handlers.member_handler import MemberHandler
        if cart is None:
            cart = ShoppingCart()
        self._cart = cart
        self._user = user
        self._member_handler = MemberHandler.get_instance()

    def set_user(self, user):
        self._user = user


    @abstractmethod
    def get_username(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def login(self, username, password):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def register(self, username, password):
        return Response(False, msg="Abstract Method")

    def save_product_in_cart(self, store_id, product_id, quantity):
        from Backend.Domain.TradingSystem.stores_manager import StoresManager

        response = StoresManager.get_store(store_id)
        if not response.succeeded():
            return response

        return self._cart.add_product(store_id, product_id, quantity, response.object)

    def show_cart(self):
        return Response[ShoppingCart](True, obj=self._cart, msg="got cart successfully")

    def delete_from_cart(self, store_id, product_id):
        return self._cart.remove_product(store_id, product_id)

    def change_product_quantity_in_cart(self, store_id, product_id, new_amount):
        return self._cart.change_product_quantity(store_id, product_id, new_amount)

    def buy_cart(self, user_age: int):
        return self._cart.buy_products(user_age, username=self.get_username())

    def get_cart_price(self):
        return self._cart.get_price()

    @abstractmethod
    def delete_products_after_purchase(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def open_store(self, store_name):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_purchase_history(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_new_product(
        self, store_id, product_name, category, product_price, quantity, keywords=None
    ):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_product(self, store_id, product_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def edit_product_details(
        self, store_id, product_id, new_name, new_category, new_price, keywords=None
    ):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_discount(
        self, store_id: str, discount_data: dict, exist_id: str, condition_type: str = None
    ):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def move_discount(self, store_id: str, src_id: str, dest_id: str):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_discounts(self, store_id: str):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_discount(self, store_id: str, discount_id: str):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def edit_simple_discount(
        self,
        store_id: str,
        discount_id: str,
        percentage: float = None,
        context: dict = None,
        duration=None,
    ):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def edit_complex_discount(
        self, store_id: str, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_appointment(self, store_id, username):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_personnel_info(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_my_appointments(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_purchase_history(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_any_store_purchase_history_admin(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_user_purchase_history_admin(self, username):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def is_appointed(self, store_id):
        return Response(False, msg="Abstract Method")

    def lock_cart(self):
        return self._cart.lock_cart()

    def release_cart(self):
        return self._cart.release_cart()

    def cancel_purchase(self):
        return self._cart.cancel_purchase()

    # 4.2
    @abstractmethod
    def add_purchase_rule(
        self, store_id: str, rule_details: dict, rule_type: str, parent_id: str, clause: str = None
    ):
        return Response(False, msg="Abstract Method")

    # 4.2
    @abstractmethod
    def remove_purchase_rule(self, store_id: str, rule_id: str):
        return Response(False, msg="Abstract Method")

    # 4.2
    @abstractmethod
    def edit_purchase_rule(self, store_id: str, rule_details: dict, rule_id: str, rule_type: str):
        return Response(False, msg="Abstract Method")

    # 4.2
    @abstractmethod
    def move_purchase_rule(self, store_id: str, rule_id: str, new_parent_id: str):
        return Response(False, msg="Abstract Method")

    # 4.2
    @abstractmethod
    def get_purchase_policy(self, store_id: str):
        return Response(False, msg="Abstract Method")

    # Offers
    # ==================
    @abstractmethod
    def get_user_offers(self) -> Response[ParsableList[Offer]]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_offers(self, store_id) -> Response[ParsableList[Offer]]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def create_offer(self, user, store_id, product_id) -> Response[str]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def declare_price(self, offer_id, price) -> Response[None]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def suggest_counter_offer(self, store_id, product_id, offer_id, price) -> Response[None]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def approve_manager_offer(self, offer_id) -> Response[None]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def approve_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def reject_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def cancel_offer(self, offer_id) -> Response[None]:
        return Response(False, msg="Abstract Method")

    def has_res_id(self, res_id):
        pass

