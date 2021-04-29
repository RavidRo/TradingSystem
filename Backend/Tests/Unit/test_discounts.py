import copy

import pytest
from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy
from Backend.Domain.TradingSystem.TypesPolicies.discounts import AddCompositeDiscount


# * fixtures
# * ==========================================================================================
from Backend.Domain.TradingSystem.store import Store


@pytest.fixture
def store():
    return Store("AStore")


@pytest.fixture
def product_discount():
    return {'discount_type': 'simple',
            'percentage': 75.0,
            'context': {
                'obj': 'product',
                'id': '123'
            }}


@pytest.fixture
def current_root_id(store):
    return store.get_discount_policy().get_discounts().get_obj().get_id()


# * Tests
# * ==========================================================================================

def test_constructor(store):
    discount = store.get_discount_policy().get_discounts().get_obj()
    assert isinstance(discount, AddCompositeDiscount) and discount.get_parent() is None and len(
        discount.get_children().get_obj().values) == 0

# add discount tests:

def test_add_simple_discount_success(store, product_discount, current_root_id):
    res = store.add_discount(product_discount, current_root_id)
    expected = {'merger': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    new_discount = copy.copy(product_discount)
    new_discount['id'] = str(int(current_root_id) + 1)
    expected['discounts'].append(new_discount)
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected

def test_add_simple_discount_fail_wrong_context(store, product_discount, current_root_id):
    product_discount['context']['obj'] = 'abc'
    res = store.add_discount(product_discount, current_root_id)
    assert not res.succeeded()


