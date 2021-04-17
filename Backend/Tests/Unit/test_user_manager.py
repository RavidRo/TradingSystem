import pytest

from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission
from Backend.Domain.TradingSystem.user_manager import UserManager
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser


@pytest.fixture(scope="function", autouse=True)
def set_up(request):
    # This function will get called before every test in the module
    IUser.use_mock = True
    UserManager.cookie_user.clear()
    UserManager.username_user.clear()
    yield
    IUser.use_mock = False
    UserManager.cookie_user.clear()
    UserManager.username_user.clear()


@pytest.fixture
def cookie():
    return UserManager.enter_system()


@pytest.fixture
def cookie2():
    return UserManager.enter_system()


# * enter __system tests - 2.1
# * ==============================================================
def test_enter_system_registers_returned_cookie(cookie):
    cookie_registered = cookie in UserManager.cookie_user
    assert cookie_registered


def test_enter_system_creates_unique_cookie():
    cookies = [UserManager.enter_system() for _ in range(1, 500)]
    assert len(UserManager.cookie_user) == len(cookies)


# * register tests - 2.3
# * ==============================================================
def test_register_successfully(cookie):
    assert UserManager.register("username", "password", cookie).succeeded()


def test_register_fails_when_given_invalid_cookie():
    assert not UserManager.register("username", "password", "boogie boogie").succeeded()


def test_registers_user_when_registered_successfully(cookie):
    username = "username"
    UserManager.cookie_user[cookie].set_username(username)
    UserManager.register(username, "password", cookie)
    assert UserManager.username_user[username] == UserManager.cookie_user[cookie]


def test_does_not_register_when_registration_fails(cookie):
    UserManager.cookie_user[cookie].can_register = False
    UserManager.register("username", "password", cookie)
    assert "username" not in UserManager.username_user


# * login tests - 2.4
# * ==============================================================
def test_login_successfully(cookie):
    UserManager.register("username", "password", cookie)
    assert UserManager.login("username", "password", cookie).succeeded()


def test_login_fails_when_given_invalid_cookie():
    assert not UserManager.login("username", "password", "boogie boogie").succeeded()


def test_login_gets_back_old_data_on_success(cookie, cookie2):
    username = "username"
    UserManager.cookie_user[cookie].set_username(username)
    UserManager.cookie_user[cookie2].set_username(username)
    UserManager.register(username, "password", cookie2)
    UserManager.login(username, "password", cookie2)
    same_user = UserManager.cookie_user[cookie] == UserManager.cookie_user[cookie2]
    assert same_user


def test_login_does_not_get_back_old_data_on_fail(cookie, cookie2):
    UserManager.register("username", "password", cookie)
    UserManager.cookie_user[cookie].can_login = False
    UserManager.login("username", "password", cookie2)
    assert not UserManager.cookie_user[cookie] == UserManager.cookie_user[cookie2]


# * add to cart tests - 2.7
# * ==============================================================
def test_add_to_cart_deligate_to_user_successfully(cookie):
    UserManager.add_to_cart(cookie, "", "", 0)
    assert UserManager.cookie_user[cookie]._add_to_cart


def test_add_to_cart_fails_when_given_invalid_cookie():
    assert not UserManager.add_to_cart("boogie boogie", "", "", 0).succeeded()


# * get cart details tests - 2.8
# * ==============================================================
def test_get_cart_details_deligates_to_user_successfully(cookie):
    UserManager.get_cart_details(cookie)
    assert UserManager.cookie_user[cookie]._get_cart_details


def test_get_cart_details_fails_when_given_invalid_cookie():
    assert not UserManager.get_cart_details("boogie boogie").succeeded()


# * remove product from cart tests - 2.8
# * ==============================================================
def test_remove_product_from_cart_deligates_to_user_successfully(cookie):
    UserManager.remove_product_from_cart(cookie, "", "")
    assert UserManager.cookie_user[cookie]._remove_product_from_cart


def test_remove_product_from_cart_fails_when_given_invalid_cookie():
    assert not UserManager.remove_product_from_cart("boogie boogie", "", "").succeeded()


# * change product quantity in cart tests - 2.8
# * ==============================================================
def test_change_product_quantity_in_cart_deligates_to_user_successfully(cookie):
    UserManager.change_product_quantity_in_cart(cookie, "", "", 0)
    assert UserManager.cookie_user[cookie]._change_product_quantity_in_cart


def test_change_product_quantity_in_cart_fails_when_given_invalid_cookie():
    assert not UserManager.change_product_quantity_in_cart("boogie boogie", "", "", 0).succeeded()


# * purchase cart tests - 2.9
# * ==============================================================
def test_purchase_cart_deligates_to_user_successfully(cookie):
    UserManager.purchase_cart(cookie)
    assert UserManager.cookie_user[cookie]._purchase_cart


def test_purchase_cart_fails_when_given_invalid_cookie():
    assert not UserManager.purchase_cart("boogie boogie").succeeded()


# * purchase completed tests - 2.9
# * ==============================================================
def test_purchase_completed_deligates_to_user_successfully(cookie):
    UserManager.purchase_completed(cookie)
    assert UserManager.cookie_user[cookie]._purchase_completed


def test_purchase_completed_fails_when_given_invalid_cookie():
    assert not UserManager.purchase_completed("boogie boogie").succeeded()


# * get cart price tests - 2.9
# * ==============================================================
def test_get_cart_price_deligates_to_user_successfully(cookie):
    UserManager.get_cart_price(cookie)
    assert UserManager.cookie_user[cookie]._get_cart_price


def test_get_cart_price_fails_when_given_invalid_cookie():
    assert not UserManager.get_cart_price("boogie boogie").succeeded()


# * create store tests - 3.2
# * ==============================================================
def test_create_store_deligates_to_user_successfully(cookie):
    UserManager.create_store(cookie, "")
    assert UserManager.cookie_user[cookie]._create_store


def test_create_store_fails_when_given_invalid_cookie():
    assert not UserManager.create_store("boogie boogie", "").succeeded()


# * get purchase history tests - 3.7
# * ==============================================================
def test_get_purchase_history_deligates_to_user_successfully(cookie):
    UserManager.get_purchase_history(cookie)
    assert UserManager.cookie_user[cookie]._get_purchase_history


def test_get_purchase_history_fails_when_given_invalid_cookie():
    assert not UserManager.get_purchase_history("boogie boogie").succeeded()


# * create product tests - 4.1
# * ==============================================================
def test_create_product_deligates_to_user_successfully(cookie):
    UserManager.create_product(cookie, "", "", 0, 0)
    assert UserManager.cookie_user[cookie]._create_product


def test_create_product_fails_when_given_invalid_cookie():
    assert not UserManager.create_product("boogie boogie", "", "", 0, 0).succeeded()


# * remove products tests - 4.1
# * ==============================================================
def test_remove_product_from_store_deligates_to_user_successfully(cookie):
    UserManager.remove_product_from_store(cookie, "", "")
    assert UserManager.cookie_user[cookie]._remove_product_from_store


def test_remove_product_from_store_fails_when_given_invalid_cookie():
    assert not UserManager.remove_product_from_store("boogie boogie", "", "").succeeded()


# * change product quantity tests - 4.1
# * ==============================================================
def test_change_product_quantity_in_store_deligates_to_user_successfully(cookie):
    UserManager.change_product_quantity_in_store(cookie, "", "", 0)
    assert UserManager.cookie_user[cookie]._change_product_quantity_in_store


def test_change_product_quantity_in_store_fails_when_given_invalid_cookie():
    assert not UserManager.change_product_quantity_in_store("boogie boogie", "", "", 0).succeeded()


# * edit product details tests - 4.1
# * ==============================================================
def test_edit_product_details_deligates_to_user_successfully(cookie):
    UserManager.edit_product_details(cookie, "", "", "", 0)
    assert UserManager.cookie_user[cookie]._edit_product_details


def test_edit_product_details_fails_when_given_invalid_cookie():
    assert not UserManager.edit_product_details("boogie boogie", "", "", "", 0).succeeded()


# * appoint owner tests - 4.3
# * ==============================================================
def test_appoint_owner_deligates_to_user_successfully(cookie, cookie2):
    UserManager.register(
        UserManager.cookie_user[cookie2].get_username().get_obj().get_val(), "", cookie2
    )
    UserManager.appoint_owner(
        cookie, "", UserManager.cookie_user[cookie2].get_username().get_obj().get_val()
    )
    assert UserManager.cookie_user[cookie]._appoint_owner


def test_appoint_owner_fails_when_given_invalid_cookie():
    assert not UserManager.appoint_owner("boogie boogie", "", "").succeeded()


def test_appoint_owner_fails_when_given_username_does_not_exist(cookie):
    result = UserManager.appoint_owner(cookie, "", "")
    assert not UserManager.cookie_user[cookie]._appoint_owner and not result.succeeded()


# * appoint manager tests - 4.5
# * ==============================================================
def test_appoint_manager_deligates_to_user_successfully(cookie, cookie2):
    UserManager.register(
        UserManager.cookie_user[cookie2].get_username().get_obj().get_val(), "", cookie2
    )
    UserManager.appoint_manager(
        cookie, "", UserManager.cookie_user[cookie2].get_username().get_obj().get_val()
    )
    assert UserManager.cookie_user[cookie]._appoint_manager


def test_appoint_manager_fails_when_given_invalid_cookie():
    assert not UserManager.appoint_manager("boogie boogie", "", "").succeeded()


def test_appoint_manager_fails_when_given_username_does_not_exist(cookie):
    result = UserManager.appoint_manager(cookie, "", "")
    assert not UserManager.cookie_user[cookie]._appoint_manager and not result.succeeded()


# * add manager permission tests - 4.6
# * ==============================================================
def test_add_manager_permission_deligates_to_user_successfully(cookie):
    UserManager.add_manager_permission(cookie, "", "", Permission.APPOINT_MANAGER)
    assert UserManager.cookie_user[cookie]._add_manager_permission


def test_add_manager_permission_fails_when_given_invalid_cookie():
    assert not UserManager.add_manager_permission(
        "boogie boogie", "", "", Permission.APPOINT_MANAGER
    ).succeeded()


# * remove manager permission tests - 4.6
# * ==============================================================
def test_remove_manager_permission_deligates_to_user_successfully(cookie):
    UserManager.remove_manager_permission(cookie, "", "", Permission.APPOINT_MANAGER)
    assert UserManager.cookie_user[cookie]._remove_manager_permission


def test_remove_manager_permission_fails_when_given_invalid_cookie():
    assert not UserManager.remove_manager_permission(
        "boogie boogie", "", "", Permission.APPOINT_MANAGER
    ).succeeded()


# * remove appointment tests - 4.4 and 4.7
# * ==============================================================
def test_remove_appointment_deligates_to_user_successfully(cookie):
    UserManager.remove_appointment(cookie, "", "")
    assert UserManager.cookie_user[cookie]._remove_appointment


def test_remove_appointment_fails_when_given_invalid_cookie():
    assert not UserManager.remove_appointment("boogie boogie", "", "").succeeded()


# * get store appointments tests - 4.9
# * ==============================================================
def test_get_store_appointments_deligates_to_user_successfully(cookie):
    UserManager.get_store_appointments(cookie, "")
    assert UserManager.cookie_user[cookie]._get_store_appointments


def test_get_store_appointments_fails_when_given_invalid_cookie():
    assert not UserManager.get_store_appointments("boogie boogie", "").succeeded()


# * get store purchase history tests - 4.11
# * ==============================================================
def test_get_store_purchase_history_deligates_to_user_successfully(cookie):
    UserManager.get_store_purchase_history(cookie, "")
    assert UserManager.cookie_user[cookie]._get_store_purchase_history


def test_get_store_purchases_history_fails_when_given_invalid_cookie():
    assert not UserManager.get_store_purchase_history("boogie boogie", "").succeeded()


# * get any store purchase history tests - 6.4
# * ==============================================================
def test_get_any_store_purchase_history_deligates_to_user_successfully(cookie):
    UserManager.get_any_store_purchase_history_admin(cookie, "")
    assert UserManager.cookie_user[cookie]._get_any_store_purchase_history


def test_get_any_store_purchase_history_fails_when_given_invalid_cookie():
    assert not UserManager.get_any_store_purchase_history_admin("boogie boogie", "").succeeded()


# * get any user purchase history tests - 4.11
# * ==============================================================
def test_get_any_user_purchase_history_deligates_to_user_successfully(cookie):
    UserManager.get_any_user_purchase_history_admin(cookie, "")
    assert UserManager.cookie_user[cookie]._get_any_user_purchase_history


def test_get_any_user_purchase_history_fails_when_given_invalid_cookie():
    assert not UserManager.get_any_user_purchase_history_admin("boogie boogie", "").succeeded()