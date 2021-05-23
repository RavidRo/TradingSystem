import requests

from Backend.response import Response
from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment

# TODO: Add to config file
domain = "https://cs-bgu-wsep.herokuapp.com/"


class SupplyAdapter:
    use_stub = False

    def __init__(self):
        self.__outside_supplyment = OutsideSupplyment.getInstance()
        response = self.__send_handshake()
        if response.status_code != 200 or response.text != "OK":
            raise "Could not connect properly to outside systems"

    def __send(self, action_type, paramaters={}):
        return requests.post(domain, data=({"action_type": action_type} | paramaters))

    def __send_handshake(self):
        return self.__send("handshake")

    def __send_supply(self, name, address, city, country, zip):
        return self.__send("supply", {name, address, city, country, zip})

    def __send_cancel_supply(self, transaction_id):
        return self.__send("cancel_supply", {"transaction_id": transaction_id})

    def deliver(self, product_ids_to_quantity, address):
        if SupplyAdapter.use_stub:
            response = self.__outside_supplyment.deliver(product_ids_to_quantity, address)
            if response == "-1":
                return Response(False, msg="Delivery dispatching failed")
            return Response(True, response)

        if (
            "name" not in address
            or "address" not in address
            or "city" not in address
            or "country" not in address
            or "zip" not in address
        ):
            return Response(False, msg="Address was missing a required argument")

        response = self.__send_supply(
            address["name"],
            address["address"],
            address["city"],
            address["country"],
            address["zip"],
        )

        if response.status_code != 200 or response.text == "-1":
            return Response(False, "Delivery dispatching failed")
        return Response(True, response.text)

    def cancel_delivery(self, transaction_id) -> Response[None]:
        if SupplyAdapter.use_stub:
            return Response(self.__outside_supplyment.cancel_delivery(transaction_id))

        response = self.__send_cancel_supply(transaction_id)
        if response.status_code != 200 or response.text == "-1":
            return Response(False, "Delivery cancelation has failed")
        return Response(True)
