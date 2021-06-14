from .Adapters.cashing_adapter import CashingAdapter
from .Adapters.supply_adapter import SupplyAdapter
from Backend.response import Response
from Backend.Service.logs import critical


class PaymentManager:
    def __init__(self):
        self.__cashing_adapter = CashingAdapter()
        self.__supply_adapter = SupplyAdapter()

    def pay(self, price, payment_details, product_ids_to_quantity, address):
        try:
            payment_response = self.__cashing_adapter.pay(price, payment_details)
        except Exception as e:
            critical(e)
            return Response(success=False, msg="Something went wrong with Outside Cashing")
        if payment_response.success:
            try:
                transaction_id = payment_response.get_obj()
                supply_response = self.__supply_adapter.deliver(product_ids_to_quantity, address)
                if not supply_response.success:
                    self.__rollback(transaction_id)
                    return supply_response
                return Response(True, [payment_response.get_obj(), supply_response.get_obj()])
            except Exception as e:
                critical(e)
                self.__rollback(transaction_id)
                return Response(success=False, msg="Something went wrong with Outside Supplyment")
        else:
            return payment_response

    def __rollback(self, transaction_id):
        return self.__cashing_adapter.cancel_payment(transaction_id)

    def rollback(self, transaction_id, delivery_id):
        response = self.__rollback(transaction_id)
        if not response.succeeded():
            return response
        response2 = self.__supply_adapter(delivery_id)
        return response2
