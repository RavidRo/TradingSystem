from .StoresManager import StoresManager
from .UserManager import UserManager
from .SearchEngine import SearchEngine
from .Responsibilities.Responsibility import permissions

# TODO: import response and data objects
class TradingSystem:

	#2.1
	# returns the guest newly created cookie
	def enter_system() -> str:
		return UserManager.enter_system()

	#2.3
	def register(username : str, password : str, cookie : str) -> response[None]:
		return UserManager.register(username, password, cookie)

	#2.4
	def login(username : str, password : str, cookie : str) -> response[None]:
		return UserManager.login(username, password, cookie)

	#2.5
	def get_stores_details() -> response[list[StoreData]]:
		return StoresManager.get_stores_details()

	#2.5
	def get_products_by_store(store_id : str) -> response[list[ProductData]]:
		return StoresManager.get_products_by_store(store_id)

	#2.6
	# kwargs = You can search for a product by additional key words
	def search_products(product_name="", category=None, min_price=None, max_price=None, **kwargs) -> response[list[ProductData]]:
		return SearchEngine.search_products(product_name, category, min_price, max_price, **kwargs)

	#2.7
	def add_to_cart(cookie : str, product_id : str, quantity=1) -> response[None]:
		return UserManager.add_to_cart(cookie, product_id, quantity)

	#2.8
	def get_cart_details(cookie : str) -> response[ShoppingCartData]:
		return UserManager.get_cart_details(cookie)

	#2.8
	def remove_product_from_cart(cookie : str, product_id : str, quantity=1) -> response[None]:
		return UserManager.remove_product_from_cart(cookie, product_id, quantity)

	#2.9
	def purchase_cart(cookie : str) -> response[float]:
		return UserManager.purchase_cart(cookie)

	#2.9
	def purchase_completed(cookie : str) -> response[None]:
		return UserManager.purchase_completed(cookie)

	# Member
	# ===============================

	#3.2
	def create_store(cookie : str, name : str) -> response[None]:
		response = UserManager.create_store(cookie, name);
		if response.success:
			return StoresManager.create_store(response.data)
		return response

	#3.7
	def ger_purchase_history(cookie : str) -> response[list[PurchaseDetailsData]]:
		return UserManager.ger_purchase_history(cookie)

	# Owner and manager
	# =======================

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(cookie : str, store_id : str, name : str, price : float) -> response[None]:
		return UserManager.create_product(cookie, store_id, name, price)

	#4.1
	def add_products(cookie : str, store_id : str, product_id : str, quantity : int) -> response[None]:
		return UserManager.add_products(cookie, store_id, product_id, quantity)

	#4.1
	def remove_products(cookie : str, store_id : str, product_id : str, quantity : int) -> response[None]:
		return UserManager.remove_products(cookie, store_id, product_id, quantity)

	#4.1
	def set_product_price(cookie : str, store_id : str, product_id : str, new_price : float) -> response[None]:
		return UserManager.set_product_price(cookie, store_id, product_id, new_price)

	#4.3
	def appoint_owner(cookie : str, store_id : str, username : str) -> response[None]:
		return UserManager.appoint_owner(cookie, store_id, username)

	#4.5
	def appoint_manager(cookie : str, store_id : str, username : str) -> response[None]:
		return UserManager.appoint_manager(cookie, store_id, username)

	#4.6
	def add_manager_permission(cookie : str, store_id : str, username : str, permission_number : int) -> response[None]:
		return UserManager.add_manager_permission(cookie, store_id, username, permissions(permission_number))

	#4.6
	def remove_manager_permission(cookie : str, store_id : str, username : str, permission_number : int) -> response[None]:
		return UserManager.remove_manager_permission(cookie, store_id, username, permissions(permission_number))

	#4.4, 4.7
	def remove_appointment(cookie : str, store_id : str, username : str) -> response[None]:
		return UserManager.remove_appointment(cookie, store_id, username)

	#4.9
	def get_store_appointments(cookie : str, store_id : str) -> response[ResponsibilityData]:
		return UserManager.get_store_appointments(cookie, store_id)

	#4.11
	def get_store_purchases_history(cookie : str, store_id : str) -> response[list[PurchaseDetailsData]]:
		return UserManager.get_store_purchases_history(cookie, store_id)

	#System Manager
	#====================

	#6.4
	def get_user_purchase_history(cookie : str, username : str) -> response[list[PurchaseDetailsData]]:
		return UserManager.get_user_purchase_history(cookie, username)