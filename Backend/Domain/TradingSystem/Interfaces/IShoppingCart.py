from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem.Interfaces import IPurchaseDetails, IShoppingBag
from Backend.response import Response


class IShoppingCart(metaclass=ABC):
    # @classmethod
    # def __subclasshook__(cls, subclass):
    #     return (hasattr(subclass, 'add_shopping_bag') and
    #             callable(subclass.load_data_source) and
    #             hasattr(subclass, 'remove_shopping_bag') and
    #             callable(subclass.extract_text) and
    #             hasattr(subclass, 'add_product') and
    #             callable(subclass.extract_text) and
    #             hasattr(subclass, 'add_product') and
    #             callable(subclass.extract_text) and
    #             hasattr(subclass, 'remove_product') and
    #             callable(subclass.extract_text) and
    #             hasattr(subclass, 'show_cart') and
    #             callable(subclass.extract_text) and
    #             hasattr(subclass, 'show_bag') and
    #             callable(subclass.extract_text) and
    #             hasattr(subclass, 'buy_products') and
    #             callable(subclass.extract_text) or
    #             NotImplemented)

    @abstractmethod
    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        """Add a product from a specified store with specified quantity"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        """Remove a product from a specified store"""
        raise NotImplementedError

    @abstractmethod
    # todo: think how to handle the return type since can't return IShoppingCart
    def show_cart(self) -> Response:
        """show the cart of the user"""
        raise NotImplementedError

    @abstractmethod
    def change_product_qunatity(self, store_id: str, product_id: str, new_amount: int) -> Response[None]:
        """ Change product's quantity (add or remove) - new amount overrides the current amount"""
        raise NotImplementedError

    @abstractmethod
    def buy_products(self, products_purchase_info, user) -> Response[None]:
        """buy transaction"""
        raise NotImplementedError

    @abstractmethod
    def delete_products_after_purchase(self) -> Response[IPurchaseDetails]:
        """delete products which successfully been purchased"""
        raise NotImplementedError

    @abstractmethod
    def show_bag(self, store_id: str) -> Response[IShoppingBag]:
        """show a store's bag from the cart
            todo: Think if needed?"""
        raise NotImplementedError


