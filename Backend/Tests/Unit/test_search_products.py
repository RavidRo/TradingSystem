import pytest

from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.search_engine import SearchEngine
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Tests.stubs.product_stub import ProductStub
from Backend.Tests.stubs.store_stub import StoreStub
from unittest import mock

from Backend.response import Response, ParsableList


@pytest.fixture
def store_a():
    return Store("A")

@pytest.fixture
def store_b():
    return Store("B")


# Tests:
# ================================================================================

def test_search_no_stores_success():
    with mock.patch.object(StoresManager, 'get_stores_details', return_value=Response(True, ParsableList([]))):
        res = SearchEngine.search_products("name", search_by="name")
        assert res.succeeded() and len(res.get_obj().parse()) == 0


def test_search_no_products_success():
    with mock.patch.object(StoresManager, 'get_stores_details',
                           return_value=Response(True, ParsableList([Store("A"), Store("B"), Store("C")]))):
        res = SearchEngine.search_products("name", search_by="name")
        num_of_products = 0
        for store, products_to_quantities in res.get_obj().parse().items():
            for product, quantity in products_to_quantities:
                num_of_products += quantity
        assert res.succeeded() and len(res.get_obj().parse()) == 3 and num_of_products == 0


def test_search_fails_invalid_search_by():
    res = SearchEngine.search_products("name", search_by="ABC")
    assert not res.succeeded()


def test_search_single_search_by_name_success(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products("name", search_by="name")
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 10


def test_search_single_search_by_category_success(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "category", 2), 5), "2": (Product("B", "A", 3), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products("category", search_by="category")
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 10


def test_search_multiple_search_by_exist_both_success(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_phrase="name", search_by=["category", "name"])
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 10


def test_search_multiple_search_by_neither_of_them(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_phrase="other_name", search_by=["category", "name"])
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 0


def test_search_missing_argument_to_search_by(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="name")
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 0


def test_search_by_keywords_have_all(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3, ["cats", "dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="keywords", keywords=["cats", "dogs"])
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 14


def test_search_by_keywords_missing_some(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3, ["dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="keywords", keywords=["cats", "dogs"])
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 0


def test_search_by_keywords_product_have_more_keywords(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2), 5), "2": (Product("B", "A", 3, ["cats", "dogs", "horses"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="keywords", keywords=["cats", "dogs"])
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 14


def test_search_by_keywords_product_multiple_stores(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2, ["cats"]), 5), "2": (Product("B", "A", 3, ["cats", "dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="keywords", keywords=["cats"])
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 24


def test_search_min_price(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 1, ["cats"]), 5), "2": (Product("B", "A", 3, ["cats", "dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="category", search_phrase="A", min_price=2.0)
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 14


def test_search_min_price_include_border(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 1, ["cats"]), 5), "2": (Product("B", "A", 2, ["cats", "dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="category", search_phrase="A", min_price=2.0)
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 14


def test_search_max_price(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 1, ["cats"]), 5), "2": (Product("B", "A", 3, ["cats", "dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="category", search_phrase="A", max_price=2.0)
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 10


def test_search_max_price_include_border(store_a, store_b):
    with mock.patch.object(Store, 'get_products_to_quantities', return_value={"1": (Product("name", "A", 2, ["cats"]), 5), "2": (Product("B", "A", 3, ["cats", "dogs"]), 7)}):
        with mock.patch.object(StoresManager, 'get_stores_details',
                               return_value=Response(True, ParsableList([store_a, store_b]))):
            res = SearchEngine.search_products(search_by="category", search_phrase="A", max_price=2.0)
            num_of_products = 0
            for store, products_to_quantities in res.get_obj().parse().items():
                for product, quantity in products_to_quantities:
                    num_of_products += quantity
            assert res.succeeded() and len(res.get_obj().parse()) == 2 and num_of_products == 10
