import pytest

from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.user import User


@pytest.fixture
def user():
    return User()


@pytest.fixture
def store():
    return Store("store")


@pytest.fixture
