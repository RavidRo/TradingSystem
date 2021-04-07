from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict

"""
Interface that every object we wish to refer to in Response must implement.
"""


class Parsable(ABC):
    @abstractmethod
    def parse(self):
        raise RuntimeError("must import parse")


"""
In order to support primitive return objects, a primitive parsable wrapper is introduced
"""

S = TypeVar("S")


class PrimitiveParsable(Parsable, Generic[S]):
    def __init__(self, value: S):
        self.value: S = value

    def parse(self) -> S:
        return self.value


"""
In order to support list return objects, a parsable list wrapper is introduced
"""

T = TypeVar("T", bound=Parsable)


class ParsableList(Parsable, Generic[T]):
    def __init__(self, values: List[T]):
        self.values = values

    def parse(self):
        return ParsableList(map(self.values, lambda value: value.parse()))


"""
In order to support map return objects, a parsable map wrapper is introduced (parse only values)
"""

S = TypeVar("S")


class ParsableMap(Parsable, Generic[S, T]):
    def __init__(self, values: Dict[S, T]):
        self.values = values

    def parse(self):
        for value in self.values.values():
            value.parse()


# """
# Return object which contains message to print and object to inspect, and success flag.
# *Important* each class which self.object refers to must implement parse()
# """


class Response(Generic[T]):
    def __init__(self, success: bool, obj: T = None, msg="Uninitialized"):
        self.msg = msg
        self.object = obj
        self.success = success

    def parse(self):
        return Response(self.success, self.object.parse(), self.msg)

    def get_msg(self):
        return self.msg

    def succeeded(self):
        return self.success




# %%
