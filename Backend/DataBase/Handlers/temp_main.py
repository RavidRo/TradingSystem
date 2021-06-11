from Backend.DataBase.Handlers.member_handler import MemberHandler
from Backend.DataBase.Handlers.offer_handler import OfferHandler
from Backend.DataBase.Handlers.product_handler import ProductHandler
from Backend.DataBase.Handlers.purchase_details_handler import PurchaseDetailsHandler
from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
from Backend.DataBase.Handlers.shopping_bag_handler import ShoppingBagHandler
from Backend.DataBase.Handlers.store_handler import StoreHandler
from Backend.DataBase.database import mapper_registry, engine, Base
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.user import User
from Backend.Service.trading_system import TradingSystem

def save():
    mapper_registry.metadata.drop_all(engine)
    mapper_registry.metadata.create_all(engine)
    trading_system = TradingSystem.getInstance()
    cookie = trading_system.enter_system()
    res = trading_system.register(cookie, "user", "password")
    if not res.succeeded():
        print("register: " + res.get_msg())
    res = trading_system.login(cookie, "user", "password")
    cookie2 = trading_system.enter_system()
    res2 = trading_system.register(cookie2, "user2", "password2")
    if not res2.succeeded():
        print("register2: " + res2.get_msg())

    cookie3 = trading_system.enter_system()
    res3 = trading_system.register(cookie3, "user3", "password3")
    if not res3.succeeded():
        print("register3: " + res3.get_msg())

    res2 = trading_system.login(cookie2, "user2", "password2")
    res3 = trading_system.login(cookie3, "user3", "password3")


    store_res = trading_system.create_store(cookie, "The Store")
    if not store_res.succeeded():
        print("open_store: " + store_res.get_msg())

    store_res2 = trading_system.create_store(cookie2, "The Store of cookie2")
    if not store_res2.succeeded():
        print("open_store: " + store_res2.get_msg())

    product_res = trading_system.create_product(cookie, store_res.get_obj(), "The Product", "The Category", 5, 8, ["The Keyword A", "The Keyword B"])
    if not product_res.succeeded():
        print("add_product: " + product_res.get_msg())

    product2_res = trading_system.create_product(cookie, store_res.get_obj(), "The Product2", "The Category2", 10, 16,
                                                ["The Keyword A2", "The Keyword B2"])
    if not product2_res.succeeded():
        print("add_product: " + product2_res.get_msg())

    res_save_prod = trading_system.save_product_in_cart(cookie2, store_res.get_obj(), product_res.get_obj(), 2)
    if not res_save_prod.succeeded():
        print("save in cart: " + res_save_prod.get_msg())

    res_save_prod2 = trading_system.save_product_in_cart(cookie2, store_res.get_obj(), product2_res.get_obj(), 5)
    if not res_save_prod2.succeeded():
        print("save in cart: " + res_save_prod.get_msg())

    res_create_offer = trading_system.create_offer(cookie2, store_res.get_obj(), product2_res.get_obj())
    if not res_create_offer.succeeded():
        print("create offer: " + res_create_offer.get_msg())

    res_declare_price = trading_system.declare_price(cookie2, res_create_offer.get_obj(), 1.0)
    if not res_declare_price.succeeded():
        print("create offer: " + res_declare_price.get_msg())

    res_appoint_owner = trading_system.appoint_owner(cookie, store_res.get_obj(), "user2")
    if not res_appoint_owner.succeeded():
        print("appoint owner: " + res_appoint_owner.get_msg())

    res_appoint_owner = trading_system.appoint_owner(cookie2, store_res.get_obj(), "user3")
    if not res_appoint_owner.succeeded():
        print("appoint owner: " + res_appoint_owner.get_msg())

    res_appoint_owner = trading_system.appoint_owner(cookie2, store_res2.get_obj(), "user")
    if not res_appoint_owner.succeeded():
        print("appoint owner: " + res_appoint_owner.get_msg())


if __name__ == '__main__':
    member_handler = MemberHandler.get_instance()
    store_handler = StoreHandler.get_instance()
    responsibility_handler = ResponsibilitiesHandler.get_instance()
    shopping_bag_handler = ShoppingBagHandler.get_instance()
    product_handler = ProductHandler.get_instance()
    purchase_details_handler = PurchaseDetailsHandler.get_instance()
    offer_handler = OfferHandler.get_instance()
    save()

    # trading_system = TradingSystem.getInstance()
    # cookie2 = trading_system.enter_system()
    # res2 = trading_system.login(cookie2, "user2", "password2")
    # res_cart = trading_system.get_cart_details(cookie2)
    # print(res_cart.get_obj())
    # price_res = trading_system.purchase_cart(cookie2, 17)
    # res_pay = trading_system.send_payment(cookie2, "", "")
    # print(res_pay.get_msg())

    # res_del_prod = trading_system.remove_product_from_cart(cookie, store_res.get_obj(), product_res.get_obj())
    # if not res_del_prod.succeeded():
    #     print("del from cart: " + res_del_prod.get_msg())
    #
    # change_prod_quantity = trading_system.change_product_quantity_in_cart(cookie, store_res.get_obj(), product2_res.get_obj(), 4)
    # if not change_prod_quantity.succeeded():
    #     print("change quantity in cart: " + change_prod_quantity.get_msg())
    #
    #
    # res = shopping_bag_handler.load_cart("user")
    # if not res.succeeded():
    #     print("load cart: " + res.get_msg())

    # user2 = User()
    # user2.register("user2", "password2")
    # res = member_handler.save_user_credentials("user2", "password2")
    # if not res.succeeded():
    #     print("save credentials: " + res.get_msg())
    # user2.login("user2", "password2")
    #
    # res = member_handler.save(user2.state)
    # if not res.succeeded():
    #     print("save user: " + res.get_msg())
    #
    # user.appoint_owner(store_res.get_obj().get_id(), user2)
    #
    # res = responsibility_handler.update_child("user", store_res.get_obj().get_id(), user2.state._Member__responsibilities[store_res.get_obj().get_id()])
    # # res = responsibility_handler.save(user2.state._Member__responsibilities[store_res.get_obj().get_id()])
    # if not res.succeeded():
    #     print("save responsibility: " + res.get_msg())
    # store = Store("Me Store")
    # member = Member(User(), "Me")
    # responsibility = Responsibility(member, store)
    # member.add_responsibility(responsibility, store.get_id())
    #
    # res = member_handler.save_user("Me", "Pass")
    # if not res.succeeded():
    #     print(res.get_msg())
    #
    # store.set_responsibility(responsibility)
    #
    # res = store_handler.save(store)
    # if not res.succeeded():
    #     print(res.get_msg())
    #
    # res = responsibility_handler.save(responsibility)
    # if not res.succeeded():
    #     print(res.get_msg())

    # res_cart = shopping_bag_handler.load_cart("user2")
    # if not res_cart.succeeded():
    #     print("load cart: " + res_cart.get_msg())
    #
    # # store_res = store_handler.load_store('f9729a4f-fe95-407d-9d9b-47af160aed61')
    # # print(store_res.get_obj())
    #
