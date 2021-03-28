from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem.Interfaces import IProduct
from Backend.response import Response, ParsableList


class IShoppingBag(metaclass=ABC):
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
    def add_product(self, product_id: str, quantity: int) -> Response[None]:
        """Add a product to the bag with specified quantity"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, product_id: str) -> Response[None]:
        """Remove a product from the bag"""
        raise NotImplementedError

    @abstractmethod
    # todo: think how to handle the return type since can't return IShoppingBag
    def show_bag(self) -> Response:
        """show the bag to the user"""
        raise NotImplementedError

    @abstractmethod
    def buy_products(self, products_info, user_info) -> Response[None]:
        """buy transaction"""
        raise NotImplementedError

    @abstractmethod
    def change_product_qunatity(self, product_id: str, new_amount: int) -> Response[None]:
        """ Change product's quantity (add or remove) - new amount overrides the current amount"""
        raise NotImplementedError

    @abstractmethod
    def delete_products_after_purchase(self) -> Response[ParsableList[IProduct]]:
        """delete products which successfully been purchased"""
        raise NotImplementedError

