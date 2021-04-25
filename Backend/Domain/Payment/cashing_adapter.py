from Backend.Domain.Payment.outside_cashing import OutsideCashing
from Backend.response import Response


def pay(price, payment_info):
    # Temporal implementation, will be change with the real implementation of OutsideCashing
    # Assuming outside cashing returns boolean, wrapping with response to include message later.
    answer = OutsideCashing.pay(price, payment_info)
    return Response(success=answer)
