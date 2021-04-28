import pytest
from Backend.Domain.TradingSystem.TypesPolicies.discount_policy import DefaultDiscountPolicy

# * fixtures
# * ==========================================================================================

@pytest.fixture
def discount_policy():
    return DefaultDiscountPolicy()


# * Tests
# * ==========================================================================================
