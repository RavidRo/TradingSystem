from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseLeaf
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import AndCompositePurchaseRule, \
    OrCompositePurchaseRule, ConditioningCompositePurchaseRule
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_leaves import ConcreteLeaf
from Backend.response import Response


class PurchasePolicy:
    def __init__(self):
        pass




class DefaultPurchasePolicy(PurchasePolicy):

    def __init__(self):
        super().__init__()
        self.__id = 0
        # the root will be always an AndComposite
        self.__purchase_rules = AndCompositePurchaseRule(self.generate_id())


    def generate_id(self) -> str:
        self.__id+=1
        return str(self.__id)

    """
    rule_details json of relevant details.
    Options: 
        simple rule - {context:
                        {object: _
                         object_identifier: _
                        }
                       comparator: _
                       constraint: _
                      }
        complex rule - {logic_type: conditional/or/and
                        }
    """

    def add_purchase_rule(self, rule_details: dict, rule_type: str, parent_id: str) -> Response[None]:
        if rule_type == "simple":
            simple_rule = ConcreteLeaf(rule_details)
            return self.__purchase_rules.add(simple_rule, parent_id)

        elif rule_type == "complex":
            logic_type = rule_details['logic_type']
            if logic_type == "or":
                return self.__purchase_rules.add(OrCompositePurchaseRule(self.generate_id()), parent_id)

            elif logic_type == "and":
                return self.__purchase_rules.add(AndCompositePurchaseRule(self.generate_id()), parent_id)

            elif logic_type == "conditional":
                return self.__purchase_rules.add(ConditioningCompositePurchaseRule(self.generate_id()), parent_id)

            else:
                return Response(False, msg=f"invalid logic type: {logic_type}")

        else:
            return Response(False, msg=f"invalid rule type: {rule_type}")


    def remove_purchase_rule(self):
        pass

    def get_purchase_rules(self):
        return self.__purchase_rules

    def checkPolicy(self, purchase_type) -> Response:
        return Response(True, msg="purchase type is approved by the policy")

