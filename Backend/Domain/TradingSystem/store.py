import uuid

from Backend.response import Response, ParsableList
from Backend.Domain.TradingSystem.product import Product
from Backend.Service.DataObjects.store_data import StoreData


class Store:
    from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
    from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails

    def __init__(self, store_name: str):
        from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
        from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy

        """Create a new store with it's specified info"""
        self.id = self.id_generator()
        self.name = store_name
        self.products_to_quantities: dict[str, tuple[Product, int]] = {}
        self.responsibility = None
        # These fields will be changed in the future versions
        self.discount_policy = DefaultDiscountPolicy()
        self.purchase_policy = DefaultPurchasePolicy()
        self.purchase_history = []

    def parse(self):
        return StoreData(self.id, self.name)

    def parse_products(self):
        parsed_products = []
        for product, quantity in self.products_to_quantities.values():
            parsed_products.append(
                (product.get_id(), product.get_name(), product.get_price(), quantity)
            )
        return parsed_products

    def get_products(self) -> Response[ParsableList[Product]]:
        products = [product for product, _ in self.products_to_quantities.values()]
        return Response(True, ParsableList(products))

    """checks need to be made:
       ----------------------
       1. A product with product_id exists in the store"""

    def set_product_name(self, product_id, new_name) -> Response[None]:
        if self.products_to_quantities[product_id] is None:
            return Response(False, msg=f"product with {product_id} doesn't exist in the store!")

        self.products_to_quantities[product_id][0].set_product_name(new_name)
        return Response(True, msg=f"Product {product_id} name was changed successfully!")

    def get_name(self) -> str:
        return self.name

    """checks need to be made:
       ----------------------
       1. product_name != ""
       2. quantity >= 0
       3. price >= 0
       4. a product with product_name exists"""

    def add_product(self, product_name: str, price: float, quantity: int) -> Response[str]:
        from Backend.Domain.TradingSystem.product import Product

        if not product_name:
            return Response(False, msg="Product's name can't be empty!")

        if quantity < 0:
            # actually it's non-negative but adding 0 amount is redundant
            return Response(False, msg="Product's quantity must be positive!")

        if price < 0:
            return Response(False, msg="Product's price must pe positive!")

        if self.check_existing_product(product_name):
            return Response(False, msg="This product is already in the store's inventory")

        product = Product(product_name=product_name, price=price)
        product_id = product.get_id()
        self.products_to_quantities[product_id] = (product, quantity)
        return Response(True, product_id, msg=f"The product {product_name} successfully added")

    """checks need to be made:
       ----------------------
       1. a product with product_id exists"""

    def remove_product(self, product_id: str) -> Response[None]:
        result = self.products_to_quantities.pop(product_id, None)
        if result is None:
            return Response(
                False, msg="The product " + product_id + "is already not in the inventory!"
            )
        return Response(
            True, msg="Successfully removed product with product id: " + str(product_id)
        )

    """checks need to be made:
       ----------------------
       1. price > 0
       2. a product with product_id exists"""

    def edit_product_details(
        self, product_id: str, product_name: str, price: float
    ) -> Response[None]:
        if product_id not in self.products_to_quantities:
            return Response(False, msg="No such product in the store")

        return self.products_to_quantities[product_id][0].edit_product_details(product_name, price)

    """checks need to be made:
       ----------------------
       1. quantity > 0
       2. a product with product_name exists"""

    def change_product_quantity(self, product_id: str, quantity: int) -> Response[None]:
        if quantity < 0:
            return Response(False, msg="quantity must be positive!")
        if product_id in self.products_to_quantities:
            new_product_quantity = (self.products_to_quantities[product_id][0], quantity)
            self.products_to_quantities[product_id] = new_product_quantity
            return Response(
                True,
                msg="Successfully updated product "
                + str(self.products_to_quantities[product_id][0].get_name())
                + "'s quantity",
            )
        return Response(False, msg=f"The product with id: {product_id} isn't in the inventory!")

    def get_personnel_info(self) -> Response[Responsibility]:
        from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility

        if self.responsibility is None:
            return Response(False, msg="The store doesn't have assigned personnel")
        return Response[Responsibility](True, self.responsibility, msg="Personnel info")

    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        return Response[ParsableList](
            True, ParsableList(self.purchase_history), msg="Purchase history"
        )

    def update_store_history(self, purchase_details: PurchaseDetails):
        self.purchase_history.append(purchase_details)

    @staticmethod
    def id_generator() -> str:
        return str(uuid.uuid4())

    def get_id(self) -> str:
        return self.id

    def set_responsibility(self, responsibility: Responsibility):
        self.responsibility = responsibility

    def check_existing_product(self, product_name: str):
        for (prod, quantity) in self.products_to_quantities.values():
            if prod.get_name() == product_name:
                return True
        return False

    def get_product_name(self, product_id: str):
        return self.products_to_quantities.get(product_id)[0].get_name()

    def send_back(self, products_to_quantities: dict):
        for prod_id, (product, quantity) in products_to_quantities.items():
            if self.products_to_quantities.get(prod_id) is None:
                self.products_to_quantities.update({prod_id: (product, quantity)})
            else:
                self.products_to_quantities[prod_id][1] += quantity

    # This function checks for available products
    def check_available_products(self, products_to_quantities: dict) -> Response[None]:
        for prod_id, (_, quantity) in products_to_quantities.items():
            prod_to_current_quantity = self.products_to_quantities.get(prod_id)
            if prod_to_current_quantity is None:
                return Response(
                    False,
                    msg=f"The product with id: {prod_id} doesn't exist in the inventory of the store",
                )
            elif prod_to_current_quantity[1] < quantity:
                return Response(
                    False,
                    msg=f"The store has less than {quantity} of product with id: {prod_id} left",
                )

        return Response(True, msg="All products are available")

    def acquire_products(self, products_to_quantities: dict) -> None:
        for prod_id, (product, quantity) in products_to_quantities.items():
            current_quantity = self.products_to_quantities.get(prod_id)[1]
            if current_quantity == quantity:
                self.products_to_quantities.pop(prod_id)
            else:
                product = self.products_to_quantities.get(prod_id)[0]
                self.products_to_quantities[prod_id] = (product, current_quantity - quantity)

    # this will be added in the future - maybe I will apply Default Policy for now
    def check_purchase_types(self, products_info, user_info) -> Response[None]:
        return Response(True, msg="all purchase types arew available")

    def apply_discounts(self, user_info, product_to_quantity: dict):
        return self.discount_policy.applyDiscount(
            user=user_info, store=self, products_to_quantities=product_to_quantity
        )

    def get_product(self, product_id: str):
        return self.products_to_quantities.get(product_id)[0]

    def product_exists(self, product_id, quantity):
        product_quantity = self.products_to_quantities.get(product_id)
        if product_quantity is None or product_quantity[1] < quantity:
            return False
        return True
