import requests

from Backend.response import Response
from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing


domain = "https://cs-bgu-wsep.herokuapp.com/"


class CashingAdapter:
    def __init__(self):
        self.__outside_cashing = OutsideCashing()
        response = self.__send_handshake()
        if response.status_code != 200 or response.text != "OK":
            raise "Could not connect properly to outside systems"

    def __send(self, action_type, paramaters={}):
        return requests.post(domain, data=({"action_type": action_type} | paramaters))

    def __send_handshake(self):
        return self.__send("handshake")

    def __send_pay(self, card_number, month, year, holder, cvv, id):
        return self.__send("pay", {card_number, month, year, holder, cvv, id})

    def __send_cancel_pay(self, transaction_id):
        return self.__send("cancel_pay", {transaction_id})

    def __send_supply(self, name, address, city, country, zip):
        return self.__send("supply", {name, address, city, country, zip})

    def __send_cancel_supply(self, transaction_id):
        return self.__send("cancel_supply", {transaction_id})

    def pay(self, price, payment_details):
        # Temporal implementation, will be change with the real implementation of OutsideCashing
        # Assuming outside cashing returns boolean, wrapping with response to include message later.
        response = self.__send_pay(
            payment_details["card_number"],
            payment_details["month"],
            payment_details["year"],
            payment_details["holder"],
            payment_details["cvv"],
            payment_details["id"],
        )
        if response.status_code != 200 or response.text == "-1":
            return Response(False, "Transaction has failed")
        return Response(True, response.text)

    def cancel_payment(self, payment_details):

        return self.__outside_cashing.get_balance(payment_details)
