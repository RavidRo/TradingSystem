from __future__ import annotations      # for self type annotating

import threading
from abc import ABC, abstractmethod

from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import AndCompositePurchaseRule
from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy
from Backend.response import Response, Parsable, ParsableList


class IDiscount(Parsable, ABC):

    @abstractmethod
    def __init__(self, id):
        self._parent = None
        self._id = id
        self.discount_func = None
        self._conditions_policy = DefaultPurchasePolicy()

    def get_parent(self) -> IDiscount:
        return self._parent

    def set_parent(self, parent):
        self._parent = parent

    def get_id(self):
        return self._id

    def get_conditions_policy(self):
        return self._conditions_policy

    def apply_discount(self, products_to_quantities: dict, user_age: int) -> float:
        if self._conditions_policy.checkPolicy(products_to_quantities, user_age).succeeded():
            return self.discount_func(products_to_quantities)
        return 0.0

    @abstractmethod
    def is_composite(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def edit_simple_discount(self, discount_id, percentage=None, context=None, duration=None) -> Response[None]:
        raise NotImplementedError

    @abstractmethod
    def edit_complex_discount(self, discount_id, new_id, complex_type=None, decision_rule=None) -> Response[None]:
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

    def parse(self):
        discount = dict()
        discount['id'] = self._id
        condition_parse = self._conditions_policy.parse()
        if len(condition_parse['children']) > 0:
            discount['condition'] = condition_parse
        return discount
