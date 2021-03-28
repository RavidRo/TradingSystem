from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem.Interfaces import IPurchaseDetails
from Backend.Domain.TradingSystem.Responsibilities import Responsibility
from Backend.response import Response, ParsableList


class IStore(metaclass=ABC):

    @abstractmethod
    def __init__(self, store_info):
        """Create a new store with it's specified info"""
        raise NotImplementedError

    """2.5"""
    @abstractmethod
    # todo: think how to handle the return type since can't return IStore
    def show_store_data(self) -> Response:
        """A query for the store's data"""
        raise NotImplementedError

    """4.1"""
    @abstractmethod
    def add_product(self, product_name: str, price: float, quantity: int) -> Response[None]:
        """Add product with specified quantity to the store"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, product_id: str) -> Response[None]:
        """Remove a product from the store"""
        raise NotImplementedError

    @abstractmethod
    def change_product_qunatity(self, product_id: str, quantity: int) -> Response[None]:
        """Change product's quantity"""
        raise NotImplementedError

    @abstractmethod
    def edit_product_details(self, product_id: str, product_name: str, price: float) -> Response[None]:
        """Edit product's details with received product_info"""
        raise NotImplementedError

    """4.9"""
    @abstractmethod
    def get_personnel_info(self) -> Response[Responsibility]:
        "Query for the store's personnel info"
        raise NotImplementedError

    """4.11"""
    @abstractmethod
    def get_purchases_history(self) -> Response[ParsableList[IPurchaseDetails]]:
        """Query for store's purchases history"""
        raise NotImplementedError



