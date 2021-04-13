from ..OutsideSystems.outside_supplyment import OutsideSupplyment
from Backend.response import Response


class SupplyAdapter:

    def __init__(self, outside_system, is_using_stub_system):
        self.outside_supplyment = outside_system
        self.is_using_stub_system = is_using_stub_system

    def deliver(self, product_ids_to_quantity, address):
        # Temporal implementation, will be change with the real implementation of OutsideSupplyment.
        # Assuming outside supplyment returns boolean, wrapping with response to include message later.
        answer = self.outside_supplyment.deliver(product_ids_to_quantity, address)
        if self.is_using_stub_system:
            return answer
        return Response(success=answer)
