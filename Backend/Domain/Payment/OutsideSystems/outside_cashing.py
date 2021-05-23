from __future__ import annotations
import threading
import uuid


class OutsideCashing:
    __instance = None

    # https://medium.com/@rohitgupta2801/the-singleton-class-python-c9e5acfe106c
    # double locking mechanism
    @staticmethod
    def getInstance() -> OutsideCashing:
        """Static access method."""
        if OutsideCashing.__instance is None:
            with threading.Lock():
                if OutsideCashing.__instance is None:
                    OutsideCashing()
        return OutsideCashing.__instance

    def __init__(self):
        """Virtually private constructor."""
        if OutsideCashing.__instance is not None:
            raise Exception("This class is a singleton!")

        OutsideCashing.__instance = self
        self.balances = {}

    def pay(self, price, payment_details):
        transaction_id = self.get_transaction_id()
        self.balances[transaction_id] = price
        return transaction_id

    def cancel_payment(self, transaction_id):
        transacted = transaction_id in self.balances
        if transacted:
            self.balances[transaction_id] = 0
        return transacted

    def get_balance(self, transaction_id):
        return self.balances[transaction_id]

    def get_transaction_id(self):
        return str(uuid.uuid4())
