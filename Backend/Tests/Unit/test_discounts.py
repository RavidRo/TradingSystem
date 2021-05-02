import copy

import pytest
from Backend.Domain.TradingSystem.TypesPolicies.discounts import AddCompositeDiscount
from Backend.Domain.TradingSystem.product import Product
from Backend.Domain.TradingSystem.store import Store


# * fixtures
# * ==========================================================================================


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
def category_discount():
    return {'discount_type': 'simple',
            'percentage': 75.0,
            'context': {
                'obj': 'category',
                'id': 'A'
            }}


@pytest.fixture
def store_discount():
    return {'discount_type': 'simple',
            'percentage': 75.0,
            'context': {
                'obj': 'store'
            }}


@pytest.fixture
def complex_max_discount():
    return {'discount_type': 'complex',
            'type': 'max'}


@pytest.fixture
def complex_add_discount():
    return {'discount_type': 'complex',
            'type': 'add'}


@pytest.fixture
def complex_and_discount():
    return {'discount_type': 'complex',
            'type': 'and'}


@pytest.fixture
def complex_or_discount():
    return {'discount_type': 'complex',
            'type': 'or'}


@pytest.fixture
def complex_xor_discount():
    return {'discount_type': 'complex',
            'type': 'xor',
            'decision_rule': "first"}


@pytest.fixture
def current_root_id(store):
    return store.get_discount_policy().get_discounts().get_obj().get_id()


@pytest.fixture
def products_to_quantity():
    return {"123": (Product("milk", "A", 4), 4),
            "456": (Product("cheese", "A", 8), 2),
            "789": (Product("dog food", "B", 12), 1)}


# * Tests
# * ==========================================================================================

def test_constructor(store):
    discount = store.get_discount_policy().get_discounts().get_obj()
    assert isinstance(discount, AddCompositeDiscount) and discount.get_parent() is None and len(
        discount.get_children()) == 0


# add discount tests:

def test_add_simple_discount_success(store, product_discount, current_root_id):
    res = store.add_discount(product_discount, current_root_id)
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    new_discount = copy.copy(product_discount)
    new_discount['id'] = str(int(current_root_id) + 1)
    expected['discounts'].append(new_discount)
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_add_simple_discount_fail_wrong_context(store, product_discount, current_root_id):
    product_discount['context']['obj'] = 'abc'
    res = store.add_discount(product_discount, current_root_id)
    assert not res.succeeded()


def test_add_simple_discount_fail_wrong_percentage(store, product_discount, current_root_id):
    product_discount['percentage'] = -5
    res = store.add_discount(product_discount, current_root_id)
    assert not res.succeeded()


def test_add_complex_discount_fail_wrong_type(store, complex_max_discount, current_root_id):
    complex_max_discount['type'] = 'abc'
    res = store.add_discount(complex_max_discount, current_root_id)
    assert not res.succeeded()


def test_add_xor_discount_fail_missing_decision_rule(store, complex_xor_discount, current_root_id):
    del complex_xor_discount['decision_rule']
    res = store.add_discount(complex_xor_discount, current_root_id)
    assert not res.succeeded()


def test_add_complex_discount_success(store, complex_max_discount, current_root_id):
    res = store.add_discount(complex_max_discount, current_root_id)
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    new_discount = copy.copy(complex_max_discount)
    new_discount['discounts'] = []
    new_discount['id'] = str(int(current_root_id) + 1)
    expected['discounts'].append(new_discount)
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_add_multiple_discounts_success(store, complex_max_discount, complex_and_discount, product_discount,
                                        current_root_id):
    res1 = store.add_discount(complex_max_discount, current_root_id)
    res2 = store.add_discount(complex_and_discount, current_root_id)
    res3 = store.add_discount(product_discount, str(int(current_root_id) + 1))
    product2_discount = copy.copy(product_discount)
    product2_discount["context"]["id"] = "456"
    res4 = store.add_discount(product2_discount, str(int(current_root_id) + 2))

    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected["discounts"].append(
        {'type': 'max', 'discount_type': 'complex', 'discounts': [], 'id': str(int(current_root_id) + 1)})
    expected["discounts"].append(
        {'type': 'and', 'discount_type': 'complex', 'discounts': [], 'id': str(int(current_root_id) + 2)})
    expected["discounts"][0]['discounts'].append(copy.copy(product_discount))
    expected["discounts"][0]["discounts"][0]['id'] = str(int(current_root_id) + 3)
    expected["discounts"][1]["discounts"].append(copy.copy(product_discount))
    expected["discounts"][1]["discounts"][0]['id'] = str(int(current_root_id) + 4)

    assert all(list(map(lambda res: res.succeeded(),
                        [res1, res2, res3, res4]))) and store.get_discounts().get_obj().parse() == expected


def test_add_to_simple_discount_fails(store, product_discount, current_root_id):
    res1 = store.add_discount(product_discount, current_root_id)
    res2 = store.add_discount(product_discount, str(int(current_root_id) + 1))
    assert res1.succeeded() and not res2.succeeded()


# remove discount tests:

def test_remove_hidden_root_fails(store, current_root_id):
    res = store.remove_discount(current_root_id)
    assert not res.succeeded()


def test_remove_simple_success(store, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    res = store.remove_discount(str(int(current_root_id) + 1))
    assert res.succeeded() and store.get_discounts().get_obj().parse() == {'type': 'add', 'discount_type': 'complex',
                                                                           'discounts': [], 'id': current_root_id}


def test_remove_complex_success(store, complex_or_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_or_discount, current_root_id)
    res = store.remove_discount(str(int(current_root_id) + 1))
    assert res.succeeded() and store.get_discounts().get_obj().parse() == {'type': 'add', 'discount_type': 'complex',
                                                                           'discounts': [], 'id': current_root_id}


def test_remove_multiple_children_success(store, product_discount, complex_xor_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    store.add_discount(complex_xor_discount, current_root_id)
    res1 = store.remove_discount(str(int(current_root_id) + 1))
    res2 = store.remove_discount(str(int(current_root_id) + 2))
    assert res1.succeeded() and res2.succeeded() and store.get_discounts().get_obj().parse() == {'type': 'add',
                                                                                                 'discount_type': 'complex',
                                                                                                 'discounts': [],
                                                                                                 'id': current_root_id}


def test_remove_nested_children_success(store, product_discount, complex_xor_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_xor_discount, current_root_id)
    store.add_discount(product_discount, str(int(current_root_id) + 1))
    res = store.remove_discount(str(int(current_root_id) + 1))
    assert res.succeeded() and store.get_discounts().get_obj().parse() == {'type': 'add', 'discount_type': 'complex',
                                                                           'discounts': [], 'id': current_root_id}


def test_remove_non_existed_discount_fails(store):
    res = store.remove_discount("123")
    assert not res.succeeded()


# move discount tests:

def test_move_simple_discount_success(store, product_discount, complex_max_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(product_discount, current_root_id)
    res = store.move_discount(str(int(current_root_id) + 2), str(int(current_root_id) + 1))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = [copy.copy(product_discount)]
    expected['discounts'][0]['discounts'][0]['id'] = str(int(current_root_id) + 2)
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_complex_discount_success(store, complex_and_discount, complex_add_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_and_discount, current_root_id)
    store.add_discount(complex_add_discount, current_root_id)
    res = store.move_discount(str(int(current_root_id) + 2), str(int(current_root_id) + 1))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_and_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = [copy.copy(complex_add_discount)]
    expected['discounts'][0]['discounts'][0]['id'] = str(int(current_root_id) + 2)
    expected['discounts'][0]['discounts'][0]['discounts'] = []
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_nested_discounts_success(store, complex_max_discount, complex_or_discount, product_discount,
                                       current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(complex_or_discount, current_root_id)
    store.add_discount(product_discount, str(int(current_root_id) + 2))
    res = store.move_discount(str(int(current_root_id) + 2), str(int(current_root_id) + 1))

    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = [copy.copy(complex_or_discount)]
    expected['discounts'][0]['discounts'][0]['id'] = str(int(current_root_id) + 2)
    expected['discounts'][0]['discounts'][0]['discounts'] = [copy.copy(product_discount)]
    expected['discounts'][0]['discounts'][0]['discounts'][0]['id'] = str(int(current_root_id) + 3)
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_to_descendant_fails(store, complex_max_discount, complex_or_discount, current_root_id):
    # assume add_discount_works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(complex_or_discount, str(int(current_root_id) + 1))
    res = store.move_discount(str(int(current_root_id) + 1), str(int(current_root_id) + 2))

    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = [copy.copy(complex_or_discount)]
    expected['discounts'][0]['discounts'][0]['id'] = str(int(current_root_id) + 2)
    expected['discounts'][0]['discounts'][0]['discounts'] = []
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_root_fails(store, complex_add_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_add_discount, current_root_id)
    res = store.move_discount(current_root_id, str(int(current_root_id) + 1))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_add_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = []
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_to_simple_discount_fails(store, product_discount, complex_and_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_and_discount, current_root_id)
    store.add_discount(product_discount, current_root_id)
    res = store.move_discount(str(int(current_root_id) + 1), str(int(current_root_id) + 2))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_and_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = []
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][1]['id'] = str(int(current_root_id) + 2)
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_source_not_found(store, complex_max_discount, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(product_discount, current_root_id)
    res = store.move_discount(str(int(current_root_id) + 10), str(int(current_root_id) + 1))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = []
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][1]['id'] = str(int(current_root_id) + 2)

    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_move_destination_not_found(store, complex_max_discount, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(product_discount, current_root_id)
    res = store.move_discount(str(int(current_root_id) + 1), str(int(current_root_id) + 10))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['discounts'] = []
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][1]['id'] = str(int(current_root_id) + 2)

    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


# edit simple discount tests:

def test_edit_simple_discount_success(store, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    res = store.edit_simple_discount(str(int(current_root_id) + 1), 25.0,
                                     {'obj': 'category', 'id': "smartphones"}, None)
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['percentage'] = 25.0
    expected['discounts'][0]['context'] = {'obj': 'category', 'id': "smartphones"}

    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_simple_not_all_args_success(store, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    res = store.edit_simple_discount(str(int(current_root_id) + 1), percentage=12.5)
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    expected['discounts'][0]['percentage'] = 12.5

    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_simple_invalid_discount_id(store, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    res = store.edit_simple_discount(str(int(current_root_id) + 5))
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)

    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_simple_invalid_percentage(store, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    res = store.edit_simple_discount(str(int(current_root_id) + 1), percentage=-5.0)
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_simple_invalid_context(store, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    res = store.edit_simple_discount(str(int(current_root_id) + 1), context={'obj': 'abc', 'id': "456"})
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(product_discount))
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


# edit complex discount tests

def test_edit_complex_discount_success(store, complex_max_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    res = store.edit_complex_discount(str(int(current_root_id) + 1), complex_type="and")
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['type'] = 'and'
    expected['discounts'][0]['discounts'] = []
    expected['discounts'][0]['id'] = str(int(current_root_id) + 2)
    assert res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_complex_discount_invalid_type(store, complex_max_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    res = store.edit_complex_discount(str(int(current_root_id) + 1), complex_type="abc")
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_max_discount))
    expected['discounts'][0]['discounts'] = []
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_complex_non_exist_discount_id(store, complex_max_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    res = store.edit_complex_discount(str(int(current_root_id) + 3), complex_type="and")
    assert not res.succeeded()


def test_edit_complex_to_xor_without_decision_rule_fails(store, complex_or_discount, current_root_id):
    # assume add_discount works
    store.add_discount(complex_or_discount, current_root_id)
    res = store.edit_complex_discount(str(int(current_root_id) + 1), complex_type="xor")
    expected = {'type': 'add', 'discount_type': 'complex', 'discounts': [], 'id': current_root_id}
    expected['discounts'].append(copy.copy(complex_or_discount))
    expected['discounts'][0]['discounts'] = []
    expected['discounts'][0]['id'] = str(int(current_root_id) + 1)
    assert not res.succeeded() and store.get_discounts().get_obj().parse() == expected


def test_edit_complex_on_simple_discount_fail(store, product_discount, current_root_id):
    # assume add_discount_works
    store.add_discount(product_discount, current_root_id)
    res = store.edit_complex_discount(str(int(current_root_id) + 1), complex_type="add")
    assert not res.succeeded()


# apply_discount tests:

def test_apply_discount_no_added_discounts_success(store, products_to_quantity):
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 44


def test_apply_discount_no_products(store):
    price = store.apply_discounts({}, 0)
    assert price == 0


def test_apply_simple_discount_product(store, products_to_quantity, product_discount, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 32


def test_apply_simple_discount_category(store, category_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(category_discount, current_root_id)
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 20


def test_apply_simple_discount_store(store, store_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(store_discount, current_root_id)
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 11


def test_apply_two_discounts_add_success(store, product_discount, category_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(product_discount, current_root_id)
    store.add_discount(category_discount, current_root_id)
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 8


def test_apply_two_discount_overflow_success(store, store_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(store_discount, current_root_id)
    store.add_discount(store_discount, current_root_id)
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 0


def test_apply_nested_discounts(store, complex_add_discount, product_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(complex_add_discount, current_root_id)
    store.add_discount(product_discount, str(int(current_root_id) + 1))
    store.add_discount(product_discount, str(int(current_root_id) + 1))
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 20


def test_apply_max(store, complex_max_discount, product_discount, category_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(product_discount, str(int(current_root_id) + 1))
    store.add_discount(category_discount, str(int(current_root_id) + 1))
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 20


def test_apply_xor(store, complex_xor_discount, product_discount, category_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(complex_xor_discount, current_root_id)
    store.add_discount(product_discount, str(int(current_root_id) + 1))
    store.add_discount(category_discount, str(int(current_root_id) + 1))
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 32


def test_apply_xor_first_with_no_children(store, complex_xor_discount, product_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(complex_xor_discount, current_root_id)
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 44


def test_apply_complex_tree(store, complex_max_discount, complex_xor_discount, product_discount, category_discount, store_discount, products_to_quantity, current_root_id):
    # assume add_discount works
    store.add_discount(complex_max_discount, current_root_id)
    store.add_discount(category_discount, str(int(current_root_id) + 1))
    store.add_discount(product_discount, str(int(current_root_id) + 1))
    store.add_discount(complex_xor_discount, current_root_id)
    store.add_discount(product_discount, str(int(current_root_id) + 4))
    store.add_discount(complex_xor_discount, str(int(current_root_id) + 5))
    store.add_discount(category_discount, str(int(current_root_id) + 6))
    store.add_discount(store_discount, str(int(current_root_id) + 6))
    price = store.apply_discounts(products_to_quantity, 0)
    assert price == 8
