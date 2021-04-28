from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import AndCompositePurchaseRule, \
    OrCompositePurchaseRule, ConditioningCompositePurchaseRule
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.purchase_leaves import ConcreteLeaf
from Backend.Domain.TradingSystem.user import User
from Backend.response import Response


class PurchasePolicy:
    def __init__(self):
        pass


# region data

logic_types = {"or": lambda self: OrCompositePurchaseRule(self.generate_id()),
               "and": lambda self: AndCompositePurchaseRule(self.generate_id()),
               "conditional": lambda self: ConditioningCompositePurchaseRule(self.generate_id())}


# endregion

class DefaultPurchasePolicy(PurchasePolicy):

    def __init__(self):
        super().__init__()
        self.__id = 0
        # the root will be always an AndComposite
        self.__purchase_rules = AndCompositePurchaseRule(self.generate_id())

    def generate_id(self) -> str:
        self.__id += 1
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
    clause - only for conditional - valid values: if/then
    """

    def add_purchase_rule(self, rule_details: dict, rule_type: str, parent_id: str, clause: str= None) -> Response[None]:
        if rule_type == "simple":
            simple_rule = ConcreteLeaf(rule_details, self.generate_id())
            return self.__purchase_rules.add(simple_rule, parent_id, clause)

        elif rule_type == "complex":
            logic_type = rule_details['operator']
            if logic_type in logic_types.keys():
                return self.__purchase_rules.add(logic_types[logic_type](self), parent_id, clause)
            else:
                return Response(False, msg=f"invalid logic type: {logic_type}")
        else:
            return Response(False, msg=f"invalid rule type: {rule_type}")

    def remove_purchase_rule(self, rule_id: str):
        return self.__purchase_rules.remove(rule_id)

    def move_purchase_rule(self, rule_id: str, new_parent_id: str):
        rule_to_move_response = self.__purchase_rules.get_rule(rule_id)
        if not rule_to_move_response.succeeded():
            return rule_to_move_response
        rule_to_move = rule_to_move_response.get_obj()

        new_parent_response = self.__purchase_rules.get_rule(new_parent_id)
        if not new_parent_response.succeeded():
            return new_parent_response
        new_parent = new_parent_response.get_obj()
        check_validity = rule_to_move.check_validity(new_parent_id)
        if not check_validity.succeeded():
            return check_validity
        rule_to_move.parent.children.remove(rule_to_move)
        rule_to_move.parent = new_parent
        new_parent.children.append(rule_to_move)

    """rule_details json of relevant details.
    Options: 
        simple rule - {context:
                        {object: _
                         object_identifier: _
                        }
                       comparator: _
                       constraint: _
                      }
        complex rule - {logic_type: conditional/or/and
                        } """

    def edit_purchase_rule(self, rule_details: dict, rule_id: str, rule_type: str):
        if rule_type == "simple":
            simple_rule = ConcreteLeaf(rule_details, self.generate_id())
            self.__purchase_rules.edit_rule(rule_id, simple_rule)

        elif rule_type == "complex":
            logic_type = rule_details['logic_type']
            if logic_type in logic_types.keys():
                return self.__purchase_rules.edit_rule(rule_id, logic_types[logic_type](self))

            else:
                return Response(False, msg=f"invalid logic type: {logic_type}")

        else:
            return Response(False, msg=f"invalid rule type: {rule_type}")

    def get_purchase_rules(self):
        return self.__purchase_rules

    def checkPolicy(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        return self.__purchase_rules.operation(products_to_quantities, user_age)
