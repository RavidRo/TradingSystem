import threading
from Backend.Tests.Acceptance.test_TradingSystem import username_number, store_number, product_number

from Backend.Service.trading_system import TradingSystem

system = TradingSystem.getInstance()
user_lock = threading.Lock()
store_lock = threading.Lock()
product_lock = threading.Lock()


def _initialize_info(
    username: str, password: str, store_name: str = None
) -> tuple[str, str, str, str, str]:
    store_id = ""
    cookie = system.enter_system()
    system.register(cookie, username, password)
    system.login(cookie, username, password)
    if store_name:
        store_res = system.create_store(cookie, store_name)
        store_id = store_res.object
    return cookie, username, password, store_name, store_id


def _create_product(
    cookie: str, store_id: str, product_name: str, category: str, price: float, quantity: int
) -> tuple[str, str, str, float, int]:
    product_res = system.create_product(cookie, store_id, product_name, category, price, quantity)
    product_id = product_res.object
    return product_id, product_name, category, price, quantity


def _generate_username() -> str:
    global username_number
    user_lock.acquire()
    username_number += 1
    username = "test_MileStone3Acceptance" + str(username_number)
    print(username)
    user_lock.release()
    return username


def _generate_store_name() -> str:
    global store_number
    store_lock.acquire()
    store_number += 1
    store = "test_MileStone3Acceptance" + str(store_number)
    store_lock.release()
    return store


def _simple_rule_details_age() -> dict:
    return {"context": {"obj": "user"}, "operator": "great-equals", "target": 18}


def _simple_rule_details_age_edited() -> dict:
    return {"context": {"obj": "user"}, "operator": "great-equals", "target": 21}


def _simple_rule_details_product() -> dict:
    return {"context": {"obj": "product", "identifier": "1"}, "operator": "less-than", "target": 10}


def _simple_rule_details_age_invalid_operator() -> dict:
    return {"context": {"obj": "user"}, "operator": "invalid", "target": 18}


def _simple_rule_details_age_missing_key_target() -> dict:
    return {"context": {"obj": "user"}, "operator": "invalid"}


def _complex_rule_details_or() -> dict:
    return {"operator": "or"}


def _complex_rule_details_and() -> dict:
    return {"operator": "and"}


def _complex_rule_details_conditioning() -> dict:
    return {"operator": "conditional"}


def _complex_rule_details_invalid_operator() -> dict:
    return {"operator": "invalid"}


def _complex_rule_details_missing_operator() -> dict:
    return {}


def _product_discount(product_id="123") -> dict:
    return {
        "discount_type": "simple",
        "percentage": 50.0,
        "context": {"obj": "product", "id": product_id},
    }


def _category_discount() -> dict:
    return {
        "discount_type": "simple",
        "percentage": 25.0,
        "context": {"obj": "category", "id": "A"},
    }


def _store_discount() -> dict:
    return {"discount_type": "simple", "percentage": 10.0, "context": {"obj": "store"}}


def _complex_max_discount() -> dict:
    return {"discount_type": "complex", "type": "max"}


def _complex_add_discount() -> dict:
    return {"discount_type": "complex", "type": "add"}


def _complex_and_discount() -> dict:
    return {"discount_type": "complex", "type": "and"}


def _complex_or_discount() -> dict:
    return {"discount_type": "complex", "type": "or"}


def _complex_xor_discount() -> dict:
    return {"discount_type": "complex", "type": "xor", "decision_rule": "first"}


def _generate_product_name() -> str:
    global product_number
    product_lock.acquire()
    product_number += 1
    product = "test_MileStone3Acceptance" + str(product_number)
    product_lock.release()
    return product

def test_buy_offer_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass", _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(), "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    result = system.create_offer(buyer_cookie, store_id, product_id)
    assert result.succeeded()

def test_buy_offer_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass", _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(), "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    wrong_store = "starbuc"
    result = system.create_offer(buyer_cookie, wrong_store, product_id)
    assert not result.succeeded()

def test_buy_offer_wrong_product_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass", _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(), "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    wrong_product = "cofe"
    result = system.create_offer(buyer_cookie, wrong_product, product_id)
    assert not result.succeeded()

def test_get_users_offers_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass", _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(), "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    result = system.get_user_offers(buyer_cookie)
    assert result.succeeded() and len(result.get_obj().values) == 1 and result.get_obj().values[0].id == offer_id


def test_get_stores_offers_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    result = system.get_store_offers(cookie, store_id)
    assert result.succeeded() and len(result.get_obj().values) == 1 and result.get_obj().values[0].id == offer_id

def test_get_stores_offers_no_permission_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    system.create_offer(buyer_cookie, store_id, product_id)
    result = system.get_store_offers(buyer_cookie, store_id)
    assert not result.succeeded()

def test_get_stores_offers_wrong_store_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    wrong_store = "starbuc"
    system.create_offer(buyer_cookie, wrong_store, product_id)
    result = system.get_store_offers(buyer_cookie, store_id)
    assert not result.succeeded()

def test_declare_price_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    result = system.declare_price(buyer_cookie, offer_id, 1.0)
    offer = system.get_user_offers(buyer_cookie)
    assert result.succeeded() and offer.get_obj().values[0].price == 1.0

def test_declare_price_wrong_offer_id_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    result = system.declare_price(buyer_cookie, "ofer", 1.0)
    assert not result.succeeded()


def test_declare_price_negative_price_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    result = system.declare_price(buyer_cookie, offer_id, -1.0)
    assert not result.succeeded()


def test_declare_price_twice_id_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.declare_price(buyer_cookie, offer_id, 1.0)
    assert not result.succeeded()

def test_suggest_counter_offer_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    offer = system.get_user_offers(buyer_cookie)
    assert result.succeeded() and offer.get_obj().values[0].price == 1.1, result.get_msg()

def test_suggest_counter_offer_wrong_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.suggest_counter_offer(cookie, store_id, product_id, "ofer", 1.1)
    assert not result.succeeded()

def test_suggest_counter_offer_negative_price_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, -1.1)
    assert not result.succeeded()

def test_suggest_counter_offer_without_declaration_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    result = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    assert not result.succeeded()

def test_suggest_counter_offer_twice_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    result = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    assert not result.succeeded()

def test_declare_then_counter_offer_twice_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 10.0, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 9.0)
    result1 = system.declare_price(buyer_cookie, offer_id, 4.0)
    offer1 = system.get_user_offers(buyer_cookie).get_obj().values[0]
    result2 = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 5.0)
    offer2 = system.get_user_offers(buyer_cookie).get_obj().values[0]
    assert result1.succeeded() and result2.succeeded() and offer1.price == 4.0 and offer2.price == 5.0

def test_approve_manager_offer_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    result = system.approve_manager_offer(buyer_cookie, offer_id)
    offer = system.get_user_offers(buyer_cookie).get_obj().values[0]
    assert result.succeeded() and offer.status == "approved"

def test_approve_manager_offer_no_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.approve_manager_offer(buyer_cookie, offer_id)
    assert not result.succeeded()

def test_approve_user_offer_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.approve_user_offer(cookie, store_id, product_id, offer_id)
    offer = system.get_user_offers(buyer_cookie).get_obj().values[0]
    assert result.succeeded() and offer.status == "approved"

def test_approve_user_offer_no_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    result = system.approve_user_offer(cookie, store_id, product_id, offer_id)
    assert not result.succeeded()

def test_reject_user_offer_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.reject_user_offer(cookie, store_id, product_id, offer_id)
    offer = system.get_user_offers(buyer_cookie).get_obj().values[0]
    assert result.succeeded() and offer.status == "rejected"

def test_reject_user_offer_no_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    result = system.reject_user_offer(cookie, store_id, product_id, offer_id)
    assert not result.succeeded()


def test_reject_user_offer_declare_price_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.reject_user_offer(cookie, store_id, product_id, offer_id)
    result = system.declare_price(buyer_cookie, offer_id, 1.0)
    assert not result.succeeded()


def test_reject_user_offer_counter_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.reject_user_offer(cookie, store_id, product_id, offer_id)
    result = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    assert not result.succeeded()


def test_reject_user_offer_approve_user_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.reject_user_offer(cookie, store_id, product_id, offer_id)
    result = system.approve_user_offer(cookie, store_id, product_id, offer_id)
    assert not result.succeeded()


def test_reject_user_offer_approve_manager_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.reject_user_offer(cookie, store_id, product_id, offer_id)
    result = system.approve_manager_offer(buyer_cookie, offer_id)
    assert not result.succeeded()


def test_reject_user_offer_reject_user_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.reject_user_offer(cookie, store_id, product_id, offer_id)
    result = system.reject_user_offer(cookie, store_id, product_id, offer_id)
    assert not result.succeeded()


def test_reject_user_offer_cancel_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.reject_user_offer(cookie, store_id, product_id, offer_id)
    result = system.cancel_offer(buyer_cookie, offer_id)
    assert not result.succeeded()

def test_cancel_offer_success():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    result = system.cancel_offer(buyer_cookie, offer_id)
    offer = system.get_user_offers(buyer_cookie).get_obj().values[0]
    assert result.succeeded() and offer.status == "cancled"

def test_cancel_offer_declare_price_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.cancel_offer(buyer_cookie, offer_id)
    result = system.declare_price(buyer_cookie, offer_id, 1.0)
    assert not result.succeeded()

def test_cancel_offer_counter_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.cancel_offer(buyer_cookie, offer_id)
    result = system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    assert not result.succeeded()

def test_cancel_offer_approve_user_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.cancel_offer(buyer_cookie, offer_id)
    result = system.approve_user_offer(cookie, store_id, product_id, offer_id)
    assert not result.succeeded()

def test_cancel_offer_approve_manager_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.suggest_counter_offer(cookie, store_id, product_id, offer_id, 1.1)
    system.cancel_offer(buyer_cookie, offer_id)
    result = system.approve_manager_offer(buyer_cookie, offer_id)
    assert not result.succeeded()


def test_cancel_offer_reject_user_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.declare_price(buyer_cookie, offer_id, 1.0)
    system.cancel_offer(buyer_cookie, offer_id)
    result = system.reject_user_offer(cookie, store_id, product_id, offer_id)
    assert not result.succeeded()

def test_cancel_offer_cancel_offer_fail():
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "pass",
                                                                        _generate_store_name())
    product_id, product_name, category, price, quantity = _create_product(cookie, store_id, _generate_product_name(),
                                                                          "cat", 1.2, 10)

    buyer_cookie, buyer_username, buyer_password, _, _ = _initialize_info(_generate_username(), "pass")
    offer_id = system.create_offer(buyer_cookie, store_id, product_id).get_obj()
    system.cancel_offer(buyer_cookie, offer_id)
    result = system.cancel_offer(buyer_cookie, offer_id)
    assert not result.succeeded()
