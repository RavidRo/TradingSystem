from unittest import mock
from unittest.mock import patch, MagicMock

import pytest

from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.UnitTests.stubs.product_stub import ProductStub
from Backend.UnitTests.stubs.shopping_bag_stub import ShoppingBagStub
from Backend.UnitTests.stubs.store_stub import StoreStub
from Backend.UnitTests.stubs.user_stub import UserStub


@pytest.fixture
def shopping_cart():
    return ShoppingCart()


@pytest.fixture()
def shopping_bag_stub():
    return ShoppingBagStub()


@pytest.fixture()
def store_stub():
    return StoreStub()


@pytest.fixture()
def store_stub():
    return StoreStub()


@pytest.fixture()
def user_stub():
    return UserStub()


# * add product
# * ====================================================
@patch.multiple(ShoppingCart,
                create_new_bag=MagicMock(return_value=ShoppingBagStub()),
                get_store_by_id=MagicMock(return_value=StoreStub()))
def test_add_product_valid_not_existing_bag(shopping_cart: ShoppingCart):
    result = shopping_cart.add_product('0', '0', 5)
    assert result.success == True


@patch.multiple(ShoppingCart,
                get_store_by_id=MagicMock(return_value=StoreStub()))
def test_add_product_valid_existing_bag(shopping_cart: ShoppingCart, shopping_bag_stub: ShoppingBagStub):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.add_product('0', '0', 5)
        assert result.success == True


def test_add_product_negative_quantity(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.add_product('0', '0', -1)
        assert result.success == False


@patch.multiple(ShoppingCart,
                get_store_by_id=MagicMock(return_value=None))
def test_add_product_from_not_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.add_product('1', '0', 1)
        assert result.success == False


# * remove product
# * ====================================================
def test_remove_product_from_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.remove_product('0', '1')
        assert result.success == True


def test_remove_product_from_non_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.remove_product('3', '1')
        assert result.success == False


# * change product quantity
# * ====================================================
def test_change_product_quantity_valid_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.change_product_quantity('0', '0', 6)
        assert result.success == True


def test_change_product_quantity_no_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.change_product_quantity('4', '0', 6)
        assert result.success == False


def test_change_product_quantity_not_valid_amount(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub()}):
        result = shopping_cart.change_product_quantity('0', '0', -1)
        assert result.success == False


# # * buy products
# # * ====================================================
def test_buy_products(shopping_cart: ShoppingCart, user_stub: UserStub):
    with patch.dict(shopping_cart.shopping_bags, {'0': ShoppingBagStub(), '1': ShoppingBagStub()}):
        result = shopping_cart.buy_products(user_stub)
        assert result.object.value == 10
        assert result.success == True