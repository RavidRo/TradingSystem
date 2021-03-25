from abc import ABC, abstractmethod


class IPurchaseDetails(metaclass=ABC):

    @abstractmethod
    def __init__(self, purchase_info):
        """Create a purchase_details object"""
        raise NotImplementedError

    @abstractmethod
    def show_details(self):
        """A query for the purchse details"""
        raise NotImplementedError
