from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem.IUser import IUser
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, ParsableList, Parsable


class IShoppingBag(metaclass=ABC, Parsable):

    @abstractmethod
    def add_product(self, product_id: str, quantity: int) -> Response[None]:
        """Add a product to the bag with specified quantity"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, product_id: str) -> Response[None]:
        """Remove a product from the bag"""
        raise NotImplementedError

    @abstractmethod
    def buy_products(self, user_info: IUser, products_info={}) -> Response[None]:
        """buy transaction"""
        raise NotImplementedError

    @abstractmethod
    def change_product_qunatity(self, product_id: str, new_amount: int) -> Response[None]:
        """ Change product's quantity (add or remove) - new amount overrides the current amount"""
        raise NotImplementedError

    @abstractmethod
    def delete_products_after_purchase(self, user_name: str) -> PurchaseDetails:
        """delete products which successfully been purchased"""
        raise NotImplementedError

