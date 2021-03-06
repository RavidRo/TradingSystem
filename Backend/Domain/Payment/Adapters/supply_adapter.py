from Backend.settings import Settings
import requests

from Backend.response import Response
from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment


class SupplyAdapter:
    use_stub = Settings.get_instance(False).get_supply_system() == ""

    def __init__(self):
        self.__outside_supplyment = OutsideSupplyment.getInstance()
        try:
            response = self.__send_handshake()
        except:
            raise "Could not connect properly to outside supply system"
        if response.status_code != 200 or response.text != "OK":
            raise "Could not connect properly to outside supply system"

    def __send(self, action_type, paramaters={}):
        return requests.post(
            Settings.get_instance(False).get_supply_system(),
            data=({"action_type": action_type} | paramaters),
            timeout=4,
        )

    def __send_handshake(self):
        if SupplyAdapter.use_stub:

            class Handshake:
                def __init__(self):
                    self.status_code = 200
                    self.text = "OK"

            return Handshake()
        return self.__send("handshake")

    def __send_supply(self, name, address, city, country, zip):
        return self.__send(
            "supply",
            {"name": name, "address": address, "city": city, "country": country, "zip": zip},
        )

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
            return Response(False, msg="Delivery dispatching failed")
        return Response(True, response.text)

    def cancel_delivery(self, transaction_id) -> Response[None]:
        if SupplyAdapter.use_stub:
            return Response(self.__outside_supplyment.cancel_delivery(transaction_id))

        response = self.__send_cancel_supply(transaction_id)
        if response.status_code != 200 or response.text == "-1":
            return Response(False, msg="Delivery cancelation has failed")
        return Response(True)
