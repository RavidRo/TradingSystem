# Temporal implementation of OutsideCashing. Real implementation will be given in future milestones.

from time import sleep
from collections import defaultdict

class OutsideCashing:

    def __init__(self):
        self.balances = defaultdict(lambda: 0.0)

    def pay(self, price, payment_details):
        # sleep(1)
        self.balances[payment_details] += price
        return True

    # test_function:
    def get_balance(self, payment_details):
        return self.balances[payment_details]
