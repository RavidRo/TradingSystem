import pytest

from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission
from Backend.Domain.TradingSystem.Responsibilities.manager import Manager
from Backend.Domain.TradingSystem.Responsibilities.owner import Owner
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder

from .stubs.member_stub import MemberStub
from .stubs.store_stub import StoreStub
from .stubs.user_stub import UserStub

# * fixtures
# * ==========================================================================================
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


@pytest.fixture
def user():
    return UserStub()


# * constructor tests
# * ==========================================================================================
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


# * add product tests - #4.1
# * ==========================================================================================
def test_founder_add_product_calls_store_successfully(founder: Founder):
    assert founder.add_product("", 0, 0).succeeded()


def test_owner_add_product_calls_store_successfully(owner: Owner):
    assert owner.add_product("", 0, 0).succeeded()


def test_manager_add_product_prohibited_by_default(manager: Manager):
    assert not manager.add_product("", 0, 0).succeeded()


# * remove product tests - #4.1
# * ==========================================================================================
def test_founder_remove_product_calls_store_successfully(founder: Founder):
    assert founder.remove_product("0").succeeded()


def test_owner_remove_product_calls_store_successfully(owner: Owner):
    assert owner.remove_product("0").succeeded()


def test_manager_remove_product_prohibited_by_default(manager: Manager):
    assert not manager.remove_product("0").succeeded()


# * change product quantity tests - #4.1
# * ==========================================================================================
def test_founder_change_product_quantity_calls_store_successfully(founder: Founder):
    assert founder.change_product_quantity_in_store("0", 0).succeeded()


def test_owner_change_product_quantity_calls_store_successfully(owner: Owner):
    assert owner.change_product_quantity_in_store("0", 0).succeeded()


def test_manager_change_product_quantity_prohibited_by_default(manager: Manager):
    assert not manager.change_product_quantity_in_store("0", 0).succeeded()


# * edit product details tests - #4.1
# * ==========================================================================================
def test_founder_edit_product_details_calls_store_successfully(founder: Founder):
    assert founder.edit_product_details("0", "", 0).succeeded()


def test_owner_edit_product_details_calls_store_successfully(owner: Owner):
    assert owner.edit_product_details("0", "", 0).succeeded()


def test_manager_edit_product_details_prohibited_by_default(manager: Manager):
    assert not manager.edit_product_details("0", "", 0).succeeded()


# * appoint owner tests - #4.3
# * ==========================================================================================
def test_founder_appoint_owner_successfully(founder: Founder, user):
    assert founder.appoint_owner(user).succeeded()


def test_owner_appoint_owner_successfully(owner: Owner, user):
    assert owner.appoint_owner(user).succeeded()


def test_cant_appoint_an_already_appointed_user(member, store: StoreStub, user):
    founder = Founder(member, store)
    user.appoint(store.get_id())
    assert not founder.appoint_owner(user).succeeded()


def test_cant_appoint_a_user_twice_to_the_same_store_as_owner(founder, user):
    founder.appoint_owner(user).succeeded()
    assert not founder.appoint_owner(user).succeeded()


def test_manager_appoint_owner_is_prohibited(manager: Manager, user):
    assert not manager.appoint_owner(user).succeeded()


# * appoint manager tests - #4.5
# * ==========================================================================================
def test_founder_appoint_manager_successfully(founder: Founder, user):
    assert founder.appoint_manager(user).succeeded()


def test_owner_appoint_manager_successfully(owner: Owner, user):
    assert owner.appoint_manager(user).succeeded()


def test_cant_appoint_an_already_appointed_user(member, store: StoreStub, user):
    founder = Founder(member, store)
    user.appoint(store.get_id())
    assert not founder.appoint_manager(user).succeeded()


def test_cant_appoint_a_user_twice_to_the_same_store_as_manager(founder, user):
    founder.appoint_manager(user).succeeded()
    assert not founder.appoint_manager(user).succeeded()


def test_manager_appoint_manager_is_prohibited_by_default(manager: Manager, user):
    assert not manager.appoint_manager(user).succeeded()


# * add manager permission tests - #4.6
# * ==========================================================================================
def test_founder_add_manager_permission_successfully(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert founder.add_manager_permission(
        member2.get_username(), Permission.MANAGE_PRODUCTS
    ).succeeded()


def test_owner_add_manager_permission_successfully(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    owner = Owner(member1, store)
    manager = Manager(member2, store)
    owner.appointed.append(manager)

    assert owner.add_manager_permission(
        member2.get_username(), Permission.MANAGE_PRODUCTS
    ).succeeded()


def test_can_add_same_permission_twice(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    founder.add_manager_permission(member2.get_username(), Permission.MANAGE_PRODUCTS)
    assert founder.add_manager_permission(
        member2.get_username(), Permission.MANAGE_PRODUCTS
    ).succeeded()


def test_manager_gained_the_permission(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    owner = Owner(member1, store)
    manager = Manager(member2, store)
    owner.appointed.append(manager)

    owner.add_manager_permission(member2.get_username(), Permission.MANAGE_PRODUCTS).succeeded()
    assert manager.add_product("", 0, 0).succeeded()


def test_add_permission_fails_when_personal_never_appointed(founder):
    assert not founder.add_manager_permission(
        "some_manager", Permission.MANAGE_PRODUCTS
    ).succeeded()


def test_add_permission_fails_when_username_was_never_appointed(founder, store):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert not founder.add_manager_permission(
        "no one's username", Permission.MANAGE_PRODUCTS
    ).succeeded()


def test_add_permission_fails_when_the_given_user_is_not_a_manager(founder, store):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    owner = Owner(member2, store)
    founder.appointed.append(owner)

    assert not founder.add_manager_permission(
        member2.get_username(), Permission.MANAGE_PRODUCTS
    ).succeeded()


def test_manager_add_manager_permission_is_prohibited_by_default(
    manager: Manager, store: StoreStub
):
    member1 = MemberStub()
    member2 = MemberStub()
    manager_father = Manager(member1, store)
    manager = Manager(member2, store)
    manager_father.appointed.append(manager)

    assert not manager_father.add_manager_permission(
        member2.get_username(), Permission.MANAGE_PRODUCTS
    ).succeeded()


# * remove manager permission tests - #4.6
# * ==========================================================================================
def test_founder_remove_manager_permission_successfully(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert founder.remove_manager_permission(
        member2.get_username(), Permission.GET_APPOINTMENTS
    ).succeeded()


def test_owner_remove_manager_permission_successfully(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    owner = Owner(member1, store)
    manager = Manager(member2, store)
    owner.appointed.append(manager)

    assert owner.remove_manager_permission(
        member2.get_username(), Permission.GET_APPOINTMENTS
    ).succeeded()


def test_can_remove_manager_permission_twice(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    founder.remove_manager_permission(member2.get_username(), Permission.GET_APPOINTMENTS)
    assert founder.remove_manager_permission(
        member2.get_username(), Permission.GET_APPOINTMENTS
    ).succeeded()


def test_manager_cant_get_appointments_after_permission_removed(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    owner = Owner(member1, store)
    manager = Manager(member2, store)
    owner.appointed.append(manager)

    owner.remove_manager_permission(member2.get_username(), Permission.GET_APPOINTMENTS).succeeded()
    assert not manager.get_store_appointments().succeeded()


def test_remove_permission_fails_when_personal_never_appointed(founder):
    assert not founder.remove_manager_permission(
        "some_manager", Permission.GET_APPOINTMENTS
    ).succeeded()


def test_remove_permission_fails_when_username_was_never_appointed(founder, store):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert not founder.remove_manager_permission(
        "no one's username", Permission.GET_APPOINTMENTS
    ).succeeded()


def test_remove_permission_fails_when_the_given_user_is_not_a_manager(founder, store):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    owner = Owner(member2, store)
    founder.appointed.append(owner)

    assert not founder.remove_manager_permission(
        member2.get_username(), Permission.GET_APPOINTMENTS
    ).succeeded()


def test_manager_remove_manager_permission_is_prohibited_by_default(
    manager: Manager, store: StoreStub
):
    member1 = MemberStub()
    member2 = MemberStub()
    manager_father = Manager(member1, store)
    manager = Manager(member2, store)
    manager_father.appointed.append(manager)

    assert not manager_father.remove_manager_permission(
        member2.get_username(), Permission.GET_APPOINTMENTS
    ).succeeded()


# * remove appointments tests - #4.4 and #4.7
# * ==========================================================================================
def test_founder_removed_appointment_successfully(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert founder.remove_appointment(member2.get_username()).succeeded()


def test_all_child_appointments_removed_too_when_father_was_removed(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    member3 = MemberStub()
    founder = Founder(member1, store)
    owner = Owner(member2, store)
    manager = Manager(member3, store)
    founder.appointed.append(owner)
    owner.appointed.append(manager)

    founder.remove_appointment(member2.get_username()).succeeded()
    assert not member3.is_appointed(store.get_id())


def test_fails_when_trying_to_remove_himself(store: StoreStub):
    member1 = MemberStub("other username")
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert not founder.remove_appointment(member1.get_username()).succeeded()


def test_fails_when_removing_appointment_of_not_appointed_username(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    founder = Founder(member1, store)
    manager = Manager(member2, store)
    founder.appointed.append(manager)

    assert not founder.remove_appointment("some none appointed username").succeeded()


def test_owner_removed_appointment_successfully(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    owner = Owner(member1, store)
    manager = Manager(member2, store)
    owner.appointed.append(manager)

    assert owner.remove_appointment(member2.get_username()).succeeded()


def test_manager_prohibited_from_removing_appointments_by_default(store: StoreStub):
    member1 = MemberStub()
    member2 = MemberStub()
    manager_father = Manager(member1, store)
    manager = Manager(member2, store)
    manager_father.appointed.append(manager)

    assert not manager_father.remove_appointment(member2.get_username()).succeeded()


# * get store appointments tests - #4.9
# * ==========================================================================================
def test_founder_get_store_appointments_calls_store_successfully(founder: Founder):
    assert founder.get_store_appointments().succeeded()


def test_owner_get_store_appointments_calls_store_successfully(owner: Owner):
    assert owner.get_store_appointments().succeeded()


def test_manager_get_store_appointments_allowed_by_default(manager: Manager):
    assert manager.get_store_appointments().succeeded()


# * get store purchase history tests - #4.11
# * ==========================================================================================
def test_founder_get_store_purchase_history_calls_store_successfully(founder: Founder):
    assert founder.get_store_purchase_history().succeeded()


def test_owner_get_store_purchases_history_calls_store_successfully(owner: Owner):
    assert owner.get_store_purchase_history().succeeded()


def test_manager_get_store_purchases_history_prohibited_by_default(manager: Manager):
    assert not manager.get_store_purchase_history().succeeded()