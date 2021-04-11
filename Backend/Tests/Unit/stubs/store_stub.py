from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, ParsableList
from Backend.rw_lock import ReadWriteLock


class StoreStub(Store):
    def __init__(self, products={}) -> None:
        self.product_added = False
        self.product_removed = False
        self.product_quantity_changed = False
        self.product_details_changed = False
        self.products_to_quantities: dict = products
        self.products_lock = ReadWriteLock()

    # 4.1
    # Creating a new product a the store
    def add_product(self, name: str, price: float, quantity: int) -> Response[None]:
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
        self, product_id: str, new_name: str, new_price: float
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

    def product_exists(self, product_id, quantity):
        if self.products_to_quantities.get(product_id) is None:
            return False
        if self.products_to_quantities.get(product_id)[1] < quantity:
            return False
        return True

    def get_product(self, product_id):
        return self.products_to_quantities.get(product_id)[0]

    # def acquire_products(self):