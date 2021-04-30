from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility, Permission
from Backend.response import Response, ParsableList
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class ResponsibilityStub(Responsibility):
    def __init__(self):
        self.add_product_delegated = False
        self.remove_product_delegated = False
        self.change_product_quantity_delegated = False
        self.edit_product_details_delegated = False
        self.appoint_owner_delegated = False
        self.appoint_manager_delegated = False
        self.add_permission_delegated = False
        self.remove_permission_delegated = False
        self.dismiss_delegated = False
        self.get_personnel_info_delegated = False
        self.get_store_purchase_history_delegated = False

    def add_product(self, name: str, category: str, price: float, quantity: int, keywords: list[str] = None) -> Response[None]:
        self.add_product_delegated = True
        return Response(True)

    def remove_product(self, product_id: str) -> Response[None]:
        self.remove_product_delegated = True
        return Response(True)

    def change_product_quantity_in_store(self, product_id: str, quantity: int) -> Response[None]:
        self.change_product_quantity_delegated = True
        return Response(True)

    def edit_product_details(self, product_id: str, new_name: str, new_category: str, new_price: float, keywords: list[str] = None) -> Response[None]:
        self.edit_product_details_delegated = True
        return Response(True)

    def appoint_owner(self, user: IUser) -> Response[None]:
        self.appoint_owner_delegated = True
        return Response(True)

    def appoint_manager(self, user: IUser) -> Response[None]:
        self.appoint_manager_delegated = True
        return Response(True)

    def add_manager_permission(self, username: str, permission: Permission) -> Response[None]:
        self.add_permission_delegated = True
        return Response(True)

    def remove_manager_permission(self, username: str, permission: Permission) -> Response[None]:
        self.remove_permission_delegated = True
        return Response(True)

    def remove_appointment(self, username: str) -> Response[None]:
        self.dismiss_delegated = True
        return Response(True)

    def get_store_appointments(self) -> Response[Responsibility]:
        self.get_personnel_info_delegated = True
        return Response(True)

    def get_store_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        self.get_store_purchase_history_delegated = True
        return Response(True)
