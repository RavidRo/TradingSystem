from __future__ import annotations

import json
import threading


class Settings:
    __instance = None

    @staticmethod
    def get_instance() -> Settings:
        if Settings.__instance is None:
            with threading.Lock():
                if Settings.__instance is None:
                    Settings()
        return Settings.__instance

    def __init__(self):
        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        Settings.__instance = self
        try:
            read_file = open("config.json", "r")
        except OSError:
            OSError("config.json file is absent")
        with read_file:
            data = json.load(read_file)
            self.__admins = data["admins"] if "admins" in data else None
            self.__password = data["password"] if "password" in data else None
            self.__timer_length = data["timer_length"] if "timer_length" in data else None
            self.__payment_system = data["payment_system"] if "payment_system" in data else None
            self.__supply_system = data["supply_system"] if "supply_system" in data else None
            self.__DB = data["DB"] if "DB" in data else None

    def get_admins(self):
        return self.__admins

    def get_password(self):
        return self.__password

    def get_timer_length(self):
        return self.__timer_length

    def get_payment_system(self):
        return self.__payment_system

    def get_supply_system(self):
        return self.__supply_system

    def get_DB(self):
        return self.__DB
