import pytest
import json
import threading
from queue import Queue
from unittest import mock
from unittest.mock import patch, MagicMock

from Backend.Service import logs
from Backend.Service.trading_system import TradingSystem
from Backend.response import Response
from Backend.Domain.Payment.Adapters.cashing_adapter import CashingAdapter
from Backend.Domain.Payment.Adapters.supply_adapter import SupplyAdapter
from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing
from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.store import Store
from Backend.settings import Settings

system = TradingSystem.getInstance()
username_number = 0
user_lock = threading.Lock()
store_number = 0
store_lock = threading.Lock()
product_number = 0
product_lock = threading.Lock()


@pytest.fixture(scope="function", autouse=True)
def set_up():
    CashingAdapter.use_stub = True
    SupplyAdapter.use_stub = True
    yield
    CashingAdapter.use_stub = False
    SupplyAdapter.use_stub = False
    Settings.get_instance(True)


def _initialize_info(
    username: str, password: str, store_name: str = None
) -> tuple[str, str, str, str, str]:
    store_id = ""
    cookie = system.enter_system()
    system.register(cookie, username, password)
    system.login(cookie, username, password)
    if store_name:
        store_res = system.create_store(cookie, store_name)
        store_id = store_res.object
    return cookie, username, password, store_name, store_id


def _create_product(
    cookie: str, store_id: str, product_name: str, category: str, price: float, quantity: int
) -> tuple[str, str, str, float, int]:
    product_res = system.create_product(cookie, store_id, product_name, category, price, quantity)
    product_id = product_res.object
    return product_id, product_name, category, price, quantity


def _generate_username() -> str:
    global username_number
    user_lock.acquire()
    username_number += 1
    username = "test_TradingSystem" + str(username_number)
    user_lock.release()
    return username


def _generate_store_name() -> str:
    global store_number
    store_lock.acquire()
    store_number += 1
    store = "test_TradingSystem" + str(store_number)
    store_lock.release()
    return store


def _simple_rule_details_age() -> dict:
    return {"context": {"obj": "user"}, "operator": "great-equals", "target": 18}


def _simple_rule_details_age_edited() -> dict:
    return {"context": {"obj": "user"}, "operator": "great-equals", "target": 21}


def _simple_rule_details_product() -> dict:
    return {"context": {"obj": "product", "identifier": "1"}, "operator": "less-than", "target": 10}


def _simple_rule_details_age_invalid_operator() -> dict:
    return {"context": {"obj": "user"}, "operator": "invalid", "target": 18}


def _simple_rule_details_age_missing_key_target() -> dict:
    return {"context": {"obj": "user"}, "operator": "invalid"}


def _complex_rule_details_or() -> dict:
    return {"operator": "or"}


def _complex_rule_details_and() -> dict:
    return {"operator": "and"}


def _complex_rule_details_conditioning() -> dict:
    return {"operator": "conditional"}


def _complex_rule_details_invalid_operator() -> dict:
    return {"operator": "invalid"}


def _complex_rule_details_missing_operator() -> dict:
    return {}


def _product_discount(product_id="123") -> dict:
    return {
        "discount_type": "simple",
        "percentage": 50.0,
        "context": {"obj": "product", "id": product_id},
    }


def _category_discount() -> dict:
    return {
        "discount_type": "simple",
        "percentage": 25.0,
        "context": {"obj": "category", "id": "A"},
    }


def _store_discount() -> dict:
    return {"discount_type": "simple", "percentage": 10.0, "context": {"obj": "store"}}


def _complex_max_discount() -> dict:
    return {"discount_type": "complex", "type": "max"}


def _complex_add_discount() -> dict:
    return {"discount_type": "complex", "type": "add"}


def _complex_and_discount() -> dict:
    return {"discount_type": "complex", "type": "and"}


def _complex_or_discount() -> dict:
    return {"discount_type": "complex", "type": "or"}


def _complex_xor_discount() -> dict:
    return {"discount_type": "complex", "type": "xor", "decision_rule": "first"}


def _generate_product_name() -> str:
    global product_number
    product_lock.acquire()
    product_number += 1
    product = "test_TradingSystem" + str(product_number)
    product_lock.release()
    return product


# 2.3 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#23-Registration


def test_register_success():
    new_username = _generate_username()
    password = "aaa"
    cookie = system.enter_system()
    res = system.register(cookie, new_username, password)
    assert res.succeeded()


def test_register_used_username_fail():
    existing_username = _generate_username()
    password = "aaa"
    cookie = system.enter_system()
    system.register(cookie, existing_username, password)
    res = system.register(cookie, existing_username, password)
    assert not res.succeeded()

    # 2.4 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#24-Login


def test_login_success():
    new_username = _generate_username()
    password = "aaa"
    cookie = system.enter_system()
    system.register(cookie, new_username, password)
    res = system.login(cookie, new_username, password)
    assert res.succeeded()


def test_login_wrong_username_fail():
    new_username = _generate_username()
    password = "aaa"
    wrong_username = "doorbelman"
    cookie = system.enter_system()
    system.register(cookie, new_username, password)
    res = system.login(cookie, wrong_username, password)
    assert not res.succeeded()


def test_login_wrong_password_fail():
    new_username = _generate_username()
    password = "aaa"
    wrong_password = "aa"
    cookie = system.enter_system()
    system.register(cookie, new_username, password)
    res = system.login(cookie, new_username, wrong_password)
    assert not res.succeeded()

    # 3.2 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#32-#Open-a-store
    def test_open_store_success():
        cookie, username, password, _, _ = _initialize_info(_generate_username(), "aaa")
        store_name = _generate_store_name()
        res = system.create_store(cookie, store_name)
        assert res.succeeded()


# def test_open_store_unsupported_character_fail():
#     cookie, username, password, _ = _initialize_info(_generate_username(), "aaa")
#     store_name = "stαrbucks"
#     assert not system.create_store(cookie, store_name).succeeded()
# not a fail condition

# 2.5 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#25-Getting-store-information
def test_get_store_information_success():
    store_details = system.get_stores_details()
    num_of_stores = len(store_details.object.values)
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    response = system.get_stores_details()
    assert response.succeeded() and len(response.object.values) == num_of_stores + 1


# def test_get_store_information_no_stores_fail():
#     cookie, username, password, _ = _initialize_info(_generate_username(), "aaa")
#     assert not system.get_stores_details().succeeded()  # an empty list evaluates to false
# assumed empty list means failure

# 4.1 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#41-Add-new-product
def test_add_new_product_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "A"
    price = 5.50
    quantity = 10
    response = system.create_product(cookie, store_id, product_name, category, price, quantity)
    assert response.succeeded(), response.get_msg()


def test_add_new_product_negative_quantity_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "A"
    price = 5.50
    quantity = -10
    res = system.create_product(cookie, store_id, product_name, category, price, quantity)
    assert not res.succeeded()


def test_add_new_product_negative_price_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "B"
    price = -5.50
    quantity = 10
    res = system.create_product(cookie, store_id, product_name, category, price, quantity)
    assert not res.succeeded()


def test_remove_product_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.remove_product_from_store(cookie, store_id, product_id)
    assert res.succeeded()


def test_remove_product_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    wrong_product = "cofee"
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.remove_product_from_store(cookie, store_id, wrong_product)
    assert not res.succeeded()


def test_change_product_quantity_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_quantity = 15
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    response = system.change_product_quantity_in_store(cookie, store_id, product_id, new_quantity)
    assert response.succeeded(), response.get_msg()


def test_change_product_quantity_negative_quantity_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_quantity = -15
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.change_product_quantity_in_store(cookie, store_id, product_id, new_quantity)
    assert not res.succeeded()


def test_change_product_quantity_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    wrong_product = "cofee"
    new_quantity = 15
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.change_product_quantity_in_store(cookie, store_id, wrong_product, new_quantity)
    assert not res.succeeded()


def test_edit_product_details_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_name = _generate_product_name()
    new_category = "B"
    new_price = 6.0
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.edit_product_details(
        cookie, store_id, product_id, new_name, new_category, new_price
    )
    assert res.succeeded()


def test_edit_product_details_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    wrong_product = "coffe"
    new_name = _generate_product_name()
    new_category = "B"
    new_price = 6.0
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.edit_product_details(
        cookie, store_id, wrong_product, new_name, new_category, new_price
    )
    assert not res.succeeded()


def test_edit_product_details_negative_price_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    new_name = _generate_product_name()
    new_category = "C"
    new_price = -6.0
    res = system.edit_product_details(
        cookie, store_id, product_id, new_name, new_category, new_price
    )
    assert not res.succeeded()


def test_get_product_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )

    prod_data_res = system.get_product(store_id, product_id)
    assert prod_data_res.succeeded() and prod_data_res.get_obj().name == product_name


# 2.6 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#26-Filter-search-results


def test_product_search_no_args_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    response = system.search_products(product_name)
    num_of_products = 0
    for store, products_to_quantities in response.get_obj().items():
        for product, quantity in products_to_quantities:
            num_of_products += quantity
    assert response.succeeded() and num_of_products == 10, response.get_msg()


def test_product_search_args_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    min_price = 5.0
    max_price = 6.0
    response = system.search_products(product_name, min_price=min_price, max_price=max_price)
    num_of_products = 0
    for store, products_to_quantities in response.get_obj().items():
        for product, quantity in products_to_quantities:
            num_of_products += quantity
    assert response.succeeded() and num_of_products == 10, response.get_msg()


def test_product_search_wrong_product_no_args_cant_find():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "A"
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, category, price, quantity)
    response = system.search_products(wrong_product)
    num_of_products = 0
    for store, products_to_quantities in response.get_obj().items():
        for product, quantity in products_to_quantities:
            num_of_products += quantity
    assert response.succeeded() and num_of_products == 0


def test_product_search_wrong_product_args_cant_find():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "A"
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    min_price = 5.0
    max_price = 6.0
    system.create_product(cookie, store_name, product_name, category, price, quantity)
    response = system.search_products(wrong_product, min_price=min_price, max_price=max_price)
    num_of_products = 0
    for store, products_to_quantities in response.get_obj().items():
        for product, quantity in products_to_quantities:
            num_of_products += quantity
    assert response.succeeded() and num_of_products == 0


def test_product_search_wrong_args_min_cant_find():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "A"
    price = 5.50
    quantity = 10
    min_price = 6.0
    max_price = 7.0
    system.create_product(cookie, store_name, product_name, category, price, quantity)
    response = system.search_products(product_name, min_price=min_price, max_price=max_price)
    num_of_products = 0
    for store, products_to_quantities in response.get_obj().items():
        for product, quantity in products_to_quantities:
            num_of_products += quantity
    assert response.succeeded() and num_of_products == 0


def test_product_search_wrong_args_max_cant_find():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_name = _generate_product_name()
    category = "A"
    price = 5.50
    quantity = 10
    min_price = 4.0
    max_price = 5.0
    system.create_product(cookie, store_name, product_name, category, price, quantity)
    response = system.search_products(product_name, min_price=min_price, max_price=max_price)
    num_of_products = 0
    for store, products_to_quantities in response.get_obj().items():
        for product, quantity in products_to_quantities:
            num_of_products += quantity
    assert response.succeeded() and num_of_products == 0


def test_products_by_store_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    response = system.get_products_by_store(store_id)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_products_by_store_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_store = "starbux"
    response = system.get_products_by_store(wrong_store)
    assert not response.succeeded()

    # # 2.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#27-Save-products-in-shopping-bag


def test_add_to_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.save_product_in_cart(cookie, store_id, product_id, 1)
    assert res.succeeded()


def test_add_to_cart_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_product = "cofee"
    res = system.save_product_in_cart(cookie, store_id, wrong_product, 1)
    assert not res.succeeded()


def test_add_to_cart_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_store = "starbux"
    res = system.save_product_in_cart(cookie, wrong_store, product_id, 1)
    assert not res.succeeded()


def test_add_to_cart_quantity_too_high_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    res = system.save_product_in_cart(cookie, store_id, product_id, 11)
    assert not res.succeeded()

    # # 2.8 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#28-Visit-cart


def test_visit_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and len(response.object.bags) == 1
        and response.object.bags[0].store_name == store_name
        and len(response.object.bags[0].product_ids_to_quantities) == 1
        and response.object.bags[0].product_ids_to_quantities[product_id] == 1
    ), response.get_msg()


# def test_visit_cart_no_items_fail():
#     cookie, username, password, store_name, store_id = _initialize_info(
#         _generate_username(), "aaa", _generate_store_name()
#     )
#     assert not system.get_cart_details(cookie).succeeded()
#   assumed empty list means failure


def test_change_amount_in_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = system.change_product_quantity_in_cart(cookie, store_id, product_id, 2)
    cart_details_res = system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and cart_details_res.object.bags[0].product_ids_to_quantities[product_id] == 2
    ), response.get_msg()


def test_change_amount_in_cart_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_product = "cofee"
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.change_product_quantity_in_cart(cookie, store_id, wrong_product, 2)
    assert not res.succeeded()


def test_change_amount_in_cart_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_store = "starbux"
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.change_product_quantity_in_cart(cookie, wrong_store, product_id, 2)
    assert not res.succeeded()


def test_change_amount_in_cart_negative_quantity_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.change_product_quantity_in_cart(cookie, store_id, product_id, -1)
    assert not res.succeeded()


def test_change_amount_in_cart_quantity_too_high_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.change_product_quantity_in_cart(cookie, store_id, product_id, 11)
    assert not res.succeeded()


def test_remove_product_from_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.remove_product_from_cart(cookie, store_id, product_id)
    assert res.succeeded()


def test_remove_product_from_cart_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_product = "cofee"
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.remove_product_from_cart(cookie, store_id, wrong_product)
    assert not res.succeeded()


def test_remove_product_from_cart_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    wrong_store = "starbux"
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = system.remove_product_from_cart(cookie, wrong_store, product_id)
    assert not res.succeeded()


# 2.9 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#29-Purchase-products
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_purchase_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    store_res = system.get_store(store_id)
    cart_res = system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 9
        and cart_res.succeeded()
        and response.object.value == price
    ), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_purchase_cart_no_items_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    user_age = 25
    res = system.purchase_cart(cookie, user_age)
    assert not res.succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_purchase_cart_twice_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    response = system.purchase_cart(cookie)
    assert not response.succeeded(), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_send_payment_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    response = system.send_payment(cookie, "", "")
    res = system.get_store(store_id)
    ids_to_quantity = res.object.ids_to_quantities[product_id]
    assert response.succeeded() and ids_to_quantity == 9, response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_send_payment_success_guest():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )

    cookie_g = system.enter_system()
    system.save_product_in_cart(cookie_g, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie_g, user_age)
    response = system.send_payment(cookie_g, "", "")
    res = system.get_store(store_id)
    ids_to_quantity = res.object.ids_to_quantities[product_id]
    assert response.succeeded() and ids_to_quantity == 9, response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_send_payment_success_timer_over():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    response = system.send_payment(cookie, "", "")
    timer = threading.Timer(
        6, finish_test_send_payment_success_timer_over(store_id, product_id, response)
    )
    timer.start()


def finish_test_send_payment_success_timer_over(store_id, product_id, response):
    res2 = system.get_store(store_id)
    assert (
        response.succeeded() and res2.object.ids_to_quantities[product_id] == 9
    ), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_send_payment_before_purchase_cart_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    res1 = system.send_payment(cookie, "", "")
    res2 = system.get_store(store_id)
    res2 = res2.object.ids_to_quantities[product_id]
    res3 = system.get_cart_details(cookie)
    assert not res1.succeeded() and res2 == 10 and res3.succeeded()


# bad scenarios
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_paying_after_time_passed():
    import time

    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    time.sleep(6)
    res1 = system.send_payment(cookie, "", "")
    res2 = system.get_store(store_id)
    res3 = system.get_cart_details(cookie)
    assert (
        not res1.succeeded()
        and res2.object.ids_to_quantities[product_id] == 10
        and res3.object.bags[0].product_ids_to_quantities[product_id] == 1
    )


# region payment system mocks
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_send_payment_failed():
    with mock.patch.object(OutsideCashing, "pay", return_value=False):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        res1 = system.send_payment(cookie, "", "")
        # this line is added since the user might cancel the purchase after unsuccessful payment
        res_cancel = system.cancel_purchase(cookie)
        res2 = system.get_store(store_id)
        res3 = system.get_cart_details(cookie)
        assert (
            res_cancel.succeeded()
            and not res1.succeeded()
            and res2.object.ids_to_quantities[product_id] == 10
            and res3.object.bags[0].product_ids_to_quantities[product_id] == 1
        )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_paying_first_time_failed_than_success():
    with mock.patch.object(OutsideCashing, "pay", return_value=False):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id)
    assert (
        not response.succeeded()
        and try_again_response.succeeded()
        and get_response.object.ids_to_quantities[product_id] == 9
    )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_paying_first_time_incorrect_info_second_time_timer_over():
    import time

    with mock.patch.object(OutsideCashing, "pay", return_value=False):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    time.sleep(6)
    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id).object.ids_to_quantities[product_id]
    assert not response.succeeded() and not try_again_response.succeeded() and get_response == 10


# endregion

# region supply systems mocks
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_supply_order_failed():
    with mock.patch.object(OutsideSupplyment, "deliver", return_value=False):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        res1 = system.send_payment(cookie, "", "")
        # this line is added since the user might cancel the purchase after unsuccessful payment
        res_cancel = system.cancel_purchase(cookie)
        res2 = system.get_store(store_id)
        res3 = system.get_cart_details(cookie)
        assert (
            res_cancel.succeeded()
            and not res1.succeeded()
            and res2.object.ids_to_quantities[product_id] == 10
            and res3.object.bags[0].product_ids_to_quantities[product_id] == 1
        )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_supply_first_time_failed_than_success():
    with mock.patch.object(OutsideSupplyment, "deliver", return_value=False):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id)
    assert (
        not response.succeeded()
        and try_again_response.succeeded()
        and get_response.object.ids_to_quantities[product_id] == 9
    )


# todo: make this test pass
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_supply_first_time_exception_second_time_timer_over():
    import time

    with mock.patch.object(OutsideSupplyment, "deliver", return_value=Exception()):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    time.sleep(6)
    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id).object.ids_to_quantities[product_id]
    assert not response.succeeded() and not try_again_response.succeeded() and get_response == 10


# endregion


# 3.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#37-Get-personal-purchase-history
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_get_purchase_history_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    response = system.get_purchase_history(cookie)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].product_names[0] == product_name
    )


# def test_get_purchase_history_no_purchases_fail():
#     cookie, username, password, store_name, store_id = _initialize_info(
#         _generate_username(), "aaa", _generate_store_name()
#     )
#     product_name = _generate_product_name()
#     category = "A"
#     price = 5.50
#     quantity = 10
#     system.create_product(cookie, store_name, product_name, category, price, quantity)
#     response = system.get_purchase_history(cookie)
#     assert not response.succeeded()
# assumed empty list means failure


def test_get_purchase_history_no_purchases_saved_to_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = system.get_purchase_history(cookie)
    assert len(response.object.values) == 0


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_get_purchase_history_no_payment_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    response = system.get_purchase_history(cookie)
    assert len(response.object.values) == 0

    # 4.3 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#43-Appoint-new-store-owner


def test_appoint_store_owner_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    response = system.appoint_owner(cookie, store_id, new_owner_username)
    assert response.succeeded(), response.get_msg()


def test_appoint_store_owner_chain_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    res = system.appoint_owner(new_owner_cookie, store_id, last_owner_username)
    assert res.succeeded()


def test_appoint_store_owner_wrong_name_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    wrong_name = "Ravit Ron"
    res = system.appoint_owner(cookie, store_id, wrong_name)
    assert not res.succeeded()


def test_appoint_store_owner_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    wrong_store = "starbux"
    res = system.appoint_owner(cookie, wrong_store, new_owner_username)
    assert not res.succeeded()


def test_appoint_store_owner_direct_circular_appointment_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    res = system.appoint_owner(new_owner_cookie, store_id, username)
    assert not res.succeeded()


def test_appoint_store_owner_circular_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    system.appoint_owner(new_owner_cookie, store_id, last_owner_username)
    res = system.appoint_owner(last_owner_cookie, store_id, username)
    assert not res.succeeded()

    # 4.5 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#45-Appoint-new-store-manager


def test_appoint_store_manager_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    res = system.appoint_manager(cookie, store_id, new_manager_username)
    assert res.succeeded()


# def test_appoint_store_manager_manager_chain_success():
#     cookie, username, password, store_name, store_id = _initialize_info(
#         _generate_username(), "aaa", _generate_store_name()
#     )
#     new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
#         _generate_username(), "bbb"
#     )
#     last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
#         _generate_username(), "ccc"
#     )
#     system.appoint_manager(cookie, store_name, new_manager_username)
#     assert system.appoint_manager(new_manager_cookie, store_name, last_manager_username).succeeded()
# tested elsewhere


def test_appoint_store_owner_manager_chain_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    res = system.appoint_manager(new_owner_cookie, store_id, last_manager_username)
    assert res.succeeded()


def test_appoint_store_manager_wrong_name_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    wrong_name = "Ravit Ron"
    res = system.appoint_manager(cookie, store_id, wrong_name)
    assert not res.succeeded()


def test_appoint_store_manager_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    wrong_store = "starbux"
    res = system.appoint_manager(cookie, wrong_store, new_manager_username)
    assert not res.succeeded()


def test_appoint_store_manager_direct_circular_appointment_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    res = system.appoint_manager(new_manager_cookie, store_id, username)
    assert not res.succeeded()


# def test_appoint_store_manager_circular_fail():
#     cookie, username, password, store_name, store_id = _initialize_info(
#         _generate_username(), "aaa", _generate_store_name()
#     )
#     new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
#         _generate_username(), "bbb"
#     )
#     last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
#         _generate_username(), "ccc"
#     )
#     system.appoint_manager(cookie, store_id, new_manager_username)
#     system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
#     assert not system.appoint_manager(last_manager_cookie, store_name, username).succeeded()
# tested elsewhere


def test_appoint_store_manager_owner_chain_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    res = system.appoint_owner(new_manager_cookie, store_id, last_owner_username)
    assert not res.succeeded()

    # 4.6 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#46-Edit-manager%E2%80%99s-responsibilities
    # def test_add_responsibility_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    new_responsibility = "remove manager"
    system.appoint_manager(cookie, store_id, new_manager_username)
    response = system.add_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility
    )
    assert response.succeeded(), response.get_msg()


def test_remove_responsibility_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    new_responsibility = "remove manager"
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, new_responsibility)
    res = system.remove_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility
    )
    assert res.succeeded()


def test_default_permissions_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )

    default_permission = "get appointments"
    other_permissions = ["remove manager", "manage products", "appoint manager", "get history"]
    system.appoint_manager(cookie, store_id, new_manager_username)
    res = system.remove_manager_permission(
        cookie, store_id, new_manager_username, default_permission
    )
    assert res.succeeded()
    for responsibility in other_permissions:
        res_2 = system.add_manager_permission(
            cookie, store_id, new_manager_username, responsibility
        )
        assert res_2.succeeded()


def test_add_responsibility_twice_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    new_responsibility = "remove manager"
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, new_responsibility)
    res = system.add_manager_permission(cookie, store_id, new_manager_username, new_responsibility)
    assert res.succeeded()


def test_remove_responsibility_twice_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    new_responsibility = "remove manager"
    system.appoint_manager(cookie, store_id, new_manager_username)
    res = system.remove_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility
    )
    assert res.succeeded()


def test_get_appointment_permission_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    response = system.get_store_appointments(new_manager_cookie, store_id)
    assert response.succeeded(), response.get_msg()


def test_get_history_permission_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, "get history")
    res = system.get_store_purchase_history(new_manager_cookie, store_id)
    assert res.succeeded()


def test_appoint_manager_permission_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, "appoint manager")
    res = system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
    assert res.succeeded()


def test_remove_manager_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.appoint_manager(cookie, store_id, last_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, "remove manager")
    res = system.remove_appointment(new_manager_cookie, store_id, last_manager_username)
    assert not res.succeeded()


def test_remove_manager_permission_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, "appoint manager")
    system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, "remove manager")
    response = system.remove_appointment(new_manager_cookie, store_id, last_manager_username)
    assert response.succeeded(), response.get_msg()


def test_manage_products_permission_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.add_manager_permission(cookie, store_id, new_manager_username, "manage products")
    product_name = _generate_product_name()
    category = "A"
    price = 5.50
    quantity = 10
    response = system.create_product(
        new_manager_cookie, store_id, product_name, category, price, quantity
    )
    assert response.succeeded(), response.get_msg()


def test_get_appointment_no_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.remove_manager_permission(cookie, store_id, new_manager_username, "get appointments")
    res = system.get_store_appointments(new_manager_cookie, store_id)
    assert not res.succeeded()


def test_get_history_no_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    res = system.get_store_purchase_history(new_manager_cookie, store_id)
    assert not res.succeeded()


def test_appoint_manager_no_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    res = system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
    assert not res.succeeded()


def test_remove_manager_no_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    system.appoint_manager(cookie, store_id, last_manager_username)
    res = system.remove_appointment(new_manager_cookie, store_id, last_manager_username)
    assert not res.succeeded()


def test_manage_products_no_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    product_name = _generate_product_name()
    category = "A"
    price = 5.50
    quantity = 10
    res = system.create_product(
        new_manager_cookie, store_id, product_name, category, price, quantity
    )
    assert not res.succeeded()

    # 4.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#43-Dismiss-an-owner
    # def test_dismiss_owner_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    response = system.remove_appointment(cookie, store_id, new_owner_username)
    assert response.succeeded()


def test_dismiss_owner_wrong_name_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    wrong_name = "Ravit Ron"
    system.appoint_owner(cookie, store_id, new_owner_username)
    res = system.remove_appointment(cookie, store_id, wrong_name)
    assert not res.succeeded()


def test_dismiss_owner_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    wrong_store = "starbux"
    system.appoint_owner(cookie, store_id, new_owner_username)
    res = system.remove_appointment(cookie, wrong_store, new_owner_username)
    assert not res.succeeded()


def test_dismiss_owner_appointing_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    system.remove_appointment(cookie, store_id, new_owner_username)
    res = system.appoint_manager(new_owner_cookie, store_id, last_manager_username)
    assert not res.succeeded()


def test_dismiss_owner_chain_appointing_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = _initialize_info(
        _generate_username(), "ccc"
    )
    final_manager_cookie, final_manager_username, final_manager_password, _, _ = _initialize_info(
        _generate_username(), "ddd"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    system.appoint_owner(new_owner_cookie, store_id, last_owner_username)
    system.remove_appointment(cookie, store_id, new_owner_username)
    res = system.appoint_manager(last_owner_cookie, store_id, final_manager_username)
    assert not res.succeeded()

    # 4.9 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#49-Get-store-personnel-information
    # def test_get_store_personnel_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    response = system.get_store_appointments(cookie, store_id)
    assert (
        response.succeeded()
        and response.object.username == username
        and response.object.role == "Founder"
    )


def test_get_store_personnel_owner_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    response = system.get_store_appointments(cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.appointees) == 1
        and response.object.appointees[0].username == new_owner_username
        and response.object.appointees[0].role == "Owner"
    )


def test_get_store_personnel_manager_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_manager(cookie, store_id, new_manager_username)
    response = system.get_store_appointments(cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.appointees) == 1
        and response.object.appointees[0].username == new_manager_username
        and response.object.appointees[0].role == "Manager"
    )


def test_get_store_personnel_wrong_store_name_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    wrong_store = "starbux"
    res = system.get_store_appointments(cookie, wrong_store)
    assert not res.succeeded()


# 4.11 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#411-Get-store-purchase-history
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_get_store_purchase_history_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    response = system.get_store_purchase_history(cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].product_names[0] == product_name
    )


# def test_get_store_purchase_history_no_purchases_fail():
#     cookie, username, password, store_name, store_id = _initialize_info(
#         _generate_username(), "aaa", _generate_store_name()
#     )
#     product_name = _generate_product_name()
#     category = "A"
#     price = 5.50
#     quantity = 10
#     system.create_product(cookie, store_name, product_name, category, price, quantity)
#     response = system.get_store_purchase_history(cookie, store_name)
#     assert response.succeeded()
# assumed empty list means failure


def test_get_store_purchase_history_no_purchases_saved_to_cart_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = system.get_store_purchase_history(cookie, store_id)
    assert len(response.object.values) == 0


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_get_store_purchase_history_no_payment_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    response = system.get_store_purchase_history(cookie, store_id)
    assert len(response.object.values) == 0


# # 6.4 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#64-Get-store-purchase-history-system-manager

def _get_admin() -> str:
    admin_cookie = system.enter_system()
    settings = Settings.get_instance(True)
    system.login(admin_cookie, settings.get_admins()[0], settings.get_password())
    return admin_cookie


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_admin_get_store_purchase_history_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    admin_cookie = _get_admin()
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_ccv = "123"
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    response = system.get_any_store_purchase_history(admin_cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].product_names[0] == product_name
    ), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_admin_get_user_purchase_history_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    admin_cookie = _get_admin()
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    response = system.get_user_purchase_history(admin_cookie, username)
    assert response.succeeded()


# region parallel testing
_t_responses = []


def __get_product(cookie: str, thread: int) -> None:
    global _t_responses
    response = system.purchase_cart(cookie, 25)
    _t_responses.append((thread, response.succeeded()))


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_buy_last_product_together_fail():
    for i in range(100):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        new_cookie, new_username, new_password_, _, _ = _initialize_info(
            _generate_username(), "aaa"
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 1
        )
        system.save_product_in_cart(cookie, store_id, product_id, quantity=1)
        system.save_product_in_cart(new_cookie, store_id, product_id, quantity=1)
        t1 = threading.Thread(target=lambda: __get_product(cookie, 1))
        t2 = threading.Thread(target=lambda: __get_product(new_cookie, 2))
        t1.start()
        t2.start()
        t2.join()
        t1.join()
        assert not (_t_responses[i * 2][1] and _t_responses[i * 2 + 1][1])


def _remove_product(cookie: str, store_id: str, product_id: str, thread: str) -> None:
    global _t_responses
    response = system.remove_product_from_store(cookie, store_id, product_id)
    if response.succeeded():
        _t_responses.append((thread, response.get_obj().get_val()))
    else:
        _t_responses.append((thread, False))


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_buy_delete_product():
    global _t_responses
    _t_responses = []
    for i in range(100):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        new_manager_cookie, new_manager_username, new_manager_password, _, _ = _initialize_info(
            _generate_username(), "bbb"
        )
        system.appoint_manager(cookie, store_id, new_manager_username)
        system.add_manager_permission(cookie, store_id, new_manager_username, "appoint manager")
        system.add_manager_permission(cookie, store_id, new_manager_username, "manage products")
        product_id, product_name, category, price, quantity = _create_product(
            new_manager_cookie, store_id, _generate_product_name(), "A", 5.50, 3
        )
        system.save_product_in_cart(cookie, store_id, product_id, quantity=1)

        t1 = threading.Thread(
            target=lambda: _remove_product(new_manager_cookie, store_id, product_id, "owner")
        )
        t2 = threading.Thread(target=lambda: __get_product(cookie, 2))
        t1.start()
        t2.start()
        t2.join()
        t1.join()
        # assert not (_t_responses[i * 2][1] and _t_responses[i * 2 + 1][1])
        if _t_responses[i * 2][1] and _t_responses[i * 2 + 1][1]:
            assert (
                _t_responses[i * 2][1] == quantity - 1 or _t_responses[i * 2 + 1][1] == quantity - 1
            )
        else:
            assert _t_responses[i * 2][1] == quantity or _t_responses[i * 2 + 1][1] == quantity


def __appoint_manager(cookie, store_id, username, thread: int):
    global _t_responses
    response = system.appoint_manager(cookie, store_id, username)
    if response.succeeded():
        _t_responses.append((thread, True))
    else:
        _t_responses.append((thread, False))


def test_two_appointments():
    global _t_responses
    _t_responses = []
    for i in range(100):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        owner_cookie, owner_username, owner_password, _, _ = _initialize_info(
            _generate_username(), "aaa"
        )
        system.appoint_owner(cookie, store_id, owner_username)
        manager_cookie, manager_username, manager_password, _, _ = _initialize_info(
            _generate_username(), "aaa"
        )
        t1 = threading.Thread(
            target=lambda: __appoint_manager(cookie, store_id, manager_username, 1)
        )
        t2 = threading.Thread(
            target=lambda: __appoint_manager(owner_cookie, store_id, manager_username, 2)
        )
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        a = _t_responses[i * 2]
        b = _t_responses[i * 2 + 1]
        assert (a[1] and not b[1]) or (not a[1] and b[1])  # exactly one to succeed


# endregion

# region notifications tests


def apply(owner_queue, messages):
    for message in messages:
        owner_queue.put(message)
    return True


def _initialize_info_notifications(
    username: str, password: str, connect: bool, store_name: str = None, owner_queue=None
) -> tuple[str, str, str, str, str]:
    store_id = ""
    cookie = system.enter_system()

    if connect:
        system.connect(cookie, lambda messages: apply(owner_queue, messages))
    system.register(cookie, username, password)
    system.login(cookie, username, password)
    if store_name:
        store_res = system.create_store(cookie, store_name)
        store_id = store_res.object
    return cookie, username, password, store_name, store_id


def test_store_owner_notification_after_purchase():
    first_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", True, _generate_store_name(), owner_queue=first_owner_queue
    )
    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(new_cookie, store_id, product_id, 1)
    user_age = 25
    price = system.purchase_cart(new_cookie, user_age)
    system.send_payment(new_cookie, "", "")
    assert (not first_owner_queue.empty()) and system.empty_notifications(cookie)


def test_store_owner_notification_after_purchase_owner_not_connected():
    first_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", False, _generate_store_name()
    )
    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(new_cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(new_cookie, user_age)
    system.send_payment(new_cookie, "", "")
    assert first_owner_queue.empty() and not system.empty_notifications(cookie)


def test_store_multiple_owners_notification_after_purchase_all_connected():
    first_owner_queue = Queue()
    second_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", True, _generate_store_name(), first_owner_queue
    )

    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    system.connect(new_owner_cookie, lambda messages: apply(second_owner_queue, messages))
    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(new_cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(new_cookie, user_age)
    system.send_payment(new_cookie, "", "")
    assert (
        not first_owner_queue.empty()
        and not second_owner_queue.empty()
        and system.empty_notifications(cookie)
        and system.empty_notifications(new_owner_cookie)
    )


def test_store_multiple_owners_notification_after_purchase_one_connected():
    first_owner_queue = Queue()
    second_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", False, _generate_store_name(), first_owner_queue
    )

    new_owner_cookie, new_owner_username, new_owner_password, _, _ = _initialize_info(
        _generate_username(), "bbb"
    )
    system.appoint_owner(cookie, store_id, new_owner_username)
    system.connect(new_owner_cookie, lambda messages: apply(second_owner_queue, messages))
    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(new_cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(new_cookie, user_age)
    system.send_payment(new_cookie, "", "")
    assert (
        first_owner_queue.empty()
        and not second_owner_queue.empty()
        and not system.empty_notifications(cookie)
        and system.empty_notifications(new_owner_cookie)
    )


def test_connect_after_notification_sent():
    first_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", False, _generate_store_name(), first_owner_queue
    )
    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(new_cookie, store_id, product_id, 1)
    user_age = 25
    system.purchase_cart(new_cookie, user_age)
    system.send_payment(new_cookie, "", "")
    first_queue_before_connect_empty = first_owner_queue.empty()
    pending_before_connect_empty = system.empty_notifications(cookie)
    system.connect(cookie, lambda messages: apply(first_owner_queue, messages))
    assert (
        first_queue_before_connect_empty
        and not pending_before_connect_empty
        and not first_owner_queue.empty()
        and system.empty_notifications(cookie)
    )


def test_get_notification_after_remove_appointment_connected():
    first_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", False, _generate_store_name()
    )
    new_cookie, new_username, new_password_, _, _ = _initialize_info_notifications(
        _generate_username(), "bbb", connect=True, owner_queue=first_owner_queue
    )
    system.appoint_manager(cookie, store_id, new_username)
    system.remove_appointment(cookie, store_id, new_username)
    assert not first_owner_queue.empty() and system.empty_notifications(new_cookie)


def test_get_notification_after_remove_appointment_not_connected():
    first_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", False, _generate_store_name()
    )
    new_cookie, new_username, new_password_, _, _ = _initialize_info_notifications(
        _generate_username(), "bbb", connect=False
    )
    system.appoint_manager(cookie, store_id, new_username)
    system.remove_appointment(cookie, store_id, new_username)
    assert first_owner_queue.empty() and not system.empty_notifications(new_cookie)


def test_connect_after_get_notification():
    first_owner_queue = Queue()
    cookie, username, password, store_name, store_id = _initialize_info_notifications(
        _generate_username(), "aaa", False, _generate_store_name()
    )
    new_cookie, new_username, new_password_, _, _ = _initialize_info_notifications(
        _generate_username(), "bbb", connect=False
    )

    system.appoint_manager(cookie, store_id, new_username)
    system.remove_appointment(cookie, store_id, new_username)
    first_queue_before_connect_empty = first_owner_queue.empty()
    pending_before_connect_empty = system.empty_notifications(new_cookie)
    system.connect(new_cookie, lambda messages: apply(first_owner_queue, messages))
    assert (
        first_queue_before_connect_empty
        and not pending_before_connect_empty
        and not first_owner_queue.empty()
        # I (Ravid) am adding a not here. The new user got notifications for being appointed and removed.
        and not system.empty_notifications(cookie)
    )


# endregion


# region 4.2  purchase tests

# region add_purchase_rules
def test_purchase_add_simple_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age(), "simple", parent_id
    )
    assert response_add.succeeded()


def test_purchase_add_simple_rule_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age_invalid_operator(), "simple", parent_id
    )
    assert not response_add.succeeded()


def test_purchase_add_simple_rule_missing_key_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age_missing_key_target(), "simple", parent_id
    )
    assert not response_add.succeeded()


def test_purchase_add_complex_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert response_add.succeeded()


def test_purchase_add_complex_rule_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_invalid_operator(), "complex", parent_id
    )
    assert not response_add.succeeded()


def test_purchase_add_complex_missing_key_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_missing_operator(), "complex", parent_id
    )
    assert not response_add.succeeded()


def test_purchase_add_complex_success_simple_child_invalid():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    parent_or_id = "2"
    response_add_simple = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age_invalid_operator(), "simple", parent_or_id
    )
    assert response_add_complex.succeeded() and not response_add_simple.succeeded()


def test_purchase_add_child_rule_to_not_existing_parent():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "2"
    response_add_complex = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert not response_add_complex.succeeded()


def test_purchase_add_rule_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        new_cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert not response_add_complex.succeeded()


def test_purchase_add_rule_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        new_cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert not response_add_complex.succeeded()


def test_purchase_add_rule_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage purchase policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        new_cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert response_add_complex.succeeded()


def test_purchase_founder_add_rule_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        new_cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert not response_add_complex.succeeded()


def test_purchase_founder_add_rule_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    response_add_complex_wrong_store = system.add_purchase_rule(
        new_cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )

    response_add_complex_right_store = system.add_purchase_rule(
        new_cookie, new_store_id, _complex_rule_details_or(), "complex", parent_id
    )
    assert not response_add_complex_wrong_store.succeeded() and response_add_complex_right_store


def test_purchase_add_complex_with_two_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    response_add_simple_first = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age(), "simple", "2"
    )
    response_add_simple_second = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_product(), "simple", "2"
    )
    assert (
        response_add_complex.succeeded()
        and response_add_simple_first.succeeded()
        and response_add_simple_second.succeeded()
    )


def test_purchase_add_complex_conditioning():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )

    response_add_simple_first = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age(), "simple", "2", clause="test"
    )
    response_add_simple_second = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_product(), "simple", "2", clause="then"
    )

    assert (
        response_add_complex.succeeded()
        and response_add_simple_first.succeeded()
        and response_add_simple_second.succeeded()
    )


def test_purchase_add_complex_two_conditioning():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add_complex = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    response_add_complex_second = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    response_add_simple_rule = system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age(), "simple", "3", clause="test"
    )

    assert (
        response_add_complex.succeeded()
        and response_add_complex_second.succeeded()
        and response_add_simple_rule.succeeded()
    )


# endregion

# region remove_purchase_rules


def test_remove_conditional():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    response_remove = system.remove_purchase_rule(cookie, store_id, "2")
    assert response_remove.succeeded()


def test_purchase_remove_simple_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_remove = system.remove_purchase_rule(cookie, store_id, "2")
    assert response_remove.succeeded()


def test_purchase_remove_not_existing_rule():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age_invalid_operator(), "simple", parent_id
    )
    response_remove = system.remove_purchase_rule(cookie, store_id, "3")
    assert not response_remove.succeeded()


def test_purchase_remove_root_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    response_remove = system.remove_purchase_rule(cookie, store_id, "1")
    assert not response_remove.succeeded()


def test_purchase_complex_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_remove = system.remove_purchase_rule(cookie, store_id, "2")
    assert response_remove.succeeded()


def test_purchase_remove_rule_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_remove_complex = system.remove_purchase_rule(new_cookie, store_id, "2")
    assert not response_remove_complex.succeeded()


def test_purchase_remove_rule_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_remove_complex = system.remove_purchase_rule(new_cookie, store_id, "2")
    assert not response_remove_complex.succeeded()


def test_purchase_remove_rule_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage purchase policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_remove_complex = system.remove_purchase_rule(new_cookie, store_id, "2")
    assert response_remove_complex.succeeded()


def test_purchase_founder_remove_rule_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_remove_complex = system.remove_purchase_rule(new_cookie, store_id, "2")
    assert not response_remove_complex.succeeded()


def test_purchase_founder_remove_rule_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(
        new_cookie, new_store_id, _complex_rule_details_or(), "complex", parent_id
    )
    response_remove_wrong = system.remove_purchase_rule(new_cookie, store_id, "2")
    response_remove_right = system.remove_purchase_rule(new_cookie, new_store_id, "2")
    assert not response_remove_wrong.succeeded() and response_remove_right


def test_purchase_remove_complex_with_two_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", "2")
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_product(), "simple", "2")
    response_remove = system.remove_purchase_rule(cookie, store_id, "2")
    assert response_remove.succeeded()


# endregion

# region edit_purchase_rules
def test_purchase_edit_simple_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _simple_rule_details_age_edited(), "2", "simple"
    )
    assert response_edit.succeeded()


def test_purchase_edit_simple_rule_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _simple_rule_details_age_invalid_operator(), "2", "simple"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_simple_rule_missing_key_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age_missing_key_target(), "simple", parent_id
    )
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _simple_rule_details_age_missing_key_target(), "2", "simple"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_complex_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert response_edit.succeeded()


def test_purchase_edit_complex_rule_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _complex_rule_details_invalid_operator(), "2", "complex"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_complex_missing_key_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _complex_rule_details_missing_operator(), "2", "complex"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_complex_success_simple_child_invalid():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    parent_or_id = "2"
    system.add_purchase_rule(
        cookie, store_id, _simple_rule_details_age_invalid_operator(), "simple", parent_or_id
    )
    response_edit_complex = system.edit_purchase_rule(
        cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    response_edit_simple = system.edit_purchase_rule(
        cookie, store_id, _simple_rule_details_age_invalid_operator(), "3", "simple"
    )
    assert response_edit_complex.succeeded() and not response_edit_simple.succeeded()


def test_purchase_edit_child_not_existing_rule():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "2"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        cookie, store_id, _complex_rule_details_and(), "3", "complex"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_rule_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        new_cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_rule_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        new_cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert not response_edit.succeeded()


def test_purchase_edit_rule_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage purchase policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    added = system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_or(), "complex", parent_id
    )
    response_edit = system.edit_purchase_rule(
        new_cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert response_edit.succeeded()


def test_purchase_founder_edit_rule_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit = system.edit_purchase_rule(
        new_cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert not response_edit.succeeded()


def test_purchase_founder_edit_rule_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_purchase_rule(
        new_cookie, new_store_id, _complex_rule_details_or(), "complex", parent_id
    )
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_edit_wrong = system.edit_purchase_rule(
        new_cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    response_edit_right = system.edit_purchase_rule(
        new_cookie, new_store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert response_edit_right.succeeded() and not response_edit_wrong.succeeded()


def test_purchase_edit_complex_with_two_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", "2")
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_product(), "simple", "2")
    response_edit_right = system.edit_purchase_rule(
        cookie, store_id, _complex_rule_details_and(), "2", "complex"
    )
    assert response_edit_right.succeeded()


# endregion

# region move_purchase_rules
def test_purchase_move_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_move = system.move_purchase_rule(cookie, store_id, "3", "2")
    assert response_move.succeeded()


def test_purchase_move_rule_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_move = system.move_purchase_rule(new_cookie, store_id, "3", "2")
    assert not response_move.succeeded()


def test_purchase_move_rule_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_move = system.move_purchase_rule(new_cookie, store_id, "3", "2")
    assert not response_move.succeeded()


def test_purchase_move_rule_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage purchase policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_move = system.move_purchase_rule(new_cookie, store_id, "3", "2")
    assert response_move.succeeded()


def test_purchase_founder_move_rule_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_move = system.move_purchase_rule(new_cookie, store_id, "3", "2")
    assert not response_move.succeeded()


def test_purchase_founder_move_rule_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    system.add_purchase_rule(
        new_cookie, new_store_id, _complex_rule_details_or(), "complex", parent_id
    )
    system.add_purchase_rule(
        new_cookie, new_store_id, _simple_rule_details_age(), "simple", parent_id
    )
    response_move_wrong = system.move_purchase_rule(new_cookie, store_id, "3", "2")
    response_move_right = system.move_purchase_rule(new_cookie, new_store_id, "3", "2")
    assert response_move_right.succeeded() and not response_move_wrong.succeeded()


def test_purchase_move_complex_with_children_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_and(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", "3")
    response_move = system.move_purchase_rule(cookie, store_id, "3", "2")
    assert response_move.succeeded()


def test_purchase_move_root_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    response_move = system.move_purchase_rule(cookie, store_id, "1", "2")
    assert not response_move.succeeded()


def test_purchase_move_to_leaf_as_parent_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    response_move = system.move_purchase_rule(cookie, store_id, "2", "3")
    assert not response_move.succeeded()


# endregion

# region buy_products_with purchase rules


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
# age
def test_purchase_cart_with_simple_age_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    assert system.purchase_cart(cookie, user_age).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_age_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", parent_id)
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 17
    assert not system.purchase_cart(cookie, user_age).succeeded()


# product
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_product_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 9
    )
    product_simple_rule = {
        "context": {"obj": "product", "identifier": product_id},
        "operator": "less-than",
        "target": 6,
    }
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "1")
    system.save_product_in_cart(cookie, store_id, product_id, 5)
    assert system.purchase_cart(cookie, 20).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_product_rule_failed():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 9
    )
    product_simple_rule = {
        "context": {"obj": "product", "identifier": product_id},
        "operator": "less-than",
        "target": 6,
    }
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "1")
    system.save_product_in_cart(cookie, store_id, product_id, 8)
    assert not system.purchase_cart(cookie, 20).succeeded()


# category
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_category_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 9.50, 4
    )

    product_simple_rule = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 10,
    }
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "1")
    system.save_product_in_cart(cookie, store_id, product_id, 7)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    assert system.purchase_cart(cookie, 20).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_category_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 9.50, 4
    )

    product_simple_rule = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 10,
    }
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "1")
    system.save_product_in_cart(cookie, store_id, product_id, 5)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    assert not system.purchase_cart(cookie, 20).succeeded()


# bag
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_bag_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.0, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )

    product_simple_rule = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "1")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    assert system.purchase_cart(cookie, 20).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_bag_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.0, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )

    product_simple_rule = {"context": {"obj": "bag"}, "operator": "great-than", "target": 60}
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "1")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    assert not system.purchase_cart(cookie, 20).succeeded()


# or
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_or_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 9
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", "2")
    product_simple_rule = {
        "context": {"obj": "product", "identifier": product_id},
        "operator": "less-than",
        "target": 10,
    }
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "2")
    system.save_product_in_cart(cookie, store_id, product_id, 9)
    user_age = 17
    assert system.purchase_cart(cookie, user_age).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_or_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 9
    )
    parent_id = "1"
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", "2")
    product_simple_rule = {
        "context": {"obj": "product", "identifier": product_id},
        "operator": "less-than",
        "target": 6,
    }
    system.add_purchase_rule(cookie, store_id, product_simple_rule, "simple", "2")
    system.save_product_in_cart(cookie, store_id, product_id, 9)
    user_age = 17
    assert not system.purchase_cart(cookie, user_age).succeeded()


# and
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_and_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 6,
    }
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_and(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    assert system.purchase_cart(cookie, user_age).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_and_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.0, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 7,
    }
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_and(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    assert not system.purchase_cart(cookie, user_age).succeeded()


# conditioning


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_conditioning_rule_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 6,
    }
    system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2", clause="test")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2", clause="then")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    assert system.purchase_cart(cookie, user_age).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_conditioning_rule_success_test_clause_false():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 60}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 6,
    }
    system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2", clause="test")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2", clause="then")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    assert system.purchase_cart(cookie, user_age).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_conditioning_rule_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 8,
    }
    system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2", clause="test")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2", clause="then")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    assert not system.purchase_cart(cookie, user_age).succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_condition_fail_then_remove_purchase_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 8,
    }
    system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2", clause="test")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2", clause="then")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    response_with_condition = system.purchase_cart(cookie, user_age)
    system.remove_purchase_rule(cookie, store_id, "4")
    response_without_condition = system.purchase_cart(cookie, user_age)
    assert not response_with_condition.succeeded() and response_without_condition.succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_condition_fail_then_edit_purchase_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 50}
    simple_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 8,
    }
    system.add_purchase_rule(
        cookie, store_id, _complex_rule_details_conditioning(), "complex", parent_id
    )
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", "2", clause="test")
    system.add_purchase_rule(cookie, store_id, simple_rule_category, "simple", "2", clause="then")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    response_with_condition = system.purchase_cart(cookie, user_age)
    edited_rule_category = {
        "context": {"obj": "category", "identifier": "A"},
        "operator": "equals",
        "target": 6,
    }
    system.edit_purchase_rule(cookie, store_id, edited_rule_category, "4", "simple")
    response_without_condition = system.purchase_cart(cookie, user_age)
    assert not response_with_condition.succeeded() and response_without_condition.succeeded()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_condition_fail_then_move_purchase_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8.5, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )
    parent_id = "1"
    simple_rule_bag = {"context": {"obj": "bag"}, "operator": "great-than", "target": 60}
    system.add_purchase_rule(cookie, store_id, _complex_rule_details_or(), "complex", parent_id)
    system.add_purchase_rule(cookie, store_id, _simple_rule_details_age(), "simple", "2")
    system.add_purchase_rule(cookie, store_id, simple_rule_bag, "simple", parent_id)
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 18
    response_with_condition = system.purchase_cart(cookie, user_age)
    system.move_purchase_rule(cookie, store_id, "4", "2")
    response_without_condition = system.purchase_cart(cookie, user_age)
    assert not response_with_condition.succeeded() and response_without_condition.succeeded()


# endregion

# region add_discount
def test_add_simple_discount():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_discount(cookie, store_id, _product_discount(), parent_id)
    assert response_add.succeeded(), response_add.get_msg()


def test_add_simple_discount_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    discount_data = _product_discount()
    discount_data["percentage"] = -10
    response_add = system.add_discount(cookie, store_id, discount_data, parent_id)
    assert not response_add.succeeded()


def test_add_simple_discount_missing_key_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    discount_data = _product_discount()
    del discount_data["percentage"]
    response_add = system.add_discount(cookie, store_id, discount_data, parent_id)
    assert not response_add.succeeded()


def test_add_complex_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add = system.add_discount(cookie, store_id, _complex_add_discount(), parent_id)
    assert response_add.succeeded()


def test_add_complex_discount_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    discount_data = _complex_or_discount()
    discount_data["type"] = "Halla"
    response_add = system.add_discount(cookie, store_id, discount_data, "complex", parent_id)
    assert not response_add.succeeded()


def test_add_complex_discount_missing_key_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    discount_data = _complex_xor_discount()
    del discount_data["type"]
    response_add = system.add_discount(
        cookie, store_id, _complex_rule_details_missing_operator(), parent_id
    )
    assert not response_add.succeeded()


def test_add_complex_discount_success_simple_child_invalid():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add_complex = system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    parent_or_id = "2"
    discount_data = _category_discount()
    discount_data["context"]["obj"] = "P"
    response_add_simple = system.add_discount(cookie, store_id, discount_data, parent_or_id)
    assert response_add_complex.succeeded() and not response_add_simple.succeeded()


def test_add_child_discount_to_not_existing_parent():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "2"
    response_add_complex = system.add_discount(cookie, store_id, _complex_or_discount(), parent_id)
    assert not response_add_complex.succeeded()


def test_add_discount_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    response_add_complex = system.add_discount(
        new_cookie, store_id, _complex_max_discount(), parent_id
    )
    assert not response_add_complex.succeeded()


def test_add_discount_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    response_add_complex = system.add_discount(
        new_cookie, store_id, _complex_xor_discount(), parent_id
    )
    assert not response_add_complex.succeeded()


def test_add_discount_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage discount policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    response_add_complex = system.add_discount(new_cookie, store_id, _product_discount(), parent_id)
    assert response_add_complex.succeeded()


def test_founder_add_discount_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    response_add_complex = system.add_discount(new_cookie, store_id, _store_discount(), parent_id)
    assert not response_add_complex.succeeded()


def test_founder_add_discount_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    response_add_complex_wrong_store = system.add_discount(
        new_cookie, store_id, _category_discount(), parent_id
    )

    response_add_complex_right_store = system.add_discount(
        new_cookie, new_store_id, _category_discount(), parent_id
    )
    assert not response_add_complex_wrong_store.succeeded() and response_add_complex_right_store


def test_add_complex_discount_with_two_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    response_add_complex = system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    response_add_simple_first = system.add_discount(cookie, store_id, _product_discount(), "2")
    response_add_simple_second = system.add_discount(cookie, store_id, _category_discount(), "2")
    assert (
        response_add_complex.succeeded()
        and response_add_simple_first.succeeded()
        and response_add_simple_second.succeeded()
    )


# endregion

# region remove_discount
def test_remove_simple_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    response_remove = system.remove_discount(cookie, store_id, "2")
    assert response_remove.succeeded()


def test_remove_not_existing_discount():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    discount_data = _category_discount()
    discount_data["percentage"] = 120
    system.add_discount(cookie, store_id, discount_data, parent_id)
    response_remove = system.remove_discount(cookie, store_id, "2")
    assert not response_remove.succeeded()


def test_remove_root_discount_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    response_remove = system.remove_discount(cookie, store_id, "1")
    assert not response_remove.succeeded()


def test_remove_complex_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    response_remove = system.remove_discount(cookie, store_id, "2")
    assert response_remove.succeeded()


def test_remove_discount_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_discount(cookie, store_id, _store_discount(), parent_id)
    response_remove_complex = system.remove_discount(new_cookie, store_id, "2")
    assert not response_remove_complex.succeeded()


def test_remove_discount_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_add_discount(), parent_id)
    response_remove_complex = system.remove_discount(new_cookie, store_id, "2")
    assert not response_remove_complex.succeeded()


def test_remove_discount_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage discount policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    response_remove_complex = system.remove_discount(new_cookie, store_id, "2")
    assert response_remove_complex.succeeded()


def test_founder_remove_discount_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_xor_discount(), parent_id)
    response_remove_complex = system.remove_discount(new_cookie, store_id, "2")
    assert not response_remove_complex.succeeded()


def test_founder_remove_discount_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    system.add_discount(new_cookie, new_store_id, _store_discount(), parent_id)
    response_remove_wrong = system.remove_discount(new_cookie, store_id, "2")
    response_remove_right = system.remove_discount(new_cookie, new_store_id, "2")
    assert not response_remove_wrong.succeeded() and response_remove_right


def test_remove_complex_discount_with_two_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_or_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(), "2")
    system.add_discount(cookie, store_id, _category_discount(), "2")
    response_remove = system.remove_discount(cookie, store_id, "2")
    assert response_remove.succeeded()


# endregion

# region edit_simple_discount
def test_edit_simple_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    response_edit = system.edit_simple_discount(cookie, store_id, "2", percentage=12.5)
    assert response_edit.succeeded(), response_edit.get_msg()


def test_edit_simple_discount_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    response_edit = system.edit_simple_discount(cookie, store_id, "2", percentage=-50)
    assert not response_edit.succeeded()


def test_edit_complex_discount_with_simple_function_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    response_edit = system.edit_simple_discount(cookie, store_id, "2", "add")
    assert not response_edit.succeeded()


def test_edit_simple_child_discount_not_existing_rule():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "2"
    system.add_discount(cookie, store_id, _store_discount(), parent_id)
    response_edit = system.edit_simple_discount(cookie, store_id, "3", context={"obj": "store"})
    assert not response_edit.succeeded()


def test_edit_simple_discount_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_discount(cookie, store_id, _store_discount(), parent_id)
    response_edit = system.edit_purchase_rule(
        new_cookie, store_id, "2", context={"obj": "category", "id": "456"}
    )
    assert not response_edit.succeeded()


def test_edit_simple_discount_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    response_edit = system.edit_simple_discount(new_cookie, store_id, "2", percentage=25)
    assert not response_edit.succeeded()


def test_edit_simple_discount_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage discount policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    response_edit = system.edit_simple_discount(new_cookie, store_id, "2", percentage=90)
    assert response_edit.succeeded()


def test_founder_edit_simple_discount_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    response_edit = system.edit_simple_discount(
        new_cookie, store_id, "2", context={"obj": "product", "id": "123"}
    )
    assert not response_edit.succeeded()


def test_founder_edit_simple_discount_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(new_cookie, new_store_id, _category_discount(), parent_id)
    system.add_discount(cookie, store_id, _store_discount(), parent_id)
    response_edit_wrong = system.edit_simple_discount(new_cookie, store_id, "2", percentage=5.5)
    response_edit_right = system.edit_simple_discount(
        new_cookie, new_store_id, "2", percentage=10.5
    )
    assert response_edit_right.succeeded() and not response_edit_wrong.succeeded()


# endregion

# region edit_complex_discount


def test_edit_complex_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    response_edit = system.edit_complex_discount(cookie, store_id, "2", "add")
    assert response_edit.succeeded(), response_edit.get_msg()


def test_edit_complex_discount_invalid_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_or_discount(), parent_id)
    response_edit = system.edit_complex_discount(cookie, store_id, "2", "iff")
    assert not response_edit.succeeded()


def test_edit_complex_with_simple_function_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_or_discount(), parent_id)
    response_edit = system.edit_simple_discount(cookie, store_id, "2", "and")
    assert not response_edit.succeeded()


def test_edit_complex_discount_success_simple_child_invalid():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    parent_or_id = "2"
    system.add_discount(cookie, store_id, _product_discount(), parent_or_id)
    response_edit_complex = system.edit_complex_discount(cookie, store_id, "2", "or")
    response_edit_simple = system.edit_simple_discount(cookie, store_id, "3", percentage=-1)
    assert response_edit_complex.succeeded() and not response_edit_simple.succeeded()


def test_edit_complex_child_discount_not_existing_rule():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "2"
    system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    response_edit = system.edit_complex_discount(cookie, store_id, "3", "add")
    assert not response_edit.succeeded()


def test_edit_complex_discount_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    response_edit = system.edit_complex_discount(new_cookie, store_id, "2", "add")
    assert not response_edit.succeeded()


def test_edit_complex_discount_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    response_edit = system.edit_complex_discount(new_cookie, store_id, "2", "or")
    assert not response_edit.succeeded()


def test_edit_complex_discount_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage discount policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_xor_discount(), parent_id)
    response_edit = system.edit_complex_discount(new_cookie, store_id, "2", "max")
    assert response_edit.succeeded()


def test_founder_edit_complex_discount_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_or_discount(), parent_id)
    response_edit = system.edit_complex_discount(new_cookie, store_id, "2", "xor", "first")
    assert not response_edit.succeeded()


def test_founder_edit_complex_discount_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(new_cookie, new_store_id, _complex_max_discount(), parent_id)
    system.add_discount(cookie, store_id, _complex_add_discount(), parent_id)
    response_edit_wrong = system.edit_complex_discount(new_cookie, store_id, "2", "or")
    response_edit_right = system.edit_complex_discount(new_cookie, new_store_id, "2", "and")
    assert response_edit_right.succeeded() and not response_edit_wrong.succeeded()


def test__edit_complex_discount_with_two_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(), "2")
    system.add_discount(cookie, store_id, _category_discount(), "simple", "2")
    response_edit_right = system.edit_complex_discount(cookie, store_id, "2", "or")
    assert response_edit_right.succeeded()


# endregion

# region move_discount
def test_move_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    response_move = system.move_discount(cookie, store_id, "3", "2")
    assert response_move.succeeded()


def test_move_discount_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_or_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    response_move = system.move_discount(new_cookie, store_id, "3", "2")
    assert not response_move.succeeded()


def test_move_discount_after_manager_appointment_with_no_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_add_discount(), parent_id)
    system.add_discount(cookie, store_id, _store_discount(), parent_id)
    response_move = system.move_discount(new_cookie, store_id, "3", "2")
    assert not response_move.succeeded()


def test_move_discount_after_manager_appointment_with_permission():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password_, _, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_id, new_username)
    new_responsibility = "manage discount policy"
    system.add_manager_permission(cookie, store_id, new_username, new_responsibility)
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_xor_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    response_move = system.move_discount(new_cookie, store_id, "3", "2")
    assert response_move.succeeded()


def test_founder_move_discount_to_other_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    response_move = system.move_discount(new_cookie, store_id, "3", "2")
    assert not response_move.succeeded()


def test_founder_move_discount_to_other_store_fail_but_self_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )

    new_cookie, new_username, new_password, new_store_name, new_store_id = _initialize_info(
        _generate_username(), "bbb", _generate_store_name()
    )

    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_add_discount(), parent_id)
    system.add_discount(cookie, store_id, _store_discount(), "simple", parent_id)
    system.add_discount(new_cookie, new_store_id, _complex_add_discount(), parent_id)
    system.add_discount(new_cookie, new_store_id, _store_discount(), parent_id)
    response_move_wrong = system.move_discount(new_cookie, store_id, "3", "2")
    response_move_right = system.move_discount(new_cookie, new_store_id, "3", "2")
    assert response_move_right.succeeded() and not response_move_wrong.succeeded()


def test_move_complex_discount_with_children_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_xor_discount(), parent_id)
    system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(), "3")
    response_move = system.move_discount(cookie, store_id, "3", "2")
    assert response_move.succeeded()


def test_move_root_discount_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_xor_discount(), parent_id)
    response_move = system.move_discount(cookie, store_id, "1", "2")
    assert not response_move.succeeded()


def test_move_discount_to_leaf_as_parent_fail():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_and_discount(), parent_id)
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    response_move = system.move_discount(cookie, store_id, "2", "3")
    assert not response_move.succeeded()


# region scenarios with mocks to purchase and discount policies


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=2))
@patch.multiple(
    Store,
    check_purchase=MagicMock(return_value=Response(True)),
    apply_discounts=MagicMock(return_value=10),
)
def test_purchase_success_with_mocked_policices():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    store_res = system.get_store(store_id)
    cart_res = system.get_cart_details(cookie)

    assert (
        response.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 9
        and cart_res.succeeded()
        and response.object.value == 10
    ), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=2))
@patch.multiple(
    Store,
    check_purchase=MagicMock(return_value=Response(False)),
    apply_discounts=MagicMock(return_value=10),
)
def test_purchase_success_with_mocked_policices():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    store_res = system.get_store(store_id)
    cart_res = system.get_cart_details(cookie)
    response_sent = system.send_payment(cookie, "", "")
    assert (
        not response.succeeded()
        and response_sent.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 9
        and cart_res.succeeded()
        and response.object.value == 10
    ), response.get_msg()


# endregion
# endregion

# region buy_products with discount no conditions rules


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_product_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10, 10
    )

    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 4
    )

    system.save_product_in_cart(cookie, store_id, product_id, 1)
    system.save_product_in_cart(cookie, store_id, new_product_id, 1)
    system.add_discount(cookie, store_id, _product_discount(product_id), parent_id)
    user_age = 25
    price_res = system.purchase_cart(cookie, user_age)
    assert price_res.get_obj().parse() == 15


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_discount_wrong_context():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(), parent_id)
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 17
    price_res = system.purchase_cart(cookie, user_age)
    assert price_res.get_obj().parse() == 10


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_category_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 12, 9
    )
    (
        other_product_id,
        other_product_name,
        other_category,
        other_price,
        other_quantity,
    ) = _create_product(cookie, store_id, _generate_product_name(), "A", 12, 9)
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "B", 10.0, 4
    )
    system.add_discount(cookie, store_id, _category_discount(), "1")
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    system.save_product_in_cart(cookie, store_id, other_product_id, 1)
    system.save_product_in_cart(cookie, store_id, new_product_id, 1)
    price_res = system.purchase_cart(cookie, 20)
    assert price_res.get_obj().parse() == 28


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_category_discount_wrong_context():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "B", 10, 9
    )

    system.add_discount(cookie, store_id, _category_discount(), "1")
    system.save_product_in_cart(cookie, store_id, product_id, 8)
    price_res = system.purchase_cart(cookie, 20)
    assert price_res.get_obj().parse() == 80


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_simple_store_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10, 20
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 20, 10
    )

    system.add_discount(cookie, store_id, _store_discount(), "1")
    system.save_product_in_cart(cookie, store_id, product_id, 10)
    system.save_product_in_cart(cookie, store_id, new_product_id, 5)
    price_res = system.purchase_cart(cookie, 20)
    assert price_res.get_obj().parse() == 180


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_max_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8, 20
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(product_id), "2")
    system.add_discount(cookie, store_id, _category_discount(), "2")

    system.save_product_in_cart(cookie, store_id, product_id, 10)
    price_res = system.purchase_cart(cookie, 20)
    assert price_res.get_obj().parse() == 40


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_max_with_no_children():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 20
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    system.save_product_in_cart(cookie, store_id, product_id, 10)
    price_res = system.purchase_cart(cookie, 20)
    assert price_res.get_obj().parse() == 55


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_with_complex_add_discount_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8, 20
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_add_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(product_id), "2")
    system.add_discount(cookie, store_id, _category_discount(), "2")

    system.save_product_in_cart(cookie, store_id, product_id, 10)
    price_res = system.purchase_cart(cookie, 20)
    assert price_res.get_obj().parse() == 20


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_final_price_changes_due_to_discount_remove():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5, 10
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(product_id), parent_id)
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    response_with_discount = system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    system.remove_discount(cookie, store_id, "2")
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    response_without_discount = system.purchase_cart(cookie, user_age)
    assert (
        response_with_discount.get_obj().parse() == 30
        and response_without_discount.get_obj().parse() == 45
    )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_final_price_changes_due_to_discount_edit():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5, 10
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _product_discount(product_id), parent_id)
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    user_age = 17
    response_before_edit = system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    system.edit_simple_discount(cookie, store_id, "2", percentage=25)
    system.save_product_in_cart(cookie, store_id, product_id, 3)
    system.save_product_in_cart(cookie, store_id, new_product_id, 3)
    response_after_edit = system.purchase_cart(cookie, user_age)
    assert (
        response_before_edit.get_obj().parse() == 30
        and response_after_edit.get_obj().parse() == 37.5
    )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def test_purchase_cart_discount_changed_due_to_discount_move():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 8, 9
    )
    new_product_id, new_product_name, category, new_price, new_quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 12, 10
    )
    parent_id = "1"
    system.add_discount(cookie, store_id, _complex_max_discount(), parent_id)
    system.add_discount(cookie, store_id, _product_discount(product_id), "2")
    system.add_discount(cookie, store_id, _category_discount(), parent_id)
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    system.save_product_in_cart(cookie, store_id, new_product_id, 1)
    user_age = 18
    response_before_move = system.purchase_cart(cookie, user_age)
    system.send_payment(cookie, "", "")
    system.move_discount(cookie, store_id, "4", "2")
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    system.save_product_in_cart(cookie, store_id, new_product_id, 1)
    response_after_move = system.purchase_cart(cookie, user_age)
    assert (
        response_before_move.get_obj().parse() == 11 and response_after_move.get_obj().parse() == 15
    )


# endregion

# endregion


# region payment system mocks
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_send_payment_failed():
    with mock.patch.object(OutsideCashing, "pay", return_value="-1"):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        res1 = system.send_payment(cookie, "", "")
        # this line is added since the user might cancel the purchase after unsuccessful payment
        res_cancel = system.cancel_purchase(cookie)
        res2 = system.get_store(store_id)
        res3 = system.get_cart_details(cookie)
        assert (
            res_cancel.succeeded()
            and not res1.succeeded()
            and res2.object.ids_to_quantities[product_id] == 10
            and res3.object.bags[0].product_ids_to_quantities[product_id] == 1
        )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_paying_first_time_failed_than_success():
    with mock.patch.object(OutsideCashing, "pay", return_value="-1"):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id)
    assert (
        not response.succeeded()
        and try_again_response.succeeded()
        and get_response.object.ids_to_quantities[product_id] == 9
    )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_paying_first_time_incorrect_info_second_time_timer_over():
    import time

    with mock.patch.object(OutsideCashing, "pay", return_value="-1"):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    time.sleep(6)
    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id).object.ids_to_quantities[product_id]
    assert not response.succeeded() and not try_again_response.succeeded() and get_response == 10


# endregion

# region supply systems mocks
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_supply_order_failed():
    with mock.patch.object(OutsideSupplyment, "deliver", return_value="-1"):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        res1 = system.send_payment(cookie, "", "")
        # this line is added since the user might cancel the purchase after unsuccessful payment
        res_cancel = system.cancel_purchase(cookie)
        res2 = system.get_store(store_id)
        res3 = system.get_cart_details(cookie)
        assert (
            res_cancel.succeeded()
            and not res1.succeeded()
            and res2.object.ids_to_quantities[product_id] == 10
            and res3.object.bags[0].product_ids_to_quantities[product_id] == 1
        )


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_supply_first_time_failed_than_success():
    with mock.patch.object(OutsideSupplyment, "deliver", return_value="-1"):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id)
    assert (
        not response.succeeded()
        and try_again_response.succeeded()
        and get_response.object.ids_to_quantities[product_id] == 9
    )


# todo: make this test pass
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_try_supply_first_time_exception_second_time_timer_over():
    import time

    with mock.patch.object(OutsideSupplyment, "deliver", side_effect=Exception()):
        cookie, username, password, store_name, store_id = _initialize_info(
            _generate_username(), "aaa", _generate_store_name()
        )
        product_id, product_name, category, price, quantity = _create_product(
            cookie, store_id, _generate_product_name(), "A", 5.50, 10
        )
        system.save_product_in_cart(cookie, store_id, product_id, 1)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        response = system.send_payment(cookie, "", "")

    time.sleep(6)
    try_again_response = system.send_payment(cookie, "", "")
    get_response = system.get_store(store_id).object.ids_to_quantities[product_id]
    assert not response.succeeded() and not try_again_response.succeeded() and get_response == 10


# endregion

# region scenarios with mocks to purchase and discount policies


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=2))
@patch.multiple(
    Store,
    check_purchase=MagicMock(return_value=Response(True)),
    apply_discounts=MagicMock(return_value=10),
)
def test_purchase_success_with_mocked_policices():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    store_res = system.get_store(store_id)
    cart_res = system.get_cart_details(cookie)
    response_sent = system.send_payment(cookie, "", "")
    assert (
        response.succeeded()
        and response_sent.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 9
        and cart_res.succeeded()
        and response.object.value == 10
    ), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=2))
@patch.multiple(
    Store,
    check_purchase=MagicMock(return_value=Response(False)),
    apply_discounts=MagicMock(return_value=10),
)
def test_purchase_fail_with_mocked_policy_false():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    store_res = system.get_store(store_id)
    assert (
        not response.succeeded() and store_res.object.ids_to_quantities[product_id] == 10
    ), response.get_msg()


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=2))
@patch.multiple(
    Store,
    check_purchase=MagicMock(return_value=Response(False)),
    apply_discounts=MagicMock(return_value=10),
)
def test_purchase_fail_with_mocked_policy_false_than_true():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 5.50, 10
    )
    system.save_product_in_cart(cookie, store_id, product_id, 1)
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    system.change_product_quantity_in_cart(cookie, store_id, product_id, 2)
    with patch.multiple(Store, check_purchase=MagicMock(return_value=Response(True))):
        response_after_change = system.purchase_cart(cookie, user_age)
        store_res = system.get_store(store_id)
    assert (
        not response.succeeded()
        and response_after_change.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 8
    ), response.get_msg()


# endregion


# region test_full_purchase_with_discounts_and_purchase_policy


@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=5))
def test_purchase_cart_with_rules_success():
    cookie, username, password, store_name, store_id = _initialize_info(
        _generate_username(), "aaa", _generate_store_name()
    )
    product_id, product_name, category, price, quantity = _create_product(
        cookie, store_id, _generate_product_name(), "A", 10.0, 10
    )
    saved_quantity = 5
    system.save_product_in_cart(cookie, store_id, product_id, saved_quantity)
    rule_details = {
        "context": {"obj": "product", "identifier": product_id},
        "operator": "less-than",
        "target": 10,
    }
    system.add_purchase_rule(cookie, store_id, rule_details, "simple", "1")
    system.add_discount(cookie, store_id, _category_discount(), "1")
    user_age = 25
    response = system.purchase_cart(cookie, user_age)
    store_res = system.get_store(store_id)
    cart_res = system.get_cart_details(cookie)
    response_sent = system.send_payment(cookie, "", "")
    assert (
        response.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 5
        and cart_res.succeeded()
        and response.object.value == (saved_quantity * price) * 0.75
        and response_sent.succeeded()
    ), response.get_msg()


# endregion
