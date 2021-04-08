from Backend.Service.trading_system import TradingSystem

trading_system = TradingSystem.getInstance()


def test_enter_system():
    cookie = trading_system.enter_system()
    assert True

# def test_login_all_good():
#     trading_system
#     assert response.succeeded(), response.get_msg == "login succeeded"
