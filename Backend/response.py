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

    def get_val(self):
        return self.value


"""
In order to support list return objects, a parsable list wrapper is introduced
"""

T = TypeVar("T", bound=Parsable)


class ParsableList(Parsable, Generic[T]):
    def __init__(self, values: List[T]):
        self.values = values

    def parse(self):
        return ParsableList(list(map(lambda value: value.parse(), self.values)))


class ParsableTuple(Parsable, Generic[T]):
    def __init__(self, values: tuple[T]):
        self.values: tuple[T] = values

    def parse(self):
        return tuple(map(lambda value: value.parse(), self.values))


"""
In order to support map return objects, a parsable map wrapper is introduced (parse only values)
"""

R = TypeVar("R", bound=Parsable)


class ParsableMap(Parsable, Generic[R, T]):
    def __init__(self, dictionary: Dict[R, T]):
        self.dictionary = dictionary

    def parse(self):
        return {key.parse(): value.parse() for key, value in self.dictionary.items()}


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
        return Response(
            self.success, self.object.parse() if self.object is not None else None, self.msg
        )

    def get_msg(self):
        return self.msg

    def succeeded(self):
        return self.success

    def get_obj(self):
        return self.object
