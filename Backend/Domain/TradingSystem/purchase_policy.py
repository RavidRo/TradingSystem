
from Backend.response import Response, PrimitiveParsable


class PurchasePolicy:
    def __init__(self):
        pass


class DefaultPurchasePolicy(PurchasePolicy):
    def __init__(self):
        super().__init__()

    def checkPolicy(self, purchase_type) -> Response:
        return Response(True, msg="purchase type is approved by the policy")