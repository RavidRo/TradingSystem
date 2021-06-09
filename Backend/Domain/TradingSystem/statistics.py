from __future__ import annotations
from Backend.Domain.TradingSystem.Interfaces.Subscriber import Subscriber
from Backend.Domain.Notifications.Publisher import Publisher
from Backend.Service.DataObjects.statistics_data import StatisticsData
from datetime import date

import threading

from collections import Counter


class Statistics:
    __instance = None

    # https://medium.com/@rohitgupta2801/the-singleton-class-python-c9e5acfe106c
    # double locking mechanism
    @staticmethod
    def getInstance() -> Statistics:
        """Static access method."""
        if Statistics.__instance is None:
            with threading.Lock():
                if Statistics.__instance is None:
                    Statistics()
        return Statistics.__instance

    def __init__(self):
        """Virtually private constructor."""
        if Statistics.__instance is not None:
            raise Exception("This class is a singleton!")

        Statistics.__instance = self
        self.__statistics_per_day: dict[date, Counter] = {}
        self.__admins_publisher = Publisher()

    def subscribe(self, subscriber: Subscriber) -> None:
        self.__admins_publisher.subscribe(subscriber)

    def __today(self) -> date:
        current = date.today()
        if current not in self.__statistics_per_day:
            self.__statistics_per_day[current] = Counter()
        return current

    def __update(self, name):
        today = self.__today()
        self.__statistics_per_day[today].update({name: 1})
        self.__admins_publisher.notify_all(self.get_statistics(), "statistics")

    def register_guest(self) -> None:
        self.__update("guest")

    def register_passive(self) -> None:
        self.__update("passive_members")

    def register_manager(self) -> None:
        self.__update("managers")

    def register_owner(self) -> None:
        self.__update("owners")

    def register_super(self) -> None:
        self.__update("super_members")

    def get_statistics(self) -> StatisticsData:
        return StatisticsData(self.__statistics_per_day)
