from ..OutsideSystems.outside_cashing import OutsideCashing
from Backend.response import Response


class CashingAdapter:

    def __init__(self, outside_system):
        self.outside_cashing = outside_system

    def pay(self, price, payment_info):
        # Temporal implementation, will be change with the real implementation of OutsideCashing
        # Assuming outside cashing returns boolean, wrapping with response to include message later.
        # TODO: maybe to encrypt the payment info before send it to the outside system.
        answer = self.outside_cashing.pay(price, payment_info)
        if isinstance(answer, Response):        # I wanted for test purposes to return Response, and I can't trust real outside system to return Response
            return answer
        return Response(success=answer)

    # test function:
    def get_balance(self, payment_details):
        return self.outside_cashing.get_balance(payment_details)
