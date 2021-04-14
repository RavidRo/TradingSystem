import pytest
from .stubs.outside_cashing_stub import OutsideCashingStub
from .stubs.outside_supplyment_stub import OutsideSupplymentStub
from Backend.Domain.Payment.payment_manager import PaymentManager

from Backend.response import Response


# * fixtures
# * ==========================================================================================

@pytest.fixture
def outside_cashing():
    return OutsideCashingStub()


@pytest.fixture
def outside_supplyment():
    return OutsideSupplymentStub()


@pytest.fixture
def payment_manager():
    return PaymentManager(outside_cashing, outside_supplyment)


@pytest.fixture
def payment_details():
    return {"credit_card": "1234-5678-9123-4567", "id": "123456789", "CVV": "000"}


@pytest.fixture
def address():
    return "BGU"


# * single_threaded testing
# * ==========================================================================================


def test_payment_success_delivery_success(payment_manager, payment_details):
    response = payment_manager.pay(5.0, payment_details, {}, "")
    assert response.succeeded() and payment_manager.get_balance(payment_details) == 5.0


def test_payment_and_delivery_fail(payment_manager, outside_cashing, outside_supplyment, payment_details):
    outside_cashing.brake()
    outside_supplyment.brake()
    response = payment_manager.pay(5, payment_details, {}, "")
    outside_cashing.fix()
    outside_supplyment.fix()
    assert not response.succeeded() and payment_manager.get_balance(payment_details) == 0


def test_payment_fail_delivery_success_faulty_system(payment_manager, outside_cashing, payment_details):
    outside_cashing.brake()
    response = payment_manager.pay(5, payment_details, {}, "")
    outside_cashing.fix()
    assert not response.succeeded() and payment_manager.get_balance(payment_details) == 0.0


def test_payment_fail_delivery_success_for_specific_costumer(payment_manager, outside_cashing, payment_details):
    outside_cashing.make_details_wrong(payment_details)
    response = payment_manager.pay(5, payment_details, {}, "")
    outside_cashing.make_details_right(payment_details)
    assert not response.succeeded() and payment_manager.get_balance(payment_details) == 0.0


def test_payment_success_delivery_fail_faulty_system(payment_manager, outside_supplyment, payment_details):
    outside_supplyment.brake()
    response = payment_manager.pay(5, payment_details, {}, "")
    outside_supplyment.fix()
    assert not response.succeeded() and payment_manager.get_balance(payment_details) == 0


def test_payment_success_delivery_fail_for_specific_costumer(payment_manager, outside_supplyment, payment_details, address):
    outside_supplyment.make_address_wrong(address)
    response = payment_manager.pay(5, payment_details, {}, "")
    outside_supplyment.make_address_right(address)
    assert not response.succeeded() and payment_manager.get_balance(payment_details) == 0
