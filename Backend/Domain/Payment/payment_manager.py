from .Adapters.cashing_adapter import CashingAdapter
from .Adapters.supply_adapter import SupplyAdapter
from Backend.response import Response
from OutsideSystems.outside_supplyment import OutsideSupplyment
from OutsideSystems.outside_cashing import OutsideCashing


class PaymentManager:

    def __init__(self, is_using_stub_systems):
        self.cashing_adapter = CashingAdapter(OutsideCashing(), is_using_stub_systems)
        self.supply_adapter = SupplyAdapter(OutsideSupplyment, is_using_stub_systems)

    def pay(self, price, payment_details, product_ids_to_quantity, address):
        payment_response = self.cashing_adapter.pay(price, payment_details)
        if payment_response.success:
            try:
                supply_response = self.supply_adapter.deliver(product_ids_to_quantity, address)
                if supply_response.success:
                    return Response(success=True)
                else:
                    self.rollback(price, payment_details)
                    return Response(success=False, msg="Something went wrong with the deliver")
            except:  # for any error occurs:
                self.rollback(price, payment_details)
                return Response(success=False, msg="An error occurred during the process")
        else:
            return Response(success=False, msg="Something went wrong with the payment")

    def rollback(self, price, payment_details):
        return self.cashing_adapter.pay(-price, payment_details)
