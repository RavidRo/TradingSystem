from Backend.response import Response


class PurchasePolicy:
    def __init__(self):
        pass


class DefaultPurchasePolicy(PurchasePolicy):
    def __init__(self):
        super().__init__()
        self.__purchase_rules = None

    """
    list_of_rules_details: list of jsons of relevant details
    """
    def add_purchase_rule(self, list_of_rules_details: list ,component_to_combine_with_id: str,):
        pass

    def remove_purchase_rule(self):
        pass

    def get_purchase_rules(self):
        return self.__purchase_rules

    def checkPolicy(self, purchase_type) -> Response:
        return Response(True, msg="purchase type is approved by the policy")