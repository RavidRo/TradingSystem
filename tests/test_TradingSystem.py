import pytest
from Backend.Service.TradingSystem import TradingSystem

system = TradingSystem.getInstance()  #TODO: for some reason, the object returned does not have the methods

#2.3
def test_register_success():
    new_username = "doorbellman"
    password = "aaa"
    cookie = TradingSystem.enter_system(system)   #TODO: assuming the returned value is the cookie
    assert TradingSystem.register(system, cookie, new_username, password) #TODO: assuming the return value is a boolean

def test_register_used_username_fail():
    existing_username = "doorbellman"
    password = "aaa"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, existing_username, password)
    assert not TradingSystem.register(system, cookie, existing_username, password)

#2.4
def test_login_success():
    new_username = "doorbellman"
    password = "aaa"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    assert TradingSystem.login(system, cookie, new_username, password)  #TODO: assuming return value is a boolean, might hove to check if the user strategy is different

def test_login_wrong_username_fail():
    new_username = "doorbellman"
    password = "aaa"
    wrong_username = "doorbelman"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    assert not TradingSystem.login(system, cookie, wrong_username, password)

def test_login_wrong_password_fail():
    new_username = "doorbellman"
    password = "aaa"
    wrong_password = "aa"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    assert not TradingSystem.login(system, cookie, new_username, wrong_password)

#3.2
def test_open_store_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    assert TradingSystem.create_store(system, cookie, store_name)   #TODO: assuming return value is a boolean

def test_open_store_unsupported_character_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "stαrbucks"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    assert not TradingSystem.create_store(system, cookie, store_name)

#2.5
def test_get_store_information_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    assert TradingSystem.get_stores_details(system) #TODO: assuming return value is list, might need to figure out how to see if that's the right store

def test_get_store_information_no_stores_fail():
    new_username = "doorbellman"
    password = "aaa"
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    assert not TradingSystem.get_stores_details(system) #an empty list evaluates to false

#4.1
def test_add_new_product_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    assert TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity) #TODO: assuming store_id is the store's name, return value is a boolean

def test_add_new_product_negative_quantity_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = -10
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    assert not TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity) #TODO: assuming store_id is the store's name, return value is a boolean

def test_add_new_product_negative_price_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = -5.50
    quantity = 10
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    assert not TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity) #TODO: assuming store_id is the store's name, return value is a boolean

def test_remove_product_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert TradingSystem.remove_products(system, cookie, store_name, product_name)  #TODO: assuming return value is a boolean

def test_remove_product_wrong_product_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert not TradingSystem.remove_products(system, cookie, store_name, wrong_product)

def test_change_product_quantity_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    new_quantity = 15
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert TradingSystem.change_product_quantity(cookie, store_name, product_name, new_quantity)

def test_change_product_quantity_negative_quantity_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    new_quantity = -15
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert not TradingSystem.change_product_quantity(cookie, store_name, product_name, new_quantity)

def test_change_product_quantity_wrong_product_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    new_quantity = 15
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert not TradingSystem.change_product_quantity(cookie, store_name, wrong_product, new_quantity)

def test_edit_product_details_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    new_name = "cofee"
    new_price = 6.0
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert TradingSystem.edit_product_details(cookie, store_name, product_name, new_name, new_price)

def test_edit_product_details_wrong_product_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    wrong_product = "coffe"
    price = 5.50
    quantity = 10
    new_name = "cofee"
    new_price = 6.0
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert not TradingSystem.edit_product_details(cookie, store_name, wrong_product, new_name, new_price)

def test_edit_product_details_negative_price_fail():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    new_name = "cofee"
    new_price = -6.0
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert not TradingSystem.edit_product_details(cookie, store_name, product_name, new_name, new_price)

#2.6
def test_product_search_with_filter_no_args_success():
    new_username = "doorbellman"
    password = "aaa"
    store_name = "starbucks"
    product_name = "coffee"
    price = 5.50
    quantity = 10
    cookie = TradingSystem.enter_system(system)
    TradingSystem.register(system, cookie, new_username, password)
    TradingSystem.login(system, cookie, new_username, password)
    TradingSystem.create_store(system, cookie, store_name)
    TradingSystem.create_product(system, cookie, store_name, product_name, price, quantity)
    assert system.search_products(product_name)

