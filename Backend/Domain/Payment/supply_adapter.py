from Backend.Domain.Payment.outside_supplyment import OutsideSupplyment
from Backend.response import Response


def deliver(products, address):
    # Temporal implementation, will be change with the real implementation of OutsideSupplyment.
    # Assuming outside supplyment returns boolean, wrapping with response to include message later.
    answer = OutsideSupplyment.deliver(products, address)
    return Response(success=answer)
