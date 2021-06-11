from Backend.DataBase.database import session, db_fail_response
from Backend.Domain.TradingSystem.offer import Offer
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission, Responsibility

# from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.user import User
from Backend.response import Response, ParsableList, PrimitiveParsable


class Founder(Responsibility):

    # 4.1
    # Creating a new product a the store
    def add_product(
        self, name: str, category: str, price: float, quantity: int, keywords: list[str] = None
    ) -> Response[str]:
        return self._store.add_product(name, category, price, quantity, keywords)

    # 4.1
    def remove_product(self, product_id: str) -> Response[PrimitiveParsable[int]]:
        return self._store.remove_product(product_id)

    # 4.1
    def change_product_quantity_in_store(self, product_id: str, quantity: int) -> Response[None]:
        return self._store.change_product_quantity(product_id, quantity)

    # 4.1
    def edit_product_details(
        self,
        product_id: str,
        new_name: str,
        new_category: str,
        new_price: float,
        keywords: list[str] = None,
    ) -> Response[None]:
        return self._store.edit_product_details(
            product_id, new_name, new_category, new_price, keywords
        )

    # 4.2
    def add_purchase_rule(
        self, rule_details: dict, rule_type: str, parent_id: str, clause: str = None
    ):
        return self._store.add_purchase_rule(rule_details, rule_type, parent_id, clause)

    # 4.2
    def remove_purchase_rule(self, rule_id: str):
        return self._store.remove_purchase_rule(rule_id)

    # 4.2
    def edit_purchase_rule(self, rule_details: dict, rule_id: str, rule_type: str):
        return self._store.edit_purchase_rule(rule_details, rule_id, rule_type)

    # 4.2
    def move_purchase_rule(self, rule_id: str, new_parent_id: str):
        return self._store.move_purchase_rule(rule_id, new_parent_id)

    # 4.2
    def get_purchase_policy(self):
        return self._store.get_purchase_policy()

    # 4.2
    def add_discount(self, discount_data: dict, exist_id: str, condition_type: str = None):
        return self._store.add_discount(discount_data, exist_id, condition_type)

    # 4.2
    def move_discount(self, src_id: str, dest_id: str):
        return self._store.move_discount(src_id, dest_id)

    # 4.2
    def get_discounts(self):
        return self._store.get_discounts()

    # 4.2
    def remove_discount(self, discount_id: str):
        return self._store.remove_discount(discount_id)

    # 4.2
    def edit_simple_discount(
        self, discount_id: str, percentage: float = None, context: dict = None, duration=None
    ):
        return self._store.edit_simple_discount(discount_id, percentage, context, duration)

    # 4.2
    def edit_complex_discount(
        self, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        return self._store.edit_complex_discount(discount_id, complex_type, decision_rule)

    # 4.3
    def appoint_owner(self, user: IUser) -> Response[None]:
        # * The import is here to fix circular dependency problem
        from Backend.Domain.TradingSystem.Responsibilities.owner import Owner

        # We don't to appoint a user to the same store twice
        with user.get_appointment_lock():
            appointed_response = user.is_appointed(self._store.get_id())
            if not appointed_response.succeeded():
                result = appointed_response
            elif appointed_response.get_obj():
                result = Response(
                    False,
                    msg=f"{user.get_username().get_obj().get_val()} is already appointed to {self._store.get_name()}",
                )
            else:
                #! I am guessing that user.state is of type member because at user_manager, with a given username he found a user object
                #! (guest does not hae a username)
                new_responsibility = Owner(user.state, self._store, user)
                self._appointed.append(new_responsibility)
                from Backend.DataBase.Handlers.responsibilities_handler import Owner_Responsibility_DAL
                self.save_appointment(new_responsibility, Owner_Responsibility_DAL)
                new_responsibility._user_state.add_responsibility(new_responsibility, self._store.get_id())
                res = self._responsibilities_handler.commit_changes()
                return res

        return result

    def save_appointment(self, new_responsibility, class_type):
        dal_responsibility_res = new_responsibility._responsibilities_handler.save_res(class_type, parent=self._responsibility_dal)
        if dal_responsibility_res.succeeded():
            new_responsibility._responsibility_dal = dal_responsibility_res.get_obj()
            new_responsibility._responsibility_dal_id = dal_responsibility_res.get_obj().id
            return Response(True)
        return db_fail_response

    # 4.5
    def appoint_manager(self, user: User) -> Response[None]:
        # * The import is here to fix circular depandency problem
        from Backend.Domain.TradingSystem.Responsibilities.manager import Manager

        # We don't to appoint a user to the same store twice
        with user.get_appointment_lock():
            appointed_response = user.is_appointed(self._store.get_id())
            if not appointed_response.succeeded():
                result = appointed_response
            elif appointed_response.get_obj():
                result = Response(
                    False,
                    msg=f"{user.get_username().get_obj().get_val()} is already appointed to {self._store.get_name()}",
                )
            else:
                #! I am guessing that user.state is of type member because at user_manager, with a given username he found a user object
                #! (guest does not hae a username)
                newResponsibility = Manager(user.state, self._store, user)
                self._appointed.append(newResponsibility)
                from Backend.DataBase.Handlers.responsibilities_handler import Manager_Responsibility_DAL
                self.save_appointment(newResponsibility, Manager_Responsibility_DAL)
                newResponsibility._user_state.add_responsibility(newResponsibility, self._store.get_id())
                res = self._responsibilities_handler.commit_changes()
                result = Response(True)

        return result

    # 4.6
    # recursively call children function until the child is found and the permission is added
    def add_manager_permission(self, username: str, permission: Permission) -> Response[None]:
        if not self._add_permission(username, permission):
            return Response(
                False,
                msg=f"{self._user_state.get_username().get_obj().get_val()} never appointed {username} as a manager",
            )
        return Response(True)

    # 4.6
    def remove_manager_permission(self, username: str, permission: Permission) -> Response[None]:
        if not self._remove_permission(username, permission):
            return Response(
                False,
                msg=f"{self._user_state.get_username().get_obj().get_val()} never appointed {username} as a manager",
            )
        return Response(True)

    # 4.4, 4.7
    def remove_appointment(self, username: str) -> Response[None]:
        if not self._remove_appointment(username):
            return Response(
                False,
                msg=f"{self._user_state.get_username().get_obj().get_val()} never appointed {username}",
            )
        return Response(True)

    # 4.9
    def get_store_appointments(self) -> Response[Responsibility]:
        return self._store.get_personnel_info()

    # 4.11
    def get_store_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        return self._store.get_purchase_history()

    # Offers
    # ======================

    def get_store_offers(self) -> Response[ParsableList[Offer]]:
        return self._store.get_store_offers()

    def suggest_counter_offer(self, product_id, offer_id, price) -> Response[None]:
        return self._store.suggest_counter_offer(product_id, offer_id, price)

    def approve_user_offer(self, product_id, offer_id) -> Response[None]:
        return self._store.approve_user_offer(product_id, offer_id)

    def reject_user_offer(self, product_id, offer_id) -> Response[None]:
        return self._store.reject_user_offer(product_id, offer_id)
