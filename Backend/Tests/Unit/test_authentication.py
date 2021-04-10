import pytest
import json

from Backend.Domain.Authentication.authentication import Authentication


@pytest.fixture
def auth():
    return Authentication.get_instance()


@pytest.fixture
def config_path():
    return "config.json"


@pytest.fixture
def admin_username(config_path):
    with open(config_path, "r") as read_file:
        data = json.load(read_file)
        return data["admins"][0]


@pytest.fixture
def admin_password(config_path):
    with open(config_path, "r") as read_file:
        data = json.load(read_file)
        return data["admin-password"]


def test_login_all_good(auth):
    auth.register("test_login_all_good", "test_login_all_good")
    response = auth.login("test_login_all_good", "test_login_all_good")
    assert response.succeeded(), response.get_msg()


def test_login_username_does_not_exist(auth):
    response = auth.login(username="shahaf", password="sadna")
    assert not response.succeeded(), response.get_msg()


def test_login_username_exists_password_incorrect(auth):
    auth.register("some_username", "some_password")
    response = auth.login(username="some_username", password="wrong_password")
    assert not response.succeeded(), response.get_msg()


def test_login_as_admin_returns_true(auth: Authentication, admin_username, admin_password):
    response = auth.login(admin_username, admin_password)
    return response.succeeded() and response.get_obj().get_val(), response.get_msg()


def test_login_as_none_admin_returns_false(auth: Authentication):
    auth.register(
        "test_login_as_none_admin_returns_false", "test_login_as_none_admin_returns_false"
    )
    response = auth.login(
        "test_login_as_none_admin_returns_false", "test_login_as_none_admin_returns_false"
    )
    assert response.succeeded() and not response.get_obj().get_val(), response.get_msg()


def test_register_username_already_exists(auth):
    auth.register("some_username", "some_password")
    response = auth.register(username="some_username", password="coooool")
    assert not response.succeeded(), response.get_msg()


def test_register_all_good(auth):
    response = auth.register(username="to_register", password="sadna")
    assert response.succeeded(), response.get_msg()
