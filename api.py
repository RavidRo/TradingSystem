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
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    username = (await request.get_json())["username"]
    password = (await request.get_json())["password"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.register, cookie, username, password)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/login", methods=["POST"])
async def login():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    username = (await request.get_json())["username"]
    password = (await request.get_json())["password"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.login, cookie, username, password)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_stores_details", methods=["GET"])
async def get_stores_details():
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_stores_details)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/get_products_by_store", methods=["GET"])
async def get_products_by_store():
    store_id = request.args.get("store_id")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_products_by_store, store_id)
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/search_products", methods=["GET"])
async def search_products():
    product_name = request.args.get("product_name")
    category = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    kwargs = request.args.get("kwargs")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.search_products, product_name, category, min_price, max_price, **kwargs
    )
    return json.dumps([ob.__dict__ for ob in answer.get_obj()])


@app.route("/save_product_in_cart", methods=["POST"])
async def save_product_in_cart():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    product_id = (await request.get_json())["product_id"]
    quantity = (await request.get_json())["quantity"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.save_product_in_cart, cookie, store_id, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_cart_details", methods=["GET"])
async def get_cart_details():
    cookie = request.args.get("cookie")
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_cart_details, cookie)
    return json.dumps({"cookie": cookie}.update([ob.__dict__ for ob in answer.get_obj()]))


@app.route("/remove_product_from_cart", methods=["POST"])
async def remove_product_from_cart():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    product_id = (await request.get_json())["product_id"]
    quantity = (await request.get_json())["quantity"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.remove_product_from_cart, cookie, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/change_product_quantity_in_cart", methods=["POST"])
async def change_product_quantity_in_cart():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    product_id = (await request.get_json())["product_id"]
    quantity = (await request.get_json())["quantity"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.remove_product_from_cart, cookie, store_id, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/purchase_cart", methods=["POST"])
async def purchase_cart():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.purchase_cart, cookie)
    return json.dumps({"cookie": cookie, "price": answer.get_obj()})


@app.route("/send_payment", methods=["POST"])
async def send_payment():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    payment_details = (await request.get_json())["payment_details"]
    address = (await request.get_json())["address"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(system.send_payment, cookie, payment_details, address)
    return json.dumps({"cookie": cookie, "price": answer.get_obj()})


# Member
# ===============================


@app.route("/create_store", methods=["POST"])
async def create_store():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    name = (await request.get_json())["name"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.create_store, cookie, name)
    return json.dumps({"cookie": cookie, "store_id": answer.get_obj()})


@app.route("/get_purchase_history", methods=["GET"])
async def get_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_purchase_history, cookie)
    return json.dumps({"cookie": cookie}.update([ob.__dict__ for ob in answer.get_obj()]))


# Owner and manager
# =======================


@app.route("/create_product", methods=["POST"])
async def create_product():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    name = (await request.get_json())["name"]
    price = (await request.get_json())["price"]
    quantity = (await request.get_json())["quantity"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.create_product, cookie, store_id, name, price, quantity
    )
    return json.dumps({"cookie": cookie, "product_id": answer.get_obj()})


@app.route("/remove_product_from_store", methods=["POST"])
async def remove_products():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    product_id = (await request.get_json())["product_id"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.remove_product_from_store, cookie, store_id, product_id
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/change_product_quantity", methods=["POST"])
async def change_product_quantity():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    product_id = (await request.get_json())["product_id"]
    quantity = (await request.get_json())["quantity"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.change_product_quantity_in_store, cookie, store_id, product_id, quantity
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/edit_product_details", methods=["POST"])
async def edit_product_details():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    product_id = (await request.get_json())["product_id"]
    new_name = (await request.get_json())["new_name"]
    new_price = (await request.get_json())["new_price"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.edit_product_details, cookie, store_id, product_id, new_name, new_price
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/appoint_owner", methods=["POST"])
async def appoint_owner():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    username = (await request.get_json())["username"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.appoint_owner, cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/appoint_manager", methods=["POST"])
async def appoint_manager():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    username = (await request.get_json())["username"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.appoint_manager, cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/add_manager_permission", methods=["POST"])
async def add_manager_permission():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    username = (await request.get_json())["username"]
    permission_number = (await request.get_json())["permission_number"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.add_manager_permission, cookie, store_id, username, permission_number
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/remove_manager_permission", methods=["POST"])
async def remove_manager_permission():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    username = (await request.get_json())["username"]
    permission_number = (await request.get_json())["permission_number"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.remove_manager_permission, cookie, store_id, username, permission_number
    )
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/remove_appointment", methods=["POST"])
async def remove_appointment():
    cookie = (await request.get_json())["cookie"]
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = (await request.get_json())["store_id"]
    username = (await request.get_json())["username"]
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.remove_appointment, cookie, store_id, username)
    return json.dumps(
        {"cookie": cookie, "answer": answer.get_msg(), "succeeded": answer.succeeded()}
    )


@app.route("/get_store_appointments", methods=["GET"])
async def get_store_appointments():
    cookie = request.args.get("cookie")
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_store_appointments, cookie, store_id)

    return json.dumps(
        {
            "cookie": cookie,
            "answer": answer.get_msg(),
            "succeeded": answer.succeeded(),
            "data": answer.get_obj().__dict__ if answer.get_obj() else None,
        }
    )


@app.route("/get_my_appointees", methods=["GET"])
async def get_my_appointees():
    cookie = request.args.get("cookie")
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_my_appointees, cookie, store_id)
    return json.dumps(
        {
            "cookie": cookie,
            "answer": answer.get_msg(),
            "succeeded": answer.succeeded(),
            "data": answer.get_obj().__dict__ if answer.succeeded() else None,
        }
    )


@app.route("/get_store_purchase_history", methods=["GET"])
async def get_store_purchases_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_store_purchase_history, cookie, store_id)
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
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    username = request.args.get("username")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(pool, system.get_user_purchase_history, cookie, username)
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
        loop = asyncio.get_event_loop()
        cookie = await loop.run_in_executor(pool, system.enter_system)
    store_id = request.args.get("store_id")
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        pool, system.get_any_store_purchase_history, cookie, store_id
    )
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
