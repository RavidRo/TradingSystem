from Backend.Domain.TradingSystem import StoresManager
from Backend.Domain.TradingSystem.Interfaces import IShoppingBag, IPurchaseDetails
from Backend.Domain.TradingSystem.Interfaces.IShoppingCart import IShoppingCart
from Backend.Domain.TradingSystem.ShoppingBag import ShoppingBag
from Backend.response import Response, PrimitiveParsable, Parsable, ParsableList


class ShoppingCart(IShoppingCart, Parsable):

    def __init__(self):
        self.stores_manager = StoresManager.get_instance()
        self.shopping_bags = dict()

    def parse(self):
        pass

    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        if quantity <= 0:
            return Response(False, msg="Product's quantity must be positive!")

        # todo: check if store with store id exists + check if product with product id and quantity is within the store
        check_existence_response = self.stores_manager.check_existence(store_id, product_id, quantity)
        if not check_existence_response.sucess:
            return check_existence_response

        for bag in self.shopping_bags:
            if bag.get_store_ID() == store_id:
                if bag.product_in_bag(product_id):
                    return Response(False,
                                    msg="A product with id: " + str(product_id) + " already exists in the store's bag")
                bag.add_product(product_id, quantity)
                return self.success_adding_product(store_id, product_id)

        # no bag for store with store_id
        new_bag = ShoppingBag(self.stores_manager.get_store(store_id))
        self.shopping_bags.update({store_id, new_bag})
        new_bag.add_product(product_id, quantity)
        return self.success_adding_product(store_id, product_id)

    def success_adding_product(self, store_id, product_id):
        return Response(True, msg="Successfully added product with id: " + str(product_id) + "to cart")

    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(False, msg="There is no existing bag for store with store id: " + str(store_id))
        if bag.product_in_bag(product_id):
            bag.remove_product(product_id)
            return Response(True, msg="Successfully removed product with id: " + str(product_id) + " from cart")
        else:
            return Response(False, msg="There is no product with id: " + str(product_id) +
                                       "in the bag of store with id: " + str(store_id))

    def change_product_qunatity(self, store_id: str, product_id: str, new_amount: int) -> Response[None]:
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(False, msg="There is no existing bag for store with store id: " + str(store_id))
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")

        check_existence_response = self.stores_manager.check_existence(store_id, product_id, new_amount)
        if not check_existence_response.sucess:
            return check_existence_response

        if bag.product_in_bag(product_id):
            return bag.change_product_qunatity(product_id, new_amount)
        else:
            return Response(False, msg="There is no product with id: " + str(product_id) +
                                       "in the bag of store with id: " + str(store_id))

    # products_purchase_info -a dict between store_id to list of tuples tuple (product_id to purchase_type)
    def buy_products(self, user, products_purchase_info={}) -> Response[PrimitiveParsable]:
        sum = 0
        for store_id in products_purchase_info.keys():
            result = self.shopping_bags[store_id].buy_products(products_purchase_info[store_id], user)
            if not result.success:
                return result
            sum += result.get_obj().get_val()
        return Response[PrimitiveParsable(sum)](True,
                                                msg="All purchase details are valid. The overall sum is: " + str(sum))

    def delete_products_after_purchase(self, user_name="guest") -> Response[ParsableList]:
        purchase_cart_details = []
        for store_id in self.shopping_bags.keys():
            purchase_cart_details.append(self.shopping_bags[store_id].delete_products_after_purchase(user_name))
            # For now - the bag will be deleted since only regular purchase type enabled
            self.shopping_bags.pop(store_id)

        return Response[ParsableList](True, ParsableList(purchase_cart_details), msg="Here are the purchase details!")

    def show_bag(self, store_id: str) -> Response[IShoppingBag]:
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(False, msg="No bag available for this store_id")
        return Response[ShoppingBag](True, bag, msg="Shopping bag")
