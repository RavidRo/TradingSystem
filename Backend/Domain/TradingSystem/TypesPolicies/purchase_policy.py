import operator
import threading
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import AndCompositePurchaseRule, \
    OrCompositePurchaseRule, ConditioningCompositePurchaseRule
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_leaf import ProductLeafPurchaseRule, \
    BagLeafPurchaseRule, UserLeafPurchaseRule, CategoryLeafPurchaseRule
from Backend.response import Response


class PurchasePolicy:
    def __init__(self):
        pass


# region data

logic_types = {"or": lambda self: OrCompositePurchaseRule(self.generate_id()),
               "and": lambda self: AndCompositePurchaseRule(self.generate_id()),
               "conditional": lambda self: ConditioningCompositePurchaseRule(self.generate_id())}

leaf_types = {"product": lambda self, leaf_details: ProductLeafPurchaseRule(leaf_details=leaf_details, identifier=self.generate_id()),
              "bag": lambda self, leaf_details: BagLeafPurchaseRule(leaf_details=leaf_details, identifier=self.generate_id()),
              "user": lambda self, leaf_details: UserLeafPurchaseRule(leaf_details=leaf_details, identifier=self.generate_id()),
              "category": lambda self, leaf_details: CategoryLeafPurchaseRule(leaf_details=leaf_details, identifier=self.generate_id()),
              }


objects = ['product', 'user', 'category', 'bag']
objects_with_id = ['category', 'product']
ops = {'great-than': operator.gt,
       'less-than': operator.lt,
       'great-equals': operator.ge,
       'less-equals': operator.le,
       'equals': operator.eq}

# endregion

class DefaultPurchasePolicy(PurchasePolicy):

    def __init__(self):
        super().__init__()
        self.__id = 0
        self.auto_id_lock = threading.Lock()
        # the root will be always an AndComposite
        self.__purchase_rules = AndCompositePurchaseRule(self.generate_id())

    def generate_id(self) -> str:
        with self.auto_id_lock:
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

    def check_keys_in_rule_details(self, keys: list[str], rule_details: dict):
        for key in keys:
            if key not in rule_details.keys():
                return Response(False, msg= f"Missing {key} in details!")
        return Response(True, msg="all keys exist")

    def check_simple_rule_details_validity(self, rule_details: dict) -> Response[None]:
        keys = ['context', 'operator', 'target']
        check_response = self.check_keys_in_rule_details(keys, rule_details)
        if not check_response.succeeded():
            return check_response

        context_dict = rule_details['context']
        if 'obj' not in context_dict:
            return Response(False, msg="Missing object in details!")

        object = context_dict['obj']
        if object not in objects:
            return Response(False, msg=f"Invalid object {object} in details!")

        if object in objects_with_id and 'identifier' not in context_dict:
            return Response(False, msg="Missing identifier in details!")

        if rule_details['operator'] not in ops.keys():
            return Response(False, msg="Invalid operator!")
        return Response(True, msg="No missing keys")

    def check_complex_rule_details_validity(self, rule_details: dict) -> Response[None]:
        if 'operator' not in rule_details.keys():
            return Response(False, msg="Missing type in details!")
        return Response(True, msg="No missing keys")

    def add_purchase_rule(self, rule_details: dict, rule_type: str, parent_id: str, clause: str= None) -> Response[None]:
        if rule_type == "simple":
            response_validity = self.check_simple_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                return response_validity
            leaf_type = rule_details['context']['obj']
            if leaf_type in leaf_types.keys():
                simple_rule = leaf_types[leaf_type](self, rule_details)
                return self.__purchase_rules.add(simple_rule, parent_id, clause)
            else:
                return Response(False, msg=f"invalid simple rule type: {leaf_type}")

        elif rule_type == "complex":
            response_validity = self.check_complex_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                return response_validity
            logic_type = rule_details['operator']
            if logic_type in logic_types.keys():
                return self.__purchase_rules.add(logic_types[logic_type](self), parent_id, clause)
            else:
                return Response(False, msg=f"invalid logic type: {logic_type}")
        else:
            return Response(False, msg=f"invalid rule type: {rule_type}")


    def remove_purchase_rule(self, rule_id: str):
        return self.__purchase_rules.remove(rule_id)

    def move_purchase_rule(self, rule_id: str, new_parent_id: str) -> Response[None]:
        rule_to_move_response = self.__purchase_rules.get_rule(rule_id)
        if not rule_to_move_response.succeeded():
            return Response(False, msg=rule_to_move_response.get_msg())
        rule_to_move = rule_to_move_response.get_obj()

        new_parent_response = self.__purchase_rules.get_rule(new_parent_id)
        if not new_parent_response.succeeded():
            return Response(False, msg=new_parent_response.get_msg())

        new_parent = new_parent_response.get_obj()
        check_validity = rule_to_move.check_validity(new_parent_id)
        if not check_validity.succeeded():
            return check_validity
        rule_to_move.parent.children.remove(rule_to_move)
        rule_to_move.parent = new_parent
        new_parent.children.append(rule_to_move)
        return Response(True, msg="Move succeeded!")

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
            response_validity = self.check_simple_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                return response_validity
            leaf_type = rule_details['context']['obj']
            if leaf_type in leaf_types.keys():
                return self.__purchase_rules.edit_rule(rule_id, leaf_types[leaf_type](self, rule_details))
            else:
                return Response(False, msg=f"invalid simple rule type: {leaf_type}")

        elif rule_type == "complex":
            response_validity = self.check_complex_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                return response_validity
            logic_type = rule_details['operator']
            if logic_type in logic_types.keys():
                return self.__purchase_rules.edit_rule(rule_id, logic_types[logic_type](self))

            else:
                return Response(False, msg=f"invalid logic type: {logic_type}")

        else:
            return Response(False, msg=f"invalid rule type: {rule_type}")

    def get_purchase_rules(self) -> Response[PurchasePolicy]:
        return Response(True, obj=self, msg="Here are the purchase rules")

    def checkPolicy(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        return self.__purchase_rules.operation(products_to_quantities, user_age)

    def parse(self):
        return self.__purchase_rules.parse()
