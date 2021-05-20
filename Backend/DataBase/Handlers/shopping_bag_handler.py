from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint, insert
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, Session, engine
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class ShoppingBagHandler:
    _lock = Lock()
    _instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        with ShoppingBagHandler._lock:
            if ShoppingBagHandler._instance is None:
                ShoppingBagHandler._instance = ShoppingBagHandler()
        return ShoppingBagHandler._instance


