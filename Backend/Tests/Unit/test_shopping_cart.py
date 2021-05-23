from unittest.mock import patch, MagicMock

import pytest

from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Tests.stubs.shopping_bag_stub import ShoppingBagStub
from Backend.Tests.stubs.store_stub import StoreStub
from Backend.Tests.stubs.user_stub import UserStub


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
@patch.multiple(
    ShoppingCart,
    create_new_bag=MagicMock(return_value=ShoppingBagStub()),
)
def test_add_product_valid_not_existing_bag(shopping_cart: ShoppingCart, store_stub):
    result = shopping_cart.add_product("0", "0", 5, store_stub)
    assert result.success == True


def test_add_product_valid_existing_bag(shopping_cart: ShoppingCart, store_stub):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.add_product("0", "0", 5, store_stub)
        assert result.success == True


def test_add_product_negative_quantity(shopping_cart: ShoppingCart, store_stub):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.add_product("0", "0", -1, store_stub)
        assert result.success == False


# @patch.multiple(ShoppingCart, get_store_by_id=MagicMock(return_value=None))
# def test_add_product_from_not_existing_store(shopping_cart: ShoppingCart):
#     with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
#         result = shopping_cart.add_product("1", "0", 1)
#         assert result.success == False


# * remove product
# * ====================================================
def test_remove_product_from_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.remove_product("0", "1")
        assert result.success == True


def test_remove_product_from_non_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.remove_product("3", "1")
        assert result.success == False


# * change product quantity
# * ====================================================
def test_change_product_quantity_valid_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.change_product_quantity("0", "0", 6)
        assert result.success == True


def test_change_product_quantity_no_existing_store(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.change_product_quantity("4", "0", 6)
        assert result.success == False


def test_change_product_quantity_not_valid_amount(shopping_cart: ShoppingCart):
    with patch.dict(shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub()}):
        result = shopping_cart.change_product_quantity("0", "0", -1)
        assert result.success == False


# * buy products
# * ====================================================
def test_buy_products(shopping_cart: ShoppingCart, user_stub: UserStub):
    with patch.dict(
        shopping_cart.get_shopping_bags(), {"0": ShoppingBagStub(), "1": ShoppingBagStub()}
    ):
        result = shopping_cart.buy_products(user_stub)
        assert result.object.value == 10
        assert result.success == True
        shopping_cart.cancel_timer()