from Backend.response import Response, ParsableList, PrimitiveParsable

from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission, Responsibility
from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class Manager(Owner):
    def __init__(self, user_state: Member, store) -> None:
        super().__init__(user_state, store, None)
        self.__permissions = {
            Permission.MANAGE_PRODUCTS: False,
            Permission.GET_APPOINTMENTS: True,
            Permission.APPOINT_MANAGER: False,
            Permission.REMOVE_MANAGER: False,
            Permission.GET_HISTORY: False,
        }

    def __create_no_permission_Response(self, permission: Permission) -> Response:
        return Response(
            False,
            msg=f"{self._user_state.get_username().get_obj().get_val()} does not have permission to {permission.name}",
        )

    # 4.1
    # Creating a new product a the store
    def add_product(self, name: str, category: str, price: float, quantity: int) -> Response[str]:
        if self.__permissions[Permission.MANAGE_PRODUCTS]:
            return super().add_product(name, category, price, quantity)

        return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

    # 4.1
    def remove_product(self, product_id: str) -> Response[PrimitiveParsable[int]]:
        if self.__permissions[Permission.MANAGE_PRODUCTS]:
            return super().remove_product(product_id)

        return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

    # 4.1
    def change_product_quantity_in_store(self, product_id: str, quantity: int) -> Response[None]:
        if self.__permissions[Permission.MANAGE_PRODUCTS]:
            return super().change_product_quantity_in_store(product_id, quantity)

        return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

    # 4.1
    def edit_product_details(self, product_id: str, new_name: str, new_category: str, new_price: float) -> Response[None]:
        if self.__permissions[Permission.MANAGE_PRODUCTS]:
            return super().edit_product_details(product_id, new_name, new_category, new_price)

        return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

    # 4.3
    def appoint_owner(self, user: IUser) -> Response[None]:
        return Response(False, msg=f"Managers can't appoint owners")

    # 4.5
    def appoint_manager(self, user: IUser) -> Response[None]:
        if self.__permissions[Permission.APPOINT_MANAGER]:
            return super().appoint_manager(user)

        return self.__create_no_permission_Response(Permission.APPOINT_MANAGER)

    # 4.6
    def add_manager_permission(self, username: str, permission) -> Response[None]:
        return Response(False, msg=f"Managers can't add permissions")

    # 4.6
    def remove_manager_permission(self, username: str, permission) -> Response[None]:
        return Response(False, msg=f"Managers can't remove permissions")

    # 4.4, 4.7
    def remove_appointment(self, username: str) -> Response[None]:
        if self.__permissions[Permission.REMOVE_MANAGER]:
            return super().remove_appointment(username)

        return self.__create_no_permission_Response(Permission.REMOVE_MANAGER)

    # 4.9
    def get_store_appointments(self) -> Response[Responsibility]:
        if self.__permissions[Permission.GET_APPOINTMENTS]:
            return super().get_store_appointments()

        return self.__create_no_permission_Response(Permission.GET_APPOINTMENTS)

    # 4.11
    def get_store_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        if self.__permissions[Permission.GET_HISTORY]:
            return super().get_store_purchase_history()

        return self.__create_no_permission_Response(Permission.GET_HISTORY)

    def _add_permission(self, username: str, permission: Permission) -> bool:
        if self._user_state.get_username().get_obj().get_val() == username:
            self.__permissions[permission] = True
            return True

        return super()._add_permission(username, permission)

    def _remove_permission(self, username: str, permission: Permission) -> bool:
        if self._user_state.get_username().get_obj().get_val() == username:
            self.__permissions[permission] = False
            return True

        return super()._remove_permission(username, permission)

    def _is_manager(self) -> bool:
        return True

    def _permissions(self) -> list[str]:
        exec = list(filter(lambda per: self.__permissions[per], Permission))
        return [per.name for per in exec]
