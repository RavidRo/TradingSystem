import threading

from Backend.Service.trading_system import TradingSystem

system = TradingSystem.getInstance()
username_number = 0
user_lock = threading.Lock()
store_number = 0
store_lock = threading.Lock()
product_number = 0
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
    username = str(username_number)
    user_lock.release()
    return username


def _generate_store_name() -> str:
    global store_number
    store_lock.acquire()
    store_number += 1
    store = str(store_number)
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
    product = str(product_number)
    product_lock.release()
    return product

def test_buy_suggestion() -> :
    cookie, username, password, store_name, store_id = _initialize_info(_generate_username(), "a", _generate_store_name())