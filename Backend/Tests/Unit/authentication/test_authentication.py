import pytest
from Backend.Domain.Authentication.authentication import Authentication

auth = Authentication(is_mock=True)


def test_login_all_good():
    auth = Authentication.get_instance()
    response = auth.login(username="Tali", password="puppy")
    assert response.succeeded(), response.get_msg == "login succeeded"


def test_login_username_doesnt_exist():
    auth = Authentication.get_instance()
    response = auth.login(username="shahaf", password="sadna")
    assert not response.succeeded(), response.get_msg == "username doesn't exist in the system"


def test_login_username_exists_password_incorrect():
    auth = Authentication.get_instance()
    response = auth.login(username="Inon", password="gguy")
    assert not response.succeeded(), response.get_msg == "password incorrect"


def test_register_username_already_exists():
    auth = Authentication.get_instance()
    response = auth.login(username="Omer", password="coooool")
    assert not response.succeeded(), response.get_msg == "username already exists"


def test_register_all_good():
    auth = Authentication.get_instance()
    response = auth.register(username="Shahaf", password="sadna")
    assert response.succeeded(), response.get_msg == "registration succeeded"


# for debugging purposes
#
# if __name__ == "__main__":
#     test_login_all_good()