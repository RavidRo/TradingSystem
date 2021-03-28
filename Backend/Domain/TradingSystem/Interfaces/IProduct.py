from abc import ABC, abstractmethod

from Backend.response import Response, ParsableList


class IProduct(metaclass=ABC):

    @abstractmethod
    def __init__(self, product_name: str, price: float, qunatity: int):
        """Create a new store with it's specified info"""
        raise NotImplementedError

    @abstractmethod
    #todo: think how to handle the return type since can't return IProduct
    def show_product_data(self) -> Response:
        """A query for the product's data"""
        raise NotImplementedError

    @abstractmethod
    def edit_product_details(self, product_name: str, price: float):
        """Edit product's details with received product_info"""
        raise NotImplementedError