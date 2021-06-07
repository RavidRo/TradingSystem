from __future__ import annotations

import json
import threading
import Backend.Service.logs as logs


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
        except:
            e = FileNotFoundError("config.json file is absent")
            logs.log_file_errors(e)
            raise e
        with read_file:
            data = json.load(read_file)
            missing_args = ""
            if "admins" in data:
                self.__admins = data["admins"]
            else:
                missing_args += "admins "
            if "password" in data:
                self.__password = data["password"]
            else:
                missing_args += "password "
            if "timer_length" in data:
                self.__timer_length = data["timer_length"]
            else:
                missing_args += "timer_length "
            if "payment_system" in data:
                self.__payment_system = data["payment_system"]
            else:
                missing_args += "payment_system "
            if "supply_system" in data:
                self.__supply_system = data["supply_system"]
            else:
                missing_args += "supply_system "
            if "DB" in data:
                self.__DB = data["DB"]
            else:
                missing_args += "DB "
            if not missing_args == "":
                raise KeyError("the keys "+missing_args+"are missing from config.json file")

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
