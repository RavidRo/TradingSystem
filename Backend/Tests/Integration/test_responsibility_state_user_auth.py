from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.States.admin import Admin
from Backend.Domain.TradingSystem.user import User
import pytest

from Backend.Domain.TradingSystem.States.guest import Guest


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
    assert not guest.get_username().succeeded()
