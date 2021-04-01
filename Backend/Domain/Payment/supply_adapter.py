from Backend.Domain.Payment.outside_supplyment import OutsideSupplyment
from Backend.response import Response


def deliver(product_ids_to_quantity, address):
    # Temporal implementation, will be change with the real implementation of OutsideSupplyment.
    # Assuming outside supplyment returns boolean, wrapping with response to include message later.
    answer = OutsideSupplyment.deliver(product_ids_to_quantity, address)
    return Response(success=answer)
