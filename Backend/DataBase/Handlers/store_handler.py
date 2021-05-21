from sqlalchemy import Table, Column, String
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.store import Store

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class StoreHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock())

        self.__stores = Table("stores", Base.metadata,
                              Column("store_id", String(50), primary_key=True),
                              Column("store_name", String(30)))

        mapper(Store, self.__stores, properties={
            "_Store__id": self.__stores.c.store_id,
            "_Store__name": self.__stores.c.store_name,
            "_Store__responsibility": relationship(Responsibility, uselist=False)
        })

    @staticmethod
    def get_instance():
        with StoreHandler._lock:
            if StoreHandler._instance is None:
                StoreHandler._instance = StoreHandler()
        return StoreHandler._instance
