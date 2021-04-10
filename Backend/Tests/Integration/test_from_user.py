import pytest

from Backend.Domain.TradingSystem.user import User


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
def user_admin():
    # ? @TODO create admin somehow
    user = User()
    user.register("some_username", "password")
    user.login("some_username", "password")
    return user


# * get username
# * =================================================================
def test_guest_does_not_have_a_username(user_guest: User):
    assert not user_guest.get_username().succeeded()
