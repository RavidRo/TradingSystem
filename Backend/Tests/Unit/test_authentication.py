import pytest
import json

from Backend.Domain.Authentication import authentication
from Backend.settings import Settings


@pytest.fixture(autouse=True)
def get_settings():
    return Settings.get_instance(True)


@pytest.fixture
def admin_username(get_settings):
    return get_settings.get_admins()


@pytest.fixture
def admin_password(get_settings):
    return get_settings.get_password()


def test_login_all_good():
    authentication.register("test_login_all_good", "test_login_all_good")
    response = authentication.login("test_login_all_good", "test_login_all_good")
    assert response.succeeded(), response.get_msg()


def test_login_username_does_not_exist():
    response = authentication.login(username="shahaf", password="sadna")
    assert not response.succeeded(), response.get_msg()


def test_login_username_exists_password_incorrect():
    authentication.register("some_username", "some_password")
    response = authentication.login(username="some_username", password="wrong_password")
    assert not response.succeeded(), response.get_msg()


def test_register_username_already_exists():
    authentication.register("some_username", "some_password")
    response = authentication.register(username="some_username", password="coooool")
    assert not response.succeeded(), response.get_msg()


def test_register_all_good():
    response = authentication.register(username="to_register", password="sadna")
    assert response.succeeded(), response.get_msg()
