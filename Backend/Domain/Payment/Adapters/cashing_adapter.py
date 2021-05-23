import requests

from Backend.response import Response
from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing


domain = "https://cs-bgu-wsep.herokuapp.com/"


class CashingAdapter:
    use_stub = False

    def __init__(self):
        self.__outside_cashing = OutsideCashing.getInstance()
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

    def pay(self, price, payment_details) -> Response[str]:
        if CashingAdapter.use_stub:
            response = self.__outside_cashing.pay(price, payment_details)
            if response == "-1":
                return Response(False, msg="Transaction has failed")
            return Response(True, response)

        if (
            "card_number" not in payment_details
            or "month" not in payment_details
            or "year" not in payment_details
            or "holder" not in payment_details
            or "cvv" not in payment_details
            or "id" not in payment_details
        ):
            return Response(False, msg="Payment details was missing a required argument")

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

    def cancel_payment(self, transaction_id) -> Response[None]:
        if CashingAdapter.use_stub:
            return Response(self.__outside_cashing.cancel_payment(transaction_id))

        response = self.__send_cancel_pay(transaction_id)
        if response.status_code != 200 or response.text == "-1":
            return Response(False, "Transaction cancelation has failed")
        return Response(True)
