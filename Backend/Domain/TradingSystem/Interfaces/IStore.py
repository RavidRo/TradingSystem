from abc import ABC, abstractmethod


class IStore(metaclass=ABC):

    @abstractmethod
    def __init__(self, store_info):
        """Create a new store with it's specified info"""
        raise NotImplementedError

    """2.5"""
    @abstractmethod
    def show_store_data(self):
        """A query for the store's data"""
        raise NotImplementedError

    """4.1"""
    @abstractmethod
    def add_product(self, product_info, quantity: int):
        """Add product with specified quantity to the store"""
        raise NotImplementedError

    @abstractmethod
    def remove_product(self, product_id: str):
        """Remove a product from the store"""
        raise NotImplementedError

    @abstractmethod
    def change_product_qunatity(self, product_id: str, quantity: int):
        """Change product's quantity"""
        raise NotImplementedError

    @abstractmethod
    def edit_product_details(self, product_info):
        """Edit product's details with received product_info"""
        raise NotImplementedError

    """4.9"""
    def get_personnel_info(self):
        "Query for the store's personnel info"
        raise NotImplementedError

    """4.11"""
    @abstractmethod
    def get_purchases_history(self):
        """Query for store's purchases history"""
        raise NotImplementedError



