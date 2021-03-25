from abc import ABC, abstractmethod
from typing import TypeVar, Generic

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


class PrimitiveParsable(Parsable):

    def __init__(self, value):
        self.value = value

    def parse(self):
        return self.value


"""
Return object which contains message to print and object to inspect, and success flag.
*Important* each class which self.object refers to must implement parse()
"""


T = TypeVar('T', bound=Parsable)


class Response(Generic[T]):

    def __init__(self, success: bool, obj: T = None, msg="Uninitialized"):
        self.msg = msg
        self.object = obj
        self.success = success

    def parse(self):
        return self.object.parse()

    def get_msg(self):
        return self.msg

    def succeeded(self):
        return self.success
