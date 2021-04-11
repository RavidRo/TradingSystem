import pytest

from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission
from Backend.Domain.TradingSystem.Interfaces.IUserState import IUserState
from Backend.Domain.TradingSystem.user import User

from .stubs.member_stub import MemberStub


@pytest.fixture(scope="function", autouse=True)
def set_up():
    IUserState.use_mock = True
    yield
    IUserState.use_mock = False


@pytest.fixture
def user() -> User:
    return User()


# * register tests - 2.3
# * ===========================================================
def test_register_deligates_to_state(user: User):
    result = user.register("", "")
    assert user.state._register and result


# * login tests - 2.4
# * ===========================================================
def test_login_deligates_to_state(user: User):
    result = user.login("", "")
    assert user.state._login and result


# * add_to_cart tests - 2.7
# * ===========================================================
def test_add_to_cart_deligates_to_state(user: User):
    result = user.add_to_cart("", "", 0)
    assert user.state._save_product_in_cart and result


# * get_cart_details tests - 2.8
# * ===========================================================
def test_get_cart_details_deligates_to_state(user: User):
    result = user.get_cart_details()
    assert user.state._show_cart and result


# * remove_product_from_cart tests - 2.8
# * ===========================================================
def test_remove_product_from_cart_deligates_to_state(user: User):
    result = user.remove_product_from_cart("", "")
    assert user.state._delete_from_cart and result


# * change_product_quantity in cart tests - 2.8
# * ===========================================================
def test_change_product_quantity_deligates_in_cart_to_state(user: User):
    result = user.change_product_quantity_in_cart("", "", 0)
    assert user.state._change_product_quantity_in_cart and result


# * purchase_cart tests - 2.9
# * ===========================================================
def test_purchase_cart_deligates_to_state(user: User):
    result = user.purchase_cart()
    assert user.state._buy_cart and result


# * purchase_completed tests - 2.9
# * ===========================================================
def test_purchase_completed_deligates_to_state(user: User):
    result = user.purchase_completed()
    assert user.state._delete_products_after_purchase and result


# * create_store tests - 3.2
# * ===========================================================
def test_create_store_deligates_to_state(user: User):
    result = user.create_store("")
    assert user.state._open_store and result


# * get_purchase_history tests - 3.7
# * ===========================================================
def test_get_purchase_history_deligates_to_state(user: User):
    result = user.get_purchase_history()
    assert user.state._get_purchase_history and result


# * create_product tests - 4.1
# * ===========================================================
def test_create_product_deligates_to_state(user: User):
    result = user.create_product("", "", 0, 0)
    assert user.state._add_new_product and result


# * remove_product tests - 4.1
# * ===========================================================
def test_remove_product_from_store_deligates_to_state(user: User):
    result = user.remove_product_from_store("", "")
    assert user.state._remove_product and result


# * change_product_quantity_in_store tests - 4.1
# * ===========================================================
def test_change_product_quantity_in_store_deligates_to_state(user: User):
    result = user.change_product_quantity_in_store("", "", 0)
    assert user.state._change_product_quantity_in_store and result


# * edit_product_details tests - 4.1
# * ===========================================================
def test_edit_product_details_deligates_to_state(user: User):
    result = user.edit_product_details("", "", "", 0)
    assert user.state._edit_product_details and result


# * appoint_owner tests - 4.3
# * ===========================================================
def test_appoint_owner_deligates_to_state(user: User):
    result = user.appoint_owner("", None)
    assert user.state._appoint_new_store_owner and result


# * appoint_manager tests - 4.5
# * ===========================================================
def test_appoint_manager_deligates_to_state(user: User):
    result = user.appoint_manager("", None)
    assert user.state._appoint_new_store_manager and result


# * add_manager_permission tests - 4.6
# * ===========================================================
def test_add_manager_permission_deligates_to_state(user: User):
    result = user.add_manager_permission("", "", Permission.APPOINT_MANAGER)
    assert user.state._add_manager_permission and result


# * remove_manager_permission tests - 4.6
# * ===========================================================
def test_remove_manager_permission_deligates_to_state(user: User):
    result = user.remove_manager_permission("", "", Permission.APPOINT_MANAGER)
    assert user.state._remove_manager_permission and result


# * remove_appointment tests - 4.4 and 4.7
# * ===========================================================
def test_remove_appointment_deligates_to_state(user: User):
    result = user.remove_appointment("", "")
    assert user.state._remove_appointment and result


# * get_store_appointments tests - 4.9
# * ===========================================================
def test_get_store_appointments_deligates_to_state(user: User):
    result = user.get_store_appointments("")
    assert user.state._get_store_personnel_info and result


# * get_store_purchase_history tests - 4.11
# * ===========================================================
def test_get_store_purchase_history_deligates_to_state(user: User):
    result = user.get_store_purchase_history("")
    assert user.state._get_store_purchase_history and result


# * get_any_user_purchase_history tests - 6.4
# * ===========================================================
def test_get_any_user_purchase_history_deligates_to_state(user: User):
    result = user.get_any_user_purchase_history_admin("")
    assert user.state._get_user_purchase_history_admin and result


# * get_any_store_purchase_history tests - 6.4
# * ===========================================================
def test_get_any_store_purchase_history_deligates_to_state(user: User):
    result = user.get_any_store_purchase_history_admin("")
    assert user.state._get_any_store_purchase_history_admin and result


# * is_appointed tests
# * ===========================================================
def test_is_appointed_deligates_to_state(user: User):
    store_id = "123"
    assert not user.is_appointed(store_id)
    user.state.appoints = [store_id]
    assert user.is_appointed(store_id)


# * get_username tests
# * ===========================================================
def test_get_username_deligates_to_state(user: User):
    assert user.state.get_username().get_obj().get_val() == user.get_username().get_obj().get_val()


# * change_state tests
# * ===========================================================
def test_change_state_does_change_the_state(user: User):
    new_state = MemberStub()
    user.change_state(new_state)
    assert user.state == new_state
