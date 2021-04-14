from Backend.response import Response
from werkzeug.security import generate_password_hash


class CashingAdapter:

    def __init__(self, outside_system):
        self.outside_cashing = outside_system
        self.hashes = dict()

    def pay(self, price, payment_info):
        # Temporal implementation, will be change with the real implementation of OutsideCashing
        # Assuming outside cashing returns boolean, wrapping with response to include message later.
        hashed_details = generate_password_hash(payment_info, method="sha256")
        if payment_info not in self.hashes:
            self.hashes[payment_info] = hashed_details
        answer = self.outside_cashing.pay(price, self.hashes[payment_info])
        if isinstance(answer, Response):        # I wanted for test purposes to return Response, and I can't trust real outside system to return Response
            return answer
        return Response(success=answer)

    # test function:
    def get_balance(self, payment_details):
        hashed_details = generate_password_hash(payment_details, method="sha256")
        if payment_details not in self.hashes:
            self.hashes[payment_details] = hashed_details
        return self.outside_cashing.get_balance(self.hashes[payment_details])

    def make_details_wrong(self, payment_details):
        hashed_details = generate_password_hash(payment_details, method="sha256")
        if payment_details not in self.hashes:
            self.hashes[payment_details] = hashed_details
        return self.outside_cashing.make_details_wrong(self.hashes[payment_details])

    def make_details_right(self, payment_details):
        hashed_details = generate_password_hash(payment_details, method="sha256")
        if payment_details not in self.hashes:
            self.hashes[payment_details] = hashed_details
        return self.outside_cashing.make_details_right(self.hashes[payment_details])
