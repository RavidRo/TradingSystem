import pytest
import json

from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.user import User
import Backend.Service.logs as logs
from Backend.settings import Settings

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


@pytest.fixture
def user_member2():
    user = User()
    user.register("some_username2", "password")
    user.login("some_username2", "password")
    return user


@pytest.fixture
def user_member3():
    user = User()
    user.register("some_username3", "password")
    user.login("some_username3", "password")
    return user


@pytest.fixture(autouse=True)
def user_admin():
    s = Settings.get_instance(True)
    user = User()
    user.login(s.get_admins()[0], s.get_password())
    return user


@pytest.fixture(autouse=True)
def user_admin2():
    user = User()
    s = Settings.get_instance(True)
    user.login(s.get_admins()[1], s.get_password())
    return user


@pytest.fixture(autouse=True)
def user_admin3():
    user = User()
    s = Settings.get_instance(True)
    user.login(s.get_admins()[2], s.get_password())
    return user


@pytest.fixture(params=[True, False])
def member(request, user_member, user_admin):
    if request.param:
        return user_member
    return user_admin


@pytest.fixture(params=[True, False])
def member2(request, user_member2, user_admin2):
    if request.param:
        return user_member2
    return user_admin2


@pytest.fixture(params=[True, False])
def member3(request, user_member3, user_admin3):
    if request.param:
        return user_member3
    return user_admin3


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
def test_can_not_create_product_to_none_existent_store(member: User):
    store: Store = member.create_store("test_can_not_create_product_to_unassigned_store").get_obj()
    assert not member.create_product("some_wrong_id", "new_product", "A", 19.90, 5).succeeded()


def test_can_not_create_product_to_unassigned_store(member: User, user_member2: User):
    store: Store = member.create_store("test_can_not_create_product_to_unassigned_store").get_obj()
    assert not user_member2.create_product(store.get_id(), "new_product", "A", 19.90, 5).succeeded()


def test_adds_product_successfully(member: User):
    store: Store = member.create_store("test_adds_product_successfully").get_obj()
    assert member.create_product(store.get_id(), "new_product", "A", 19.90, 5).succeeded()


def test_cant_add_product_with_negative_quantity(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_quantity").get_obj()
    assert not member.create_product(store.get_id(), "new_product", "A", 19.90, -5).succeeded()


def test_cant_add_product_with_negative_price(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert not member.create_product(store.get_id(), "new_product", "A", -19.90, 5).succeeded()


def test_cant_add_2_products_with_same_name(member: User):
    store: Store = member.create_store("store_name").get_obj()
    member.create_product(store.get_id(), "new_product", "A", 19.90, 3).succeeded()
    assert not member.create_product(store.get_id(), "new_product", "A", 19.90, 5).succeeded()


def test_can_add_products_free_price(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert member.create_product(store.get_id(), "new_product", "A", 0, 5).succeeded()


def test_can_add_products_with_zero_quantity(member: User):
    store: Store = member.create_store("test_cant_add_product_with_negative_price").get_obj()
    assert member.create_product(store.get_id(), "new_product", "A", 20.7, 0).succeeded()


def test_cant_add_products_with_empty_strings(member: User):
    store: Store = member.create_store("test_cant_add_products_with_empty_strings").get_obj()
    assert not member.create_product(store.get_id(), "", "A", 20.7, 30).succeeded()


# * remove_product_from_store
# * =================================================================
def test_can_not_remove_product_from_none_existent_store(member: User):
    store: Store = member.create_store(
        "test_can_not_remove_product_from_none_existent_store"
    ).get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.remove_product_from_store("some_wrong_id", product_id).succeeded()


def test_can_not_remove_product_from_unassigned_store(member: User, user_member2: User):
    store: Store = user_member2.create_store(
        "test_can_not_remove_product_from_unassigned_store"
    ).get_obj()
    product_id = user_member2.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.remove_product_from_store(store.get_id(), product_id).succeeded()


def test_removes_product_successfully(member: User):
    store: Store = member.create_store("test_removes_product_successfully").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert member.remove_product_from_store(store.get_id(), product_id).succeeded()


# * change_product_quantity_in_store
# * =================================================================
def test_can_not_change_product_of_none_existent_store(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.change_product_quantity_in_store("some_wrong_id", product_id, 24).succeeded()


def test_can_not_change_product_of_none_existent_product(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.change_product_quantity_in_store(
        store.get_id(), "some_wrong_id", 24
    ).succeeded()


def test_can_not_change_product_of_unassigned_store(member: User, user_member2: User):
    store: Store = user_member2.create_store("store_name").get_obj()
    product_id = user_member2.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.change_product_quantity_in_store(store.get_id(), product_id, 24).succeeded()


def test_changes_product_quantity_in_store_successfully(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert member.change_product_quantity_in_store(store.get_id(), product_id, 24).succeeded()


def test_changes_product_quantity_in_store_to_0_successfully(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert member.change_product_quantity_in_store(store.get_id(), product_id, 0).succeeded()


def test_changes_product_quantity_in_store_to_negative_fails(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.change_product_quantity_in_store(store.get_id(), product_id, -1).succeeded()


# * edit_product_details
# * =================================================================
def test_can_not_edit_product_details_of_none_existent_store(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.edit_product_details(
        "some_wrong_id", product_id, "product name", "B", 123.90
    ).succeeded()


def test_can_not_edit_product_details_of_none_existent_product(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.edit_product_details(
        store.get_id(), "some_wrong_id", "product name", "B", 24.90
    ).succeeded()


def test_can_not_edit_product_details_of_unassigned_store(member: User, user_member2: User):
    store: Store = user_member2.create_store("store_name").get_obj()
    product_id = user_member2.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.edit_product_details(
        store.get_id(), product_id, "product name", "B", 24.90
    ).succeeded()


def test_changes_edit_product_details_of_store_successfully(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert member.edit_product_details(
        store.get_id(), product_id, "product name", "A", 24.90
    ).succeeded()


def test_edit_product_price_in_store_to_0_successfully(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert member.edit_product_details(store.get_id(), product_id, "new_product", "B", 0).succeeded()


def test_edit_product_name_in_store_to_empty_fails(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.edit_product_details(store.get_id(), product_id, "", "B", 5.90).succeeded()


def test_edit_product_category_in_store_to_empty_fails(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert not member.edit_product_details(store.get_id(), product_id, "new_product", "", 5.90).succeeded()


def test_edit_product_details_accepts_none_arguments(member: User):
    store: Store = member.create_store("store_name").get_obj()
    product_id = member.create_product(store.get_id(), "new_product", "A", 19.90, 5).get_obj()
    assert member.edit_product_details(store.get_id(), product_id, None, None, None).succeeded()


# * appoint_owner
# * =================================================================
def test_founder_can_appoint_owner_successfully(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    result = member.appoint_owner(store.get_id(), member2)
    assert result.succeeded(), result.get_msg()


def test_founder_cant_appoint_himself_as_owner(member: User):
    store: Store = member.create_store("store_name").get_obj()
    assert not member.appoint_owner(store.get_id(), member).succeeded()


def test_founder_cant_appoint_guest_as_owner(member: User, user_guest: User):
    store: Store = member.create_store("store_name").get_obj()
    assert not member.appoint_owner(store.get_id(), user_guest).succeeded()


def test_founder_cant_appoint_some_one_twice_as_owner(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    result = member.appoint_owner(store.get_id(), member2)
    assert not result.succeeded(), result.get_msg()


def test_appointed_owner_has_permissions_for_store(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    result = member2.create_product(store.get_id(), "name", "A", 5, 5)
    assert result.succeeded(), result.get_msg()


def test_appointed_owners_can_appoint_more_owners(member: User, member2: User, member3: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    result = member2.appoint_owner(store.get_id(), member3)
    assert result.succeeded(), result.get_msg()


# * appoint_manager
# * =================================================================
def test_founder_can_appoint_manager_successfully(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    result = member.appoint_manager(store.get_id(), member2)
    assert result.succeeded(), result.get_msg()


def test_founder_cant_appoint_himself_as_manager(member: User):
    store: Store = member.create_store("store_name").get_obj()
    assert not member.appoint_manager(store.get_id(), member).succeeded()


def test_founder_cant_appoint_guest_as_manager(member: User, user_guest: User):
    store: Store = member.create_store("store_name").get_obj()
    assert not member.appoint_manager(store.get_id(), user_guest).succeeded()


def test_founder_cant_appoint_some_one_twice_as_manager(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.appoint_manager(store.get_id(), member2)
    assert not result.succeeded(), result.get_msg()


def test_appointed_manager_has_permissions_for_store(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member2.get_store_appointments(store.get_id())
    assert result.succeeded(), result.get_msg()


def test_appointed_manager_cant_appoint_owners(member: User, member2: User, member3: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member2.appoint_manager(store.get_id(), member3)
    assert not result.succeeded(), result.get_msg()


# * add_manager_permission
# * =================================================================
def test_cant_add_permission_to_manager_at_none_existing_store(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.add_manager_permission(
        "wrong_store_id", member2.get_username().get_obj().get_val(), Permission.MANAGE_PRODUCTS
    )
    assert not result.succeeded(), result.get_msg()


def test_cant_add_permission_to_not_assigned_manager(member: User, member2: User, member3: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.add_manager_permission(
        store.get_id(), member3.get_username().get_obj().get_val(), Permission.MANAGE_PRODUCTS
    )
    assert not result.succeeded(), result.get_msg()


def test_managers_cant_add_permissions(member: User, member2: User, member3: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    member.add_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    member2.appoint_manager(store.get_id(), member3)
    result = member2.add_manager_permission(
        store.get_id(), member3.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert not result.succeeded(), result.get_msg()


def test_owners_cant_add_permissions_to_managers_not_assigned_by_him(
    member: User, member2: User, member3: User
):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    member.appoint_owner(store.get_id(), member3)
    result = member3.add_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert not result.succeeded(), result.get_msg()


def test_cant_add_permissions_to_owners(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    result = member.add_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert not result.succeeded(), result.get_msg()


def test_founder_can_add_permissions_to_managers_successfully(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.add_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert result.succeeded(), result.get_msg()


def test_owner_can_add_permissions_to_managers_successfully(
    member: User, member2: User, member3: User
):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    member2.appoint_manager(store.get_id(), member3)
    result = member2.add_manager_permission(
        store.get_id(), member3.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert result.succeeded(), result.get_msg()


# * remove_manager_permission
# * =================================================================
def test_cant_remove_permission_to_manager_at_none_existing_store(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.remove_manager_permission(
        "wrong_store_id", member2.get_username().get_obj().get_val(), Permission.MANAGE_PRODUCTS
    )
    assert not result.succeeded(), result.get_msg()


def test_cant_remove_permission_to_not_assigned_manager(member: User, member2: User, member3: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.remove_manager_permission(
        store.get_id(), member3.get_username().get_obj().get_val(), Permission.MANAGE_PRODUCTS
    )
    assert not result.succeeded(), result.get_msg()


def test_managers_cant_remove_permissions(member: User, member2: User, member3: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    member.add_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    member2.appoint_manager(store.get_id(), member3)
    result = member2.remove_manager_permission(
        store.get_id(), member3.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert not result.succeeded(), result.get_msg()


def test_owners_cant_remove_permissions_to_managers_not_assigned_by_him(
    member: User, member2: User, member3: User
):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    member.appoint_owner(store.get_id(), member3)
    result = member3.remove_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert not result.succeeded(), result.get_msg()


def test_cant_remove_permissions_to_owners(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    result = member.remove_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert not result.succeeded(), result.get_msg()


def test_founder_can_remove_permissions_to_managers_successfully(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    result = member.remove_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert result.succeeded(), result.get_msg()


def test_owner_can_remove_permissions_to_managers_successfully(
    member: User, member2: User, member3: User
):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_owner(store.get_id(), member2)
    member2.appoint_manager(store.get_id(), member3)
    result = member2.remove_manager_permission(
        store.get_id(), member3.get_username().get_obj().get_val(), Permission.APPOINT_MANAGER
    )
    assert result.succeeded(), result.get_msg()


def test_removes_permission_takes_permission_successfully(member: User, member2: User):
    store: Store = member.create_store("store_name").get_obj()
    member.appoint_manager(store.get_id(), member2)
    member.remove_manager_permission(
        store.get_id(), member2.get_username().get_obj().get_val(), Permission.GET_APPOINTMENTS
    )
    result = member2.get_store_appointments(store.get_id())
    assert not result.succeeded(), result.get_msg()


# * remove_appointment
# * =================================================================

# * get_store_appointments
# * =================================================================

# * get_store_purchase_history
# * =================================================================


def test_guest_does_not_have_a_username(user_guest: User):
    assert not user_guest.get_username().succeeded()
