import pytest
import json

from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.user import User

"""
In this test file were are testing all the requirements from user which includes authentication and responsibility.
"""


@pytest.fixture
def user_guest():
    return User()


@pytest.fixture
def user_member():
    user = User()
    user.register("some_username", "password")
    user.login("some_username", "password")
    return user


user_member2 = user_member


@pytest.fixture
def user_admin():
    user = User()
    with open("config.json", "r") as read_file:
        data = json.load(read_file)
        user.login(data["admins"][0], data["admin-password"])
    return user


@pytest.fixture(params=[True, False])
def member(request, user_member, user_admin):
    if request.param:
        return user_member
    return user_admin


# * register
# * =================================================================
def test_registered_members_cant_register_again(user_member):
    assert not user_member.register(
        "test_registered_members_cant_register_again", "pass"
    ).succeeded()


def test_registered_admins_cant_register_again(user_admin):
    assert not user_admin.register("test_registered_admins_cant_register_again", "pass").succeeded()


def test_cant_register_to_taken_username():
    user1 = User()
    user2 = User()
    user1.register("test_cant_register_to_taken_username", "pass")
    assert not user2.register("test_cant_register_to_taken_username", "pass").succeeded()


def test_register_successfully_when_username_is_free(user_guest):
    assert user_guest.register(
        "test_register_successfully_when_username_is_free", "pass"
    ).succeeded()


def test_stays_guest_after_register(user_guest: User):
    state = user_guest.state
    user_guest.register("test_stays_guest_after_register", "pass")
    assert state == user_guest.state


# * login
# * =================================================================
def test_registered_members_cant_login_again(user_guest: User, user_member: User):
    user_guest.register("test_registered_members_cant_login_again", "pass")
    assert not user_member.login("test_registered_members_cant_login_again", "pass").succeeded()


def test_registered_admins_cant_login_again(user_guest: User, user_admin: User):
    user_guest.register("test_registered_members_cant_login_again", "pass")
    assert not user_admin.login("test_registered_members_cant_login_again", "pass").succeeded()


def test_guest_can_register_successfully(user_guest: User):
    user_guest.register("test_guest_can_register_successfully", "pass")
    assert user_guest.login("test_guest_can_register_successfully", "pass").succeeded()


def test_state_changes_after_login(user_guest: User):
    state = user_guest.state
    user_guest.register("test_state_changes_after_login", "pass")
    user_guest.login("test_state_changes_after_login", "pass")
    assert state != user_guest.state


def test_state_changes_after_login_to_logged_username(user_guest: User):
    user_guest.register("test_state_changes_after_login_to_logged_username", "pass")
    user_guest.login("test_state_changes_after_login_to_logged_username", "pass")
    assert (
        user_guest.get_username().get_obj().get_val()
        == "test_state_changes_after_login_to_logged_username"
    )


# * create_store
# * =================================================================
def test_guests_can_not_open_stores(user_guest: User):
    assert not user_guest.create_store("test_guests_can_not_open_stores").succeeded()


def test_members_can_open_stores_successfully(user_member: User):
    assert user_member.create_store("test_members_can_open_stores_successfully").succeeded()


def test_admins_can_open_stores_successfully(user_admin: User):
    assert user_admin.create_store("test_admins_can_open_stores_successfully").succeeded()


def test_stores_names_are_not_unique(user_member: User):
    user_member.create_store("test_stores_names_are_not_unique")
    assert user_member.create_store("test_stores_names_are_not_unique").succeeded()


# * create_product
# * =================================================================
def test_can_not_create_product_to_unassigned_store(member: User, user_member2: User):
    store: Store = member.create_store("test_can_not_create_product_to_unassigned_store").get_obj()
    assert not user_member2.create_product(store.get_id(), "new_product", 19.90, 5).succeeded()


def test_adds_product_successfully(member: User):
    store: Store = member.create_store("test_adds_product_successfully").get_obj()
    assert member.create_product(store.get_id(), "new_product", 19.90, 5).succeeded()


def test_cant_add_product_with_negative_quantity(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_quantity").get_obj()
    assert not member.create_product(store.get_id(), "new_product", 19.90, -5).succeeded()


def test_cant_add_product_with_negative_price(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert not member.create_product(store.get_id(), "new_product", -19.90, 5).succeeded()


def test_cant_add_2_products_with_same_name(member: User):
    store: Store = member.create_store("store_name").get_obj()
    member.create_product(store.get_id(), "new_product", 19.90, 3).succeeded()
    assert not member.create_product(store.get_id(), "new_product", 19.90, 5).succeeded()


def test_can_add_products_free_price(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert member.create_product(store.get_id(), "new_product", 0, 5).succeeded()


def test_can_add_products_with_zero_quantity(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert member.create_product(store.get_id(), "new_product", 20.7, 0).succeeded()


def test_cant_add_products_with_empty_strings(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert not member.create_product(store.get_id(), "", 20.7, 30).succeeded()


# * remove_product_from_store
# * =================================================================

# * change_product_quantity_in_store
# * =================================================================

# * edit_product_details
# * =================================================================

# * appoint_owner
# * =================================================================

# * appoint_manager
# * =================================================================

# * add_manager_permission
# * =================================================================

# * remove_manager_permission
# * =================================================================

# * remove_appointment
# * =================================================================

# * get_store_appointments
# * =================================================================

# * get_store_purchase_history
# * =================================================================


def test_guest_does_not_have_a_username(user_guest: User):
    assert not user_guest.get_username().succeeded()
