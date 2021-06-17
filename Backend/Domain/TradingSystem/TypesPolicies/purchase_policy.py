import operator
import threading

from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import AndCompositePurchaseRule, \
    OrCompositePurchaseRule, ConditioningCompositePurchaseRule
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_leaf import ProductLeafPurchaseRule, \
    BagLeafPurchaseRule, UserLeafPurchaseRule, CategoryLeafPurchaseRule
from Backend.response import Response
from Backend.rw_lock import ReadWriteLock


class PurchasePolicy:
    def __init__(self):
        pass


# region data

logic_types = {"or": lambda parent: OrCompositePurchaseRule(parent),
               "and": lambda parent: AndCompositePurchaseRule(parent),
               "conditional": lambda parent: ConditioningCompositePurchaseRule(parent)}

leaf_types = {"product": lambda self, leaf_details, parent: ProductLeafPurchaseRule(leaf_details=leaf_details, parent=parent),
              "bag": lambda self, leaf_details, parent: BagLeafPurchaseRule(leaf_details=leaf_details, parent=parent),
              "user": lambda self, leaf_details, parent: UserLeafPurchaseRule(leaf_details=leaf_details, parent=parent),
              "category": lambda self, leaf_details, parent: CategoryLeafPurchaseRule(leaf_details=leaf_details, parent=parent),
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

    def __init__(self, root_rule):
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        super().__init__()
        self.__purchase_rules_handler = PurchaseRulesHandler.get_instance()
        # self.__id = 0
        # the root will be always an AndComposite
        self.__purchase_rules = root_rule
        self.__purchase_rules_lock = None
        self.__purchase_rules_lock = ReadWriteLock()

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
    def get_purchase_rules(self):
        if self.__purchase_rules is None:
            rules_loaded = self.__purchase_rules_handler.load()
            if rules_loaded.succeeded():
                self.__purchase_rules = rules_loaded.get_obj()
                return Response(True, obj=self.__purchase_rules)
            else:
                return db_fail_response
        return Response(True, obj=self.__purchase_rules)

    def check_keys_in_rule_details(self, keys: list[str], rule_details: dict):
        for key in keys:
            if key not in rule_details.keys():
                return Response(False, msg=f"Missing {key} in details!")
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
        self.__purchase_rules_lock.acquire_write()
        parent_rule_res = self.__purchase_rules.get_rule(parent_id)
        if not parent_rule_res.succeeded():
            self.__purchase_rules_lock.release_write()
            return Response(False, msg=f"invalid parent id: {parent_id}")
        parent = parent_rule_res.get_obj()
        if rule_type == "simple":
            response_validity = self.check_simple_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                self.__purchase_rules_lock.release_write()
                return response_validity
            leaf_type = rule_details['context']['obj']
            if leaf_type in leaf_types.keys():
                simple_rule = leaf_types[leaf_type](self, rule_details, parent)
                simple_rule.set_clause(clause)
                add_response = self.__purchase_rules.add(simple_rule, parent_id)

                self.__purchase_rules_lock.release_write()
                return add_response
            else:
                self.__purchase_rules_lock.release_write()
                return Response(False, msg=f"invalid simple rule type: {leaf_type}")

        elif rule_type == "complex":
            response_validity = self.check_complex_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                self.__purchase_rules_lock.release_write()
                return response_validity
            logic_type = rule_details['operator']
            if logic_type in logic_types.keys():
                complex_rule = logic_types[logic_type](parent)
                complex_rule.set_clause(clause)
                add_response = self.__purchase_rules.add(complex_rule, parent_id)
                self.__purchase_rules_lock.release_write()
                return add_response
            else:
                self.__purchase_rules_lock.release_write()
                return Response(False, msg=f"invalid logic type: {logic_type}")
        else:
            self.__purchase_rules_lock.release_write()
            return Response(False, msg=f"invalid rule type: {rule_type}")

    def remove_purchase_rule(self, rule_id: str):
        self.__purchase_rules_lock.acquire_write()
        remove_response = self.__purchase_rules.remove(rule_id)
        self.__purchase_rules_lock.release_write()
        return remove_response

    def move_purchase_rule(self, rule_id: str, new_parent_id: str) -> Response[None]:
        self.__purchase_rules_lock.acquire_write()
        rule_to_move_response = self.__purchase_rules.get_rule(rule_id)
        if not rule_to_move_response.succeeded():
            self.__purchase_rules_lock.release_write()
            return Response(False, msg=rule_to_move_response.get_msg())
        rule_to_move = rule_to_move_response.get_obj()

        new_parent_response = self.__purchase_rules.get_rule(new_parent_id)
        if not new_parent_response.succeeded():
            self.__purchase_rules_lock.release_write()
            return Response(False, msg=new_parent_response.get_msg())

        new_parent = new_parent_response.get_obj()

        check_validity = rule_to_move.check_validity(new_parent_id)
        if not check_validity.succeeded():
            self.__purchase_rules_lock.release_write()
            return check_validity

        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        PurchaseRulesHandler.get_instance().move_rule(rule_to_move, new_parent)
        res = self.__purchase_rules_handler.commit_changes()
        self.__purchase_rules_lock.release_write()
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
        self.__purchase_rules_lock.acquire_write()
        res_rule = self.__purchase_rules.get_rule(rule_id)
        if not res_rule.succeeded():
            self.__purchase_rules_lock.release_write()
            return res_rule

        parent = res_rule.get_obj().parent

        if rule_type == "simple":
            response_validity = self.check_simple_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                self.__purchase_rules_lock.release_write()
                return response_validity
            leaf_type = rule_details['context']['obj']
            if leaf_type in leaf_types.keys():
                edited_rule = leaf_types[leaf_type](self, rule_details, parent)
                edit_response = self.__purchase_rules.edit_rule(rule_id, edited_rule)
                self.__purchase_rules_lock.release_write()
                return edit_response
            else:
                self.__purchase_rules_lock.release_write()
                return Response(False, msg=f"invalid simple rule type: {leaf_type}")

        elif rule_type == "complex":
            response_validity = self.check_complex_rule_details_validity(rule_details)
            if not response_validity.succeeded():
                self.__purchase_rules_lock.release_write()
                return response_validity
            logic_type = rule_details['operator']
            if logic_type in logic_types.keys():
                edit_response = self.__purchase_rules.edit_rule(rule_id, logic_types[logic_type](parent))
                self.__purchase_rules_lock.release_write()
                return edit_response

            else:
                self.__purchase_rules_lock.release_write()
                return Response(False, msg=f"invalid logic type: {logic_type}")

        else:
            self.__purchase_rules_lock.release_write()
            return Response(False, msg=f"invalid rule type: {rule_type}")

    def get_purchase_rules(self) -> Response[PurchasePolicy]:
        self.__purchase_rules_lock.acquire_read()
        reponse = Response(True, obj=self, msg="Here are the purchase rules")
        self.__purchase_rules_lock.release_read()
        return reponse

    def checkPolicy(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        self.__purchase_rules_lock.acquire_read()
        policy_response = self.__purchase_rules.operation(products_to_quantities, user_age)
        self.__purchase_rules_lock.release_read()
        return policy_response

    def parse(self):
        self.__purchase_rules_lock.acquire_read()
        parse_result = self.__purchase_rules.parse()
        self.__purchase_rules_lock.release_read()
        return parse_result

    def get_root_id(self):
        return self.__purchase_rules._id

