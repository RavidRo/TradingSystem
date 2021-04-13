from ..OutsideSystems.outside_cashing import OutsideCashing
from Backend.response import Response


class CashingAdapter:

    def __init__(self, outside_system, is_using_stub_system):
        self.outside_cashing = outside_system
        self.is_using_stub_system = is_using_stub_system

    def pay(self, price, payment_info):
        # Temporal implementation, will be change with the real implementation of OutsideCashing
        # Assuming outside cashing returns boolean, wrapping with response to include message later.
        # TODO: maybe to encrypt the payment info before send it to the outside system.
        answer = self.outside_cashing.pay(price, payment_info)
        if self.is_using_stub_system:
            return answer
        return Response(success=answer)
