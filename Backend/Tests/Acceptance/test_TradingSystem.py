import asyncio
import json
import threading

import pytest

from Backend.Service.trading_system import TradingSystem

__system = TradingSystem.getInstance()
__username_number = 0
__user_lock = threading.Lock()
__store_number = 0
__store_lock = threading.Lock()
__product_number = 0
__product_lock = threading.Lock()


# @pytest.fixture
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


async def __initialize_info(
    username: str, password: str, store_name: str = None
) -> tuple[str, str, str, str, str]:
    store_id = ""
    cookie = await __system.enter_system()
    await __system.register(cookie, username, password)
    await __system.login(cookie, username, password)
    if store_name:
        store_res = await __system.create_store(cookie, store_name)
        store_id = store_res.object
    return cookie, username, password, store_name, store_id


async def __create_product(cookie: str, store_id: str, product_name: str, price: float, quantity: int) -> tuple[str, str, float, int]:
    product_res = await __system.create_product(cookie, store_id, product_name, price, quantity)
    product_id = product_res.object
    return product_id, product_name, price, quantity


def __generate_username() -> str:
    global __username_number
    __user_lock.acquire()
    __username_number += 1
    username = str(__username_number)
    __user_lock.release()
    return username


def __generate_store_name() -> str:
    global __store_number
    __store_lock.acquire()
    __store_number += 1
    store = str(__store_number)
    __store_lock.release()
    return store


def __generate_product_name() -> str:
    global __product_number
    __product_lock.acquire()
    __product_number += 1
    product = str(__product_number)
    __product_lock.release()
    return product


# 2.3 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#23-Registration
@pytest.mark.asyncio
async def test_register_success():
    new_username = __generate_username()
    password = "aaa"
    cookie = await __system.enter_system()
    res = await __system.register(cookie, new_username, password)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_register_used_username_fail():
    existing_username = __generate_username()
    password = "aaa"
    cookie = await __system.enter_system()
    await __system.register(cookie, existing_username, password)
    res = await __system.register(cookie, existing_username, password)
    assert not res.succeeded()


# 2.4 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#24-Login
@pytest.mark.asyncio
async def test_login_success():
    new_username = __generate_username()
    password = "aaa"
    cookie = await __system.enter_system()
    await __system.register(cookie, new_username, password)
    res = await __system.login(cookie, new_username, password)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_login_wrong_username_fail():
    new_username = __generate_username()
    password = "aaa"
    wrong_username = "doorbelman"
    cookie = await __system.enter_system()
    await __system.register(cookie, new_username, password)
    res = await __system.login(cookie, wrong_username, password)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_login_wrong_password_fail():
    new_username = __generate_username()
    password = "aaa"
    wrong_password = "aa"
    cookie = await __system.enter_system()
    await __system.register(cookie, new_username, password)
    res = await __system.login(cookie, new_username, wrong_password)
    assert not res.succeeded()


# 3.2 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#32-#Open-a-store
@pytest.mark.asyncio
async def test_open_store_success():
    cookie, username, password, _, _ = await __initialize_info(__generate_username(), "aaa")
    store_name = __generate_store_name()
    res = await __system.create_store(cookie, store_name)
    assert res.succeeded()


# def test_open_store_unsupported_character_fail():
#     cookie, username, password, _ = __initialize_info(__generate_username(), "aaa")
#     store_name = "stαrbucks"
#     assert not ____system.create_store(cookie, store_name).succeeded()
# not a fail condition


# 2.5 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#25-Getting-store-information
@pytest.mark.asyncio
async def test_get_store_information_success():
    store_details = await __system.get_stores_details()
    num_of_stores = len(store_details.object.values)
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    response = await __system.get_stores_details()
    assert (
        response.succeeded()
        and len(response.object.values) == num_of_stores+1
    )


# def test_get_store_information_no_stores_fail():
#     cookie, username, password, _ = __initialize_info(__generate_username(), "aaa")
#     assert not ____system.get_stores_details().succeeded()  # an empty list evaluates to false
# assumed empty list means failure


# 4.1 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#41-Add-new-product
@pytest.mark.asyncio
async def test_add_new_product_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_name = __generate_product_name()
    price = 5.50
    quantity = 10
    response = await __system.create_product(cookie, store_id, product_name, price, quantity)
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_add_new_product_negative_quantity_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_name = __generate_product_name()
    price = 5.50
    quantity = -10
    res = await __system.create_product(cookie, store_id, product_name, price, quantity)
    assert not res.succeeded()


# def test_add_new_product_negative_price_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_name = __generate_product_name()
    price = -5.50
    quantity = 10
    res = await __system.create_product(cookie, store_id, product_name, price, quantity)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_remove_product_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.remove_product_from_store(cookie, store_id, product_id)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_remove_product_wrong_product_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    wrong_product = "cofee"
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.remove_product_from_store(cookie, store_id, wrong_product)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_change_product_quantity_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_quantity = 15
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    response = await __system.change_product_quantity_in_store(
        cookie, store_id, product_id, new_quantity
    )
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_change_product_quantity_negative_quantity_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_quantity = -15
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.change_product_quantity_in_store(
        cookie, store_id, product_id, new_quantity
    )
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_change_product_quantity_wrong_product_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    wrong_product = "cofee"
    new_quantity = 15
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.change_product_quantity_in_store(
        cookie, store_id, wrong_product, new_quantity
    )
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_edit_product_details_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_name = __generate_product_name()
    new_price = 6.0
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.edit_product_details(
        cookie, store_id, product_id, new_name, new_price
    )
    assert res.succeeded()

@pytest.mark.asyncio
async def test_edit_product_details_wrong_product_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    wrong_product = "coffe"
    new_name = __generate_product_name()
    new_price = 6.0
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.edit_product_details(
        cookie, store_id, wrong_product, new_name, new_price
    )
    assert not res.succeeded()

@pytest.mark.asyncio
async def test_edit_product_details_negative_price_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    new_name = __generate_product_name()
    new_price = -6.0
    res = await __system.edit_product_details(
        cookie, store_id, product_id, new_name, new_price
    )
    assert not res.succeeded()


# 2.6 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#26-Filter-search-results
@pytest.mark.asyncio
async def test_product_search_no_args_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    response = await __system.search_products(product_name=product_name)
    assert (
        response.succeeded()
        and len(list(filter(lambda product: product.name == product_name, response.object.values))) == 1
    ), response.get_msg()


@pytest.mark.asyncio
async def test_product_search_args_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    min_price = 5.0
    max_price = 6.0
    response = await __system.search_products(product_name, min_price=min_price, max_price=max_price)
    assert (
        response.succeeded()
        and len(list(filter(lambda product: product.name == product_name, response.object.values))) == 1
    )


# def test_product_search_wrong_product_no_args_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     product_name = __generate_product_name()
#     wrong_product = "cofee"
#     price = 5.50
#     quantity = 10
#     ____system.create_product(cookie, store_name, product_name, price, quantity)
#     response = ____system.search_products(wrong_product)
#     assert not response.succeeded()
# assumed empty list means failure


# def test_product_search_wrong_product_args_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     product_name = __generate_product_name()
#     wrong_product = "cofee"
#     price = 5.50
#     quantity = 10
#     min_price = 5.0
#     max_price = 6.0
#     ____system.create_product(cookie, store_name, product_name, price, quantity)
#     response = ____system.search_products(wrong_product, min_price=min_price, max_price=max_price)
#     assert not response.succeeded()
# assumed empty list means failure


# def test_product_search_wrong_args_min_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     product_name = __generate_product_name()
#     price = 5.50
#     quantity = 10
#     min_price = 6.0
#     max_price = 7.0
#     ____system.create_product(cookie, store_name, product_name, price, quantity)
#     response = ____system.search_products(product_name, min_price=min_price, max_price=max_price)
#     assert not response.succeeded()
# assumed empty list means failure


# def test_product_search_wrong_args_max_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     product_name = __generate_product_name()
#     price = 5.50
#     quantity = 10
#     min_price = 4.0
#     max_price = 5.0
#     ____system.create_product(cookie, store_name, product_name, price, quantity)
#     response = ____system.search_products(product_name, min_price=min_price, max_price=max_price)
#     assert not response.succeeded()
# assumed empty list means failure


@pytest.mark.asyncio
async def test_products_by_store_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    response = await __system.get_products_by_store(store_id)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


@pytest.mark.asyncio
async def test_products_by_store_wrong_store_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_store = "starbux"
    response = await __system.get_products_by_store(wrong_store)
    assert not response.succeeded()


# # 2.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#27-Save-products-in-shopping-bag
@pytest.mark.asyncio
async def test_add_to_cart_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_add_to_cart_wrong_product_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_product = "cofee"
    res = await __system.save_product_in_cart(cookie, store_id, wrong_product, 1)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_add_to_cart_wrong_store_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_store = "starbux"
    res = await __system.save_product_in_cart(cookie, wrong_store, product_id, 1)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_add_to_cart_quantity_too_high_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    res = await __system.save_product_in_cart(cookie, store_id, product_id, 11)
    assert not res.succeeded()


# # 2.8 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#28-Visit-cart
@pytest.mark.asyncio
async def test_visit_cart_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = await __system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and len(response.object.bags) == 1
        and response.object.bags[0].store_name == store_name
        and len(response.object.bags[0].product_ids_to_quantities) == 1
        and response.object.bags[0].product_ids_to_quantities[product_id] == 1
    ), response.get_msg()


# def test_visit_cart_no_items_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     assert not ____system.get_cart_details(cookie).succeeded()
#   assumed empty list means failure

@pytest.mark.asyncio
async def test_change_amount_in_cart_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = await __system.change_product_quantity_in_cart(cookie, store_id, product_id, 2)
    cart_details_res = await __system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and cart_details_res.object.bags[0].product_ids_to_quantities[product_id] == 2
    ), response.get_msg()


@pytest.mark.asyncio
async def test_change_amount_in_cart_wrong_product_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_product = "cofee"
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.change_product_quantity_in_cart(
        cookie, store_id, wrong_product, 2
    )
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_change_amount_in_cart_wrong_store_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_store = "starbux"
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.change_product_quantity_in_cart(
        cookie, wrong_store, product_id, 2
    )
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_change_amount_in_cart_negative_quantity_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.change_product_quantity_in_cart(
        cookie, store_id, product_id, -1
    )
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_change_amount_in_cart_quantity_too_high_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.change_product_quantity_in_cart(
        cookie, store_id, product_id, 11
    )
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_remove_product_from_cart_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.remove_product_from_cart(cookie, store_id, product_id)
    assert (
        res.succeeded()
    )


@pytest.mark.asyncio
async def test_remove_product_from_cart_wrong_product_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_product = "cofee"
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.remove_product_from_cart(cookie, store_id, wrong_product)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_remove_product_from_cart_wrong_store_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    wrong_store = "starbux"
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res = await __system.remove_product_from_cart(cookie, wrong_store, product_id)
    assert not res.succeeded()


# 2.9 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#29-Purchase-products
@pytest.mark.asyncio
async def test_purchase_cart_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = await __system.purchase_cart(cookie)
    store_res = await __system.get_store(store_id)
    cart_res = await __system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and store_res.object.ids_to_quantities[product_id] == 9
        and cart_res.succeeded()
        and response.object.value == price
    ), response.get_msg()


@pytest.mark.asyncio
async def test_purchase_cart_no_items_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    res = await __system.purchase_cart(cookie)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_purchase_cart_twice_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    response = await __system.purchase_cart(cookie)
    assert not response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_send_payment_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    response = await __system.send_payment(cookie, {}, {})
    res = await __system.get_store(store_id)
    ids_to_quantity = res.object.ids_to_quantities[product_id]
    assert (
        response.succeeded()
        and  ids_to_quantity == 9
    ), response.get_msg()


@pytest.mark.asyncio
async def test_send_payment_before_purchase_cart_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    res1 = await __system.send_payment(cookie, {}, {})
    res2 = await __system.get_store(store_id)
    res2 = res2.object.ids_to_quantities[product_id]
    res3 = await __system.get_cart_details(cookie)
    assert (
        not res1.succeeded()
        and  res2== 10
        and res3.succeeded()
    )


# 3.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#37-Get-personal-purchase-history
@pytest.mark.asyncio
async def test_get_purchase_history_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    await __system.send_payment(cookie, {}, {})
    response = await __system.get_purchase_history(cookie)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].product_names[0] == product_name
    )

# def test_get_purchase_history_no_purchases_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     product_name = __generate_product_name()
#     price = 5.50
#     quantity = 10
#     ____system.create_product(cookie, store_name, product_name, price, quantity)
#     response = ____system.get_purchase_history(cookie)
#     assert not response.succeeded()
# assumed empty list means failure


@pytest.mark.asyncio
async def test_get_purchase_history_no_purchases_saved_to_cart_success():
    cookie, username, password, store_name, store_id = await __initialize_info (
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = await __system.get_purchase_history(cookie)
    assert len(response.object.values) == 0


@pytest.mark.asyncio
async def test_get_purchase_history_no_payment_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    response = await __system.get_purchase_history(cookie)
    assert len(response.object.values) == 0


# 4.3 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#43-Appoint-new-store-owner
@pytest.mark.asyncio
async def test_appoint_store_owner_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    response = await __system.appoint_owner(cookie, store_id, new_owner_username)
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_appoint_store_owner_chain_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    res = await __system.appoint_owner(new_owner_cookie, store_id, last_owner_username)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_owner_wrong_name_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ =await __initialize_info(
        __generate_username(), "bbb"
    )
    wrong_name = "Ravit Ron"
    res = await __system.appoint_owner(cookie, store_id, wrong_name)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_owner_wrong_store_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    wrong_store = "starbux"
    res = await __system.appoint_owner(cookie, wrong_store, new_owner_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_owner_direct_circular_appointment_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    res = await __system.appoint_owner(new_owner_cookie, store_id, username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_owner_circular_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    await __system.appoint_owner(new_owner_cookie, store_id, last_owner_username)
    res = await __system.appoint_owner(last_owner_cookie, store_id, username)
    assert not res.succeeded()


# 4.5 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#45-Appoint-new-store-manager
@pytest.mark.asyncio
async def test_appoint_store_manager_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    res = await __system.appoint_manager(cookie, store_id, new_manager_username)
    assert res.succeeded()


# def test_appoint_store_manager_manager_chain_success():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     new_manager_cookie, new_manager_username, new_manager_password, _, _ = __initialize_info(
#         __generate_username(), "bbb"
#     )
#     last_manager_cookie, last_manager_username, last_manager_password, _, _ = __initialize_info(
#         __generate_username(), "ccc"
#     )
#     ____system.appoint_manager(cookie, store_name, new_manager_username)
#     assert ____system.appoint_manager(new_manager_cookie, store_name, last_manager_username).succeeded()
# tested elsewhere


@pytest.mark.asyncio
async def test_appoint_store_owner_manager_chain_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    res = await __system.appoint_manager(new_owner_cookie, store_id, last_manager_username)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_manager_wrong_name_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    wrong_name = "Ravit Ron"
    res = await __system.appoint_manager(cookie, store_id, wrong_name)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_manager_wrong_store_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    wrong_store = "starbux"
    res = await __system.appoint_manager(cookie, wrong_store, new_manager_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_appoint_store_manager_direct_circular_appointment_fail():
    cookie, username, password, store_name, store_id = await __initialize_info (
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    res = await __system.appoint_manager(new_manager_cookie, store_id, username)
    assert not res.succeeded()


# def test_appoint_store_manager_circular_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     new_manager_cookie, new_manager_username, new_manager_password, _, _ = __initialize_info(
#         __generate_username(), "bbb"
#     )
#     last_manager_cookie, last_manager_username, last_manager_password, _, _ = __initialize_info(
#         __generate_username(), "ccc"
#     )
#     ____system.appoint_manager(cookie, store_id, new_manager_username)
#     ____system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
#     assert not ____system.appoint_manager(last_manager_cookie, store_name, username).succeeded()
# tested elsewhere


@pytest.mark.asyncio
async def test_appoint_store_manager_owner_chain_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    res = await __system.appoint_owner(new_manager_cookie, store_id, last_owner_username)
    assert not res.succeeded()


# 4.6 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#46-Edit-manager%E2%80%99s-responsibilities
@pytest.mark.asyncio
async def test_add_responsibility_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    new_responsibility = "remove_manager"
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    response = await __system.add_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility)
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_remove_responsibility_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    new_responsibility = "remove_manager"
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    __system.add_manager_permission(cookie, store_id, new_manager_username, new_responsibility)
    res = await __system.remove_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility
    )
    assert res.succeeded()


@pytest.mark.asyncio
async def test_default_permissions_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    default_permission = "get_appointments"
    other_permissions = ["remove_manager", "manage_products", "appoint_manager", "get_history"]
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    res = await __system.remove_manager_permission(
        cookie, store_id, new_manager_username, default_permission
    )
    assert res.succeeded()
    for responsibility in other_permissions:
        res_2 = await __system.add_manager_permission(
            cookie, store_id, new_manager_username, responsibility
        )
        assert res_2.succeeded()


@pytest.mark.asyncio
async def test_add_responsibility_twice_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    new_responsibility = "remove_manager"
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, new_responsibility)
    res = await __system.add_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility
    )
    assert res.succeeded()


@pytest.mark.asyncio
async def test_remove_responsibility_twice_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    new_responsibility = "remove_manager"
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    res = await __system.remove_manager_permission(
        cookie, store_id, new_manager_username, new_responsibility)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_get_appointment_permission_success():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info (
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    response = await __system.get_store_appointments(new_manager_cookie, store_id)
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_get_history_permission_success():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, "get_history")
    res = await __system.get_store_purchase_history(new_manager_cookie, store_id)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_appoint_manager_permission_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, "appoint_manager")
    res = await __system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
    assert res.succeeded()


@pytest.mark.asyncio
async def test_remove_manager_permission_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.appoint_manager(cookie, store_id, last_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, "remove_manager")
    res = await __system.remove_appointment(new_manager_cookie, store_id, last_manager_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_remove_manager_permission_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, "appoint_manager")
    await __system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, "remove_manager")
    response = await __system.remove_appointment(new_manager_cookie, store_id, last_manager_username)
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_manage_products_permission_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.add_manager_permission(cookie, store_id, new_manager_username, "manage_products")
    product_name = __generate_product_name()
    price = 5.50
    quantity = 10
    response = await __system.create_product(new_manager_cookie, store_id, product_name, price, quantity)
    assert response.succeeded(), response.get_msg()


@pytest.mark.asyncio
async def test_get_appointment_no_permission_fail():
    cookie, username, password, store_name, store_id = await __initialize_info (
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.remove_manager_permission(cookie, store_id, new_manager_username, "get_appointments")
    res = await __system.get_store_appointments(new_manager_cookie, store_id)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_get_history_no_permission_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    res = await __system.get_store_purchase_history(new_manager_cookie, store_id)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_appoint_manager_no_permission_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = await __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    res = await __system.appoint_manager(new_manager_cookie, store_id, last_manager_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_remove_manager_no_permission_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    await __system.appoint_manager(cookie, store_id, last_manager_username)
    res = await __system.remove_appointment(new_manager_cookie, store_id, last_manager_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_manage_products_no_permission_fail():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    product_name = __generate_product_name()
    price = 5.50
    quantity = 10
    res = await __system.create_product(new_manager_cookie, store_id, product_name, price, quantity)
    assert not res.succeeded()


# 4.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#43-Dismiss-an-owner
@pytest.mark.asyncio
async def test_dismiss_owner_success():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "ccc"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    response = await __system.remove_appointment(cookie, store_id, new_owner_username)
    assert response.succeeded()


@pytest.mark.asyncio
async def test_dismiss_owner_wrong_name_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ = await __initialize_info(
        __generate_username(), "bbb"
    )
    wrong_name = "Ravit Ron"
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    res = await __system.remove_appointment(cookie, store_id, wrong_name)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_dismiss_owner_wrong_store_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    wrong_store = "starbux"
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    res = await __system.remove_appointment(cookie, wrong_store, new_owner_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_dismiss_owner_appointing_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    last_manager_cookie, last_manager_username, last_manager_password, _, _ = await __initialize_info (
        __generate_username(), "ccc"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    await __system.remove_appointment(cookie, store_id, new_owner_username)
    res = await __system.appoint_manager(new_owner_cookie, store_id, last_manager_username)
    assert not res.succeeded()


@pytest.mark.asyncio
async def test_dismiss_owner_chain_appointing_fail():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    last_owner_cookie, last_owner_username, last_owner_password, _, _ =await  __initialize_info(
        __generate_username(), "ccc"
    )
    final_manager_cookie, final_manager_username, final_manager_password, _, _ = await __initialize_info(
        __generate_username(), "ddd"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    await __system.appoint_owner(new_owner_cookie, store_id, last_owner_username)
    await __system.remove_appointment(cookie, store_id, new_owner_username)
    res = await __system.appoint_manager(last_owner_cookie, store_id, final_manager_username)
    assert not res.succeeded()


# 4.9 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#49-Get-store-personnel-information
@pytest.mark.asyncio
async def test_get_store_personnel_success():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    response = await __system.get_store_appointments(cookie, store_id)
    assert (
        response.succeeded()
        and response.object.username == username
        and response.object.role == "Founder"
    )


@pytest.mark.asyncio
async def test_get_store_personnel_owner_success():
    cookie, username, password, store_name, store_id = await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_owner_cookie, new_owner_username, new_owner_password, _, _ =await __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_owner(cookie, store_id, new_owner_username)
    response = await __system.get_store_appointments(cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.appointees) == 1
        and response.object.appointees[0].username == new_owner_username
        and response.object.appointees[0].role == "Owner"
    )


@pytest.mark.asyncio
async def test_get_store_personnel_manager_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    new_manager_cookie, new_manager_username, new_manager_password, _, _ =await  __initialize_info(
        __generate_username(), "bbb"
    )
    await __system.appoint_manager(cookie, store_id, new_manager_username)
    response = await __system.get_store_appointments(cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.appointees) == 1
        and response.object.appointees[0].username == new_manager_username
        and response.object.appointees[0].role == "Manager"
    )


@pytest.mark.asyncio
async def test_get_store_personnel_wrong_store_name_fail():
    cookie, username, password, store_name, store_id = await __initialize_info (
        __generate_username(), "aaa", __generate_store_name()
    )
    wrong_store = "starbux"
    res = await __system.get_store_appointments(cookie, wrong_store)
    assert not res.succeeded()


# 4.11 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#411-Get-store-purchase-history
@pytest.mark.asyncio
async def test_get_store_purchase_history_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    await __system.send_payment(cookie, {}, {})
    response = await __system.get_store_purchase_history(cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].product_names[0] == product_name
    )


# def test_get_store_purchase_history_no_purchases_fail():
#     cookie, username, password, store_name, store_id = __initialize_info(
#         __generate_username(), "aaa", __generate_store_name()
#     )
#     product_name = __generate_product_name()
#     price = 5.50
#     quantity = 10
#     ____system.create_product(cookie, store_name, product_name, price, quantity)
#     response = ____system.get_store_purchase_history(cookie, store_name)
#     assert response.succeeded()
# assumed empty list means failure


@pytest.mark.asyncio
async def test_get_store_purchase_history_no_purchases_saved_to_cart_success():
    cookie, username, password, store_name, store_id =await  __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    response = await __system.get_store_purchase_history(cookie, store_id)
    assert len(response.object.values) == 0


@pytest.mark.asyncio
async def test_get_store_purchase_history_no_payment_success():
    cookie, username, password, store_name, store_id = await __initialize_info(
        __generate_username(), "aaa", __generate_store_name()
    )
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    response = await __system.get_store_purchase_history(cookie, store_id)
    assert len(response.object.values) == 0


# # 6.4 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#64-Get-store-purchase-history-system-manager


async def _get_admin() -> str:
    admin_cookie = await __system.enter_system()
    with open("config.json",  "r") as read_file:
        data = json.load(read_file)
        await __system.login(admin_cookie, data["admins"][0], data["admin-password"])
    return admin_cookie


@pytest.mark.asyncio
async def test_admin_get_store_purchase_history_success():
    cookie, username, password, store_name, store_id = await __initialize_info(__generate_username(), "aaa", __generate_store_name())
    admin_cookie = await _get_admin()
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_id, product_name, price, quantity =await  __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    await __system.send_payment(cookie, {}, {})
    response = await __system.get_any_store_purchase_history(admin_cookie, store_id)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].product_names[0] == product_name
    ), response.get_msg()


@pytest.mark.asyncio
async def test_admin_get_user_purchase_history_success():
    cookie, username, password, store_name, store_id = await __initialize_info(__generate_username(), "aaa", __generate_store_name())
    admin_cookie = await _get_admin()
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_id, product_name, price, quantity = await __create_product(cookie, store_id, __generate_product_name(), 5.50, 10)
    await __system.save_product_in_cart(cookie, store_id, product_id, 1)
    await __system.purchase_cart(cookie)
    await __system.send_payment(cookie, {}, {})
    response = await __system.get_user_purchase_history(admin_cookie, username)
    assert response.succeeded()


# parallel testing
__t1_response = __system.get_stores_details()   # getting a successful response
__t2_response = __system.get_stores_details()


def __get_product(cookie: str, thread: int) -> None:
    if thread == 1:
        __t1_response = __system.purchase_cart(cookie)
    else:
        __t2_response = __system.purchase_cart(cookie)


def test_buy_last_product_together_fail():
    for i in range(100):
        cookie, username, password, store_name, store_id = __initialize_info(__generate_username(), "aaa", __generate_store_name())
        new_cookie, new_username, new_password_, _, _ = __initialize_info(__generate_username(), "aaa")
        product_id, product_name, price, quantity = __create_product(cookie, store_id, __generate_product_name(), 5.50, 1)
        __system.save_product_in_cart(cookie, store_id, product_id, quantity=1)
        __system.save_product_in_cart(new_cookie, store_id, product_id, quantity=1)
        t1 = threading.Thread(target=lambda: __get_product(cookie, 1))
        t2 = threading.Thread(target=lambda: __get_product(new_cookie, 2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert not (__t1_response.succeeded() and __t2_response.succeeded())


def __remove_product(cookie: str, store_id: str, product_id: str) -> None:
    __t1_response = __system.remove_product_from_store(cookie, store_id, product_id)


def test_buy_delete_product():
    for i in range(100):
        cookie, username, password, store_name, store_id = __initialize_info(__generate_username(), "aaa", __generate_store_name())
        new_cookie, new_username, new_password_, _, _ = __initialize_info(__generate_username(), "aaa")
        product_id, product_name, price, quantity = __create_product(cookie, store_id, __generate_product_name(), 5.50, 1)
        t1 = threading.Thread(target=lambda: __remove_product(cookie, store_id, product_id))
        t2 = threading.Thread(target=lambda: __get_product(new_cookie, 2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


def __appoint_manager(cookie, store_id, username, thread: int):
    if thread == 1:
        __t1_response = __system.appoint_manager(cookie, store_id, username)
    else:
        __t2_response = __system.appoint_manager(cookie, store_id, username)


def test_two_appointments():
    for i in range(100):
        cookie, username, password, store_name, store_id = __initialize_info(__generate_username(), "aaa", __generate_store_name())
        owner_cookie, owner_username, owner_password, _, _ = __initialize_info(__generate_username(), "aaa")
        __system.appoint_owner(cookie, store_id, owner_username)
        manager_cookie, manager_username, manager_password, _, _ = __initialize_info(__generate_username(), "aaa")
        t1 = threading.Thread(target=lambda: __appoint_manager(cookie, store_id, manager_username, 1))
        t2 = threading.Thread(target=lambda: __appoint_manager(owner_cookie, store_id, manager_username, 2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
