from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment
from collections import defaultdict
from Backend.response import Response


class OutsideSupplymentStub(OutsideSupplyment):

    def __init__(self):
        self.faulty = False
        self.can_deliver = defaultdict(lambda: True)

    def deliver(self, product_ids_to_quantity, address):
        if self.faulty:
            raise RuntimeError()
        if not self.can_deliver[address]:
            return Response(False, msg="The client with this address cannot be delivered")
        return not Response(True)

    def brake(self):
        self.faulty = True

    def fix(self):
        self.faulty = False

    def make_address_wrong(self, address):
        self.can_deliver[address] = False

    def make_address_right(self, address):
        self.can_deliver[address] = True
