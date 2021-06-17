import threading
from datetime import date

from sqlalchemy import orm

from Backend.DataBase.database import db_fail_response
from Backend.Service.DataObjects.statistics_data import StatisticsData
from Backend.Domain.TradingSystem.offer import Offer
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.store import Store

# from Backend.Domain.TradingSystem.States.user_state import UserState
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails

from .user_state import UserState
from ..statistics import Statistics


class Member(UserState):
    def get_username(self):
        return Response(
            True, obj=PrimitiveParsable(self._username), msg="got username successfully"
        )

    def add_responsibility(self, responsibility, store_id):
        # res = self.get_responsibility(store_id)
        #
        # if res.get_obj().get_dal_responsibility_id() not in self._responsibilities_ids:
        #     self._responsibilities_ids += [responsibility.get_dal_responsibility_id()]
        #     self._member_handler.update_responsibilities_ids(self._username, self._responsibilities_ids)
        if store_id not in self._responsibilities:
            self._responsibilities[store_id] = responsibility
        if responsibility.get_dal_responsibility_id() not in self._responsibilities_ids:
            self._member_handler.update_responsibilities_ids(self._username, self._responsibilities_ids + [
                responsibility.get_dal_responsibility_id()])

    def remove_responsibility(self, store_id):
        self._responsibilities.pop(store_id)

    def get_purchase_details(self):
        return self._purchase_details

    def get_responsibilities(self):
        return self._responsibilities

    def load_cart(self):
        from Backend.DataBase.Handlers.member_handler import MemberHandler
        self._member_handler = MemberHandler.get_instance()
        cart_res = self._member_handler.load_cart(self._username)
        if cart_res.succeeded():
            self._cart = cart_res.get_obj()
        return cart_res

    def __init__(
            self, user, username, responsibilities=None, purchase_details=None, cart=None
    ):
        super().__init__(user, cart)
        if purchase_details is None:
            purchase_details = []
        if responsibilities is None:
            responsibilities = dict()
        self._username = username
        self._responsibilities = responsibilities
        if responsibilities is None:
            self._responsibilities_ids = []
        else:
            self._responsibilities_ids = [res.get_dal_responsibility_id() for res in responsibilities]

        self._purchase_details = purchase_details
        self._notifications: list[str] = []
        self.notifications_lock = threading.Lock()
        self._offers: dict[str, Offer] = {}
        from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
        self._responsibilities_handler = ResponsibilitiesHandler.get_instance()

    @orm.reconstructor
    def init_on_load(self):
        self._statistics = Statistics.getInstance()
        from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
        self._responsibilities_handler = ResponsibilitiesHandler.get_instance()

    def login(self, username, password):
        return Response(False, msg="Members cannot re-login")

    def register(self, username, password):
        return Response(False, msg="Members cannot re-register")

    def save_product_in_cart(self, store_id, product_id, quantity):
        response = self._cart.add_product(store_id, product_id, quantity, self._username)
        # update data in DB in later milestones
        return response

    def delete_from_cart(self, store_id, product_id):
        response = self._cart.remove_product(store_id, product_id, self._username)
        # update data in DB in later milestones
        return response

    def change_product_quantity_in_cart(self, store_id, product_id, new_quantity):
        response = self._cart.change_product_quantity(store_id, product_id, new_quantity, self._username)
        # update data in DB in later milestones
        return response

    def buy_cart(self, current_user):
        response = super().buy_cart(current_user)
        # update data in DB in later milestones
        return response

    def delete_products_after_purchase(self):
        response = self._cart.delete_products_after_purchase(self._username)
        # if response.succeeded():
        #     # update data in DB in later milestones
        #     self._purchase_details += response.object

        return response

    def open_store(self, store_name) -> Response:
        store = Store(store_name)
        res_create_purchase_root = store.create_purchase_rules_root()
        if not res_create_purchase_root.succeeded():
            return db_fail_response
        res_create_discounts_root = store.create_discounts_rules_root()
        if not res_create_discounts_root.succeeded():
            return db_fail_response

        store.save()
        founder = Founder(self, store, self._user)
        res_save = founder.save_self(self._username, store.get_id())
        if not res_save.succeeded():
            return res_save
        store.set_responsibility(founder)
        self.add_responsibility(founder, store.get_id())
        res = self._member_handler.commit_changes()
        if not res.succeeded():
            self.remove_responsibility(store.get_id())
            return Response(False, msg="DB Error")
        return Response[Store](True, obj=store, msg="Store opened successfully")

    def get_user_name(self):
        return self._username

    def get_responsibility_by_store(self, store_id):
        if not self._responsibilities:
            self._responsibilities = dict()
        if store_id in self._responsibilities:
            if self._responsibilities[store_id]._user_state is None:
                self._responsibilities[store_id].set_user_state(self)
            return Response(True, self._responsibilities[store_id])
        from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
        from Backend.Domain.TradingSystem.stores_manager import StoresManager
        store_res = StoresManager.get_store(store_id)
        if not store_res.succeeded():
            return store_res
        res = ResponsibilitiesHandler.get_instance().load_res_and_appointments(store_res.get_obj().get_res_id(),
                                                                               store_res.get_obj())
        if res.succeeded():
            founder_responsibility = res.get_obj()
            responsibility = self.get_own_responsibility(founder_responsibility)
            if responsibility is None:
                return Response(False, msg="There is no such responsibility!")
            self.add_responsibility(responsibility, store_id)
            self._responsibilities[store_id].set_user_state(self)
            self._responsibilities[store_id].set_subscriber(self._user)
            # responsibility.get_user_state()
            return Response(True, obj=responsibility)
        return res

    def get_responsibilities_by_username(self):
        if not self._responsibilities:
            self._responsibilities = dict()

        responsibilities_res = self._responsibilities_handler.load_responsibilities_by_username(self._username)
        if not responsibilities_res.succeeded():
            return db_fail_response

        for responsibility in responsibilities_res.get_obj():
            responsibility.set_user_state(self)
            res = responsibility.get_store()
            if not res.succeeded():
                return res
            self.add_responsibility(responsibility, responsibility.get_store_id())
            self._responsibilities[responsibility.get_store_id()].set_subscriber(self._user)
            responsibility.get_store().get_founder()
        return Response(True)

    def get_purchase_history(self):
        return Response[ParsableList[PurchaseDetails]](
            True,
            obj=ParsableList(self._purchase_details),
            msg="Purchase history " "got successfully",
        )

    def add_new_product(
            self, store_id, product_name, category, product_price, quantity, keywords=None
    ):
        res = self.get_responsibility_by_store(store_id)
        if res.succeeded():
            return res.get_obj().add_product(product_name, category, product_price, quantity, keywords)
        # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res

    def remove_product(self, store_id, product_id):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
            return res
        return res.get_obj().remove_product(product_id)

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().change_product_quantity_in_store(
            product_id, new_quantity
        )

    def edit_product_details(
            self, store_id, product_id, new_name, new_category, new_price, keywords=None
    ):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().edit_product_details(
            product_id, new_name, new_category, new_price, keywords
        )

    def add_discount(
            self, store_id: str, discount_data: dict, exist_id: str, condition_type: str = None
    ):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().add_discount(
            discount_data, exist_id, condition_type)

    def move_discount(self, store_id: str, src_id: str, dest_id: str):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().move_discount(src_id, dest_id)

    def get_discounts(self, store_id: str):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().get_discounts()

    def remove_discount(self, store_id: str, discount_id: str):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().remove_discount(discount_id)

    def edit_simple_discount(
            self,
            store_id: str,
            discount_id: str,
            percentage: float = None,
            context: dict = None,
            duration=None,
    ):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().edit_simple_discount(
            discount_id, percentage, context, duration
        )

    def edit_complex_discount(
            self, store_id: str, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().edit_complex_discount(
            discount_id, complex_type, decision_rule
        )

    def appoint_new_store_owner(self, store_id, new_owner):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().appoint_owner(new_owner)

    def dismiss_from_store(self, store_id):
        # from Backend.DataBase.Handlers.member_handler import MemberHandler
        # self.set_responsibility_ids(MemberHandler.get_instance().load_res_ids(self._username).get_obj())
        res = self.get_responsibility_by_store(store_id)
        if res.succeeded():
            # self._responsibilities_ids.remove(res.get_obj().get_dal_responsibility_id())
            self._responsibilities.pop(store_id)
        return res

    def dismiss_from_store_db(self, responsibility):
        updated_ids = list(set(self._responsibilities_ids) - {responsibility.get_dal_responsibility_id()})
        # for appointed in responsibility._appointed:
        #     res = self.dismiss_from_store_db(appointed)
        #     if not res.succeeded():
        #         return res
        res = self._member_handler.update_responsibilities_ids(self._username, updated_ids)
        return res

    def appoint_new_store_manager(self, store_id, new_manager):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().appoint_manager(new_manager)

    def add_manager_permission(self, store_id, username, permission):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().add_manager_permission(username, permission)

    def remove_manager_permission(self, store_id, username, permission):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().remove_manager_permission(username, permission)

    def remove_appointment(self, store_id, username):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().remove_appointment(username)

    def get_store_personnel_info(self, store_id):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().get_store_appointments()

    def get_my_appointments(self):
        res = self.get_responsibilities_by_username()
        if not res.succeeded():
            return res
        return Response(True, ParsableList(list(self._responsibilities.values())))

    def get_store_purchase_history(self, store_id):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().get_store_purchase_history()

    def get_any_store_purchase_history_admin(self, store_id):
        return Response(False, msg="Regular members cannot get any store's purchase history")

    def get_user_purchase_history_admin(self, username):
        return Response(False, msg="Regular members cannot get any user's purchase history")

    def is_appointed(self, store_id):
        res = self.get_responsibility_by_store(store_id)
        return Response(True, res.succeeded())

    # 4.2
    def add_purchase_rule(self, store_id: str, rule_details: dict, rule_type: str, parent_id: str, clause: str = None):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
        return res.get_obj().add_purchase_rule(rule_details, rule_type, parent_id, clause)

    # 4.2
    def remove_purchase_rule(self, store_id: str, rule_id: str):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
        return res.get_obj().remove_purchase_rule(rule_id)

    # 4.2
    def edit_purchase_rule(self, store_id: str, rule_details: dict, rule_id: str, rule_type: str):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
        return res.get_obj().edit_purchase_rule(rule_details, rule_id, rule_type)

    # 4.2
    def move_purchase_rule(self, store_id: str, rule_id: str, new_parent_id: str):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
        return res.get_obj().move_purchase_rule(rule_id, new_parent_id)

    # 4.2
    def get_purchase_policy(self, store_id):
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
        return res.get_obj().get_purchase_policy()

    def add_purchase_rule_history(self, purchase):
        self._purchase_details.append(purchase)

    # 6.5
    def register_statistics(self) -> None:
        if len(self._responsibilities) == 0:
            return self._statistics.register_passive()

        responsibilities = self._responsibilities.values()
        isOwner = any([responsibility.is_owner() for responsibility in responsibilities])
        if isOwner:
            return self._statistics.register_owner()

        return self._statistics.register_manager()

    # Offers
    # ==================

    def get_user_offers(self) -> Response[ParsableList[Offer]]:
        return Response(True, ParsableList(list(self._offers.values())))

    def get_store_offers(self, store_id) -> Response[ParsableList[Offer]]:
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().get_store_offers()

    def create_offer(self, user, store_id, product_id) -> Response[str]:
        from Backend.Domain.TradingSystem.stores_manager import StoresManager

        response_get_store = StoresManager.get_store(store_id)
        if not response_get_store.succeeded():
            return Response(False, msg=response_get_store.get_msg())

        response_get_product = StoresManager.get_product(store_id, product_id)
        if not response_get_product.succeeded():
            return response_get_product

        offer = Offer(user, response_get_store.object, response_get_product.object)
        self._offers[offer.get_id()] = offer
        res = self._member_handler.commit_changes()
        if not res.succeeded():
            return db_fail_response
        return Response(True, offer.get_id())

    def declare_price(self, offer_id, price) -> Response[None]:
        if offer_id not in self._offers:
            return Response(False, msg=f"Offer with offer id {offer_id} does not exist")
        return self._offers[offer_id].declare_price(price)

    def suggest_counter_offer(self, store_id, product_id, offer_id, price) -> Response[None]:
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().suggest_counter_offer(product_id, offer_id, price)

    def approve_manager_offer(self, offer_id) -> Response[None]:
        if offer_id not in self._offers:
            return Response(False, msg=f"Offer with offer id {offer_id} does not exist")
        return self._offers[offer_id].approve_manager_offer()

    def approve_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().approve_user_offer(product_id, offer_id, self._username)

    def reject_user_offer(self, store_id, product_id, offer_id) -> Response[None]:
        res = self.get_responsibility_by_store(store_id)
        if not res.succeeded():
            return res
            # return Response(False, msg=f"this member do not own/manage store {store_id}")
        return res.get_obj().reject_user_offer(product_id, offer_id)

    def cancel_offer(self, offer_id) -> Response[None]:
        if offer_id not in self._offers:
            return Response(False, msg=f"Offer with offer id {offer_id} does not exist")
        return self._offers[offer_id].cancel_offer()

    def has_res_id(self, res_id):
        return res_id in self._responsibilities_ids

    def set_responsibilities(self, store_id_to_res):
        self._responsibilities = store_id_to_res
        self._responsibilities_ids = [res.get_dal_responsibility_id() for res in store_id_to_res.values()]

    def set_responsibility_ids(self, responsibility_ids):
        self._responsibilities_ids = [element for element in responsibility_ids[0]]

    def get_responsibility_ids(self):
        return self._responsibilities_ids

    def get_own_responsibility(self, root_responsibility):
        if root_responsibility.get_dal_responsibility_id() in self._responsibilities_ids:
            return root_responsibility
        elif not root_responsibility._appointed:
            return None
        for appointee in root_responsibility._appointed:
            res = self.get_own_responsibility(appointee)
            if res is not None:
                return res
        return None

    def get_users_statistics(self) -> Response[StatisticsData]:
        return Response(False, msg="Regular members cannot get statistics")
