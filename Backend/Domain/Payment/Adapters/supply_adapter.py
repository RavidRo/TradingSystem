from ..OutsideSystems.outside_supplyment import OutsideSupplyment
from Backend.response import Response


class SupplyAdapter:

    def __init__(self, outside_system):
        self.outside_supplyment = outside_system

    def deliver(self, product_ids_to_quantity, address):
        # Temporal implementation, will be change with the real implementation of OutsideSupplyment.
        # Assuming outside supplyment returns boolean, wrapping with response to include message later.
        answer = self.outside_supplyment.deliver(product_ids_to_quantity, address)
        if isinstance(answer, Response):        # I wanted for test purposes to return Response, and I can't trust real outside system to return Response
            return answer
        return Response(success=answer)
