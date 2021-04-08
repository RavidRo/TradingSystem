import aiorwlock

from Backend.Domain.TradingSystem.discount_policy import DefaultDiscountPolicy
from Backend.Domain.TradingSystem.Interfaces import IPurchaseDetails, IStore
from Backend.Domain.TradingSystem.product import Product
import uuid
from Backend.Domain.TradingSystem.purchase_policy import DefaultPurchasePolicy
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.response import Response, ParsableList
from dataclasses import dataclass


class Store(IStore):

    def __init__(self, store_name: str):
        """Create a new store with it's specified info"""
        self.id = self.id_generator()
        self.name = store_name
        self.products_to_quantities = dict()
        self.responsibility = None
        # These fields will be changed in the future versions
        self.discount_policy = DefaultDiscountPolicy()
        self.purchase_policy = DefaultPurchasePolicy()
        self.purchase_history = []
        self.products_rwlock = aiorwlock.RWLock()
        self.history_rwlock = aiorwlock.RWLock()

    def parse(self):
        return StoreDataObject(self.id, self.name)

    def parse_products(self):
        parsed_products = []
        for product, quantity in self.products_to_quantities.values():
            parsed_products.append((product.get_id(), product.get_name(), product.get_price(), quantity))
        return parsed_products

    async def set_product_name(self, product_id, new_name) -> Response[None]:
        async with self.products_rwlock.writer_lock:
            if self.products_to_quantities.get(product_id) is None:
                return Response(False, msg=f"product with {product_id} doesn't exist in the store!")

            self.products_to_quantities.get(product_id)[0].set_product_name(new_name)
            return Response(True, msg=f"Product {product_id} name was changed successfully!")

    async def show_store_data(self) -> Response:
        async with self.products_rwlock.reader_lock:
            # in the future other field will be checked too
            if self.responsibility is None:
                return Response(False, msg="Store's responsibilities aren't set yet")

            return Response[Store](True, self, msg="Store's details are complete")

    def get_name(self) -> str:
        return self.name

    async def add_product(self, product_name: str, price: float, quantity: int) -> Response[None]:
        async with self.products_rwlock.writer_lock:
            if quantity <= 0:
                # actually it's non-negative but adding 0 amount is redundant
                return Response(False, msg="Product's qunatity must be positive!")

            if price <= 0:
                return Response(False, msg="Product's price must pe positive!")

            if self.check_existing_product(product_name):
                return Response(False, msg="This product is already in the store's inventory")

            product = Product(product_name, price)
            product_id = product.get_id()
            self.products_to_quantities.update({product_id, (product, quantity)})
            return Response(True, msg="product" + str(product_name) + "successfully added")

    async def remove_product(self, product_id: str) -> Response[None]:
        async with self.products_rwlock.writer_lock:
            result = self.products_to_quantities.pop(product_id, None)
            if result is None:
                return Response(False, msg="The product " + str(result[0].get_name()) + "is already not in the "
                                                                                        "inventory!")
            return Response(True, msg="Successfully removed product with product id: " + str(product_id))

    async def edit_product_details(self, product_id: str, product_name: str, price: float) -> Response[None]:
        async with self.products_rwlock.writer_lock:
            if price <= 0:
                return Response(False, msg="Product's price must pe positive!")

            if not self.check_existing_product(product_name):
                return Response(False, msg="No such product in the store")

        self.products_to_quantities.get(product_id)[0].edit_product_details(product_id, product_name, price)
        return Response(True, msg="Successfully edited product with product id: " + str(product_id))

    async def change_product_quantity(self, product_id: str, quantity: int) -> Response[None]:
        async with self.products_rwlock.writer_lock:
            if product_id in self.products_to_quantities:
                self.products_to_quantities[product_id][1] = quantity
                return Response(True, msg="Successfully updated product " +
                                          str(self.products_to_quantities[product_id][0].get_name()) + "'s quantity")
            return Response(False, msg="The product with id: " + str(product_id) + " isn't in the inventory!")

    def get_personnel_info(self) -> Response[Responsibility]:
        if self.responsibility is None:
            return Response(False, msg="The store doesn't have assigned personnel")
        return Response[Responsibility](True, self.responsibility, msg="Personnel info")

    async def get_purchases_history(self) -> Response[ParsableList[IPurchaseDetails]]:
        async with self.history_rwlock.reader_lock:
            return Response[ParsableList](True, ParsableList(self.purchase_history), msg="Purchase history")

    async def update_store_history(self, purchase_details: IPurchaseDetails):
        async with self.history_rwlock.writer_lock:
            self.purchase_history.append(purchase_details)

    @staticmethod
    def id_generator() -> str:
        return str(uuid.uuid4())

    def get_id(self) -> str:
        return self.id

    def set_responsibility(self, responsibility: Responsibility):
        self.responsibility = responsibility

    async def check_existing_product(self, product_name: str):
        async with self.products_rwlock.reader_lock:
            for (prod, quantity) in self.products_to_quantities.values():
                if prod.get_name() == product_name:
                    return True
            return False

    async def get_product_name(self, product_id: str):
        async with self.products_rwlock.reader_lock:
            return self.products_to_quantities.get(product_id)[0].get_name()

    async def send_back(self, products_to_quantities: dict):
        async with self.products_rwlock.writer_lock:
            for prod_id, quantity in products_to_quantities.items():
                if self.products_to_quantities.get(prod_id) is None:
                    self.products_to_quantities.update({prod_id, quantity})
                else:
                    self.products_to_quantities[prod_id,] += quantity

    # This function checks for available products and catches them
    async def check_available_products(self, products_ids_to_quantities: dict) -> Response[None]:
        async with self.products_rwlock.reader_lock:
            for prod_id, quantity in products_ids_to_quantities.items():
                current_quantity = self.products_ids_to_quantities.get(prod_id)[1]
                if current_quantity is None:
                    return Response(False,
                                    msg="The product with id: " + prod_id + "doesn't exist in the inventory of the store")
                elif current_quantity < quantity:
                    return Response(False, msg="The store has less than" + str(
                        quantity) + "of the product with id: " + prod_id + "left")

            return Response(True, msg="All products are available")

    async def acquire_products(self, products_ids_to_quantities: dict) -> None:
        async with self.products_rwlock.writer_lock:
            for prod_id, quantity in products_ids_to_quantities.items():
                current_quantity = self.products_to_quantities.get(prod_id)[1]
                if current_quantity == quantity:
                    self.products_to_quantities.pop(prod_id)
                else:
                    product = self.products_to_quantities.get(prod_id)[0]
                    self.products_to_quantities.update({prod_id, (product, current_quantity - quantity)})

    # this will be added in the future - maybe I will apply Default Policy for now
    def check_purchase_types(self, products_info, user_info) -> Response[None]:
        return Response(True, msg="all purchase types arew available")

    def apply_discounts(self, user_info, product_ids_to_quantity: dict):
        return self.discount_policy.applyDiscount(user=user_info, store=self,
                                                  products_to_quantities=product_ids_to_quantity)


@dataclass
class StoreDataObject:
    id: str
    name: str
