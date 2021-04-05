from Backend.Domain.TradingSystem import store
from Backend.Domain.TradingSystem.discount_type import DefaultDiscountType
from Backend.Domain.TradingSystem.Interfaces import IPurchasePolicy, IPurchaseType
from Backend.response import Response, PrimitiveParsable


class PurchasePolicy(IPurchasePolicy):
    def __init__(self):
        pass


class DefaultPurchasePolicy(PurchasePolicy):
    def __init__(self):
        pass

    def checkPolicy(self, purchase_type) -> Response:
        return Response(True, msg="purchase type is approved by the policy")