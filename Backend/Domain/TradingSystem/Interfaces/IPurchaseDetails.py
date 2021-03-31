import datetime
from abc import ABC, abstractmethod

from Backend.response import Response


class IPurchaseDetails(metaclass=ABC):

    @abstractmethod
    def __init__(self, user_name: str, products: list, date: datetime):
        """Create a purchase_details object"""
        raise NotImplementedError
