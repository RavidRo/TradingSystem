"""this class if the gateway from the client to the domain server layer
all the api calls and data asked from the server goes here
this class is responsible for calling the right methods in the login classes"""
from typing import Callable
from Backend.response import Response
import asyncio
import concurrent

from Backend.Service.trading_system import TradingSystem
from quart import Quart, websocket, request, send_from_directory
import json

system = TradingSystem.getInstance()
pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
app = Quart(__name__, static_url_path="", static_folder="Frontend/dist")


def __responseToJson(cookie: str, response: Response, toData: Callable = lambda obj: obj):
    return json.dumps(
        {
            "cookie": cookie,
            "error_msg": response.get_msg(),
            "succeeded": response.succeeded(),
            "data": toData(response.get_obj()) if response.succeeded() else None,
        },
        default=lambda o: o.__dict__,
    )


def __missing_args(cookie: str, missing_args: str):
    return json.dumps(
        {
            "cookie": cookie,
            "error_msg": f"missing arguments: {missing_args}",
            "succeeded": False,
            "data": None,
        }
    )


async def __async_call(func: Callable, *args, **kwargs) -> Response:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(pool, func, *args, **kwargs)


@app.route("/", methods=["GET"])
async def index():
    return await send_from_directory(app.static_folder, "index.html")


@app.route("/get_cookie", methods=["GET"])
async def get_cookie():
    cookie = system.enter_system()
    return json.dumps(
        {
            "cookie": cookie,
            "error_msg": "",
            "succeeded": True,
            "data": {"cookie": cookie},
        }
    )


@app.websocket("/connect")
def connect():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = system.enter_system()
    answer = system.connect(cookie, lambda messages: websocket.send(messages))
    return __responseToJson(cookie, answer)


@app.route("/register", methods=["POST"])
async def register():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "username" not in request_json:
        missing_args += " username"
    if "password" not in request_json:
        missing_args += " password"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    username = (await request_json)["username"]
    password = (await request_json)["password"]
    answer = await __async_call(system.register, cookie, username, password)
    return __responseToJson(cookie, answer)


@app.route("/login", methods=["POST"])
async def login():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "username" not in request_json:
        missing_args += " username"
    if "password" not in request_json:
        missing_args += " password"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    username = (await request_json)["username"]
    password = (await request_json)["password"]
    answer = await __async_call(system.login, cookie, username, password)
    return __responseToJson(cookie, answer)


@app.route("/get_stores_details", methods=["GET"])
async def get_stores_details():
    answer = await __async_call(system.get_stores_details)
    return __responseToJson(None, answer, lambda obj: obj.values)


@app.route("/get_store", methods=["GET"])
async def get_store():
    store_id = request.args.get("store_id")
    answer = await __async_call(system.get_store, store_id)
    return __responseToJson(None, answer, lambda obj: obj.__dict__)


@app.route("/get_products_by_store", methods=["GET"])
async def get_products_by_store():
    store_id = request.args.get("store_id")
    answer = await __async_call(system.get_products_by_store, store_id)
    return __responseToJson(None, answer, lambda obj: obj.values)


@app.route("/search_products", methods=["GET"])
async def search_products():
    product_name = request.args.get("product_name")
    category = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    kwargs = request.args.get("kwargs")
    answer = await __async_call(
        system.search_products, product_name, category, min_price, max_price, kwargs
    )
    return __responseToJson(None, answer, lambda obj: obj.values)


@app.route("/save_product_in_cart", methods=["POST"])
async def save_product_in_cart():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "product_id" not in request_json:
        missing_args += " product_id"
    if "quantity" not in request_json:
        missing_args += " quantity"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    product_id = (await request_json)["product_id"]
    quantity = (await request_json)["quantity"]
    answer = await __async_call(system.save_product_in_cart, cookie, store_id, product_id, quantity)
    return __responseToJson(cookie, answer)


@app.route("/get_cart_details", methods=["GET"])
async def get_cart_details():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    answer = await __async_call(system.get_cart_details, cookie)
    return __responseToJson(cookie, answer, lambda obj: obj.__dict__)


@app.route("/remove_product_from_cart", methods=["POST"])
async def remove_product_from_cart():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "product_id" not in request_json:
        missing_args += " product_id"
    if "quantity" not in request_json:
        missing_args += " quantity"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    product_id = (await request_json)["product_id"]
    quantity = (await request_json)["quantity"]
    answer = await __async_call(system.remove_product_from_cart, cookie, product_id, quantity)
    return __responseToJson(cookie, answer)


@app.route("/change_product_quantity_in_cart", methods=["POST"])
async def change_product_quantity_in_cart():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "product_id" not in request_json:
        missing_args += " product_id"
    if "quantity" not in request_json:
        missing_args += " quantity"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    product_id = (await request_json)["product_id"]
    quantity = (await request_json)["quantity"]
    answer = await __async_call(
        system.remove_product_from_cart, cookie, store_id, product_id, quantity
    )
    return __responseToJson(cookie, answer)


@app.route("/purchase_cart", methods=["POST"])
async def purchase_cart():
    request_json = request.get_json()
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    answer = await __async_call(system.purchase_cart, cookie)
    return __responseToJson(cookie, answer, lambda obj: obj.get_val())


@app.route("/send_payment", methods=["POST"])
async def send_payment():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "payment_details" not in request_json:
        missing_args += " payment_details"
    if "address" not in request_json:
        missing_args += " address"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    payment_details = (await request_json)["payment_details"]
    address = (await request_json)["address"]
    answer = await __async_call(system.send_payment, cookie, payment_details, address)
    return __responseToJson(cookie, answer)


# Member
# ===============================


@app.route("/create_store", methods=["POST"])
async def create_store():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "name" not in request_json:
        missing_args += " name"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    name = (await request_json)["name"]
    answer = await __async_call(system.create_store, cookie, name)
    return __responseToJson(cookie, answer)


@app.route("/get_purchase_history", methods=["GET"])
async def get_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    answer = await __async_call(system.get_purchase_history, cookie)
    return __responseToJson(cookie, answer, lambda obj: obj.values)


# Owner and manager
# =======================


@app.route("/create_product", methods=["POST"])
async def create_product():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "name" not in request_json:
        missing_args += " name"
    if "price" not in request_json:
        missing_args += " price"
    if "quantity" not in request_json:
        missing_args += " quantity"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request.get_json())["store_id"]
    name = (await request.get_json())["name"]
    price = (await request.get_json())["price"]
    quantity = (await request.get_json())["quantity"]
    category = (await request.get_json())["category"]
    keywords = (await request.get_json())["keywords"]
    answer = await __async_call(
        system.create_product, cookie, store_id, name, category, price, quantity, keywords
    )
    return __responseToJson(cookie, answer)


@app.route("/remove_product_from_store", methods=["POST"])
async def remove_products():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "product_id" not in request_json:
        missing_args += " product_id"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    product_id = (await request_json)["product_id"]
    answer = await __async_call(system.remove_product_from_store, cookie, store_id, product_id)
    return __responseToJson(cookie, answer, lambda obj: obj.get_val())


@app.route("/change_product_quantity", methods=["POST"])
async def change_product_quantity():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "product_id" not in request_json:
        missing_args += " product_id"
    if "quantity" not in request_json:
        missing_args += " quantity"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    product_id = (await request_json)["product_id"]
    quantity = (await request_json)["quantity"]
    answer = await __async_call(
        system.change_product_quantity_in_store, cookie, store_id, product_id, quantity
    )
    return __responseToJson(cookie, answer)


@app.route("/edit_product_details", methods=["POST"])
async def edit_product_details():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "product_id" not in request_json:
        missing_args += " product_id"
    if "new_name" not in request_json:
        missing_args += " new_name"
    if "new_price" not in request_json:
        missing_args += " new_price"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    product_id = (await request_json)["product_id"]
    new_name = (await request_json)["new_name"]
    new_price = (await request_json)["new_price"]
    answer = await __async_call(
        system.edit_product_details, cookie, store_id, product_id, new_name, new_price
    )
    return __responseToJson(cookie, answer)


@app.route("/appoint_owner", methods=["POST"])
async def appoint_owner():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "username" not in request_json:
        missing_args += " username"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    username = (await request_json)["username"]
    answer = await __async_call(system.appoint_owner, cookie, store_id, username)
    return __responseToJson(cookie, answer)


@app.route("/appoint_manager", methods=["POST"])
async def appoint_manager():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "username" not in request_json:
        missing_args += " username"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    username = (await request_json)["username"]
    answer = await __async_call(system.appoint_manager, cookie, store_id, username)
    return __responseToJson(cookie, answer)


@app.route("/add_manager_permission", methods=["POST"])
async def add_manager_permission():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "username" not in request_json:
        missing_args += " username"
    if "permission_number" not in request_json:
        missing_args += " permission_number"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    username = (await request_json)["username"]
    permission_number = (await request_json)["permission_number"]
    answer = await __async_call(
        system.add_manager_permission, cookie, store_id, username, permission_number
    )
    return __responseToJson(cookie, answer)


@app.route("/remove_manager_permission", methods=["POST"])
async def remove_manager_permission():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "username" not in request_json:
        missing_args += " username"
    if "permission_number" not in request_json:
        missing_args += " permission_number"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    username = (await request_json)["username"]
    permission_number = (await request_json)["permission_number"]
    answer = await __async_call(
        system.remove_manager_permission, cookie, store_id, username, permission_number
    )
    return __responseToJson(cookie, answer)


@app.route("/remove_appointment", methods=["POST"])
async def remove_appointment():
    request_json = request.get_json()
    missing_args = ""
    if "cookie" not in request_json:
        cookie = await __async_call(system.enter_system)
    else:
        cookie = (await request_json)["cookie"]
    if "store_id" not in request_json:
        missing_args += " store_id"
    if "username" not in request_json:
        missing_args += " username"
    if missing_args != "":
        return __missing_args(cookie, missing_args)
    store_id = (await request_json)["store_id"]
    username = (await request_json)["username"]
    answer = await __async_call(system.remove_appointment, cookie, store_id, username)
    return __responseToJson(cookie, answer)


@app.route("/get_store_appointments", methods=["GET"])
async def get_store_appointments():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    store_id = request.args.get("store_id")
    answer = await __async_call(system.get_store_appointments, cookie, store_id)

    return __responseToJson(cookie, answer, lambda obj: obj.__dict__)


@app.route("/get_my_appointments", methods=["GET"])
async def get_my_appointments():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    answer = await __async_call(system.get_my_appointments, cookie)
    return __responseToJson(cookie, answer, lambda obj: obj.values)


@app.route("/get_store_purchase_history", methods=["GET"])
async def get_store_purchases_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    store_id = request.args.get("store_id")
    answer = await __async_call(system.get_store_purchase_history, cookie, store_id)
    return __responseToJson(cookie, answer, lambda obj: obj.values)


# System Manager
# ====================


@app.route("/get_user_purchase_history", methods=["GET"])
async def get_user_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    username = request.args.get("username")
    answer = await __async_call(system.get_user_purchase_history, cookie, username)
    return __responseToJson(cookie, answer, lambda obj: obj.values)


@app.route("/get_any_store_purchase_history", methods=["GET"])
async def get_any_store_purchase_history():
    cookie = request.args.get("cookie")
    if cookie is None:
        cookie = await __async_call(system.enter_system)
    store_id = request.args.get("store_id")
    answer = await __async_call(system.get_any_store_purchase_history, cookie, store_id)
    return __responseToJson(cookie, answer, lambda obj: obj.values)


@app.errorhandler(404)
async def page_not_found(e):
    return json.dumps({"error": "404 page not found"})


if __name__ == "__main__":
    app.run(debug=True)
