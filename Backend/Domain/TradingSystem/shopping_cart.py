from threading import Timer
import Backend.Domain.TradingSystem
import Backend.Domain.TradingSystem
import Backend.Domain.TradingSystem.IUser
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.response import Response, PrimitiveParsable, ParsableList
from Backend.Domain.TradingSystem.Interfaces.IShoppingCart import *


class ShoppingCart(IShoppingCart):
    def __init__(self):
        from Backend.Domain.TradingSystem import stores_manager

        self.stores_manager = stores_manager.get_instance()
        self.shopping_bags: dict[str, ShoppingBag] = dict()
        self.timer = None
        self.INTERVAL_TIME = 10 * 60
        self.purchase_time_passed = False

    def parse(self):
        parsed_bags = []
        for bag in self.shopping_bags:
            parsed_bags.append(bag.parse())
        return parsed_bags

    """checks need to be made:
       ----------------------
       1. quantity > 0
       2. If a bag with store_id already exits, add_product to it.
       3. If there is no existing bag, check if store with store_id exits.
       4. If store exists -> create new bag and add product"""

    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        if quantity <= 0:
            return Response(False, msg="Product's quantity must be positive!")

        for bag in self.shopping_bags.values():
            if bag.get_store_ID() == store_id:
                return bag.add_product(product_id, quantity)

        # no bag for store with store_id
        store = self.stores_manager.get_store(store_id)
        if store is None:
            return Response(False, msg=f"There is no such store with store_id: {store_id}")
        new_bag = Backend.ShoppingBag(store)
        self.shopping_bags.update({store_id: new_bag})
        return new_bag.add_product(product_id, quantity)

    """checks need to be made:
       ----------------------
       1. bag of store with store_id exists"""

    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        bag = self.shopping_bags.get(store_id)
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
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(
                False, msg="There is no existing bag for store with store id: " + str(store_id)
            )
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")
        return bag.change_product_quantity(product_id, new_amount)

    """notice: if buy_products of any bag fails -> return acquired products to stores"""
    # products_purchase_info -a dict between store_id to list of tuples tuple (product_id to purchase_type)
    def buy_products(self, user, products_purchase_info={}) -> Response[PrimitiveParsable]:
        sum = 0
        succeeded_bags = []
        # this if will be deleted in the version with purchase types
        if not products_purchase_info:
            bags = self.shopping_bags
        else:
            bags = products_purchase_info

        for store_id in bags:
            # this is the function call in the version with purchase types
            # result = self.shopping_bags[store_id].buy_products(products_purchase_info[store_id], user)
            # this is the current function call with default empty products_purchase_info
            result = self.shopping_bags[store_id].buy_products(user)
            if not result.success:
                for bag in succeeded_bags:
                    bag.send_back()
                return result
            succeeded_bags.append(self.shopping_bags[store_id])
            sum += result.get_obj().get_val()

        self.purchase_time_passed = False
        if self.timer is not None:
            self.timer.cancel()
        self.start_timer()
        return Response[PrimitiveParsable](
            True,
            obj=PrimitiveParsable(sum),
            msg=f"All purchase details are valid. The overall sum is: {sum}",
        )

    """notice: For now - the bag will be deleted since only regular purchase type enabled!"""

    def delete_products_after_purchase(self, user_name: str = "guest") -> Response[ParsableList]:
        self.timer.cancel()
        self.timer = None
        purchase_cart_details = []
        for store_id in self.shopping_bags.keys():
            purchase_cart_details.append(
                self.shopping_bags[store_id].delete_products_after_purchase(user_name)
            )
            self.shopping_bags.pop(store_id)

        return Response[ParsableList](
            True, ParsableList(purchase_cart_details), msg="Here are the purchase details!"
        )

    """notice: I use a flag that marks the time passed for the purchase"""

    def send_back(self):
        self.purchase_time_passed = True
        for bag in self.shopping_bags:
            bag.send_back()

    def start_timer(self):
        self.timer = Timer(self.INTERVAL_TIME, self.send_back)
        self.timer.start()
