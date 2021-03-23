from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem import ShoppingCart


class IShoppingCart(metaclass=ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'add_shopping_bag') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'remove_shopping_bag') and
                callable(subclass.extract_text) and
                hasattr(subclass, 'add_product') and
                callable(subclass.extract_text) and
                hasattr(subclass, 'add_product') and
                callable(subclass.extract_text) or
                NotImplemented)

    @abstractmethod
    def add_shopping_bag(self, store_id: str) -> None:
        """Add new shopping bag of a store into the shopping cart"""
        raise NotImplementedError

    @abstractmethod
    def remove_shopping_bag(self, store_id: str) -> None:
        """Remove an existing shopping bag from the shopping cart"""
        raise NotImplementedError

    @abstractmethod
    def remove_shopping_bag(self, store_id: str) -> None:
        """Remove an existing shopping bag from the shopping cart"""
        raise NotImplementedError

    @abstractmethod
    def add_product(self, store_id: str, product_id: str, quantity: int) -> None:
        """Add a product from a specified store with specified quantity"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, store_id: str, product_id: str, quantity: int) -> None:
        """Remove a product from a specified store with specified quantity"""
        raise NotImplementedError

    @abstractmethod
    def show_cart(self):
        """show the cart of the user
            todo: Think about the return type"""
        raise NotImplementedError

    @abstractmethod
    def show_bag(self, store_id: str):
        """show the cart of the user
            todo: Think about the return type"""
        raise NotImplementedError

    @abstractmethod
    def buy_products(self, products_info) -> None:
        """buy transaction,
                    todo: Think about the type of products_info"""
        raise NotImplementedError


