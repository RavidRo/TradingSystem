from unittest.mock import patch

import pytest

from Backend.Domain.TradingSystem import shopping_bag
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.UnitTests.stubs.product_stub import ProductStub
from Backend.UnitTests.stubs.store_stub import StoreStub


@pytest.fixture
def product_stub():
    return ProductStub()


@pytest.fixture
def store_stub():
    return StoreStub()


@pytest.fixture
def shopping_bag():
    products_to_quantities = {'1': (ProductStub('product1'), 2), '2': (ProductStub('product2'), 1), '3': (ProductStub('product3'), 1)}
    store = StoreStub(products_to_quantities)
    return ShoppingBag(store)


# * add product
# * ====================================================
def test_add_product_valid(shopping_bag: ShoppingBag):
    result = shopping_bag.add_product('1', 1)
    assert result.success == True
    assert shopping_bag.products_to_quantity.get('1')[1] == 1


def test_add_product_negative_quantity(shopping_bag: ShoppingBag):
    result = shopping_bag.add_product('1', -5)
    assert result.success == False
    assert shopping_bag.products_to_quantity == {}


def test_add_product_not_in_store(shopping_bag: ShoppingBag):
    result = shopping_bag.add_product('4', 1)
    assert result.success == False
    assert shopping_bag.products_to_quantity == {}


def test_add_product_in_store_but_low_quantity(shopping_bag: ShoppingBag):
    result = shopping_bag.add_product('2', 2)
    assert result.success == False
    assert shopping_bag.products_to_quantity == {}

#todo: complete tests!!!

def test_add_product_already_in_bag(shopping_bag: ShoppingBag):
    with patch.dict(shopping_bag.products_to_quantity, {'1': (ProductStub("prod"), 2)}):
        result = shopping_bag.add_product('1', 3)
        assert result.success == False

