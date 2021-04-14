from .Adapters.cashing_adapter import CashingAdapter
from .Adapters.supply_adapter import SupplyAdapter
from Backend.response import Response


class PaymentManager:

    def __init__(self, outside_cashing, outside_supply):
        self.cashing_adapter = CashingAdapter(outside_cashing)
        self.supply_adapter = SupplyAdapter(outside_supply)

    def pay(self, price, payment_details, product_ids_to_quantity, address):
        try:
            payment_response = self.cashing_adapter.pay(price, payment_details)
        except:
            return Response(success=False, msg="Something went wrong with Outside Cashing")
        if payment_response.success:
            try:
                supply_response = self.supply_adapter.deliver(product_ids_to_quantity, address)
                if not supply_response.success:
                    self.rollback(price, payment_details)
                return supply_response
            except:  # for any error occurs:
                self.rollback(price, payment_details)
                return Response(success=False, msg="Something went wrong with Outside Supplyment")
        else:
            return payment_response

    def rollback(self, price, payment_details):
        return self.cashing_adapter.pay(-price, payment_details)

    # test function:
    def get_balance(self, payment_details):
        return self.cashing_adapter.get_balance(payment_details)
