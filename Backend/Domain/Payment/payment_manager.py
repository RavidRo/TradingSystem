import sys

from .Adapters.cashing_adapter import CashingAdapter
from .Adapters.supply_adapter import SupplyAdapter
from Backend.response import Response


class PaymentManager:

    def __init__(self):
        self.__cashing_adapter = CashingAdapter()
        self.__supply_adapter = SupplyAdapter()

    def pay(self, price, payment_details, product_ids_to_quantity, address):
        try:
            payment_response = self.__cashing_adapter.pay(price, payment_details)
        except:
            return Response(success=False, msg="Something went wrong with Outside Cashing")
        if payment_response.success:
            try:
                supply_response = self.__supply_adapter.deliver(product_ids_to_quantity, address)
                if not supply_response.success:
                    self.__rollback(price, payment_details)
                return supply_response
            except:  # for any error occurs:
                self.__rollback(price, payment_details)
                return Response(success=False, msg="Something went wrong with Outside Supplyment")
        else:
            return payment_response

    def __rollback(self, price, payment_details):
        return self.__cashing_adapter.pay(-price, payment_details)

    # test functions:
    def get_balance(self, payment_details):
        return self.__cashing_adapter.get_balance(payment_details)
