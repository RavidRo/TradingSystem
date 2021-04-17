# from unittest.mock import patch
#
# import pytest
#
# from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
# from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
# from Backend.Domain.TradingSystem.store import Store
# from Backend.Domain.TradingSystem.user import User
# from Backend.Tests.stubs.product_stub import ProductStub
#
#
# @pytest.fixture
# def user():
#     return User()
#
# @pytest.fixture
# def shopping_bag():
#     return ShoppingBag(Store("store"))
#
#
# @pytest.fixture()
# def products_stubs_store():
#     products_to_quantities = {
#         "1": (ProductStub("product1"), 5),
#         "2": (ProductStub("product2"), 4),
#         "3": (ProductStub("product3"), 4),
#     }
#     return products_to_quantities
#
#
# @pytest.fixture()
# def products_stubs_shopping_bag():
#     products_to_quantities = {
#         "1": (ProductStub("product1"), 2),
#         "2": (ProductStub("product2"), 1),
#         "3": (ProductStub("product3"), 1),
#     }
#     return products_to_quantities
#
#
# @pytest.fixture
# def test_purchase_and_pay_success(user: User):
#
#
#
