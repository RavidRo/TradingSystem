from typing import List

import pytest
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.store import Store
from .stubs.store_stub import StoreStub
from .stubs.authentication_stub import AuthenticationStub
from .stubs.user_stub import UserStub
from .stubs.cart_stub import CartStub
from .stubs.responsibility_stub import ResponsibilityStub
from Backend.response import ParsableList


# * fixtures
# * ==========================================================================================


@pytest.fixture
def cart():
    return CartStub()


@pytest.fixture
def store():
    return StoreStub()


@pytest.fixture
def authentication():
    return AuthenticationStub()


@pytest.fixture
def guest_user(authentication, cart):
    from Backend.Domain.TradingSystem.States.guest import Guest

    user = UserStub(Guest(None, cart))
    user.state.set_user(user)
    return user


@pytest.fixture
def member_user_with_responsibility(cart, responsibility):
    user = UserStub(Member(None, "inon", responsibilities={"0": responsibility}, cart=cart))
    user.state.set_user(user)
    return user


@pytest.fixture
def member_user_without_responsibility(cart):
    user = UserStub(Member(None, "user", cart=cart))
    user.state.set_user(user)
    return user


@pytest.fixture
def admin_user(cart):
    from Backend.Domain.TradingSystem.States.admin import Admin

    user = UserStub(Admin(None, "admin", cart=cart))
    user.state.set_user(user)
    return user


@pytest.fixture
def responsibility():
    return ResponsibilityStub()


# * Constructor tests
# * =================================================================


def test_user_assigned_in_guest(guest_user, authentication):
    from Backend.Domain.TradingSystem.States.guest import Guest

    guest = Guest(guest_user, authentication)
    assert guest.user == guest_user


def test_user_assigned_in_member(member_user_with_responsibility):
    member = Member(member_user_with_responsibility, "inon")
    assert member.user == member_user_with_responsibility


def test_user_assigned_in_admin(admin_user):
    from Backend.Domain.TradingSystem.States.admin import Admin

    admin = Admin(admin_user, "inon")
    assert admin.user == admin_user


# * Register (2.3)
# * =================================================================


def test_member_cannot_register(member_user_with_responsibility):
    assert not member_user_with_responsibility.state.register("me", "123").succeeded()


def test_admin_cannot_register(admin_user):
    assert not admin_user.state.register("me", "123").succeeded()


# * Login (2.4)
# * =================================================================


def test_member_cannot_login(member_user_with_responsibility):
    member_user_with_responsibility.state.register("me", "123")
    assert not member_user_with_responsibility.state.login("me", "123").succeeded()


def test_admin_cannot_login(admin_user):
    assert not admin_user.state.login("omer", "123").succeeded()


def test_guest_turns_to_member(guest_user):
    guest_user.state.register("user", "123")
    guest_user.state.login("user", "123")
    assert isinstance(guest_user.state, Member)


def test_guest_turns_to_admin(guest_user):
    guest_user.state.login("tali", "cool-kidz")
    from Backend.Domain.TradingSystem.States.admin import Admin

    assert isinstance(guest_user.state, Admin)

# def test_login_as_none_admin_returns_false(auth: Authentication):
#     auth.register(
#         "test_login_as_none_admin_returns_false", "test_login_as_none_admin_returns_false"
#     )
#     response = auth.login(
#         "test_login_as_none_admin_returns_false", "test_login_as_none_admin_returns_false"
#     )
#     assert response.succeeded() and not response.get_obj().get_val(), response.get_msg()

# * Save Products In Cart (2.7) Only delegate
# * =================================================================


def test_guest_save_products_delegate(guest_user):
    guest_user.state.save_product_in_cart("0", "0", 3)
    assert guest_user.state.cart.save_product


def test_member_save_products_delegate(member_user_with_responsibility):
    member_user_with_responsibility.state.save_product_in_cart("0", "0", 3)
    assert member_user_with_responsibility.state.cart.save_product


def test_admin_save_products_delegate(admin_user):
    admin_user.state.save_product_in_cart("0", "0", 3)
    assert admin_user.state.cart.save_product


# * Cart Options (2.8)
# * =================================================================


def test_show_cart(member_user_with_responsibility):
    response = member_user_with_responsibility.state.show_cart()
    assert response.succeeded()


def test_remove_product_delegate(guest_user):
    guest_user.state.delete_from_cart("0", "0")
    assert guest_user.state.cart.remove_product_delegated


def test_change_quantity_delegate(guest_user):
    guest_user.state.change_product_quantity_in_cart("0", "0", 1)
    assert guest_user.state.cart.change_quantity


# * Buy cart (2.9)
# * =================================================================


def test_buy_cart_delegate(guest_user):
    guest_user.state.buy_cart(guest_user)
    assert guest_user.state.cart.buy_cart


def test_delete_after_purchase_delegated(guest_user):
    guest_user.state.delete_products_after_purchase()
    assert guest_user.state.cart.remove_after_purchase


def test_delete_after_purchase_history_really_added(member_user_without_responsibility):
    member_user_without_responsibility.state.delete_products_after_purchase()
    assert len(member_user_without_responsibility.state.purchase_details) > 0


# * Open Store (3.2)
# * =================================================================


def test_guest_cannot_open_store(guest_user):
    response = guest_user.state.open_store("store_name")
    assert not response.succeeded()


def test_open_store_return_type(member_user_with_responsibility):
    response = member_user_with_responsibility.state.open_store("store_name")
    assert response.succeeded and isinstance(response.object, Store)


def test_open_store_really_added(member_user_with_responsibility):
    response = member_user_with_responsibility.state.open_store("store_name")
    assert (
        len(member_user_with_responsibility.state.responsibilities) > 0
        and member_user_with_responsibility.state.responsibilities[response.object.get_id()]
        is not None
    )


# * Personal History (3.7)
# * =================================================================


def test_guest_dont_have_history(guest_user):
    response = guest_user.state.get_purchase_history()
    assert not response.succeeded()


def test_get_personal_history_return_type(member_user_with_responsibility):
    response = member_user_with_responsibility.state.get_purchase_history()
    assert (
        response.succeeded()
        and isinstance(response.object, ParsableList)
        and isinstance(response.object.values, List)
    )


# * Store Inventory Management (4.1)
# * =================================================================


def test_guest_cannot_add_product(guest_user):
    response = guest_user.state.add_new_product("0", "productA", 4, 1)
    assert not response.succeeded()


def test_member_need_responsibility_to_add_product(member_user_without_responsibility):
    response = member_user_without_responsibility.state.add_new_product("0", "productA", 4, 1)
    assert not response.succeeded()


def test_member_add_product_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.add_new_product("0", "productA", 4, 1)
    assert member_user_with_responsibility.state.responsibilities["0"].add_product_delegated


def test_guest_cannot_remove_product(guest_user):
    response = guest_user.state.remove_product("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_remove_product(member_user_without_responsibility):
    response = member_user_without_responsibility.state.remove_product("0", "")
    assert not response.succeeded()


def test_member_remove_product_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.remove_product("0", "")
    assert member_user_with_responsibility.state.responsibilities["0"].remove_product_delegated


def test_guest_cannot_change_product_quantity(guest_user):
    response = guest_user.state.change_product_quantity_in_store("0", "", 5)
    assert not response.succeeded()


def test_member_need_responsibility_to_change_quantity(member_user_without_responsibility):
    response = member_user_without_responsibility.state.change_product_quantity_in_store("0", "", 5)
    assert not response.succeeded()


def test_member_change_quantity_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.change_product_quantity_in_store("0", "", 0)
    assert member_user_with_responsibility.state.responsibilities[
        "0"
    ].change_product_quantity_delegated


def test_guest_cannot_edit_product_details(guest_user):
    response = guest_user.state.edit_product_details("0", "", "productB", 5)
    assert not response.succeeded()


def test_member_need_responsibility_to_edit_details(member_user_without_responsibility):
    response = member_user_without_responsibility.state.edit_product_details("0", "", "productB", 5)
    assert not response.succeeded()


def test_member_edit_details_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.edit_product_details("0", "", "productB", 5)
    assert member_user_with_responsibility.state.responsibilities[
        "0"
    ].edit_product_details_delegated


# * Appoint Owner (4.3)
# * =================================================================


def test_guest_cannot_appoint_new_owner(guest_user):
    response = guest_user.state.appoint_new_store_owner("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_appoint_owner(member_user_without_responsibility):
    response = member_user_without_responsibility.state.appoint_new_store_owner("0", "")
    assert not response.succeeded()


def test_member_appoint_owner_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.appoint_new_store_owner("0", "")
    assert member_user_with_responsibility.state.responsibilities["0"].appoint_owner_delegated


# * Appoint Manager (4.5)
# * =================================================================


def test_guest_cannot_appoint_manager(guest_user):
    response = guest_user.state.appoint_new_store_manager("0", "")
    assert not response.succeeded()


def test_member_need_responsibility_to_appoint_manager(member_user_without_responsibility):
    response = member_user_without_responsibility.state.appoint_new_store_manager("0", "")
    assert not response.succeeded()


def test_member_appoint_manager_delegate(member_user_with_responsibility):
    member_user_with_responsibility.state.appoint_new_store_manager("0", "")
    assert member_user_with_responsibility.state.responsibilities["0"].appoint_manager_delegated


# * Manage Permissions (4.6)
# * =================================================================


def test_guest_cannot_add_permission(guest_user):
    response = guest_user.state.add_manager_permission("0", "inon", 0)
    assert not response.succeeded()


def test_member_need_responsibility_to_add_permission(member_user_without_responsibility):
    response = member_user_without_responsibility.state.add_manager_permission("0", "inon", 0)
    assert not response.succeeded()


def test_member_add_permission_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.add_manager_permission("0", "inon", 0)
    assert member_user_with_responsibility.state.responsibilities["0"].add_permission_delegated


def test_guest_cannot_remove_permission(guest_user):
    response = guest_user.state.remove_manager_permission("0", "inon", 0)
    assert not response.succeeded()


def test_member_need_responsibility_to_remove_permission(member_user_without_responsibility):
    response = member_user_without_responsibility.state.remove_manager_permission("0", "inon", 0)
    assert not response.succeeded()


def test_member_remove_permission_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.remove_manager_permission("0", "inon", 0)
    assert member_user_with_responsibility.state.responsibilities["0"].remove_permission_delegated


# * Dismiss Appointment (4.4, 4.7)
# * =================================================================


def test_guest_cannot_remove_appointment(guest_user):
    response = guest_user.state.remove_appointment("0", "inon")
    assert not response.succeeded()


def test_member_need_responsibility_to_remove_appointment(member_user_without_responsibility):
    response = member_user_without_responsibility.state.remove_appointment("0", "inon")
    assert not response.succeeded()


def test_member_remove_appointment_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.remove_appointment("0", "inon")
    assert member_user_with_responsibility.state.responsibilities["0"].dismiss_delegated


# * Get Personnel Info (4.9)
# * =================================================================


def test_guest_cannot_get_personnel_info(guest_user):
    response = guest_user.state.get_store_personnel_info("0")
    assert not response.succeeded()


def test_member_need_responsibility_to_get_personnel_info(member_user_without_responsibility):
    response = member_user_without_responsibility.state.get_store_personnel_info("0")
    assert not response.succeeded()


def test_member_get_personnel_info_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.get_store_personnel_info("0")
    assert member_user_with_responsibility.state.responsibilities["0"].get_personnel_info_delegated


# * Get Store Purchase History (4.11)
# * =================================================================


def test_guest_cannot_get_store_purchase_history(guest_user):
    response = guest_user.state.get_store_purchase_history("0")
    assert not response.succeeded()


def test_member_need_responsibility_to_get_store_purchase_history(
    member_user_without_responsibility,
):
    response = member_user_without_responsibility.state.get_store_purchase_history("0")
    assert not response.succeeded()


def test_member_get_store_purchase_history_delegated(member_user_with_responsibility):
    member_user_with_responsibility.state.get_store_purchase_history("0")
    assert member_user_with_responsibility.state.responsibilities[
        "0"
    ].get_store_purchase_history_delegated


# * Admin's capability to get various data (6.4)
# * =================================================================


def test_guest_cannot_get_any_store_purchase_history(guest_user):
    response = guest_user.state.get_any_store_purchase_history_admin("0")
    assert not response.succeeded()


def test_member_cannot_get_any_store_purchase_history(member_user_with_responsibility):
    response = member_user_with_responsibility.state.get_any_store_purchase_history_admin("0")
    assert not response.succeeded()


# Cannot test delegation, TradingSystemManager is static


def test_guest_cannot_get_any_user_purchase_history(guest_user):
    response = guest_user.state.get_user_purchase_history_admin("inon")
    assert not response.succeeded()


def test_member_cannot_get_any_user_purchase_history(member_user_with_responsibility):
    response = member_user_with_responsibility.state.get_user_purchase_history_admin("inon")
    assert not response.succeeded()


# Cannot test delegation, TradingSystemManager is static
