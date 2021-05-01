from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission, Responsibility

# from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.user import User
from Backend.response import Response, ParsableList, PrimitiveParsable


class Founder(Responsibility):
    def __init__(self, user_state, store, subscriber=None) -> None:
        super().__init__(user_state, store, subscriber)
        if subscriber != None:
            self._store.subscribe(subscriber)

    # 4.1
    # Creating a new product a the store
    def add_product(self, name: str, category: str, price: float, quantity: int) -> Response[str]:
        return self._store.add_product(name, category, price, quantity)

    # 4.1
    def remove_product(self, product_id: str) -> Response[PrimitiveParsable[int]]:
        return self._store.remove_product(product_id)

    # 4.1
    def change_product_quantity_in_store(self, product_id: str, quantity: int) -> Response[None]:
        return self._store.change_product_quantity(product_id, quantity)

    # 4.1
    def edit_product_details(
        self, product_id: str, new_name: str, new_category: str, new_price: float
    ) -> Response[None]:
        return self._store.edit_product_details(product_id, new_name, new_category, new_price)

    # 4.3
    def appoint_owner(self, user: User) -> Response[None]:
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
                newResponsibility = Owner(user.state, self._store, user)
                self._appointed.append(newResponsibility)
                result = Response(True)

        return result

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
                newResponsibility = Manager(user.state, self._store)
                self._appointed.append(newResponsibility)
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

    def get_my_appointees(self) -> Response[ParsableList[Responsibility]]:
        return Response(True, ParsableList(self._appointed))

    # 4.11
    def get_store_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        return self._store.get_purchase_history()
