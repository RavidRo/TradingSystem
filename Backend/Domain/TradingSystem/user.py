from Backend.response import Response
from .Responsibilities.Responsibility import permission
from Backend.Domain.TradingSystem.shopping_cart import shopping_cart
from Backend.Domain.TradingSystem.purchase_details import purchase_details
from Backend.Domain.TradingSystem.user_state import user_state, guest
from .Responsibilities.Responsibility import permission, responsibility

class user:
	def __init__(self):
		self.state : user_state = guest(self)

	#2.3
	def register(self, username : str, password : str) -> Response[None]:
		return self.state.register(username, password)

	#2.4
	def login(self, username : str, password : str) -> Response[None]:
		return self.state.register(username, password)

	#2.7
	def add_to_cart(self, product_id : str, quantity : int) -> Response[None]:
		return self.state.add_to_cart(product_id, quantity)

	#2.8
	def get_cart_details(self) -> Response[shopping_cart]:
		return self.state.get_cart_details()

	#2.8
	def remove_product_from_cart(self, product_id : str, quantity : int) -> Response[None]:
		return self.state.remove_product_from_cart(product_id, quantity)

	#2.9
	def purchase_cart(self) -> Response[float]:
		return self.state.purchase_cart()

	#2.9
	def purchase_completed(self) -> Response[None]:
		return self.state.purchase_completed()

	# Member
	# ===============================

	#3.2
	def create_store(self, name : str) -> Response[None]:
		return self.state.create_store(name)

	#3.7
	def ger_purchase_history(self) -> Response[list[purchase_details]]:
		return self.state.ger_purchase_history()

	# Owner and manager
	# =======================

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, store_id : str, name : str, price: float, quantity : int) -> Response[None]:
		return self.state.create_product(store_id, name, price, quantity)
	#4.1
	def remove_products(self, store_id : str, product_id : str) -> Response[None]:
		return self.state.remove_products(store_id, product_id)

	#4.1
	def change_product_quantity(self, store_id : str, product_id : str, quantity : int) -> Response[None]:
		return self.state.change_product_quantity(store_id, product_id, quantity)

	#4.1
	def edit_product_details(self, store_id : str, product_id : str, new_name: str, new_price : float) -> Response[None]:
		return self.state.edit_product_details(store_id, product_id, new_name, new_price)

	#4.3
	def appoint_owner(self, store_id : str, user : user) -> Response[None]:
		return self.state.appoint_owner(store_id, user)

	#4.5
	def appoint_manager(self, store_id : str, user : user) -> Response[None]:
		return self.state.appoint_manager(store_id, user)

	#4.6
	def add_manager_permission(self, store_id : str, username : str, permission : permission) -> Response[None]:
		return self.state.add_manager_permission(store_id, username, permission)

	#4.6
	def remove_manager_permission(self, store_id : str, username : str, permission : permission) -> Response[None]:
		return self.state.remove_manager_permission(store_id, username, permission)

	#4.4, 4.7
	def remove_appointment(self, store_id : str, username : str) -> Response[None]:
		return self.state.remove_appointment(store_id, username)

	#4.9
	def get_store_appointments(self, store_id : str) -> Response[responsibility]:
		return self.state.get_store_appointments(store_id)

	#4.11
	def get_store_purchases_history(self, store_id : str) -> Response[list[purchase_details]]:
		return self.state.get_store_purchases_history(store_id)

	#System Manager
	#====================

	#6.4
	def get_user_purchase_history(self, username : str) -> Response[list[purchase_details]]:
		return self.state.get_user_purchase_history(username)

	
	# Inter component functions
	#====================

	def isAppointed(self, store_id : str) -> bool:
		return self.state.isAppointed(store_id)
	
	def get_username(self) -> str:
		return self.state.get_username()

	def change_state(self, new_state : user_state) -> None:
		self.state = new_state
	
