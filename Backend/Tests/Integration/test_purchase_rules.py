import copy
from unittest.mock import patch, MagicMock

import pytest

from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.Domain.TradingSystem.store import Store
from Backend.Tests.stubs.product_stub import ProductStub
from Backend.Tests.stubs.shopping_bag_stub import ShoppingBagStub


@pytest.fixture()
def shopping_bag_stub():
    return ShoppingBagStub()


@pytest.fixture()
def store():
    return Store("store")


@pytest.fixture()
def complex_rule_details():
    return {"operator": "or"}


@pytest.fixture()
def simple_rule_details_upper():
    return {"context": {"obj": "user"}, "operator": "great-equals", "target": 18}


@pytest.fixture()
def simple_rule_details_down():
    return {"context": {"obj": "user"}, "operator": "less-equals", "target": 24}


@pytest.fixture()
def edited_simple_rule_details():
    return {"context": {"obj": "user"}, "operator": "equals", "target": 17}


@pytest.fixture()
def edited_complex_rule_details():
    return {"operator": "and"}


@pytest.fixture
def shopping_bag():
    store = Store("store")
    return ShoppingBag(store)


@pytest.fixture()
def products_to_quantities():
    products_to_quantities = {
        "1": (ProductStub("product1"), 9),
        "2": (ProductStub("product2"), 1),
        "3": (ProductStub("product3"), 1),
    }
    return products_to_quantities


# region add_purchase_rule tests
def test_add_simple_purchase_rule_success(store: Store):
    rule_details = {"context": {"obj": "user"}, "operator": "great-equals", "target": 18}
    rule_type = "simple"
    parent_id = "1"
    result = store.add_purchase_rule(rule_details, rule_type, parent_id)
    added_rule = store.parse_purchase_policy()
    rule_details["id"] = "2"
    expected_rule = {"id": "1", "operator": "and", "children": [rule_details]}
    assert result.succeeded() and added_rule == expected_rule


def add_complex_simple_rules(complex_details, simple_details, store):
    complex_parent_id = "1"
    simple_parent_id = "2"
    result_complex = store.add_purchase_rule(complex_details, "complex", complex_parent_id)
    result_simple = store.add_purchase_rule(simple_details, "simple", simple_parent_id)
    return result_complex, result_simple


def test_add_complex_purchase_rule_and_simple_child_success(
    store: Store, complex_rule_details, simple_rule_details_upper
):
    result_complex, result_simple = add_complex_simple_rules(
        complex_rule_details, simple_rule_details_upper, store
    )
    added_rules = store.parse_purchase_policy()
    simple_rule_details_upper["id"] = "3"
    complex_rule_details["id"] = "2"
    complex_rule_details["children"] = [simple_rule_details_upper]
    expected_rule = {"id": "1", "operator": "and", "children": [complex_rule_details]}
    assert result_simple.succeeded() and result_complex.succeeded() and added_rules == expected_rule


def test_add_conditional_rule_success(store: Store):
    complex_rule_details = {"operator": "conditional"}
    test_clause_details = {"context": {"obj": "bag"}, "operator": "great-equals", "target": 40}
    then_clause_details = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 10,
    }
    complex_parent_id = "1"
    test_then_clause_parent_id = "2"
    result_complex = store.add_purchase_rule(complex_rule_details, "complex", complex_parent_id)
    result_test_clause = store.add_purchase_rule(
        test_clause_details, "simple", test_then_clause_parent_id, clause="test"
    )
    result_then_clause = store.add_purchase_rule(
        then_clause_details, "simple", test_then_clause_parent_id, clause="then"
    )
    added_rules = store.parse_purchase_policy()
    test_clause_details["id"] = "3"
    then_clause_details["id"] = "4"
    complex_rule_details["id"] = "2"
    complex_rule_details["test"] = test_clause_details
    complex_rule_details["then"] = then_clause_details
    expected_rule = {"id": "1", "operator": "and", "children": [complex_rule_details]}
    assert (
        result_complex.succeeded()
        and result_test_clause.succeeded()
        and result_then_clause.succeeded()
        and added_rules == expected_rule
    )


def test_add_rule_with_leaf_as_parent_fail(
    store: Store, complex_rule_details, simple_rule_details_upper
):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    parent_id = "3"
    new_rule_details = {"context": {"obj": "bag"}, "operator": "great-equals", "target": 40}
    add_invalid_response = store.add_purchase_rule(new_rule_details, "simple", parent_id)
    added_rules = store.parse_purchase_policy()
    simple_rule_details_upper["id"] = "3"
    complex_rule_details["id"] = "2"
    complex_rule_details["children"] = [simple_rule_details_upper]
    expected_rule = {"id": "1", "operator": "and", "children": [complex_rule_details]}
    assert not add_invalid_response.succeeded() and added_rules == expected_rule


# # endregion


# region remove_purchase_rule tests
def test_remove_simple_purchase_rule_success(
    store: Store, complex_rule_details, simple_rule_details_upper
):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    rule_id = "3"
    response_remove = store.remove_purchase_rule(rule_id)
    after_remove_rules = store.parse_purchase_policy()
    complex_rule_details["id"] = "2"
    complex_rule_details["children"] = []
    expected_rule = {"id": "1", "operator": "and", "children": [complex_rule_details]}
    assert response_remove.succeeded() and expected_rule == after_remove_rules


def test_remove_complex_and_simple_purchase_rules_success(
    store: Store, complex_rule_details, simple_rule_details_upper
):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    rule_id = "2"
    response_remove = store.remove_purchase_rule(rule_id)
    after_remove_rules = store.parse_purchase_policy()
    expected_rule = {"id": "1", "operator": "and", "children": []}
    assert response_remove.succeeded() and expected_rule == after_remove_rules


def test_remove_not_existing_purchase_rule(store: Store):
    rule_id = "2"
    response_remove = store.remove_purchase_rule(rule_id)
    after_remove_rules = store.parse_purchase_policy()
    expected_rule = {"id": "1", "operator": "and", "children": []}
    assert not response_remove.succeeded() and expected_rule == after_remove_rules


# endregion


# region edit_purchase_rule tests


def test_edit_simple_purchase_rule_success(
    store: Store, complex_rule_details, simple_rule_details_upper, edited_simple_rule_details
):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    edited_rule_id = "3"
    edit_response = store.edit_purchase_rule(edited_simple_rule_details, edited_rule_id, "simple")
    added_rules = store.parse_purchase_policy()
    edited_simple_rule_details["id"] = "4"
    complex_rule_details["id"] = "2"
    complex_rule_details["children"] = [edited_simple_rule_details]
    expected_rule = {"id": "1", "operator": "and", "children": [complex_rule_details]}
    assert edit_response.succeeded() and expected_rule == added_rules


def test_edit_complex_purchase_rule_success(
    store: Store, complex_rule_details, simple_rule_details_upper, edited_complex_rule_details
):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    edited_rule_id = "2"
    edit_response = store.edit_purchase_rule(edited_complex_rule_details, edited_rule_id, "complex")
    added_rules = store.parse_purchase_policy()
    simple_rule_details_upper["id"] = "3"
    edited_complex_rule_details["id"] = "4"
    edited_complex_rule_details["children"] = [simple_rule_details_upper]
    expected_rule = {"id": "1", "operator": "and", "children": [edited_complex_rule_details]}
    assert edit_response.succeeded() and expected_rule == added_rules


def test_edit_not_existing_rule(store: Store, edited_simple_rule_details):
    rule_id = "2"
    response_edit = store.edit_purchase_rule(edited_simple_rule_details, rule_id, "simple")
    after_edit_rules = store.parse_purchase_policy()
    expected_rule = {"id": "1", "operator": "and", "children": []}
    assert not response_edit.succeeded() and expected_rule == after_edit_rules


# endregion


# region move_purchase_rule tests
def test_move_purchase_rule_success(store: Store, complex_rule_details, simple_rule_details_upper):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    another_complex_details = {"operator": "and"}
    another_complex_parent_id = "1"
    store.add_purchase_rule(another_complex_details, "complex", another_complex_parent_id)
    another_complex_id = "4"
    moved_id = "3"
    before_move_rules = store.parse_purchase_policy()
    result_move = store.move_purchase_rule(moved_id, another_complex_id)
    after_move_rules = store.parse_purchase_policy()
    another_complex_details["children"] = [simple_rule_details_upper]
    another_complex_details["id"] = "4"
    complex_rule_details["id"] = "2"
    complex_rule_details["children"] = []
    simple_rule_details_upper["id"] = "3"
    expected_rule = {
        "id": "1",
        "operator": "and",
        "children": [complex_rule_details, another_complex_details],
    }
    assert result_move.succeeded() and expected_rule == after_move_rules


def test_move_purchase_rule_fail(store: Store, complex_rule_details, simple_rule_details_upper):
    add_complex_simple_rules(complex_rule_details, simple_rule_details_upper, store)
    another_complex_details = {"operator": "and"}
    another_complex_parent_id = "2"
    store.add_purchase_rule(another_complex_details, "complex", another_complex_parent_id)
    another_complex_id = "4"
    moved_id = "2"
    result_move = store.move_purchase_rule(moved_id, another_complex_id)
    after_move_rules = store.parse_purchase_policy()
    another_complex_details["children"] = []
    another_complex_details["id"] = "4"
    complex_rule_details["id"] = "2"
    complex_rule_details["children"] = [simple_rule_details_upper, another_complex_details]
    simple_rule_details_upper["id"] = "3"
    expected_rule = {"id": "1", "operator": "and", "children": [complex_rule_details]}
    assert not result_move.succeeded() and expected_rule == after_move_rules


# endregion

# region test_apply_discounts

# region tests- age > 18
def test_apply_simple_discount_success(
    store: Store, simple_rule_details_upper, products_to_quantities
):
    store.add_purchase_rule(simple_rule_details_upper, "simple", "1")
    user_age = 19
    response = store.check_purchase(products_to_quantities, user_age)
    assert response.succeeded()


def test_apply_simple_discount_fail(
    store: Store, simple_rule_details_upper, products_to_quantities
):
    store.add_purchase_rule(simple_rule_details_upper, "simple", "1")
    user_age = 17
    response = store.check_purchase(products_to_quantities, user_age)
    assert not response.succeeded()


# endregion

# region tests- age > 18 and age < 24
def test_apply_and_complex_age_rule_success(
    store: Store, simple_rule_details_upper, simple_rule_details_down, products_to_quantities
):
    store.add_purchase_rule({"operator": "and"}, "complex", "1")
    store.add_purchase_rule(simple_rule_details_upper, "simple", "2")
    store.add_purchase_rule(simple_rule_details_down, "simple", "2")
    user_age = 20
    response = store.check_purchase(products_to_quantities, user_age)
    assert response.succeeded()


def test_apply_and_complex_age_rule_fail(
    store: Store, simple_rule_details_upper, simple_rule_details_down, products_to_quantities
):
    store.add_purchase_rule({"operator": "and"}, "complex", "1")
    store.add_purchase_rule(simple_rule_details_upper, "simple", "2")
    store.add_purchase_rule(simple_rule_details_down, "simple", "2")
    user_age = 26
    response = store.check_purchase(products_to_quantities, user_age)
    assert not response.succeeded()


# endregion

# region test condition


@patch.multiple(ProductStub, get_category=MagicMock(return_value="milk products"))
def test_apply_condition_discount_success(store: Store, products_to_quantities):
    complex_rule_details = {"operator": "conditional"}
    test_clause_details = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 10,
    }
    then_clause_details = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 11,
    }

    result_complex = store.add_purchase_rule(complex_rule_details, "complex", "1")
    result_test_clause = store.add_purchase_rule(test_clause_details, "simple", "2", clause="test")
    result_then_clause = store.add_purchase_rule(then_clause_details, "simple", "2", clause="then")
    user_age = 26
    response = store.check_purchase(products_to_quantities, user_age)
    assert response.succeeded()


@patch.multiple(ProductStub, get_category=MagicMock(return_value="milk products"))
def test_apply_condition_discount_fail_then_clause(store: Store, products_to_quantities):
    complex_rule_details = {"operator": "conditional"}
    test_clause_details = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 10,
    }
    then_clause_details = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 9,
    }

    result_complex = store.add_purchase_rule(complex_rule_details, "complex", "1")
    result_test_clause = store.add_purchase_rule(test_clause_details, "simple", "2", clause="test")
    result_then_clause = store.add_purchase_rule(then_clause_details, "simple", "2", clause="then")
    user_age = 26
    response = store.check_purchase(products_to_quantities, user_age)
    assert not response.succeeded()


@patch.multiple(ProductStub, get_category=MagicMock(return_value="milk products"))
def test_apply_condition_discount_success_irrelevant_test_clause(
    store: Store, products_to_quantities
):
    complex_rule_details = {"operator": "conditional"}
    test_clause_details = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 8,
    }
    then_clause_details = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 9,
    }

    result_complex = store.add_purchase_rule(complex_rule_details, "complex", "1")
    result_test_clause = store.add_purchase_rule(test_clause_details, "simple", "2", clause="test")
    result_then_clause = store.add_purchase_rule(then_clause_details, "simple", "2", clause="then")
    user_age = 26
    assert store.check_purchase(products_to_quantities, user_age).succeeded()


# endregion

# region test very complex
@patch.multiple(ProductStub, get_category=MagicMock(return_value="milk products"))
def test_very_complex_success(
    store: Store, simple_rule_details_upper, simple_rule_details_down, products_to_quantities
):
    store.add_purchase_rule({"operator": "and"}, "complex", "1")
    store.add_purchase_rule({"operator": "or"}, "complex", "2")
    store.add_purchase_rule({"operator": "or"}, "complex", "2")
    simple_rule_result_true = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 10,
    }
    simple_rule_result_false = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 8,
    }
    store.add_purchase_rule(simple_rule_result_true, "simple", "3")
    store.add_purchase_rule(simple_rule_result_false, "simple", "3")
    store.add_purchase_rule({"operator": "and"}, "complex", "4")
    simple_rule_under_and = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 11,
    }
    store.add_purchase_rule(simple_rule_under_and, "simple", "7")
    user_age = 26
    assert store.check_purchase(products_to_quantities, user_age).succeeded()


@patch.multiple(ProductStub, get_category=MagicMock(return_value="milk products"))
def test_very_complex_fail_because_of_rule_under_and(
    store: Store, simple_rule_details_upper, simple_rule_details_down, products_to_quantities
):
    store.add_purchase_rule({"operator": "and"}, "complex", "1")
    store.add_purchase_rule({"operator": "or"}, "complex", "2")
    store.add_purchase_rule({"operator": "or"}, "complex", "2")
    simple_rule_result_true = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 10,
    }
    simple_rule_result_false = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 8,
    }
    store.add_purchase_rule(simple_rule_result_true, "simple", "3")
    store.add_purchase_rule(simple_rule_result_false, "simple", "3")
    store.add_purchase_rule({"operator": "and"}, "complex", "4")
    simple_rule_under_and = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 10,
    }
    store.add_purchase_rule(simple_rule_under_and, "simple", "7")
    user_age = 26
    assert not store.check_purchase(products_to_quantities, user_age).succeeded()


@patch.multiple(ProductStub, get_category=MagicMock(return_value="milk products"))
def test_very_complex_fail_because_of_rule_false(
    store: Store, simple_rule_details_upper, simple_rule_details_down, products_to_quantities
):
    store.add_purchase_rule({"operator": "and"}, "complex", "1")
    store.add_purchase_rule({"operator": "and"}, "complex", "2")
    store.add_purchase_rule({"operator": "or"}, "complex", "2")
    simple_rule_result_true = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 10,
    }
    simple_rule_result_false = {
        "context": {"obj": "product", "identifier": "1"},
        "operator": "less-than",
        "target": 8,
    }
    store.add_purchase_rule(simple_rule_result_true, "simple", "3")
    store.add_purchase_rule(simple_rule_result_false, "simple", "3")
    store.add_purchase_rule({"operator": "and"}, "complex", "4")
    simple_rule_under_and = {
        "context": {"obj": "category", "identifier": "milk products"},
        "operator": "equals",
        "target": 9,
    }
    store.add_purchase_rule(simple_rule_under_and, "simple", "7")
    user_age = 26
    assert not store.check_purchase(products_to_quantities, user_age).succeeded()
