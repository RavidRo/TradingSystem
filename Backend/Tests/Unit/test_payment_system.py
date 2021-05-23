from Backend.Domain.Payment.Adapters.supply_adapter import SupplyAdapter
from Backend.Domain.Payment.Adapters.cashing_adapter import CashingAdapter
import pytest
from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing
from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment
from unittest import mock
from Backend.Domain.Payment.payment_manager import PaymentManager


# * fixtures
# * ==========================================================================================
@pytest.fixture(scope="function", autouse=True)
def set_up():
    CashingAdapter.use_stub = True
    SupplyAdapter.use_stub = True
    yield
    CashingAdapter.use_stub = False
    SupplyAdapter.use_stub = False


@pytest.fixture
def payment_manager():
    return PaymentManager()


@pytest.fixture
def payment_details():
    return "some payment information"  # currently not dict because dict is not hashable


@pytest.fixture
def address():
    return "BGU"


# * Tests
# * ==========================================================================================


def test_payment_success_delivery_success(payment_manager, payment_details, address):
    with mock.patch.object(OutsideCashing, "get_transaction_id", return_value="transaction_id"):
        response = payment_manager.pay(5.0, payment_details, {}, address)
        assert (
            response.succeeded()
            and OutsideCashing.getInstance().get_balance("transaction_id") == 5.0
        )


def test_payment_and_delivery_fail(payment_manager, payment_details, address):
    with mock.patch.object(OutsideCashing, "pay", return_value="-1"):
        with mock.patch.object(OutsideSupplyment, "deliver", return_value="-1"):
            response = payment_manager.pay(5, payment_details, {}, address)
            assert not response.succeeded()


def test_payment_fail_delivery_success_faulty_system(payment_manager, payment_details, address):
    # assuming faulty system will raise an error
    with mock.patch.object(OutsideCashing, "pay", side_effect=Exception()):
        response = payment_manager.pay(5, payment_details, {}, address)
        assert not response.succeeded()


def test_payment_fail_delivery_success_for_specific_costumer(
    payment_manager, payment_details, address
):
    with mock.patch.object(OutsideCashing, "pay", return_value="-1"):
        response = payment_manager.pay(5, payment_details, {}, address)
        assert not response.succeeded()


def test_payment_success_delivery_fail_faulty_system(payment_manager, payment_details, address):
    # assuming faulty system will raise an error
    with mock.patch.object(OutsideCashing, "get_transaction_id", return_value="transaction_id"):
        with mock.patch.object(OutsideSupplyment, "deliver", side_effect=Exception()):
            response = payment_manager.pay(5, payment_details, {}, address)
            assert (
                not response.succeeded()
                and OutsideCashing.getInstance().get_balance("transaction_id") == 0.0
            )


def test_payment_success_delivery_fail_for_specific_costumer(
    payment_manager, payment_details, address
):
    with mock.patch.object(OutsideCashing, "get_transaction_id", return_value="transaction_id"):
        with mock.patch.object(OutsideSupplyment, "deliver", return_value="-1"):
            response = payment_manager.pay(5, payment_details, {}, address)
            assert (
                not response.succeeded()
                and OutsideCashing.getInstance().get_balance("transaction_id") == 0.0
            )
