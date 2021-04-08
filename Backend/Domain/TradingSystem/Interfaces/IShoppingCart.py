from abc import ABC, abstractmethod
from Backend.Domain.TradingSystem import IUser
from Backend.response import Response, PrimitiveParsable, Parsable, ParsableList


class IShoppingCart(Parsable):

    @abstractmethod
    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        """Add a product from a specified store with specified quantity"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        """Remove a product from a specified store"""
        raise NotImplementedError

    @abstractmethod
    def change_product_quantity(self, store_id: str, product_id: str, new_amount: int) -> Response[None]:
        """ Change product's quantity (add or remove) - new amount overrides the current amount"""
        raise NotImplementedError

    @abstractmethod
    def buy_products(self, user: IUser, products_purchase_info: dict) -> Response[PrimitiveParsable]:
        """buy transaction"""
        raise NotImplementedError

    @abstractmethod
    def delete_products_after_purchase(self, user_name: str) -> Response[ParsableList]:
        """delete products which successfully been purchased"""
        raise NotImplementedError

