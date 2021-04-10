from unittest.mock import patch, MagicMock

import pytest

from Backend.Domain.TradingSystem import shopping_bag
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.UnitTests.stubs.product_stub import ProductStub
from Backend.UnitTests.stubs.store_stub import StoreStub
from Backend.UnitTests.stubs.user_stub import UserStub


@pytest.fixture
def product_stub():
    return ProductStub()


@pytest.fixture
def store_stub():
    return StoreStub()

@pytest.fixture
def product_stub():
    return ProductStub("prod")

@pytest.fixture
def user_stub():
    return UserStub()


@pytest.fixture()
def products_stubs_store():
    products_to_quantities = {'1': (ProductStub('product1'), 5), '2': (ProductStub('product2'), 4),
                              '3': (ProductStub('product3'), 4)}
    return products_to_quantities

@pytest.fixture()
def products_stubs_shopping_bag():
    products_to_quantities = {'1': (ProductStub('product1'), 2), '2': (ProductStub('product2'), 1),
                              '3': (ProductStub('product3'), 1)}
    return products_to_quantities

@pytest.fixture
def shopping_bag():
    products_to_quantities = {'1': (ProductStub('product1'), 2), '2': (ProductStub('product2'), 1),
                              '3': (ProductStub('product3'), 1)}
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


def test_add_product_already_in_bag(shopping_bag: ShoppingBag, product_stub : ProductStub):
    with patch.dict(shopping_bag.products_to_quantity, {'1': (product_stub, 2)}):
        result = shopping_bag.add_product('1', 3)
        assert result.success == False
        assert shopping_bag.products_to_quantity.get('1')[1] == 2


# * remove product
# * ====================================================
def test_remove_product_valid(shopping_bag: ShoppingBag, product_stub: ProductStub):
    with patch.dict(shopping_bag.products_to_quantity, {'1': (product_stub, 2)}):
        result = shopping_bag.remove_product('1')
        assert result.success == True
        assert shopping_bag.products_to_quantity == {}


def test_remove_product_not_existing(shopping_bag: ShoppingBag, product_stub: ProductStub):
    with patch.dict(shopping_bag.products_to_quantity, {'1': (product_stub, 2)}):
        result = shopping_bag.remove_product('2')
        assert result.success == False
        assert shopping_bag.products_to_quantity == {'1': (product_stub, 2)}


# * buy_products
# * ====================================================
@patch.multiple(StoreStub,
                apply_discounts=MagicMock(return_value=10))
def test_buy_products_valid(shopping_bag: ShoppingBag, user_stub: UserStub, products_stubs_store: dict, products_stubs_shopping_bag: dict):
    with patch.dict(shopping_bag.store.products_to_quantities, products_stubs_store):
        with patch.dict(shopping_bag.products_to_quantity, products_stubs_shopping_bag):
            result = shopping_bag.buy_products(user_stub)
            assert result.success == True
            for i in range(1, 4):
                assert shopping_bag.store.products_to_quantities.get(f'{i}')[1] == 3
            assert shopping_bag.products_to_quantity == {}

# todo: continue with tests from here