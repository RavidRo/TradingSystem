import string
import random
from unittest.mock import patch, MagicMock

import pytest

from Backend.Domain.Payment.Adapters.cashing_adapter import CashingAdapter
from Backend.Domain.Payment.Adapters.supply_adapter import SupplyAdapter
from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Service.trading_system import TradingSystem
from Backend.response import Response


@pytest.fixture
def products_data():
    return [("A", "A", 10, 4), ("B", "A", 10, 3), ("C", "B", 10, 7)]


@pytest.fixture
@patch.multiple(ShoppingCart, interval_time=MagicMock(return_value=1))
def initialization(products_data):
    system = TradingSystem.getInstance()
    cookie = system.enter_system()
    letters = string.ascii_lowercase
    username = "".join(random.choices(letters, k=5))
    password = "".join(random.choices(letters, k=5))
    system.register(cookie, username, password)
    system.login(cookie, username, password)
    store_id = system.create_store(cookie, "store").object
    store = system.get_store(store_id).object

    product_ids = []
    for data in products_data:
        product_ids.append(system.create_product(cookie, store_id, *data).object)

    return system, cookie, store, product_ids


@pytest.fixture
def cookie(initialization):
    return initialization[1]


@pytest.fixture
def store(initialization):
    return initialization[2]


@pytest.fixture
def store_id(store):
    return store.id


@pytest.fixture
def product_ids(initialization):
    return initialization[3]


@pytest.fixture
def system(initialization):
    return initialization[0]


@pytest.fixture
def simple_product_rule(product_ids):
    return {'context': {'obj': 'product', 'identifier': product_ids[0]}, 'operator': 'less-than', 'target': 2}


@pytest.fixture
def simple_product_true_conditional_discount(product_ids):
    return {'discount_type': 'simple',
            'percentage': 75.0,
            'condition': {'context': {'obj': 'product', 'identifier': product_ids[0]}, 'operator': 'less-than',
                          'target': 8},
            'context': {
                'obj': 'product',
                'id': product_ids[0]
            }}


@pytest.fixture
def simple_category_false_conditional_discount(product_ids):
    return {'discount_type': 'simple',
            'percentage': 50.0,
            'condition': {'context': {'obj': 'product', 'identifier': product_ids[0]}, 'operator': 'great-than',
                          'target': 8},
            'context': {
                'obj': 'category',
                'id': 'A'
            }}


@pytest.fixture
def complex_and_discount():
    return {'discount_type': 'complex',
            'type': 'and'}


@pytest.fixture
def complex_or_discount():
    return {'discount_type': 'complex',
            'type': 'or'}


@patch.multiple(DefaultDiscountPolicy, applyDiscount=MagicMock(return_value=0))
@patch.multiple(DefaultPurchasePolicy, checkPolicy=MagicMock(return_value=Response(True)))
@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_purchase_success(system, cookie, store_id, store, product_ids, products_data):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(), products_data)))


def fail_purchase_payment_case(system, cookie, store_id, store, product_ids, products_data):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    system.cancel_purchase(cookie)
    assert not res.succeeded() and len(system.get_cart_details(cookie).object.bags[0].product_ids_to_quantities) == 3 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data[1] == 0 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities, products_data)))


@patch.multiple(DefaultDiscountPolicy, applyDiscount=MagicMock(return_value=0))
@patch.multiple(DefaultPurchasePolicy, checkPolicy=MagicMock(return_value=Response(True)))
@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(False)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_purchase_fail_false_payment(system, cookie, store_id, store, product_ids, products_data):
    fail_purchase_payment_case(system, cookie, store_id, store, product_ids, products_data)


@patch.multiple(DefaultDiscountPolicy, applyDiscount=MagicMock(return_value=0))
@patch.multiple(DefaultPurchasePolicy, checkPolicy=MagicMock(return_value=Response(True)))
@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(False)))
def test_purchase_fail_false_deliver(system, cookie, store_id, store, product_ids, products_data):
    fail_purchase_payment_case(system, cookie, store_id, store, product_ids, products_data)


@patch.multiple(DefaultDiscountPolicy, applyDiscount=MagicMock(return_value=0))
@patch.multiple(DefaultPurchasePolicy, checkPolicy=MagicMock(return_value=Response(True)))
@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(False)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(False)))
def test_purchase_fail_false_payment_false_deliver(system, cookie, store_id, store, product_ids, products_data):
    fail_purchase_payment_case(system, cookie, store_id, store, product_ids, products_data)


@patch.multiple(DefaultDiscountPolicy, applyDiscount=MagicMock(return_value=0))
@patch.multiple(DefaultPurchasePolicy, checkPolicy=MagicMock(return_value=Response(True)))
@patch.multiple(CashingAdapter, pay=MagicMock(side_effect=Exception()))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_purchase_fail_crash_payment(system, cookie, store_id, store, product_ids, products_data):
    fail_purchase_payment_case(system, cookie, store_id, store, product_ids, products_data)


@patch.multiple(DefaultDiscountPolicy, applyDiscount=MagicMock(return_value=0))
@patch.multiple(DefaultPurchasePolicy, checkPolicy=MagicMock(return_value=Response(True)))
@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(side_effect=Exception()))
def test_purchase_fail_crash_deliver(system, cookie, store_id, store, product_ids, products_data):
    fail_purchase_payment_case(system, cookie, store_id, store, product_ids, products_data)


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_purchase_rule_fail_blocking_rule(system, cookie, store_id, store, product_ids, products_data,
                                          simple_product_rule):
    system.add_purchase_rule(cookie, store_id, simple_product_rule, "simple", "1")
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    cart_res = system.get_cart_details(cookie)
    system.cancel_purchase(cookie)
    assert not res.succeeded() and len(cart_res.object.bags[0].product_ids_to_quantities) == 3 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data[1] == 0 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities, products_data)))


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_simple_conditional_discount_true_cond(system, cookie, store_id, store, product_ids, products_data,
                                               simple_product_true_conditional_discount):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.add_discount(cookie, store_id, simple_product_true_conditional_discount, "1", "simple")
    price_res = system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data))) and price_res.get_obj().parse() == 45, price_res.get_msg()


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_simple_conditional_discount_false_cond(system, cookie, store_id, store, product_ids, products_data,
                                                simple_product_true_conditional_discount):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    simple_product_true_conditional_discount['condition']['operator'] = 'great-than'
    system.add_discount(cookie, store_id, simple_product_true_conditional_discount, "1", "simple")
    price_res = system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data))) and price_res.get_obj().parse() == 60, price_res.get_msg()


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_and_conditional_discount_false(system, cookie, store_id, store, product_ids, products_data,
                                        simple_product_true_conditional_discount,
                                        simple_category_false_conditional_discount, complex_and_discount):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.add_discount(cookie, store_id, complex_and_discount, "1")
    system.add_discount(cookie, store_id, simple_product_true_conditional_discount, "2", "simple")

    system.add_discount(cookie, store_id, simple_category_false_conditional_discount, "2", "simple")
    price_res = system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data))) and price_res.get_obj().parse() == 60, price_res.get_msg()


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_and_conditional_discount_true(system, cookie, store_id, store, product_ids, products_data,
                                       simple_product_true_conditional_discount,
                                       simple_category_false_conditional_discount, complex_and_discount):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.add_discount(cookie, store_id, complex_and_discount, "1")
    system.add_discount(cookie, store_id, simple_product_true_conditional_discount, "2", "simple")

    simple_category_false_conditional_discount['condition']['operator'] = 'less-than'

    system.add_discount(cookie, store_id, simple_category_false_conditional_discount, "2", "simple")
    price_res = system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data))) and price_res.get_obj().parse() == 25.0, price_res.get_msg()


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_or_conditional_discount_true(system, cookie, store_id, store, product_ids, products_data,
                                      simple_product_true_conditional_discount,
                                      simple_category_false_conditional_discount, complex_or_discount):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.add_discount(cookie, store_id, complex_or_discount, "1")
    system.add_discount(cookie, store_id, simple_product_true_conditional_discount, "2", "simple")

    system.add_discount(cookie, store_id, simple_category_false_conditional_discount, "2", "simple")
    price_res = system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")
    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data))) and price_res.get_obj().parse() == 25, price_res.get_msg()


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_or_conditional_discount_false(system, cookie, store_id, store, product_ids, products_data,
                                       simple_product_true_conditional_discount,
                                       simple_category_false_conditional_discount, complex_or_discount):
    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)

    system.add_discount(cookie, store_id, complex_or_discount, "1")
    system.add_discount(cookie, store_id, simple_category_false_conditional_discount, "2", "simple")

    simple_product_true_conditional_discount['condition']['operator'] = 'great-than'

    system.add_discount(cookie, store_id, simple_product_true_conditional_discount, "2", "simple")
    price_res = system.purchase_cart(cookie, 12)
    res = system.send_payment(cookie, "", "")

    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data))) and price_res.get_obj().parse() == 60, price_res.get_msg()


@patch.multiple(CashingAdapter, pay=MagicMock(return_value=Response(True)))
@patch.multiple(SupplyAdapter, deliver=MagicMock(return_value=Response(True)))
def test_try_paying_after_time_passed(system, cookie, store_id, store, product_ids, products_data):
    import time

    for product_id in product_ids:
        system.save_product_in_cart(cookie, store_id, product_id, 2)
    system.purchase_cart(cookie, 18)
    time.sleep(2)
    res = system.send_payment(cookie, "", "")

    assert not res.succeeded() and len(system.get_cart_details(cookie).object.bags[0].product_ids_to_quantities) == 3 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data[1] == 0 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities, products_data)))


def test_try_paying_first_time_failed_than_success(system, cookie, store_id, store, product_ids, products_data):
    with patch.object(CashingAdapter, 'pay', return_value=Response(False)):
        for product_id in product_ids:
            system.save_product_in_cart(cookie, store_id, product_id, 2)

        user_age = 25
        system.purchase_cart(cookie, user_age)
        res = system.send_payment(cookie, "", "")

    assert not res.succeeded() and len(
        system.get_cart_details(cookie).object.bags[0].product_ids_to_quantities) == 3 and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data[1] == 0 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities, products_data)))

    with patch.object(CashingAdapter, 'pay', return_value=Response(True)):
        res = system.send_payment(cookie, "", "")

    assert res.succeeded() and len(system.get_cart_details(cookie).object.bags) == 0 \
           and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data == 2 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities.values(),
            products_data)))


def test_try_paying_first_time_fail_second_time_timer_over(system, cookie, store_id, store, product_ids,
                                                           products_data):
    import time
    with patch.object(CashingAdapter, 'pay', return_value=Response(False)):
        for product_id in product_ids:
            system.save_product_in_cart(cookie, store_id, product_id, 2)
        user_age = 25
        system.purchase_cart(cookie, user_age)
        system.send_payment(cookie, "", "")

    time.sleep(2)
    with patch.object(CashingAdapter, 'pay', return_value=Response(False)):
        res = system.send_payment(cookie, "", "")

    assert not res.succeeded() and len(
        system.get_cart_details(cookie).object.bags[0].product_ids_to_quantities) == 3 and all(list(
        map(lambda after_data, before_data: before_data[3] - after_data[1] == 0 and before_data[0] == store.get_product(
            after_data[0]).get_name(),
            store.ids_to_quantities, products_data)))
