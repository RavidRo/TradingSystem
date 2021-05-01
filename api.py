"""this class if the gateway from the client to the domain server layer
all the api calls and data asked from the server goes here
this class is responsible for calling the right methods in the login classes"""
import asyncio
import concurrent

from Backend.Service.trading_system import TradingSystem
from quart import Quart, websocket, request, send_from_directory
import json

system = TradingSystem.getInstance()
pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
app = Quart(__name__, static_url_path="", static_folder="Frontend/dist")
loop = asyncio.get_event_loop()


@app.route("/", methods=["GET"])
async def index():
    return await send_from_directory(app.static_folder, "index.html")


@app.route("/get_cookie", methods=["GET"])
async def get_cookie():
    cookie = system.enter_system()
    return json.dumps({"cookie": cookie})


@app.websocket("/connect")
def connect():  # TODO: this
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = system.enter_system()
    answer = system.connect(cookie, lambda messages: websocket.send(messages))
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/register", methods=["POST"])
async def register():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    answer = await loop.run_in_executor(pool, system.register, cookie, username, password)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/login", methods=["POST"])
async def login():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    answer = await loop.run_in_executor(pool, system.register, cookie, username, password)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_stores_details", methods=["GET"])
async def get_stores_details():
    answer = await loop.run_in_executor(system.get_stores_details)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/get_products_by_store", methods=["GET"])
async def get_products_by_store():
    store_id = request.args.get("store_id")
    answer = await loop.run_in_executor(system.get_products_by_store, store_id)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/search_products", methods=["GET"])
async def search_products():
    product_name = request.args.get("product_name")
    category = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    kwargs = request.args.get("kwargs")
    answer = await loop.run_in_executor(
        system.search_products, product_name, category, min_price, max_price, **kwargs
    )
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/save_product_in_cart", methods=["POST"])
async def save_product_in_cart():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    product_id = request.get_json()["product_id"]
    quantity = request.get_json()["quantity"]
    answer = await loop.run_in_executor(
        system.save_product_in_cart, cookie, store_id, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_cart_details", methods=["GET"])
async def get_cart_details():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    answer = await loop.run_in_executor(system.get_cart_details, cookie)
    return json.dumps({"cookie": cookie}.update([ob.__dict__ for ob in answer.get_obj()]))


@app.route("/remove_product_from_cart", methods=["POST"])
async def remove_product_from_cart():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    product_id = request.get_json()["product_id"]
    quantity = request.get_json()["quantity"]
    answer = await loop.run_in_executor(
        system.remove_product_from_cart, cookie, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/change_product_quantity_in_cart", methods=["POST"])
async def change_product_quantity_in_cart():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    product_id = request.get_json()["product_id"]
    quantity = request.get_json()["quantity"]
    answer = await loop.run_in_executor(
        system.remove_product_from_cart, cookie, store_id, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/purchase_cart", methods=["POST"])
async def purchase_cart():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    answer = await loop.run_in_executor(system.purchase_cart, cookie)
    return json.dumps({"cookie": cookie, "price": answer.get_obj()})


@app.route("/send_payment", methods=["POST"])
async def send_payment():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    payment_details = request.get_json()["payment_details"]
    await loop.run_in_executor(system.purchase_cart, cookie, payment_details)
    address = request.get_json()["address"]
    answer = await loop.run_in_executor(system.send_payment, cookie, payment_details, address)
    return json.dumps({"cookie": cookie, "price": answer.get_obj()})


# Member
# ===============================


@app.route("/create_store", methods=["POST"])
async def create_store():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    name = request.get_json()["name"]
    answer = await loop.run_in_executor(system.create_store, cookie, name)
    return json.dumps({"cookie": cookie, "store_id": answer.get_obj()})


@app.route("/get_purchase_history", methods=["GET"])
async def get_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    answer = await loop.run_in_executor(system.get_purchase_history, cookie)
    return json.dumps({"cookie": cookie}.update([ob.__dict__ for ob in answer.get_obj()]))


# Owner and manager
# =======================


@app.route("/create_product", methods=["POST"])
async def create_product():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    name = request.get_json()["name"]
    price = request.get_json()["price"]
    quantity = request.get_json()["quantity"]
    answer = await loop.run_in_executor(
        system.create_product, cookie, store_id, name, price, quantity
    )
    return json.dumps({"cookie": cookie, "product_id": answer.get_obj()})


@app.route("/remove_product_from_store", methods=["POST"])
async def remove_products():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    product_id = request.get_json()["product_id"]
    answer = await loop.run_in_executor(
        system.remove_product_from_store, cookie, store_id, product_id
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/change_product_quantity", methods=["POST"])
async def change_product_quantity():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    product_id = request.get_json()["product_id"]
    quantity = request.get_json()["quantity"]
    answer = await loop.run_in_executor(
        system.change_product_quantity_in_store, cookie, store_id, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/edit_product_details", methods=["POST"])
async def edit_product_details():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    product_id = request.get_json()["product_id"]
    new_name = request.get_json()["new_name"]
    new_price = request.get_json()["new_price"]
    answer = await loop.run_in_executor(
        system.edit_product_details, cookie, store_id, product_id, new_name, new_price
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/appoint_owner", methods=["POST"])
async def appoint_owner():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    username = request.get_json()["username"]
    answer = await loop.run_in_executor(system.appoint_owner, cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/appoint_manager", methods=["POST"])
async def appoint_manager():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    username = request.get_json()["username"]
    answer = await loop.run_in_executor(system.appoint_manager, cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/add_manager_permission", methods=["POST"])
async def add_manager_permission():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    username = request.get_json()["username"]
    permission_number = request.get_json()["permission_number"]
    answer = await loop.run_in_executor(
        system.add_manager_permission, cookie, store_id, username, permission_number
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/remove_manager_permission", methods=["POST"])
async def remove_manager_permission():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    username = request.get_json()["username"]
    permission_number = request.get_json()["permission_number"]
    answer = await loop.run_in_executor(
        system.remove_manager_permission, cookie, store_id, username, permission_number
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/remove_appointment", methods=["POST"])
async def remove_appointment():
    cookie = request.get_json()["cookie"]
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.get_json()["store_id"]
    username = request.get_json()["username"]
    answer = await loop.run_in_executor(system.remove_appointment, cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_store_appointments", methods=["GET"])
async def get_store_appointments():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    answer = await loop.run_in_executor(system.get_store_appointments, cookie, store_id)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
            answer.get_obj().__dict__
        )
    )


@app.route("/get_my_appointees", methods=["GET"])
async def get_my_appointees():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    answer = await loop.run_in_executor(system.get_my_appointees, cookie, store_id)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}.update(
            answer.get_obj().__dict__
        )
    )


@app.route("/get_store_purchase_history", methods=["GET"])
async def get_store_purchases_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    answer = await loop.run_in_executor(system.get_store_purchase_history, cookie, store_id)
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
        cookie = await loop.run_in_executor(pool, system.enter_system)
    username = request.args.get("username")
    answer = await loop.run_in_executor(system.get_user_purchase_history, cookie, username)
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
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    answer = await loop.run_in_executor(system.get_any_store_purchase_history, cookie, store_id)
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
async def page_not_found(e):
    return json.dumps({"error": "404 page not found"})


if __name__ == "__main__":
    app.run(debug=True)
    # asyncio.run(app.run(debug=True))
