import uuid

from Backend.Domain.Notifications.Publisher import Publisher
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.product import Product
from Backend.Service.DataObjects.store_data import StoreData
from Backend.rw_lock import ReadWriteLock


class Store:
    from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
    from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails

    def __init__(self, store_name: str):
        from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
        from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy

        """Create a new store with it's specified info"""
        self.__id = self.id_generator()
        self.__name = store_name
        self._products_to_quantities: dict[str, tuple[Product, int]] = {}
        self.__responsibility = None
        # These fields will be changed in the future versions
        self.__discount_policy = DefaultDiscountPolicy()
        self.__purchase_policy = DefaultPurchasePolicy()
        self.__purchase_history = []
        self._products_lock = ReadWriteLock()
        self.__history_lock = ReadWriteLock()
        self.__publisher: Publisher = Publisher()

    def parse(self):
        id_to_quantity = {}
        for id, (_, quantity) in self._products_to_quantities.items():
            id_to_quantity.update({id: quantity})
        return StoreData(self.__id, self.__name, id_to_quantity)

    def parse_products(self):
        parsed_products = []
        for product, quantity in self._products_to_quantities.values():
            parsed_products.append(
                (product.get_id(), product.get_name(), product.get_price(), quantity)
            )
        return parsed_products

    def subscribe(self, subscriber):
        self.__publisher.subscribe(subscriber)

    def get_products(self) -> Response[ParsableList[Product]]:
        self._products_lock.acquire_read()
        products = [product for product, _ in self._products_to_quantities.values()]
        self._products_lock.release_read()
        return Response(True, ParsableList(products))

    def get_products_to_quantities(self):
        return self._products_to_quantities

    """checks need to be made:
       ----------------------
       1. A product with product_id exists in the store"""

    def set_product_name(self, product_id, new_name) -> Response[None]:
        self._products_lock.acquire_write()
        if self._products_to_quantities[product_id] is None:
            self._products_lock.release_write()
            return Response(False, msg=f"product with {product_id} doesn't exist in the store!")

        self._products_to_quantities[product_id][0].set_product_name(new_name)
        self._products_lock.release_write()
        return Response(True, msg=f"Product {product_id} name was changed successfully!")

    def get_name(self) -> str:
        return self.__name

    """checks need to be made:
       ----------------------
       1. product_name != ""
       2. quantity >= 0
       3. price >= 0
       4. a product with product_name exists"""

    def add_product(self, product_name: str, category: str, price: float, quantity: int) -> Response[str]:
        from Backend.Domain.TradingSystem.product import Product
        self._products_lock.acquire_write()
        if not product_name:
            self._products_lock.release_write()
            return Response(False, msg="Product's name can't be empty!")

        if quantity < 0:
            # actually it's non-negative but adding 0 amount is redundant
            self._products_lock.release_write()
            return Response(False, msg="Product's quantity must be positive!")

        if price < 0:
            self._products_lock.release_write()
            return Response(False, msg="Product's price must pe positive!")

        if self.check_existing_product(product_name):
            self._products_lock.release_write()
            return Response(False, msg="This product is already in the store's inventory")

        product = Product(product_name=product_name, category=category, price=price)
        product_id = product.get_id()
        self._products_to_quantities[product_id] = (product, quantity)
        self._products_lock.release_write()
        return Response(True, product_id, msg=f"The product {product_name} successfully added")

    """checks need to be made:
       ----------------------
       1. a product with product_id exists"""

    def remove_product(self, product_id: str) -> Response[PrimitiveParsable[int]]:
        self._products_lock.acquire_write()
        result = self._products_to_quantities.pop(product_id, None)
        if result is None:
            self._products_lock.release_write()
            return Response(
                False, msg="The product " + product_id + "is already not in the inventory!"
            )
        self._products_lock.release_write()
        return Response(True, obj=PrimitiveParsable(result[1]), msg="Successfully removed product with product id: " + str(product_id))

    """checks need to be made:
       ----------------------
       1. price > 0
       2. a product with product_id exists"""

    def edit_product_details(self, product_id: str, product_name: str, category: str, price: float) -> Response[None]:
        self._products_lock.acquire_write()
        if product_id not in self._products_to_quantities:
            self._products_lock.release_write()
            return Response(False, msg="No such product in the store")

        response = self._products_to_quantities[product_id][0].edit_product_details(product_name, category, price)
        self._products_lock.release_write()
        return response

    """checks need to be made:
       ----------------------
       1. quantity > 0
       2. a product with product_name exists"""

    def change_product_quantity(self, product_id: str, quantity: int) -> Response[None]:
        self._products_lock.acquire_write()
        if quantity < 0:
            self._products_lock.release_write()
            return Response(False, msg="quantity must be positive!")
        if product_id in self._products_to_quantities:
            new_product_quantity = (self._products_to_quantities[product_id][0], quantity)
            self._products_to_quantities[product_id] = new_product_quantity
            prod_name = self._products_to_quantities[product_id][0].get_name()
            self._products_lock.release_write()
            return Response(True, msg=f"Successfully updated product {prod_name} 's quantity")
        self._products_lock.release_write()
        return Response(False, msg=f"The product with id: {product_id} isn't in the inventory!")

    def get_personnel_info(self) -> Response[Responsibility]:
        from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility

        if self.responsibility is None:
            return Response(False, msg="The store doesn't have assigned personnel")
        return Response[Responsibility](True, self.responsibility, msg="Personnel info")

    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        self.__history_lock.acquire_read()
        history = self.__purchase_history
        self.__history_lock.release_read()
        return Response[ParsableList](True, ParsableList(history), msg="Purchase history")

    def update_store_history(self, purchase_details: PurchaseDetails):
        self.__history_lock.acquire_write()
        self.__purchase_history.append(purchase_details)
        self.__history_lock.release_write()
        message = "A purchase has been made:\n"+str(purchase_details.__dict__)
        self.__publisher.notify_all(message)

    @staticmethod
    def id_generator() -> str:
        return str(uuid.uuid4())

    def get_id(self) -> str:
        return self.__id

    def set_responsibility(self, responsibility: Responsibility):
        self.responsibility = responsibility

    def check_existing_product(self, product_name: str):
        for (prod, quantity) in self._products_to_quantities.values():
            if prod.get_name() == product_name:
                return True
        return False

    def get_product_name(self, product_id: str):
        self._products_lock.acquire_read()
        name = self._products_to_quantities.get(product_id)[0].get_name()
        self._products_lock.release_read()
        return name

    def send_back(self, products_to_quantities: dict):
        self._products_lock.acquire_write()
        for prod_id, (product, quantity) in products_to_quantities.items():
            if self._products_to_quantities.get(prod_id) is None:
                self._products_to_quantities.update({prod_id: (product, quantity)})
            else:
                self._products_to_quantities[prod_id] = (self._products_to_quantities[prod_id][0], self._products_to_quantities[prod_id][1] + quantity)
        self._products_lock.release_write()

    # This function checks for available products
    def check_and_acquire_available_products(self, products_to_quantities: dict) -> Response[None]:
        acquired_product_ids_to_quantities = {}
        self._products_lock.acquire_write()
        for prod_id, (_, quantity) in products_to_quantities.items():
            prod_to_current_quantity = self._products_to_quantities.get(prod_id)
            if prod_to_current_quantity is None:
                self.__restore_products(acquired_product_ids_to_quantities)
                self._products_lock.release_write()
                return Response(False, msg=f"The product with id: {prod_id} doesn't exist in the inventory of the store")

            elif prod_to_current_quantity[1] < quantity:
                self.__restore_products(acquired_product_ids_to_quantities)
                self._products_lock.release_write()
                return Response(False, msg=f"The store has less than {quantity} of product with id: {prod_id} left")

            current_quantity = self._products_to_quantities.get(prod_id)[1]
            if current_quantity == quantity:
                self._products_to_quantities.pop(prod_id)
            else:
                product = self._products_to_quantities.get(prod_id)[0]
                self._products_to_quantities[prod_id] = (product, current_quantity - quantity)

            acquired_product_ids_to_quantities[prod_id] = quantity

        self._products_lock.release_write()
        return Response(True, msg="All products are available")

    def __restore_products(self, acquires_product_ids_to_quantities: dict):
        for product_id, quantity in acquires_product_ids_to_quantities.items():
            prod, current_quantity = self._products_to_quantities.get(product_id)
            self._products_to_quantities[product_id] = (prod, current_quantity  + quantity)


    # this will be added in the future - maybe I will apply Default Policy for now
    def check_purchase_types(self, products_info, user_info) -> Response[None]:
        return Response(True, msg="all purchase types arew available")

    def apply_discounts(self, user_info, product_to_quantity: dict):
        return self.__discount_policy.applyDiscount(
            user=user_info, store=self, products_to_quantities=product_to_quantity
        )

    def get_product(self, product_id: str):
        self._products_lock.acquire_read()
        prod = self._products_to_quantities.get(product_id)[0]
        self._products_lock.release_read()
        return prod

    def product_exists(self, product_id,):
        self._products_lock.acquire_read()
        product_quantity = self._products_to_quantities.get(product_id)
        if product_quantity is None:
            self._products_lock.release_read()
            return False
        self._products_lock.release_read()
        return True

    def has_enough(self, product_id, quantity):
        self._products_lock.acquire_read()
        product_quantity = self._products_to_quantities.get(product_id)
        if product_id in self._products_to_quantities and product_quantity[1] < quantity:
            self._products_lock.release_read()
            return False
        self._products_lock.release_read()
        return True
