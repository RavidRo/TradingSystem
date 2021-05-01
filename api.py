"""this class if the gateway from the client to the domain server layer
all the api calls and data asked from the server goes here
this class is responsible for calling the right methods in the login classes"""

from Backend.Service.trading_system import TradingSystem
from quart import Quart, websocket, request, send_from_directory
import json

system = TradingSystem.getInstance()
app = Quart(__name__, static_url_path="", static_folder="Frontend/build")


@app.route("/", methods=["GET"])
async def index():
    return await send_from_directory(app.static_folder, "index.html")


@app.route("/cookie", methods=["GET"])
async def get_cookie():
    cookie = system.enter_system()
    return json.dumps({"cookie": cookie})


@app.websocket("/connect")
def connect():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = system.enter_system()
    answer = system.connect(cookie, lambda messages: websocket.send(messages))
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/register", methods=["POST"])
async def register():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    username = request.args.get("username")
    password = request.args.get("password")
    answer = system.register(cookie=int(cookie), username=username, password=password)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/login", methods=["POST"])
async def login():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    username = request.args.get("username")
    password = request.args.get("password")
    answer = await system.login(cookie=int(cookie), username=username, password=password)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_stores_details", methods=["HEAD"])
async def get_stores_details():
    answer = await system.get_stores_details()
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/get_store", methods=["HEAD"])
async def get_store():
    store_id = request.args.get("store_id")
    answer = await system.get_store(store_id)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/get_products_by_store", methods=["GET"])
async def get_products_by_store():
    store_id = request.args.get("store_id")
    answer = await system.get_products_by_store(store_id)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/search_products", methods=["GET"])
async def search_products():
    product_name = request.args.get("product_name")
    category = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    kwargs = request.args.get("kwargs")
    answer = await system.search_products(product_name, category, min_price, max_price, **kwargs)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/save_product_in_cart", methods=["POST"])
async def save_product_in_cart():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    answer = await system.save_product_in_cart(cookie, store_id, product_id, quantity)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_cart_details", methods=["HEAD"])
async def get_cart_details():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    answer = await system.get_cart_details(cookie)
    return json.dumps({"cookie": cookie}.update([ob.__dict__ for ob in answer.get_obj()]))


@app.route("/remove_product_from_cart", methods=["POST"])
async def remove_product_from_cart():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    answer = await system.remove_product_from_cart(cookie, product_id, quantity)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/change_product_quantity_in_cart", methods=["POST"])
async def change_product_quantity_in_cart():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    answer = await system.remove_product_from_cart(cookie, store_id, product_id, quantity)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/purchase_cart", methods=["POST"])
async def purchase_cart():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    answer = await system.purchase_cart(cookie)
    return json.dumps({"cookie": cookie, "price": answer.get_obj()})


@app.route("/send_payment", methods=["POST"])
async def send_payment():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    payment_details = request.args.get("payment_details")
    await system.purchase_cart(cookie, payment_details)
    address = request.args.get("address")
    answer = await system.send_payment(cookie, payment_details, address)
    return json.dumps({"cookie": cookie, "price": answer.get_obj()})


# Member
# ===============================


@app.route("/create_store", methods=["POST"])
async def create_store():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    name = request.args.get("name")
    answer = await system.create_store(cookie, name)
    return json.dumps({"cookie": cookie, "store_id": answer.get_obj()})


@app.route("/get_purchase_history", methods=["HEAD"])
async def get_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    answer = await system.get_purchase_history(cookie)
    return json.dumps({"cookie": cookie}.update([ob.__dict__ for ob in answer.get_obj()]))


# Owner and manager
# =======================


@app.route("/create_product", methods=["POST"])
async def create_product():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    name = request.args.get("name")
    price = request.args.get("price")
    quantity = request.args.get("quantity")
    answer = await system.create_product(cookie, store_id, name, price, quantity)
    return json.dumps({"cookie": cookie, "product_id": answer.get_obj()})


@app.route("/remove_product_from_store", methods=["POST"])
async def remove_products():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    product_id = request.args.get("product_id")
    answer = await system.remove_product_from_store(cookie, store_id, product_id)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/change_product_quantity", methods=["POST"])
async def change_product_quantity():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    answer = await system.change_product_quantity_in_store(cookie, store_id, product_id, quantity)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/edit_product_details", methods=["POST"])
async def edit_product_details():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    product_id = request.args.get("product_id")
    new_name = request.args.get("new_name")
    new_price = request.args.get("new_price")
    answer = await system.edit_product_details(cookie, store_id, product_id, new_name, new_price)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/appoint_owner", methods=["POST"])
async def appoint_owner():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    username = request.args.get("username")
    answer = await system.appoint_owner(cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/appoint_manager", methods=["POST"])
async def appoint_manager():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    username = request.args.get("username")
    answer = await system.appoint_manager(cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/add_manager_permission", methods=["POST"])
async def add_manager_permission():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    username = request.args.get("username")
    permission_number = request.args.get("permission_number")
    answer = await system.add_manager_permission(cookie, store_id, username, permission_number)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/remove_manager_permission", methods=["POST"])
async def remove_manager_permission():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    username = request.args.get("username")
    permission_number = request.args.get("permission_number")
    answer = await system.remove_manager_permission(cookie, store_id, username, permission_number)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/remove_appointment", methods=["POST"])
async def remove_appointment():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    username = request.args.get("username")
    answer = await system.remove_appointment(cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_store_appointments", methods=["GET"])
async def get_store_appointments():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    answer = await system.get_store_appointments(cookie, store_id)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
            answer.get_obj().__dict__
        )
    )


@app.route("/get_my_appointees", methods=["GET"])
async def get_my_appointees():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    answer = await system.get_my_appointees(cookie, store_id)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
            answer.get_obj().__dict__
        )
    )


@app.route("/get_store_purchase_history", methods=["GET"])
async def get_store_purchases_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    answer = await system.get_store_purchase_history(cookie, store_id)
    if answer.succeeded():
        return json.dumps(
            {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
                [ob.__dict__ for ob in answer.get_obj()]
            )
        )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


# System Manager
# ====================


@app.route("/get_user_purchase_history", methods=["GET"])
async def get_user_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    username = request.args.get("username")
    answer = await system.get_user_purchase_history(cookie, username)
    if answer.succeeded():
        return json.dumps(
            {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
                [ob.__dict__ for ob in answer.get_obj()]
            )
        )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_any_store_purchase_history", methods=["GET"])
async def get_any_store_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await system.enter_system()
    store_id = request.args.get("store_id")
    answer = await system.get_any_store_purchase_history(cookie, store_id)
    if answer.succeeded():
        return json.dumps(
            {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
                [ob.__dict__ for ob in answer.get_obj()]
            )
        )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.errorhandler(404)
async def page_not_found():
    return json.dumps({"error": "404 page not found"})


if __name__ == "__main__":
    app.run(debug=True)
    # asyncio.run(app.run(debug=True))
