import datetime

from Backend.Domain.TradingSystem.Interfaces.IPurchaseDetails import IPurchaseDetails
from Backend.response import Response


class PurchaseDetails(IPurchaseDetails):
    def __init__(self, user_name: str, products: list, date: datetime):
        self.user_name = user_name
        self.products = products
        self.date = date

    def show_details(self) -> Response:
        return Response[self](True, "Purchase Details")
