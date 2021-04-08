from typing import List

import pytest
from ..Domain.TradingSystem.guest import Guest
from ..Domain.TradingSystem.member import Member
from ..Domain.TradingSystem.admin import Admin
from ..Domain.TradingSystem.store import Store
from .stubs.store_stub import StoreStub
from .stubs.authentication_stub import AuthenticationStub
from .stubs.user_stub import UserStub
from .stubs.cart_stub import CartStub
from .stubs.responsibliity_stub import ResponsibilityStub
from Backend.response import ParsableList


# * fixtures
# * ==========================================================================================

@pytest.fixture
def cart():
    return CartStub()


@pytest.fixture
def guest(guest_user, authentication, cart):
    return Guest(guest_user, authentication, cart)


@pytest.fixture
def member_with_responsibility(member_user, cart):
    return Member(member_user, "inon", responsibilities={"0": responsibility}, cart=cart)


@pytest.fixture
def member_without_responsibility(member_user, cart):
    return Member(member_user, "inon", cart=cart)


@pytest.fixture
def admin(admin_user, cart):
    return Admin(admin_user, "admin", cart)


@pytest.fixture
def store():
    return StoreStub()


@pytest.fixture
def authentication():
    return AuthenticationStub()


@pytest.fixture
def guest_user(guest):
    return UserStub(guest)


@pytest.fixture
def member_user(member_with_responsibility):
    return UserStub(member_with_responsibility)


@pytest.fixture
def admin_user(admin):
    return UserStub(admin)


@pytest.fixture
def responsibility():
    return ResponsibilityStub()


# * Constructor tests
# * =================================================================

def test_user_assigned_in_guest(guest_user):
    guest = Guest(guest_user)
    assert guest.user == guest_user


def test_user_assigned_in_member(member_user):
    member = Member(member_user, "inon")
    assert member.user == member_user


def test_user_assigned_in_admin(admin_user):
    admin = Admin(admin_user, "admin")
    assert admin.user == admin_user


# * Register (2.3)
# * =================================================================

def test_register_delegate_authentication(guest, authentication):
    guest.register("me", "123")
    assert authentication.registered


def test_member_cannot_register(member_with_responsibility):
    assert not member_with_responsibility.register("me", "123").succeeded()


def test_admin_cannot_register(admin):
    assert not admin.register("me", "123").succeeded()


# * Login (2.4)
# * =================================================================

def test_login_delegate_authentication(guest, authentication):
    guest.login("me", "123")
    assert authentication.logged_in


def test_member_cannot_login(member_with_responsibility):
    assert not member_with_responsibility.login("me", "123").succeeded()


def test_admin_cannot_login(admin):
    assert not admin.login("me", "123").succeeded()


def test_guest_turns_to_member(guest_user):
    guest_user.login("inon", "123")
    assert isinstance(guest_user.state, Member)


def test_guest_turns_to_admin(guest_user):
    guest_user.login("admin", "123")
    assert isinstance(guest_user.state, Admin)


# * Save Products In Cart (2.7) Only delegate
# * =================================================================

def test_guest_save_products_delegate(guest):
    guest.save_product_in_cart("0", "0", 3)
    assert guest.cart.save_products


def test_member_save_products_delegate(member_with_responsibility):
    member_with_responsibility.save_product_in_cart("0", "0", 3)
    assert member_with_responsibility.cart.save_products


def test_admin_save_products_delegate(admin):
    admin.save_product_in_cart("0", "0", 3)
    assert admin.cart.save_products


# * Cart Options (2.8)
# * =================================================================

def test_show_cart(member_with_responsibility):
    response = member_with_responsibility.show_cart()
    assert response.succeeded()


def test_remove_product_delegate(guest):
    guest.remove_product("0", "0")
    assert guest.cart.remove_product


def test_change_quantity_delegate(guest):
    guest.change_product_quantity("0", "0", 1)
    assert guest.cart.change_quantity


# * Buy cart (2.9)
# * =================================================================

def test_buy_cart_delegate(guest_user):
    guest_user.state.buy_cart(guest_user)
    assert guest_user.state.cart.buy_cart


def test_delete_after_purchase_delegated(guest):
    guest.delete_products_after_purchase()
    assert guest.cart.remove_after_purchase


def test_delete_after_purchase_history_really_added(member_without_responsibility):
    member_without_responsibility.delete_products_after_purchase()
    assert len(member_without_responsibility.purchase_details) > 0


# * Open Store (3.2)
# * =================================================================


def test_guest_cannot_open_store(guest):
    response = guest.open_store("store_name")
    assert not response.succeeded()


def test_open_store_return_type(member_with_responsibility):
    response = member_with_responsibility.open_store("store_name")
    assert response.succeeded and isinstance(response.object, Store)


def test_open_store_really_added(member_with_responsibility):
    response = member_with_responsibility.open_store("store_name")
    assert len(member_with_responsibility.responsibilities) > 0 and member_with_responsibility.responsibilities[
        response.object.get_id()] is not None


# * Personal History (3.7)
# * =================================================================

def test_guest_dont_have_history(guest):
    response = guest.get_purchase_history()
    assert not response.succeeded()


def test_get_personal_history_return_type(member_with_responsibility):
    response = member_with_responsibility.get_purchase_history()
    assert response.succeeded() and isinstance(response.object, ParsableList) and isinstance(response.object.values,
                                                                                             List)


# * Store Inventory Management (4.1)
# * =================================================================

def test_guest_cannot_add_product(guest):
    response = guest.add_new_product("0", "", 4, 1)
    assert not response.succeeded()


def test_member_need_responsibility_to_add_product(member_without_responsibility):
    response = member_without_responsibility.add_new_product("0", "", 4, 1)
    assert not response.succeeded()


def test_member_add_product_delegated(member_with_responsibility):
    member_with_responsibility.add_new_product("0", "", 4, 1)
    assert member_with_responsibility.responsibilities["0"].add_product_delegated


def test_guest_cannot_remove_product(guest):
    response = guest.remove_product("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_remove_product(member_without_responsibility):
    response = member_without_responsibility.remove_product("0", "")
    assert not response.succeeded()


def test_member_remove_product_delegated(member_with_responsibility):
    member_with_responsibility.remove_product("0", "")
    assert member_with_responsibility.responsibilities["0"].remove_product_delegated


def test_guest_cannot_change_product_quantity(guest):
    response = guest.change_product_quantity("0", "", 5)
    assert not response.succeeded()


def test_member_need_responsibility_to_change_quantity(member_without_responsibility):
    response = member_without_responsibility.change_product_quantity("0", "", 5)
    assert not response.succeeded()


def test_member_change_quantity_delegated(member_with_responsibility):
    member_with_responsibility.change_product_quantity("0", "", 0)
    assert member_with_responsibility.responsibilities["0"].change_product_quantity_delegated


def test_guest_cannot_edit_product_details(guest):
    response = guest.edit_product_details("0", "", "", 5)
    assert not response.succeeded()


def test_member_need_responsibility_to_edit_details(member_without_responsibility):
    response = member_without_responsibility.edit_product_details("0", "", "", 5)
    assert not response.succeeded()


def test_member_edit_details_delegated(member_with_responsibility):
    member_with_responsibility.edit_product_details("0", "", "", 5)
    assert member_with_responsibility.responsibilities["0"].edit_product_details_delegated


# * Appoint Owner (4.3)
# * =================================================================

def test_guest_cannot_appoint_new_owner(guest):
    response = guest.appoint_new_store_owner("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_appoint_owner(member_without_responsibility):
    response = member_without_responsibility.appoint_new_store_owner("0", "")
    assert not response.succeeded()


def test_member_appoint_owner_delegated(member_with_responsibility):
    member_with_responsibility.appoint_new_store_owner("0", "")
    assert member_with_responsibility.responsibilities["0"].appoint_owner_delegated


# * Appoint Manager (4.5)
# * =================================================================

def test_guest_cannot_appoint_manager(guest):
    response = guest.appoint_new_store_manager("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_appoint_manager(member_without_responsibility):
    response = member_without_responsibility.appoint_new_store_manager("0", "")
    assert not response.succeeded()


def test_member_appoint_manager_delegate(member_with_responsibility):
    member_with_responsibility.appoint_new_store_manager("0", "")
    assert member_with_responsibility.responsibilities["0"].appoint_manager_delegated


# * Manage Permissions (4.6)
# * =================================================================

def test_guest_cannot_add_permission(guest):
    response = guest.add_manager_permission("0", "", 0)
    assert not response.succeeded()


def test_member_need_responsibility_to_add_permission(member_without_responsibility):
    response = member_without_responsibility.add_manager_permission("0", "", 0)
    assert not response.succeeded()


def test_member_add_permission_delegated(member_with_responsibility):
    member_with_responsibility.add_manager_permission("0", "", 0)
    assert member_with_responsibility.responsibilities["0"].add_permission_delegated


def test_guest_cannot_remove_permission(guest):
    response = guest.remove_manager_permission("0", "", 0)
    assert not response.succeeded()


def test_member_need_responsibility_to_remove_permission(member_without_responsibility):
    response = member_without_responsibility.remove_manager_permission("0", "", 0)
    assert not response.succeeded()


def test_member_remove_permission_delegated(member_with_responsibility):
    member_with_responsibility.remove_manager_permission("0", "", 0)
    assert member_with_responsibility.responsibilities["0"].remove_permission_delegated


# * Dismiss Appointment (4.4, 4.7)
# * =================================================================

def test_guest_cannot_remove_appointment(guest):
    response = guest.remove_appointment("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_remove_appointment(member_without_responsibility):
    response = member_without_responsibility.remove_appointment("0", "")
    assert not response.succeeded()


def test_member_remove_appointment_delegated(member_with_responsibility):
    member_with_responsibility.remove_appointment("0", "")
    assert member_with_responsibility.responsibilities["0"].dismiss_delegated


# * Get Personnel Info (4.9)
# * =================================================================

def test_guest_cannot_get_personnel_info(guest):
    response = guest.get_store_personnel_info("0")
    assert not response.succeeded()


def test_member_need_responsibility_to_get_personnel_info(member_without_responsibility):
    response = member_without_responsibility.get_store_personnel_info("0")
    assert not response.succeeded()


def test_member_get_personnel_info_delegated(member_with_responsibility):
    member_with_responsibility.get_store_personnel_info("0")
    assert member_with_responsibility.responsibilities["0"].get_personnel_info_delegated


# * Get Store Purchase History (4.11)
# * =================================================================

def test_guest_cannot_get_store_purchase_history(guest):
    response = guest.get_store_purchase_history("0")
    assert not response.succeeded()


def test_member_need_responsibility_to_get_store_purchase_history(member_without_responsibility):
    response = member_without_responsibility.get_store_purchase_history("0")
    assert not response.succeeded()


def test_member_get_store_purchase_history_delegated(member_with_responsibility):
    member_with_responsibility.get_store_purchase_history("0")
    assert member_with_responsibility.responsibilities["0"].get_store_purchase_history_delegated


# * Admin's capability to get various data (6.4)
# * =================================================================

def test_guest_cannot_get_any_store_purchase_history(guest):
    response = guest.get_any_store_purchase_history_admin("0")
    assert not response.succeeded()


def test_member_cannot_get_any_store_purchase_history(member_with_responsibility):
    response = member_with_responsibility.get_any_store_purchase_history_admin("0")
    assert not response.succeeded()


# Cannot test delegation to TradingSystemManager is static


def test_guest_cannot_get_any_user_purchase_history(guest):
    response = guest.get_user_purchase_history_admin("")
    assert not response.succeeded()


def test_member_cannot_get_any_user_purchase_history(member_with_responsibility):
    response = member_with_responsibility.get_user_purchase_history_admin("")
    assert not response.succeeded()


# Cannot test delegation to TradingSystemManager is static
