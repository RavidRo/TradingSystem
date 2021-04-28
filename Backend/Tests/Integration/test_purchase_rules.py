import copy

import pytest
from Backend.Domain.TradingSystem.store import Store
from Backend.Tests.stubs.shopping_bag_stub import ShoppingBagStub


@pytest.fixture()
def shopping_bag_stub():
    return ShoppingBagStub()


@pytest.fixture()
def store():
    return Store("store")

#region add_purchase_rule tests
def test_add_simple_purchase_rule_success(store: Store):
    rule_details = {'context': {'obj': 'age'},
                    'operator': 'great-equals',
                    'target': 18}
    rule_type = 'simple'
    parent_id = '1'
    result = store.add_purchase_rule(rule_details, rule_type, parent_id)
    added_rule = store.get_purchase_policy().get_purchase_rules().children[0].parse()
    expected_rule = copy.deepcopy(rule_details)
    expected_rule['id'] = '2'
    assert result.succeeded() and added_rule == expected_rule


def test_add_complex_purchase_rule_and_simple_child_success(store: Store):
    complex_rule_details = {'operator': 'or'}
    simple_rule_details = {'context': {'obj': 'age'}, 'operator': 'great-equals', 'target': 18}
    complex_parent_id = '1'
    simple_parent_id = '2'
    result_complex = store.add_purchase_rule(complex_rule_details, 'complex', complex_parent_id)
    result_simple = store.add_purchase_rule(simple_rule_details, 'simple', simple_parent_id)
    added_rules = store.get_purchase_policy().get_purchase_rules().children[0].parse()
    expected_rule = {'id': '2',
                     'operator': 'or',
                     'children':
                         [{'id': '3', 'context': {'obj': 'age'},
                           'operator': 'great-equals',
                           'target': 18}]}
    assert result_simple.succeeded() and result_complex.succeeded() and added_rules == expected_rule


def test_add_conditional_rule_success(store: Store):
    complex_rule_details = {'operator': 'conditional'}
    test_clause_details = {'context': {'obj': 'bag'}, 'operator': 'great-equals', 'target': 40}
    then_clause_details = {'context': {'obj': 'category', 'identifier': 'milk products'}, 'operator': 'equals',
                           'target': 10}
    complex_parent_id = '1'
    test_then_clause_parent_id = '2'
    result_complex = store.add_purchase_rule(complex_rule_details, 'complex', complex_parent_id)
    result_test_clause = store.add_purchase_rule(test_clause_details, 'simple', test_then_clause_parent_id, clause="test")
    result_then_clause = store.add_purchase_rule(then_clause_details, 'simple', test_then_clause_parent_id, clause="then")
    added_rules = store.get_purchase_policy().get_purchase_rules().children[0].parse()
    expected_rule = {'id': '2',
                     'operator': 'conditional',
                     'test': {'id': '3', 'context': {'obj': 'bag'}, 'operator': 'great-equals', 'target': 40},
                     'then': {'id': '4', 'context': {'obj': 'category', 'identifier': 'milk products'}, 'operator': 'equals',
                              'target': 10}}
    assert result_complex.succeeded() and result_test_clause.succeeded() and result_then_clause.succeeded() and \
           added_rules == expected_rule
# endregion

# def test_remove_simple_purchase_rule_success(store: Store):