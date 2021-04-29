from __future__ import annotations      # for self type annotating

import threading
from abc import ABC, abstractmethod

from Backend.response import Response, Parsable, ParsableList


class IDiscount(Parsable, ABC):

    auto_id_lock = threading.Lock()

    auto_id = 0

    @staticmethod
    def generate_id() -> str:
        with IDiscount.auto_id_lock:
            IDiscount.auto_id += 1
            return str(IDiscount.auto_id - 1)

    @abstractmethod
    def __init__(self, condition=None):
        self._parent = None
        self._id = IDiscount.generate_id()
        self.discount_func = None
        # TODO: convert discount_data['condition'] to Rule
        # self._condition = AndPurchaseRule([])
        if condition is not None:
            # self.condition.add_new_rule(condition, self._condition.get_id())
            pass
        self._condition = lambda x: True

    def get_parent(self) -> IDiscount:
        return self._parent

    def set_parent(self, parent):
        self._parent = parent

    def get_id(self):
        return self._id

    def apply_discount(self, products_to_quantities: dict) -> float:
        if self._condition(products_to_quantities):
            return self.discount_func(products_to_quantities)
        return 0.0

    @abstractmethod
    def is_composite(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def edit_simple_discount(self, discount_id, percentage=None, condition=None, context=None, duration=None) -> Response[None]:
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
    def get_children(self) -> Response[ParsableList[list[IDiscount]]]:
        raise NotImplementedError

    def parse(self):
        discount = dict()
        discount['id'] = self._id
        # discount['condition'] = self._condition.parse()
        return discount
