from __future__ import annotations  # for self type annotating

from abc import ABC, abstractmethod

from sqlalchemy import orm

from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy
from Backend.rw_lock import ReadWriteLock
from Backend.response import Response, Parsable
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import AndCompositePurchaseRule


class IDiscount(Parsable, ABC):
    @abstractmethod
    def __init__(self, parent=None):
        from Backend.DataBase.Handlers.discounts_handler import discounts_id_seq
        from Backend.DataBase.database import engine
        from sqlalchemy_utils import Ltree
        _id = engine.execute(discounts_id_seq)
        self._id = _id
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id
        self._conditions_policy = None
        self._conditions_policy_root_id = None
        self.wrlock = ReadWriteLock()
        self._discounter_data = {}
        # self._context = {}

    @orm.reconstructor
    def init_on_load(self):
        self._conditions_policy = DefaultPurchasePolicy(AndCompositePurchaseRule())
        self._conditions_policy_root_id = self._conditions_policy.get_root_id()
        self.wrlock = ReadWriteLock()


    def create_purchase_rules_root(self):
        from Backend.DataBase.Handlers.store_handler import StoreHandler
        root_rule = AndCompositePurchaseRule()
        res = StoreHandler.get_instance().save_purchase_rule(root_rule)
        if not res.succeeded():
            return db_fail_response
        self._conditions_policy = DefaultPurchasePolicy(root_rule)
        self._conditions_policy_root_id = self._conditions_policy.get_root_id()
        return Response(True)

    def set_root_purchase_rule(self, root_rule):
        self._conditions_policy = DefaultPurchasePolicy(root_rule)

    def get_id(self):
        return str(self._id)

    def get_conditions_policy(self):
        from Backend.DataBase.Handlers.store_handler import StoreHandler
        if self._conditions_policy is None:
            rules_res = StoreHandler.get_instance().load_purchase_rules(self._conditions_policy_root_id)
            if rules_res.succeeded():
                self._conditions_policy = rules_res.get_obj()
                self._conditions_policy_root_id = self._conditions_policy.get_root_id()
            else:
                response = self.create_purchase_rules_root()
                if not response.succeeded():
                    return db_fail_response
        return Response(True, self._conditions_policy)


    @abstractmethod
    def is_composite(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def edit_simple_discount(
        self, discount_id, percentage=None, context=None) -> Response[None]:
        raise NotImplementedError

    @abstractmethod
    def edit_complex_discount(self, discount_id, complex_type=None, decision_rule=None) -> Response[None]:
        raise NotImplementedError

    @abstractmethod
    def remove_discount(self, discount_id: str) -> Response[None]:
        raise NotImplementedError

    @abstractmethod
    def get_discount_by_id(self, exist_id: str) -> IDiscount:
        raise NotImplementedError

    @abstractmethod
    def add_child(self, child: IDiscount) -> Response[None]:
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, child: IDiscount):
        raise NotImplementedError

    @abstractmethod
    def get_children(self) -> list[IDiscount]:
        raise NotImplementedError

    @abstractmethod
    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        raise NotImplementedError

    @abstractmethod
    def discount_func(self, products_to_quantities: dict, username) -> float:
        raise NotImplementedError

    def parse(self):
        discount = dict()
        discount['id'] = self._id
        # condition_parse = self.get_conditions_policy().get_obj().parse()
        # if len(condition_parse['children']) > 0:
        #     discount['condition'] = condition_parse
        return discount

    def set_parent(self, parent):
        self.parent = parent
