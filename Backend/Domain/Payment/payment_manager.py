from Backend.Domain.Payment import cashing_adapter, supply_adapter
from Backend.response import Response


def pay(price, payment_details, product_ids_to_quantity, address):
    payment_response = cashing_adapter.pay(price, payment_details)
    if payment_response.success:
        try:
            supply_response = supply_adapter.deliver(product_ids_to_quantity, address)
            if supply_response.success:
                return Response(success=True)
            else:
                rollback(price, payment_details)
                return Response(success=False)
        except:
            rollback(price, payment_details)
    else:
        return Response(success=False)


def rollback(price, payment_details):
    return cashing_adapter.pay(-price, payment_details)

