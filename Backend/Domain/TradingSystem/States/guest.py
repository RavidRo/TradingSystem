from Backend.Service.DataObjects.statistics_data import StatisticsData
from Backend.Domain.TradingSystem.offer import Offer
from Backend.DataBase.database import db_fail_response, session
from Backend.Domain.Authentication import authentication
from Backend.Domain.TradingSystem.States.admin import Admin
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.States.user_state import UserState
from Backend.response import ParsableList, Response
from Backend.settings import Settings



def register_admins(username, password) -> None:
    from Backend.DataBase.Handlers.member_handler import MemberHandler
    res = authentication.register(username, password)
    if res.succeeded():
        admin = Admin(None, username)
        MemberHandler.get_instance().save(admin)
        MemberHandler.get_instance().commit_changes()



def is_username_admin(username) -> bool:
    return username in Settings.get_instance(False).get_admins()


class Guest(UserState):
    def get_username(self):
        return Response(False, msg="Guests don't have username")

    def __init__(self, user, cart=None):
        super().__init__(user, cart)

    def login(self, username, password):
        response = authentication.login(username, password)
        return response

    def register(self, username, password):
        res = authentication.register(username, password)
        if res.succeeded():
            member = Member(self._user, username)
            self._member_handler.save(member)
            save_res = self._member_handler.commit_changes()
            if save_res.succeeded():
                return Response(True, member)
            authentication.remove_user_credrnials(username)
            return db_fail_response
        return res

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

    def add_discount(self, store_id: str, discount_data: dict, exist_id: str, condition_type: str = None):
        return Response(False, msg="Guests cannot add new discount to store")

    def move_discount(self, store_id: str, src_id: str, dest_id: str):
        return Response(False, msg="Guests cannot modify store's discount tree")

    def get_discounts(self, store_id: str):
        return Response(False, msg="Guests cannot get store's discount tree")

    def remove_discount(self, store_id: str, discount_id: str):
        return Response(False, msg="Guests cannot remove discount from store's discount tree")

    def edit_simple_discount(self, store_id: str, discount_id: str, percentage: float = None,
                             context: dict = None, duration=None):
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

    def get_my_appointments(self):
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

    # 6.5
    def register_statistics(self) -> None:
        self._statistics.register_guest()

    # Offers
    # ==================

    def get_user_offers(self) -> Response[ParsableList[Offer]]:
        return Response(False, msg="Guests cannot have price offers")

    def get_store_offers(self, store_id) -> Response[ParsableList[Offer]]:
        return Response(False, msg="Guests cannot have price offers")

    def create_offer(self, user, store_id, product_id) -> Response[str]:
        return Response(False, msg="Guests cannot have price offers")

    def declare_price(self, offer_id, price) -> Response[None]:
        return Response(False, msg="Guests cannot have price offers")

    def suggest_counter_offer(self, store_id, product_id, offer_id, price) -> Response[None]:
        return Response(False, msg="Guests cannot have price offers")

    def approve_manager_offer(self, offer_id) -> Response[None]:
        return Response(False, msg="Guests cannot have price offers")

    def approve_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        return Response(False, msg="Guests cannot have price offers")

    def reject_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        return Response(False, msg="Guests cannot have price offers")

    def cancel_offer(self, offer_id) -> Response[None]:
        return Response(False, msg="Guests cannot have price offers")

    def get_users_statistics(self) -> Response[StatisticsData]:
        return Response(False, msg="Guests cannot see users' statistics")
