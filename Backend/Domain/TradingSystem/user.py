from __future__ import annotations

from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.user_state import UserState, Guest
from .Responsibilities.Responsibility import Permission, Responsibility

class User:
	def __init__(self):
		self.state : UserState = Guest(self)

	#2.3
	def register(self, username : str, password : str) -> Response[None]:
		return self.state.register(username, password)

	#2.4
	def login(self, username : str, password : str) -> Response[None]:
		return self.state.login(username, password)

	#2.7
	def add_to_cart(self, stor_id : str, product_id : str, quantity : int) -> Response[None]:
		return self.state.save_product_in_cart(stor_id, product_id, quantity)

	#2.8
	def get_cart_details(self) -> Response[ShoppingCart]:
		return self.state.show_cart()

	#2.8
	def remove_product_from_cart(self, store_id : str, product_id : str) -> Response[None]:
		return self.state.delete_from_cart(store_id, product_id)
	
	#2.8
	def change_product_quantity(self, store_id, product_id, new_amount) -> Response[None]:
		return self.state.change_product_quantity(store_id, product_id, new_amount)

	#2.9
	def purchase_cart(self) -> Response[PrimitiveParsable[float]]:
		return self.state.buy_cart(self)

	#2.9
	def purchase_completed(self) -> Response[None]:
		return self.state.delete_products_after_purchase()

	# Member
	# ===============================

	#3.2
	def create_store(self, name : str) -> Response[None]:
		return self.state.open_store(name)

	#3.7
	def ger_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
		return self.state.ger_purchase_history()

	# Owner and manager
	# =======================

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, store_id : str, name : str, price: float, quantity : int) -> Response[None]:
		return self.state.add_new_product(store_id, name, price, quantity)
	#4.1
	def remove_products(self, store_id : str, product_id : str) -> Response[None]:
		return self.state.remove_product(store_id, product_id)

	#4.1
	def change_product_quantity(self, store_id : str, product_id : str, new_quantity : int) -> Response[None]:
		return self.state.change_product_quantity_in_store(store_id, product_id, new_quantity)

	#4.1
	def edit_product_details(self, store_id : str, product_id : str, new_name: str, new_price : float) -> Response[None]:
		return self.state.edit_product_details(store_id, product_id, new_name, new_price)

	#4.3
	def appoint_owner(self, store_id : str, user : User) -> Response[None]:
		return self.state.appoint_new_store_owner(store_id, user)

	#4.5
	def appoint_manager(self, store_id : str, user : User) -> Response[None]:
		return self.state.appoint_new_store_manager(store_id, user)

	#4.6
	def add_manager_permission(self, store_id : str, username : str, permission : Permission) -> Response[None]:
		return self.state.add_manager_permission(store_id, username, permission)

	#4.6
	def remove_manager_permission(self, store_id : str, username : str, permission : Permission) -> Response[None]:
		return self.state.remove_manager_permission(store_id, username, permission)

	#4.4, 4.7
	def remove_appointment(self, store_id : str, username : str) -> Response[None]:
		return self.state.dismiss_manager(store_id, username)

	#4.9
	def get_store_appointments(self, store_id : str) -> Response[Responsibility]:
		return self.state.get_store_personnel_info(store_id)

	#4.11
	def get_store_purchases_history(self, store_id : str) -> Response[ParsableList[PurchaseDetails]]:
		return self.state.get_store_purchase_history(store_id)

	#System Manager
	#====================

	#6.4
	def get_any_user_purchase_history(self, username : str) -> Response[ParsableList[PurchaseDetails]]:
		return self.state.get_user_purchase_history(username)

	#6.4
	def get_any_store_purchase_history(self, store_id : str) -> Response[ParsableList[PurchaseDetails]]:
		return self.state.get_any_store_purchase_history(store_id)

	
	# Inter component functions
	#====================

	def is_appointed(self, store_id : str) -> bool:
		return self.state.is_appointed(store_id)
	
	def get_username(self) -> str:
		return self.state.get_username()

	def change_state(self, new_state : UserState) -> None:
		self.state = new_state
	
