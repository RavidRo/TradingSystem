import datetime
from abc import ABC, abstractmethod

from Backend.response import Response


class IPurchaseDetails(metaclass=ABC):

    @abstractmethod
    def __init__(self, user_name: str, products: list, date: datetime):
        """Create a purchase_details object"""
        raise NotImplementedError

    @abstractmethod
    # todo: think how to handle the return type since can't return IPurchaseDetails
    def show_details(self) -> Response:
        """A query for the purchse details"""
        raise NotImplementedError
