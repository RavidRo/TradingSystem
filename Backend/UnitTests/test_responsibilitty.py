from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.UnitTests.stubs.member_stub import MemberStub
from Backend.UnitTests.stubs.store_stub import StoreStub
import pytest

#* fixtures
#* ==========================================================================================
@pytest.fixture
def store():
    return StoreStub()

@pytest.fixture
def member():
    return MemberStub()

@pytest.fixture
def founder(store, member):
    return Founder(member, store)

@pytest.fixture
def owner(store, member):
    return Owner(member, store)

@pytest.fixture
def manager(store, member):
    return Manager(member, store)

#* constructor tests
#* ==========================================================================================
def test_constructor_setting_self_in_state(store, member):
    founder = Founder(member, store)
    assert member.store_responsibility[store.get_id()] == founder

def test_constructor_setting_store_correctly(store, member):
    founder = Founder(member, store)
    assert founder.store == store

def test_constructor_setting_state_correctly(store, member):
    founder = Founder(member, store)
    assert founder.user_state == member

def test_constructor_no_initial_apppoints(founder):
    assert founder.appointed == []

def test_constructor_doing_the_same_for_all_subclasses(store, member):
    founder = Founder(member, store)
    owner = Owner(member, store)
    manager = Manager(member, store)

    assert founder.appointed == owner.appointed and owner.appointed == manager.appointed
    assert founder.store == owner.store and owner.store == manager.store
    assert founder.user_state == owner.user_state and owner.user_state == manager.user_state


#* add product tests - #4.1
#* ==========================================================================================
def test_founder_add_product_calls_store_successfully(founder : Founder):
    assert founder.add_product("", 0, 0).succeeded()

def test_owner_add_product_calls_store_successfully(owner : Owner):
    assert owner.add_product("", 0, 0).succeeded()

def test_manager_add_product_prohibited_by_default(manager : Manager):
    assert not manager.add_product("", 0, 0).succeeded()

#* remove product tests - #4.1
#* ==========================================================================================
def test_founder_remove_product_calls_store_successfully(founder : Founder):
    assert founder.remove_product("0").succeeded()

def test_owner_remove_product_calls_store_successfully(owner : Owner):
    assert owner.remove_product("0").succeeded()

def test_manager_remove_product_prohibited_by_default(manager : Manager):
    assert not manager.remove_product("0").succeeded()

#* change product quantity tests - #4.1
#* ==========================================================================================
def test_founder_change_product_quantity_calls_store_successfully(founder : Founder):
    assert founder.change_product_quantity("0", 0).succeeded()

def test_owner_change_product_quantity_calls_store_successfully(owner : Owner):
    assert owner.change_product_quantity("0", 0).succeeded()

def test_manager_change_product_quantity_prohibited_by_default(manager : Manager):
    assert not manager.change_product_quantity("0", 0).succeeded()

#* edit product details tests - #4.1
#* ==========================================================================================
def test_founder_edit_product_details_calls_store_successfully(founder : Founder):
    assert founder.edit_product_details("0", "", 0).succeeded()

def test_owner_edit_product_details_calls_store_successfully(owner : Owner):
    assert owner.edit_product_details("0", "", 0).succeeded()

def test_manager_edit_product_details_prohibited_by_default(manager : Manager):
    assert not manager.edit_product_details("0","", 0).succeeded()

#* appoint owner tests - #4.3
#* ==========================================================================================
# def test_founder_edit_product_details_calls_store_successfully(founder : Founder):
#     assert founder.edit_product_details("0", "", 0).succeeded()

# def test_owner_edit_product_details_calls_store_successfully(owner : Owner):
#     assert owner.edit_product_details("0", "", 0).succeeded()

def test_manager_appoint_owner_is_prohibited(manager : Manager):
    assert not manager.appoint_owner().succeeded()