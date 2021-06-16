
from Backend.Domain.TradingSystem.offer import Offer
from Backend.Domain.TradingSystem.Interfaces.Subscriber import Subscriber
import uuid
from Backend.DataBase.database import db_fail_response
from Backend.Domain.Notifications.Publisher import Publisher
from Backend.response import PrimitiveParsable, Response, ParsableList, Parsable
from Backend.Domain.TradingSystem.product import Product
from Backend.Service.DataObjects.store_data import StoreData
from Backend.rw_lock import ReadWriteLock


class Store(Parsable, Subscriber):
    from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
    from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails

    def __init__(self, store_name: str):
        from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
        """Create a new store with it's specified info"""
        self.__id = self.id_generator()
        self.__name = store_name
        self._products_to_quantities: dict[str, tuple[Product, int]] = {}
        self.__responsibility = None
        self.__responsibility_id = None
        self.__discount_policy = None
        self.__purchase_policy = None
        self.__purchase_policy_root_id = None
        self.__discount_policy_root_id = None
        self.__purchase_history = []
        self._products_lock = ReadWriteLock()
        self.__history_lock = ReadWriteLock()
        self.__publisher: Publisher = Publisher()
        from Backend.DataBase.Handlers.store_handler import StoreHandler
        self.__store_handler = StoreHandler.get_instance()

    def notify(self, message: str) -> bool:
        return self.__publisher.notify_all(message)

    def get_discount_policy(self):
        return self.__discount_policy

    def create_purchase_rules_root(self):
        from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import \
            AndCompositePurchaseRule
        from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy
        root_rule = AndCompositePurchaseRule()
        res = self.__store_handler.save_purchase_rule(root_rule)
        if not res.succeeded():
            return db_fail_response
        self.__purchase_policy = DefaultPurchasePolicy(root_rule)
        self.__purchase_policy_root_id = self.__purchase_policy.get_root_id()
        return Response(True)

    def create_discounts_rules_root(self):
        from Backend.Domain.TradingSystem.TypesPolicies.discounts import AddCompositeDiscount
        from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
        root_rule = AddCompositeDiscount()
        res = self.__store_handler.save_discount_rule(root_rule)
        if not res.succeeded():
            return db_fail_response
        res_condition = root_rule.create_condition_policy()
        if not res_condition.succeeded():
            return db_fail_response
        self.__discount_policy = DefaultDiscountPolicy(root_rule)
        self.__discount_policy_root_id = self.__discount_policy.get_root_id()
        return Response(True)

    def set_root_purchase_rule(self, root_rule):
        from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy
        self.__purchase_policy = DefaultPurchasePolicy(root_rule)

    def set_root_discounts_rule(self, root_rule):
        from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
        self.__discount_policy = DefaultDiscountPolicy(root_rule)

    def set_products(self, products_to_quantities: dict[str, tuple[Product, int]]):
        self._products_to_quantities = products_to_quantities

    def get_purchase_policy_root_id(self):
        return self.__purchase_policy_root_id

    def get_discounts_policy_root_id(self):
        return self.__discount_policy_root_id

    def init_fields(self):
        from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
        from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import PurchasePolicy
        from Backend.DataBase.Handlers.store_handler import StoreHandler
        self._products_lock = ReadWriteLock()
        self.__history_lock = ReadWriteLock()
        self.__publisher: Publisher = Publisher()
        self.__store_handler = StoreHandler.get_instance()
        self.__responsibility = None
        self.__discount_policy = None
        self.__purchase_policy = None

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

    def unsubscribe(self, subscriber):
        self.__publisher.remove_subscriber(subscriber)

    def get_products(self) -> Response[ParsableList[Product]]:
        self._products_lock.acquire_read()
        products = [product for product, _ in self._products_to_quantities.values()]
        self._products_lock.release_read()
        return Response(True, ParsableList(products))

    def get_name(self):
        return self.__name

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

    """checks need to be made:
       ----------------------
       1. product_name != ""
       2. quantity >= 0
       3. price >= 0
       4. a product with product_name exists"""

    def add_product(
        self,
        product_name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str] = None,
    ) -> Response[str]:
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

        product = Product(
            product_name=product_name, category=category, price=price, keywords=keywords
        )
        product_id = product.get_id()

        """database saving"""
        self.__store_handler.add_product(self, product, quantity)
        res = self.__store_handler.commit_changes()
        if not res.succeeded():
            self._products_lock.release_write()
            return db_fail_response

        self._products_to_quantities[product_id] = (product, quantity)
        self._products_lock.release_write()
        return Response(True, product_id, msg=f"The product {product_name} successfully added")

    """checks need to be made:
       ----------------------
       1. a product with product_id exists"""

    def remove_product(self, product_id: str) -> Response[PrimitiveParsable[int]]:
        self._products_lock.acquire_write()
        value = self._products_to_quantities.get(product_id)
        if value is None:
            self._products_lock.release_write()
            return Response(False, msg="The product " + product_id + "is already not in the inventory!")
        """database saving"""
        self.__store_handler.remove_product(value[0])
        res = self.__store_handler.commit_changes()
        if not res.succeeded():
            self._products_lock.release_write()
            return db_fail_response
        self._products_to_quantities.pop(product_id, None)
        self._products_lock.release_write()
        return Response(
            True,
            obj=PrimitiveParsable(value[1]),
            msg="Successfully removed product with product id: " + str(product_id),
        )

    """checks need to be made:
       ----------------------
       1. price > 0
       2. a product with product_id exists"""

    def edit_product_details(
        self,
        product_id: str,
        product_name: str = None,
        category: str = None,
        price: float = None,
        keywords: list[str] = None,
    ) -> Response[None]:
        self._products_lock.acquire_write()
        if product_id not in self._products_to_quantities:
            self._products_lock.release_write()
            return Response(False, msg="No such product in the store")

        response = self._products_to_quantities[product_id][0].edit_product_details(
            product_name, category, price, keywords
        )
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
            """database saving"""
            self.__store_handler.update_product_quantity(self, self._products_to_quantities[product_id][0], quantity)
            res = self.__store_handler.commit_changes()
            if not res.succeeded():
                self._products_lock.release_write()
                return db_fail_response
            new_product_quantity = (self._products_to_quantities[product_id][0], quantity)
            self._products_to_quantities[product_id] = new_product_quantity
            prod_name = self._products_to_quantities[product_id][0].get_name()
            self._products_lock.release_write()
            return Response(True, msg=f"Successfully updated product {prod_name} 's quantity")
        self._products_lock.release_write()
        return Response(False, msg=f"The product with id: {product_id} isn't in the inventory!")

    def add_discount(self, discount_data: dict, exist_id: str, condition_type: str = None):
        return self.__discount_policy.add_discount(discount_data, exist_id, condition_type)

    def move_discount(self, src_id: str, dest_id: str):
        return self.__discount_policy.move_discount(src_id, dest_id)

    def get_discounts(self):
        return self.__discount_policy.get_discounts()

    def remove_discount(self, discount_id: str):
        return self.__discount_policy.remove_discount(discount_id)

    def edit_simple_discount(
        self, discount_id: str, percentage: float = None, context: dict = None, duration=None
    ):
        return self.__discount_policy.edit_simple_discount(
            discount_id, percentage, context, duration
        )

    def edit_complex_discount(
        self, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        return self.__discount_policy.edit_complex_discount(
            discount_id, complex_type, decision_rule
        )

    def get_personnel_info(self) -> Response[Responsibility]:
        from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility

        if self.__responsibility is None:
            return Response(False, msg="The store doesn't have assigned personnel")
        return Response[Responsibility](True, self.__responsibility, msg="Personnel info")

    # def get_personnel_info(self) -> Response[Responsibility]:
    #     from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
    #
    #     if self.__responsibility is None:
    #         res_id = self.get_res_id()
    #         res = self.__store_handler.load_store_founder(res_id, self, )
    #         if res.succeeded():
    #             self.__responsibility = res.get_obj()
    #             return Response[Responsibility](True, self.__responsibility, msg="Personnel info")
    #
    #     return Response(False, msg="The store doesn't have assigned personnel")

    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        self.__history_lock.acquire_read()
        history = self.__purchase_history
        self.__history_lock.release_read()
        return Response[ParsableList](True, ParsableList(history), msg="Purchase history")

    def update_store_history(self, purchase_details: PurchaseDetails):
        self.__history_lock.acquire_write()
        self.__purchase_history.append(purchase_details)
        self.__history_lock.release_write()
        message = "A purchase has been made:\n" + str(purchase_details.__dict__)
        self.__publisher.notify_all(message)

    @staticmethod
    def id_generator() -> str:
        return str(uuid.uuid4())

    def get_id(self) -> str:
        return self.__id

    def set_responsibility(self, responsibility: Responsibility):
        self.__responsibility = responsibility
        self.__responsibility_id = responsibility.get_dal_responsibility_id()

    def save(self):
        return self.__store_handler.save(self)

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
        self.__store_handler.rollback_changes()
        for prod_id, (product, quantity) in products_to_quantities.items():
            if self._products_to_quantities.get(prod_id) is None:
                self._products_to_quantities.update({prod_id: (product, quantity)})
            else:
                self._products_to_quantities[prod_id] = (
                    self._products_to_quantities[prod_id][0],
                    self._products_to_quantities[prod_id][1] + quantity,
                )
        self._products_lock.release_write()

    # This function checks for available products
    def check_and_acquire_available_products(self, products_to_quantities: dict) -> Response[None]:
        acquired_product_ids_to_quantities = {}
        self._products_lock.acquire_write()
        for prod_id, (prod, quantity) in products_to_quantities.items():
            prod_to_current_quantity = self._products_to_quantities.get(prod_id)
            if prod_to_current_quantity is None:
                self.__restore_products(acquired_product_ids_to_quantities)
                self._products_lock.release_write()
                return Response(
                    False,
                    msg=f"The product with id: {prod_id} doesn't exist in the inventory of the store",
                )

            elif prod_to_current_quantity[1] < quantity:
                self.__restore_products(acquired_product_ids_to_quantities)
                self._products_lock.release_write()
                return Response(
                    False,
                    msg=f"The store has less than {quantity} of product with id: {prod_id} left",
                )

            current_quantity = self._products_to_quantities.get(prod_id)[1]
            if current_quantity == quantity:
                self.__store_handler.remove_product(prod)
                self._products_to_quantities.pop(prod_id)
            else:
                self.__store_handler.update_product_quantity(self, prod, current_quantity - quantity)
                self._products_to_quantities[prod_id] = (prod, current_quantity - quantity)

            acquired_product_ids_to_quantities[prod_id] = quantity

        self._products_lock.release_write()
        return Response(True, msg="All products are available")

    def __restore_products(self, acquires_product_ids_to_quantities: dict):
        self.__store_handler.rollback_changes()
        for product_id, quantity in acquires_product_ids_to_quantities.items():
            prod, current_quantity = self._products_to_quantities.get(product_id)
            self._products_to_quantities[product_id] = (prod, current_quantity + quantity)

    # this will be added in the future - maybe I will apply Default Policy for now
    def check_purchase(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        return self.__purchase_policy.checkPolicy(products_to_quantities, user_age)

    def apply_discounts(self, product_to_quantity: dict, user_age: int, username="Guest"):

        non_discount_prices = [
            prod.get_offered_price(username) * quantity
            for _, (prod, quantity) in product_to_quantity.items()
        ]
        total_discount = self.__discount_policy.applyDiscount(
            products_to_quantities=product_to_quantity, user_age=user_age, username=username
        )
        final_price = sum(non_discount_prices) - total_discount
        return final_price if final_price >= 0 else 0

    def clear_offers(self, product_ids: list[str], username):
        for product_id in product_ids:
            product = self._products_to_quantities[product_id][0]
            product.clear_offers(username)

    def get_product(self, product_id: str):
        self._products_lock.acquire_read()
        product_to_quantity = self._products_to_quantities.get(product_id)
        if product_to_quantity is None:
            self._products_lock.release_read()
            return None
        prod = self._products_to_quantities.get(product_id)[0]
        self._products_lock.release_read()
        return prod

    def product_exists(self, product_id):
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

    def add_purchase_rule(self, rule_details: dict, rule_type: str, parent_id: str, clause: str = None, discount_id=None,):
        if discount_id is not None:
            discount = self.__discount_policy.get_discount_by_id(discount_id)
            if discount is not None:
                return discount.get_conditions_policy().add_purchase_rule(
                    rule_details, rule_type, parent_id, clause
                )
            else:
                return Response(False, msg=f"There is no discount with discount id{discount_id}")
        return self.__purchase_policy.add_purchase_rule(rule_details, rule_type, parent_id, clause)

    def remove_purchase_rule(self, rule_id: str, discount_id=None):
        if discount_id is not None:
            discount = self.__discount_policy.get_discount_by_id(discount_id)
            if discount is not None:
                return discount.get_conditions_policy().remove_purchase_rule(rule_id)
            else:
                return Response(False, msg=f"There is no discount with discount id{discount_id}")
        return self.__purchase_policy.remove_purchase_rule(rule_id)

    def edit_purchase_rule(
        self, rule_details: dict, rule_id: str, rule_type: str, discount_id=None
    ):
        if discount_id is not None:
            discount = self.__discount_policy.get_discount_by_id(discount_id)
            if discount is not None:
                return discount.get_conditions_policy().edit_purchase_rule(
                    rule_details, rule_id, rule_type
                )
            else:
                return Response(False, msg=f"There is no discount with discount id{discount_id}")
        return self.__purchase_policy.edit_purchase_rule(rule_details, rule_id, rule_type)

    def move_purchase_rule(self, rule_id: str, new_parent_id: str, discount_id=None):
        if discount_id is not None:
            discount = self.__discount_policy.get_discount_by_id(discount_id)
            if discount is not None:
                return discount.get_conditions_policy().move_purchase_rule(rule_id, new_parent_id)
            else:
                return Response(False, msg=f"There is no discount with discount id{discount_id}")
        return self.__purchase_policy.move_purchase_rule(rule_id, new_parent_id)

    def get_purchase_policy(self):
        return self.__purchase_policy.get_purchase_rules()

    def parse_purchase_policy(self):
        return self.__purchase_policy.parse()

    # Offers
    # ======================

    def get_store_offers(self) -> Response[ParsableList[Offer]]:
        product_offers = [
            product.get_offers() for product, _ in self._products_to_quantities.values()
        ]
        # Flattening the list
        offers = [offer for sublist in product_offers for offer in sublist]
        return Response(True, ParsableList(offers))

    def suggest_counter_offer(self, product_id, offer_id, price) -> Response[None]:
        if product_id not in self._products_to_quantities:
            return Response(False, msg=f"The product with id: {product_id} isn't in the inventory!")

        product = self._products_to_quantities[product_id][0]
        return product.suggest_counter_offer(offer_id, price)

    def approve_user_offer(self, product_id, offer_id, username) -> Response[None]:
        if product_id not in self._products_to_quantities:
            return Response(False, msg=f"The product with id: {product_id} isn't in the inventory!")

        product = self._products_to_quantities[product_id][0]
        return product.approve_user_offer(offer_id, username)

    def reject_user_offer(self, product_id, offer_id) -> Response[None]:
        if product_id not in self._products_to_quantities:
            return Response(False, msg=f"The product with id: {product_id} isn't in the inventory!")

        product = self._products_to_quantities[product_id][0]
        return product.reject_user_offer(offer_id)

    def get_owners_names(self):
        return self.__responsibility.get_owners_names()

    def remove_owner(self, username) -> None:
        for product_id in self._products_to_quantities:
            self._products_to_quantities[product_id][0].remove_owner(username)

    def add_owner(self, username) -> None:
        for product_id in self._products_to_quantities:
            self._products_to_quantities[product_id][0].add_owner(username)


    def get_res_id(self):
        return self.__responsibility_id

    def get_name(self):
        return self.__name