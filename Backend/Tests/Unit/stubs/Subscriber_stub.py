from typing import Callable

from Backend.Domain.TradingSystem.Interfaces.Subscriber import Subscriber


class Subscriber_stub(Subscriber):
    def __init__(self, notify_checker):
        self.__notify_checker = notify_checker

    def notify(self, message: str) -> bool:
        self.__notify_checker(message)
        return True
