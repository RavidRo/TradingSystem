from Backend.response import Response
from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment


class SupplyAdapter:

    def __init__(self):
        self.__outside_supplyment = OutsideSupplyment()

    def deliver(self, product_ids_to_quantity, address):
        # Temporal implementation, will be change with the real implementation of OutsideSupplyment.
        # Assuming outside supplyment returns boolean, wrapping with response to include message later.
        answer = self.__outside_supplyment.deliver(product_ids_to_quantity, address)
        return Response(success=answer)
