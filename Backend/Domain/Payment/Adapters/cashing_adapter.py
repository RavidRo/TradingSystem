from Backend.settings import Settings
import requests

from Backend.response import Response
from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing


class CashingAdapter:
    use_stub = Settings.get_instance(False).get_payment_system() == ""

    def __init__(self):
        self.__outside_cashing = OutsideCashing.getInstance()
        response = self.__send_handshake()
        if response.status_code != 200 or response.text != "OK":
            raise "Could not connect properly to outside systems"

    def __send(self, action_type, paramaters={}):
        return requests.post(
            Settings.get_instance(False).get_payment_system(),
            data=({"action_type": action_type} | paramaters),
            timeout=4,
        )

    def __send_handshake(self):
        if CashingAdapter.use_stub:

            class Handshake:
                def __init__(self):
                    self.status_code = 200
                    self.text = "OK"

            return Handshake()
        return self.__send("handshake")

    def __send_pay(self, card_number, month, year, holder, ccv, id):
        return self.__send(
            "pay",
            {
                "card_number": card_number,
                "month": month,
                "year": year,
                "holder": holder,
                "ccv": ccv,
                "id": id,
            },
        )

    def __send_cancel_pay(self, transaction_id):
        return self.__send("cancel_pay", {"transaction_id": transaction_id})

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
            or "ccv" not in payment_details
            or "id" not in payment_details
        ):
            return Response(False, msg="Payment details was missing a required argument")

        response = self.__send_pay(
            payment_details["card_number"],
            payment_details["month"],
            payment_details["year"],
            payment_details["holder"],
            payment_details["ccv"],
            payment_details["id"],
        )
        if response.status_code != 200 or response.text == "-1":
            return Response(False, msg="Transaction has failed")
        return Response(True, response.text)

    def cancel_payment(self, transaction_id) -> Response[None]:
        if CashingAdapter.use_stub:
            return Response(self.__outside_cashing.cancel_payment(transaction_id))

        response = self.__send_cancel_pay(transaction_id)
        if response.status_code != 200 or response.text == "-1":
            return Response(False, msg="Transaction cancelation has failed")
        return Response(True)
