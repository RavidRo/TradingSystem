from Backend.DataBase.Handlers.member_handler import MemberHandler
from Backend.DataBase.Handlers.product_handler import ProductHandler
from Backend.DataBase.Handlers.purchase_details_handler import PurchaseDetailsHandler
from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
from Backend.DataBase.Handlers.store_handler import StoreHandler
from Backend.DataBase.database import Base, engine
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.States.member import Member
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.user import User

if __name__ == '__main__':
    member_handler = MemberHandler.get_instance()
    product_handler = ProductHandler.get_instance()
    purchase_details_handler = PurchaseDetailsHandler.get_instance()
    store_handler = StoreHandler.get_instance()
    responsibility_handler = ResponsibilitiesHandler.get_instance()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user = User()
    res = user.register("user", "password")
    if not res.succeeded():
        print("register: " + res.get_msg())
    res = user.login("user", "password")
    if not res.succeeded():
        print("login: " + res.get_msg())
    store_res = user.create_store("The Store")
    if not store_res.succeeded():
        print("open_store: " + store_res.get_msg())

    res = store_res.get_obj().add_product("The Product", "The Category", 5, 8, ["The Keyword A", "The Keyword B"])
    if not res.succeeded():
        print("add_product: " + res.get_msg())

    res = store_res.get_obj().change_product_quantity(res.get_obj(), 11)
    if not res.succeeded():
        print("edit product details: " + res.get_msg())


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
