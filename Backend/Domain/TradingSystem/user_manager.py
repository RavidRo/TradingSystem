import uuid

from .user import user
from Backend.response import Response, ParsableList, PrimitiveParsable
from .Responsibilities.Responsibility import permission
from Backend.Domain.TradingSystem.shopping_cart import shopping_cart
from Backend.Domain.TradingSystem.purchase_details import purchase_details
from .Responsibilities.Responsibility import permission, responsibility

class user_manager:
	cookie_user : dict[str, user] = {}
	username_user : dict[str, user] = {}

	def __deligate_to_user(cookie, func):
		user = user_manager.__get_user_by_cookie(cookie)
		if not user:
			return Response(False, msg="No user is identified by the given cookie")
		return func(user)

	def __get_user_by_cookie(cookie) -> user:
		if cookie not in user_manager.cookie_user:
			return None
		return user_manager.cookie_user[cookie]
			
	def __get_user_by_username(username) -> user:
		if username not in user_manager.username_user:
			return None
		return user_manager.username_user[username]

	def __create_cookie() -> str:
		return str(uuid.uuid4())

	# Called after register was successful and state was updated with the username
	def __user_registered(username : str) -> None:
		for cookie in user_manager.cookie_user:
			user = user_manager.cookie_user[cookie]
			if user.get_username() == username:
				user_manager.username_user[username] = user


	#2.1
	# returns the guest newly created cookie
	def enter_system() -> str:
		cookie = user_manager.__create_cookie()
		user_manager.cookie_user[cookie] = cookie
		return cookie

	#2.3
	def register(username : str, password : str, cookie : str) -> Response[None]:
		user = user_manager.__get_user_by_cookie(cookie)
		if not user:
			return Response(False, msg="No user is identified by the given cookie")
		response = user.register(username, password)
		if response.succeeded:
			user_manager.__user_registered(username)
		return response

	#2.4
	def login(username : str, password : str, cookie : str) -> Response[None]:
		user = user_manager.__get_user_by_cookie(cookie)
		if not user:
			return Response(False, msg="No user is identified by the given cookie")
		response = user.login(username, password)
		
		# If response succeeded we want to connect the cookie to the username
		for user_cookie in user_manager.cookie_user:
			old_user = user_manager.cookie_user[user_cookie]
			if old_user.get_username() == username:
				user_manager.cookie_user[cookie] = old_user
		# *This action will delete the current cart but will restore the old one and other user details

		return response

	#2.7
	def add_to_cart(cookie : str, store_id : str, product_id : str, quantity : int) -> Response[None]:
		func = lambda user: user.add_to_cart(store_id, product_id, quantity)
		return user_manager.__deligate_to_user(cookie, func)

	#2.8
	def get_cart_details(cookie : str) -> Response[shopping_cart]:
		func = lambda user: user.get_cart_details()
		return user_manager.__deligate_to_user(cookie, func)

	#2.8
	def remove_product_from_cart(cookie : str, store_id : str, product_id : str) -> Response[None]:
		func = lambda user: user.remove_product_from_cart(store_id, product_id)
		return user_manager.__deligate_to_user(cookie, func)
	
	#2.8
	def change_product_quantity(cookie : str, store_id, product_id, new_amount) -> Response[None]:
		func = lambda user: user.change_product_quantity(store_id, product_id, new_amount)
		return user_manager.__deligate_to_user(cookie, func)

	#2.9
	def purchase_cart(cookie : str) -> Response[PrimitiveParsable[float]]:
		func = lambda user: user.purchase_cart()
		return user_manager.__deligate_to_user(cookie, func)

	#2.9
	def purchase_completed(cookie : str) -> Response[None]:
		func = lambda user: user.purchase_completed()
		return user_manager.__deligate_to_user(cookie, func)

	# Member
	# ===============================

	#3.2
	def create_store(cookie : str, name : str) -> Response[None]:
		func = lambda user: user.create_store(name)
		return user_manager.__deligate_to_user(cookie, func)
	#3.7
	def ger_purchase_history(cookie : str) -> Response[ParsableList[purchase_details]]:
		func = lambda user: user.ger_purchase_history(cookie)
		return user_manager.__deligate_to_user(cookie, func)

	# Owner and manager
	# =======================

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(cookie : str, store_id : str, name : str, price: float, quantity : int) -> Response[None]:
		func = lambda user: user.create_product(store_id, name, price, quantity)
		return user_manager.__deligate_to_user(cookie, func)

	#4.1
	def remove_products(cookie : str, store_id : str, product_id : str) -> Response[None]:
		func = lambda user: user.remove_products(store_id, product_id)
		return user_manager.__deligate_to_user(cookie, func)

	#4.1
	def change_product_quantity(cookie : str, store_id : str, product_id : str, quantity : int) -> Response[None]:
		func = lambda user: user.change_product_quantity(store_id, product_id, quantity)
		return user_manager.__deligate_to_user(cookie, func)

	#4.1
	def edit_product_details(cookie : str, store_id : str, product_id : str, new_name: str, new_price : float) -> Response[None]:
		func = lambda user: user.edit_product_details(store_id, product_id, new_name, new_price)
		return user_manager.__deligate_to_user(cookie, func)

	#4.3
	def appoint_owner(cookie : str, store_id : str, username : str) -> Response[None]:
		user = user_manager.__get_user_by_username(username)
		if not user:
			return Response(False, "Given username odes not exists")
		func = lambda user: user.appoint_owner(store_id, user)
		return user_manager.__deligate_to_user(cookie, func)

	#4.5
	def appoint_manager(cookie : str, store_id : str, username : str) -> Response[None]:
		user = user_manager.__get_user_by_username(username)
		if not user:
			return Response(False, "Given username odes not exists")
		func = lambda user: user.appoint_manager(store_id, user)
		return user_manager.__deligate_to_user(cookie, func)

	#4.6
	def add_manager_permission(cookie : str, store_id : str, username : str, permission : permission) -> Response[None]:
		func = lambda user: user.add_manager_permission(store_id, username, permission)
		return user_manager.__deligate_to_user(cookie, func)

	#4.6
	def remove_manager_permission(cookie : str, store_id : str, username : str, permission : permission) -> Response[None]:
		func = lambda user: user.remove_manager_permission(store_id, username, permission)
		return user_manager.__deligate_to_user(cookie, func)

	#4.4, 4.7
	def remove_appointment(cookie : str, store_id : str, username : str) -> Response[None]:
		func = lambda user: user.remove_appointment(store_id, username)
		return user_manager.__deligate_to_user(cookie, func)

	#4.9
	def get_store_appointments(cookie : str, store_id : str) -> Response[responsibility]:
		func = lambda user: user.get_store_appointments(store_id)
		return user_manager.__deligate_to_user(cookie, func)

	#4.11
	def get_store_purchases_history(cookie : str, store_id : str) -> Response[ParsableList[purchase_details]]:
		func = lambda user: user.get_store_purchases_history(store_id)
		return user_manager.__deligate_to_user(cookie, func)

	#System Manager
	#====================

	#6.4
	def get_any_store_purchase_history(cookie : str, store_id : str) -> Response[ParsableList[purchase_details]]:
		func = lambda user: user.get_any_store_purchase_history(store_id)
		return user_manager.__deligate_to_user(cookie, func)

	#6.4
	def get_any_user_purchase_history(cookie : str, username : str) -> Response[ParsableList[purchase_details]]:
		func = lambda user: user.get_any_user_purchase_history(username)
		return user_manager.__deligate_to_user(cookie, func)
	

	# Inter component functions
	#====================



