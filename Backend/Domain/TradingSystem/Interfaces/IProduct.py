from abc import ABC, abstractmethod


class IProduct(metaclass=ABC):

    @abstractmethod
    def __init__(self, product_info):
        """Create a new store with it's specified info"""
        raise NotImplementedError

    @abstractmethod
    def show_product_data(self):
        """A query for the product's data"""
        raise NotImplementedError

    @abstractmethod
    def edit_product_details(self, product_info):
        """Edit product's details with received product_info"""
        raise NotImplementedError