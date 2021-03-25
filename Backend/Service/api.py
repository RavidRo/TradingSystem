"""this class if the gateway from the client to the domain server layer
all the api calls and data asked from the server goes here
this class is responsible for calling the right methods in the login classes"""

from flask import Flask, request
from Backend.Service.trading_system import TradingSystem

app = Flask(__name__)

system = TradingSystem.getInstance()


@app.route('/', methods=['GET'])
def main_page():
    cookie = system.enter_system()
    return '''<h1>Cookie is: {}</h1>'''.format(cookie)


@app.route('/register', methods=['GET'])
def register():
    cookie = request.args.get('cookie')
    username = request.args.get('username')
    password = request.args.get('password')
    answer = system.register(cookie=int(cookie), username=username, password=password)
    return '''<h1>Answer is: {}</h1>'''.format(answer)


@app.route('/login', methods=['GET'])
def login():
    cookie = request.args.get('cookie')
    username = request.args.get('username')
    password = request.args.get('password')
    answer = system.login(cookie=int(cookie), username=username, password=password)
    return '''<h1>Answer is: {}</h1>'''.format(answer)


@app.route('/get_stores_details', methods=['GET'])
def get_stores_details():
    answer = system.get_stores_details()
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/get_products_by_store', methods=['GET'])
def get_products_by_store() :
    store_id = request.args.get('store_id')
    answer = system.get_products_by_store(store_id)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/search_products', methods=['GET'])
def search_products():
    product_name = request.args.get('product_name')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    # TODO: what is kwargs?
    kwargs = request.args.get('kwargs')

    answer = system.search_products(product_name, category, min_price, max_price, **kwargs)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/add_to_cart', methods=['GET'])
def add_to_cart():
    cookie = request.args.get('cookie')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    answer = system.add_to_cart(cookie, product_id, quantity)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/get_cart_details', methods=['GET'])
def get_cart_details():
    cookie = request.args.get('cookie')
    answer = system.get_cart_details(cookie)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/remove_product_from_cart', methods=['GET'])
def remove_product_from_cart():
    cookie = request.args.get('cookie')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    answer = system.remove_product_from_cart(cookie, product_id, quantity)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/purchase_cart', methods=['GET'])
def purchase_cart():
    cookie = request.args.get('cookie')
    answer = system.purchase_cart(cookie)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/purchase_completed', methods=['GET'])
def purchase_completed(self,cookie : str) -> response[None]:
    cookie = request.args.get('cookie')
    answer = system.purchase_completed(cookie)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

# Member
# ===============================

@app.route('/create_store', methods=['GET'])
def create_store():
    cookie = request.args.get('cookie')
    name = request.args.get('name')
    answer = system.create_store(cookie,name)
    return '''<h1>Answer is: {}</h1>'''.format(answer)


@app.route('/ger_purchase_history', methods=['GET'])
def ger_purchase_history():
    cookie = request.args.get('cookie')
    answer = system.ger_purchase_history(cookie)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

# Owner and manager
# =======================

@app.route('/create_product', methods=['GET'])
def create_product():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    name = request.args.get('name')
    price = request.args.get('price')
    answer = system.create_product(cookie, store_id, name, price)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/add_products', methods=['GET'])
def add_products():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    answer = system.add_products(cookie, store_id, product_id, quantity)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/remove_products', methods=['GET'])
def remove_products():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    answer = system.remove_products(cookie, store_id, product_id, quantity)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/set_product_price', methods=['GET'])
def set_product_price():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    product_id = request.args.get('product_id')
    new_price = request.args.get('new_price')
    answer = system.set_product_price(cookie, store_id, product_id, new_price)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/appoint_owner', methods=['GET'])
def appoint_owner() :
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    username = request.args.get('username')
    answer = system.appoint_owner(cookie, store_id, username)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/appoint_manager', methods=['GET'])
def appoint_manager():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    username = request.args.get('username')
    answer = system.appoint_manager(cookie, store_id, username)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/add_manager_permission', methods=['GET'])
def add_manager_permission():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    username = request.args.get('username')
    permission_number = request.args.get('permission_number')
    answer = system.add_manager_permission(cookie, store_id, username,permission_number)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/remove_manager_permission', methods=['GET'])
def remove_manager_permission():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    username = request.args.get('username')
    permission_number = request.args.get('permission_number')
    answer = system.remove_manager_permission(cookie, store_id, username, permission_number)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/remove_appointment', methods=['GET'])
def remove_appointment():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    username = request.args.get('username')
    answer = system.remove_appointment(cookie, store_id, username)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/get_store_appointments', methods=['GET'])
def get_store_appointments():
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    answer = system.get_store_appointments(cookie, store_id)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/get_store_purchases_history', methods=['GET'])
def get_store_purchases_history() :
    cookie = request.args.get('cookie')
    store_id = request.args.get('store_id')
    answer = system.get_store_purchases_history(cookie, store_id)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

#System Manager
#====================

@app.route('/get_user_purchase_history', methods=['GET'])
def get_user_purchase_history():
    cookie = request.args.get('cookie')
    username = request.args.get('username')
    answer = system.get_user_purchase_history(cookie, username)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run(debug=True)
