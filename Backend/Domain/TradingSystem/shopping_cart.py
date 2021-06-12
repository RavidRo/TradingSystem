import threading
from threading import Timer

from Backend.response import Response, PrimitiveParsable, ParsableList
from Backend.Service.DataObjects.shopping_cart_data import ShoppingCartData
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.Domain.TradingSystem.Interfaces.IShoppingCart import IShoppingCart
from Backend.settings import Settings


class ShoppingCart(IShoppingCart):
    def __init__(self):
        self.__shopping_bags: dict[str, ShoppingBag] = dict()
        self.__timer = None
        self.__INTERVAL_TIME = self.interval_time()
        self.__purchase_time_passed = False
        self.__price = None
        self.__pending_purchase = False
        self.__transaction_lock = threading.Lock()

    def interval_time(self):
        settings = Settings.get_instance(False)
        return settings.get_timer_length()

    def get_shopping_bags(self):
        return self.__shopping_bags

    def cancel_timer(self):
        self.__timer.cancel()

    def parse(self):
        parsed_bags = []
        for bag in self.__shopping_bags.values():
            parsed_bags.append(bag.parse())
        return ShoppingCartData(parsed_bags)

    """checks need to be made:
       ----------------------
       1. quantity > 0
       2. If a bag with store_id already exits, add_product to it.
       3. If there is no existing bag, check if store with store_id exits.
       4. If store exists -> create new bag and add product"""

    def add_product(self, store_id: str, product_id: str, quantity: int, store) -> Response[None]:
        if quantity <= 0:
            return Response(False, msg="Product's quantity must be positive!")

        if store_id in self.__shopping_bags:
            return self.__shopping_bags[store_id].add_product(product_id, quantity)

        # no bag for store with store_id
        new_bag = self.create_new_bag(store)
        return new_bag.add_product(product_id, quantity)

    def create_new_bag(self, store):
        new_bag = ShoppingBag(store)
        self.__shopping_bags[store.get_id()] = new_bag
        return new_bag

    """checks need to be made:
       ----------------------
       1. bag of store with store_id exists"""

    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        bag = self.__shopping_bags.get(store_id)
        if bag is None:
            return Response(
                False, msg="There is no existing bag for store with store id: " + str(store_id)
            )

        return bag.remove_product(product_id)

    """checks need to be made:
       ----------------------
       1. bag of store with store_id exists
       2. new_amount > 0"""

    def change_product_quantity(
        self, store_id: str, product_id: str, new_amount: int
    ) -> Response[None]:
        bag = self.__shopping_bags.get(store_id)
        if bag is None:
            return Response(
                False, msg="There is no existing bag for store with store id: " + str(store_id)
            )
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")
        return bag.change_product_quantity(product_id, new_amount)

    """notice: if buy_products of any bag fails -> return acquired products to stores"""
    # products_purchase_info -a dict between store_id to list of tuples tuple (product_id to purchase_type)
    def buy_products(
        self, user_age: int, products_purchase_info=None, username="Guest"
    ) -> Response[PrimitiveParsable[float]]:
        if products_purchase_info is None:
            products_purchase_info = {}
        if self.__pending_purchase:
            return Response(False, msg="Purchase already in progress")
        if not self.__shopping_bags:
            return Response(False, msg="Cant buy an empty cart")

        sum_amount: float = 0
        succeeded_bags: list[ShoppingBag] = []
        # this if will be deleted in the version with purchase types
        if not products_purchase_info:
            bags = self.__shopping_bags
        else:
            bags = products_purchase_info

        for store_id in bags:
            # this is the function call in the version with purchase types
            # result = self.shopping_bags[store_id].buy_products(products_purchase_info[store_id], user)
            # this is the current function call with default empty products_purchase_info
            result = self.__shopping_bags[store_id].buy_products(user_age, username=username)
            if not result.success:
                for bag in succeeded_bags:
                    bag.send_back()
                return result
            succeeded_bags.append(self.__shopping_bags[store_id])
            sum_amount += result.object.value
            self.__price = sum_amount

        self.__purchase_time_passed = False
        if self.__timer is not None:
            self.__timer.cancel()
        self.start_timer()
        self.__pending_purchase = True
        return Response[PrimitiveParsable](
            True,
            obj=PrimitiveParsable(sum_amount),
            msg=f"All purchase details are valid. The overall sum is: {sum_amount}",
        )

    def get_price(self):
        if self.__price is not None:
            return Response(True, self.__price)
        return Response(False, msg="Can't get price when not in purchase state")

    """notice: For now - the bag will be deleted since only regular purchase type enabled!"""

    def delete_products_after_purchase(self, user_name: str = "guest") -> Response[ParsableList]:
        self.__timer.cancel()
        self.__pending_purchase = False
        self.__timer = None
        self.__price = None
        purchase_cart_details = []
        for store_id in self.__shopping_bags:
            purchase_cart_details.append(
                self.__shopping_bags[store_id].delete_products_after_purchase(user_name)
            )
        self.__shopping_bags.clear()
        return Response[ParsableList](
            True, ParsableList(purchase_cart_details), msg="Here are the purchase details!"
        )

    """notice: I use a flag that marks the time passed for the purchase"""

    def send_back(self):
        self.__transaction_lock.acquire()
        if self.__pending_purchase:
            self.__price = None
            self.__purchase_time_passed = True
            self.__pending_purchase = False
            for bag in self.__shopping_bags.values():
                bag.send_back()
        self.__transaction_lock.release()

    def start_timer(self):
        self.__timer = Timer(self.__INTERVAL_TIME, self.send_back)
        self.__timer.start()

    def lock_cart(self):
        self.__transaction_lock.acquire()

    def release_cart(self):
        self.__transaction_lock.release()

    def cancel_purchase(self):
        self.__transaction_lock.acquire()
        if self.__timer is not None:
            self.__timer.cancel()
        self.__timer = None
        self.__pending_purchase = False
        self.__price = None
        for bag in self.__shopping_bags.values():
            bag.send_back()
        self.__transaction_lock.release()
        return Response(True, msg="Purchase was cancled successfully")