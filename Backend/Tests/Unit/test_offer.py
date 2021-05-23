from Backend.response import Response
from Backend.Domain.TradingSystem.offer import Offer
from Backend.Tests.stubs.product_stub import ProductStub
from Backend.Tests.stubs.store_stub import StoreStub
from Backend.Tests.stubs.user_stub import UserStub
import pytest

from Backend.Domain.Authentication import authentication


@pytest.fixture
def user():
    return UserStub()


@pytest.fixture
def store():
    return StoreStub()


@pytest.fixture
def product():
    return ProductStub("product")


@pytest.fixture
def offer(user, store, product):
    return Offer(user, store, product)


def test_offer_initiates_as_undeclared(offer: Offer):
    assert offer.get_status_name() == "undeclared"


def test_undeclared_offers_can_be_declared(offer: Offer):
    price = 128
    response = offer.declare_price(price)
    assert response.succeeded(), response.get_msg()


def test_declaring_an_offer_changes_price(offer: Offer):
    price = 128
    response = offer.declare_price(price)
    assert offer.get_price() == price, response.get_msg()


def test_can_declare_price_as_free(offer: Offer):
    response = offer.declare_price(0)
    assert response.succeeded(), response.get_msg()


def test_cant_declare_with_negative_price(offer: Offer):
    response = offer.declare_price(-123)
    assert not response.succeeded(), response.get_msg()


def test_failed_declaration_does_not_change_price(offer: Offer):
    response = offer.declare_price(-123)
    assert offer.get_price() is None, response.get_msg()


def test_undeclared_offers_can_be_cancled(offer: Offer):
    response = offer.cancel_offer()
    assert response.succeeded(), response.get_msg()


def test_undeclared_offers_cant_get_approved_by_manager(offer: Offer):
    assert not offer.approve_user_offer().succeeded()


def test_undeclared_offers_cant_get_rejected(offer: Offer):
    assert not offer.reject_user_offer().succeeded()


def test_undeclared_offers_cant_get_countered_offer(offer: Offer):
    assert not offer.suggest_counter_offer(5).succeeded()


def test_undeclared_offers_cant_get_approved(offer: Offer):
    assert not offer.approve_manager_offer().succeeded()


def test_declared_offers_cant_get_declared_again(offer: Offer):
    offer.declare_price(0)
    response = offer.declare_price(0)
    assert not response.succeeded(), response.get_msg()


def test_declared_offers_cant_get_approved_by_user(offer: Offer):
    offer.declare_price(0)
    response = offer.approve_manager_offer()
    assert not response.succeeded(), response.get_msg()


def test_declared_offers_can_get_approved_by_manager(offer: Offer):
    offer.declare_price(0)
    response = offer.approve_user_offer()
    assert response.succeeded(), response.get_msg()


def test_declared_offers_can_get_rejected_by_manager(offer: Offer):
    offer.declare_price(0)
    response = offer.reject_user_offer()
    assert response.succeeded(), response.get_msg()


def test_declared_offers_can_get_countered_offer(offer: Offer):
    offer.declare_price(0)
    response = offer.suggest_counter_offer(5)
    assert response.succeeded(), response.get_msg()


def test_price_is_set_when_countered_offer(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    assert offer.get_price() == 5


def test_counter_offer_offers_can_be_redeclared(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    response = offer.declare_price(0)
    assert response.succeeded(), response.get_msg()


def test_counter_offer_can_be_cancled(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    response = offer.cancel_offer()
    assert response.succeeded(), response.get_msg()


def test_counter_offer_can_be_approved_by_user(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    response = offer.approve_manager_offer()
    assert response.succeeded(), response.get_msg()


def test_counter_offer_cant_be_rejected(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    response = offer.reject_user_offer()
    assert not response.succeeded(), response.get_msg()


def test_counter_offer_cant_be_recountered(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    response = offer.suggest_counter_offer(10)
    assert not response.succeeded(), response.get_msg()


def test_counter_offer_cant_be_approved_by_manager(offer: Offer):
    offer.declare_price(0)
    offer.suggest_counter_offer(5)
    response = offer.approve_user_offer()
    assert not response.succeeded(), response.get_msg()
