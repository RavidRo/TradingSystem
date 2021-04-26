from unittest.mock import patch
import pytest
from Backend.Domain.TradingSystem.store import Store
from Backend.Tests.stubs.product_stub import ProductStub


@pytest.fixture
def store():
    return Store("")


@pytest.fixture
def product1():
    return ProductStub("prod1")


# * add product
# * ====================================================
def test_add_product_valid(store: Store):
    result = store.add_product("product", "A", 1.0, 1)
    assert result.success == True


def test_add_product_negative_quantity(store: Store):
    result = store.add_product("product", "A", 1.0, -1)
    assert result.success == False


def test_add_product_negative_price(store: Store):
    result = store.add_product("product", "A", -1.0, 1)
    assert result.success == False


def test_add_product_existing_product(store: Store):
    store.add_product("product", "A", 1.0, 1)
    result = store.add_product("product", "A", 5.0, 5)
    assert result.success == False


# * remove product
# * ====================================================
def test_remove_product_valid_one_product(store: Store):
    with patch.dict(store.get_products_to_quantities(), {"123": (ProductStub("prod1"), 1)}):
        result = store.remove_product("123")
        assert result.success
        assert store.get_products_to_quantities() == {}


def test_remove_product_valid_multiple_products(store: Store):
    product1 = ProductStub("prod1")
    product2 = ProductStub("prod2")
    product3 = ProductStub("prod3")
    with patch.dict(
        store.get_products_to_quantities(),
        {"123": (product1, 1), "345": (product2, 5), "121": (product3, 4)},
    ):
        result = store.remove_product("123")
        assert result.success == True
        assert store.get_products_to_quantities() == {"345": (product2, 5), "121": (product3, 4)}


def test_remove_product_not_existing(store: Store):
    product1 = ProductStub("prod1")
    product2 = ProductStub("prod2")
    product3 = ProductStub("prod3")
    with patch.dict(
        store.get_products_to_quantities(),
        {"123": (product1, 1), "345": (product2, 5), "121": (product3, 4)},
    ):
        result = store.remove_product("444")
        assert not result.success
        assert store.get_products_to_quantities() == {
            "123": (product1, 1),
            "345": (product2, 5),
            "121": (product3, 4),
        }


# * edit product details
# * ====================================================
def test_edit_product_details_valid(store: Store, product1: ProductStub):
    with patch.dict(store.get_products_to_quantities(), {"123": (product1, 1)}):
        result = store.edit_product_details("123", "prod2", "B", 2.0)
        assert result.success
        assert product1.product_edited


def test_edit_product_details_not_existing(store: Store, product1: ProductStub):
    with patch.dict(store.get_products_to_quantities(), {"123": (product1, 1)}):
        result = store.edit_product_details("111", "prod2", "B", 2.0)
        assert not result.success
        assert not product1.product_edited


# * change product quantity
# * ====================================================
def test_change_product_quantity_valid(store: Store, product1: ProductStub):
    with patch.dict(store.get_products_to_quantities(), {"123": (product1, 1)}):
        result = store.change_product_quantity("123", 5)
        assert result.success
        assert store.get_products_to_quantities().get("123")[1] == 5


def test_change_product_quantity_negative(store: Store, product1: ProductStub):
    with patch.dict(store.get_products_to_quantities(), {"123": (product1, 1)}):
        result = store.change_product_quantity("123", -5)
        assert not result.success
        assert store.get_products_to_quantities().get("123")[1] == 1


def test_change_product_quantity_not_existing(store: Store, product1: ProductStub):
    with patch.dict(store.get_products_to_quantities(), {"123": (product1, 1)}):
        result = store.change_product_quantity("151", 5)
        assert not result.success
        assert store.get_products_to_quantities().get("123")[1] == 1
