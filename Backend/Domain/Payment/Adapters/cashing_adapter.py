from Backend.response import Response
from werkzeug.security import generate_password_hash
from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing


class CashingAdapter:

    def __init__(self, ):
        self.__outside_cashing = OutsideCashing()
        self.__hashes = dict()

    def pay(self, price, payment_info):
        # Temporal implementation, will be change with the real implementation of OutsideCashing
        # Assuming outside cashing returns boolean, wrapping with response to include message later.
        hashed_details = generate_password_hash(payment_info, method="sha256")
        if payment_info not in self.__hashes:
            self.__hashes[payment_info] = hashed_details
        answer = self.__outside_cashing.pay(price, self.__hashes[payment_info])
        return Response(success=answer)

    # test function:
    def get_balance(self, payment_details):
        hashed_details = generate_password_hash(payment_details, method="sha256")
        if payment_details not in self.__hashes:
            self.__hashes[payment_details] = hashed_details
        return self.__outside_cashing.get_balance(self.__hashes[payment_details])
