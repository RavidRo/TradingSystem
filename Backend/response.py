from abc import ABC, abstractmethod


"""
Interface that every object we wish to refer to in Response must implement.
"""
class Parsable(ABC):

    @abstractmethod
    def parse(self):
        raise RuntimeError("must import parse")


"""
Return object which contains message to print and object to inspect.
*Important* each class which self.object refers to must implement parse()
"""
class Response:

    def __init__(self, obj=None, msg="Uninitialized"):
        self.msg = msg
        self.object = obj

    def parse(self):
        return self.object.parse()

    def get_msg(self):
        return self.msg
