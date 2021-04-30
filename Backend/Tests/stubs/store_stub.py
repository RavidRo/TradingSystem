from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, ParsableList
from Backend.rw_lock import ReadWriteLock


class StoreStub(Store):
    def __init__(self, products=None) -> None:
        if products is None:
            products = {}
        self.product_added = False
        self.product_removed = False
        self.product_quantity_changed = False
        self.product_details_changed = False
        self._products_to_quantities: dict = products

    # 4.1
    # Creating a new product a the store
    def add_product(self, name: str, category: str, price: float, quantity: int, keywords: list[str] = None) -> Response[None]:
        self.product_added = True
        return Response(True)

    # 4.1
    def remove_product(self, product_id: str) -> Response[None]:
        self.product_removed = True
        return Response(True)

    # 4.1
    def change_product_quantity(self, product_id: str, quantity: int) -> Response[None]:
        self.product_quantity_changed = True
        return Response(True)

    # 4.1
    def edit_product_details(
        self, product_id: str = None, new_name: str = None, new_category: str = None, new_price: float = None, keywords: list[str] = None
    ) -> Response[None]:
        self.product_details_changed = True
        return Response(True)

    def get_id(self):
        return "0"

    def get_name(self):
        return "store"

    # 4.9
    def get_personnel_info(self) -> Response[Responsibility]:
        return Response(True)

    # 4.11
    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        return Response(True, ParsableList([]))

    def product_exists(self, product_id):
        if self._products_to_quantities.get(product_id) is None:
            return False
        return True

    def has_enough(self, product_id, quantity):
        if self._products_to_quantities.get(product_id)[1] < quantity:
            return False
        return True

    def get_product(self, product_id):
        return self._products_to_quantities.get(product_id)[0]

    def check_and_acquire_available_products(self, products_to_quantities: dict) -> Response[None]:
        for i in range(1, 4):
            self._products_to_quantities[f"{i}"] = (self._products_to_quantities[f"{i}"][0], self._products_to_quantities[f"{i}"][1] - 1)
        return Response(True)