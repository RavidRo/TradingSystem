# Temporal implementation of OutsideSupplyment. Real implementation will be given in future milestones.

from __future__ import annotations
import threading
import uuid


class OutsideSupplyment:
    __instance = None

    # https://medium.com/@rohitgupta2801/the-singleton-class-python-c9e5acfe106c
    # double locking mechanism
    @staticmethod
    def getInstance() -> OutsideSupplyment:
        """Static access method."""
        if OutsideSupplyment.__instance is None:
            with threading.Lock():
                if OutsideSupplyment.__instance is None:
                    OutsideSupplyment()
        return OutsideSupplyment.__instance

    def __init__(self):
        """Virtually private constructor."""
        if OutsideSupplyment.__instance is not None:
            raise Exception("This class is a singleton!")

        OutsideSupplyment.__instance = self
        self.deliveries = {}

    def deliver(self, product_ids_to_quantity, address):
        transaction_id = str(uuid.uuid4())
        self.deliveries[transaction_id] = product_ids_to_quantity
        return transaction_id

    def cancel_delivery(self, transaction_id):
        transacted = transaction_id in self.deliveries
        if transacted:
            self.balances[transaction_id] = None
        return transacted
