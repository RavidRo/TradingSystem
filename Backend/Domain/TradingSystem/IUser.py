from __future__ import annotations
from abc import ABC, abstractmethod

from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.user_state import UserState

class IUser(metaclass=ABC):
	from .Responsibilities.responsibility import Permission, Responsibility

	#2.3
	@abstractmethod
	def register(self, username : str, password : str) -> Response[None]:
		raise NotImplementedError

	#2.4
	@abstractmethod
	def login(self, username : str, password : str) -> Response[None]:
		raise NotImplementedError

	#2.7
	@abstractmethod
	def add_to_cart(self, stor_id : str, product_id : str, quantity : int) -> Response[None]:
		raise NotImplementedError

	#2.8
	@abstractmethod
	def get_cart_details(self) -> Response[ShoppingCart]:
		raise NotImplementedError

	#2.8
	@abstractmethod
	def remove_product_from_cart(self, store_id : str, product_id : str) -> Response[None]:
		raise NotImplementedError
	
	#2.8
	@abstractmethod
	def change_product_quantity(self, store_id, product_id, new_amount) -> Response[None]:
		raise NotImplementedError

	#2.9
	@abstractmethod
	def purchase_cart(self) -> Response[PrimitiveParsable[float]]:
		raise NotImplementedError

	#2.9
	@abstractmethod
	def purchase_completed(self) -> Response[None]:
		raise NotImplementedError

	# Member
	# ===============================

	#3.2
	@abstractmethod
	def create_store(self, name : str) -> Response[None]:
		raise NotImplementedError

	#3.7
	@abstractmethod
	def ger_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
		raise NotImplementedError

	# Owner and manager
	# =======================

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	@abstractmethod
	def create_product(self, store_id : str, name : str, price: float, quantity : int) -> Response[None]:
		raise NotImplementedError

	#4.1
	@abstractmethod
	def remove_products(self, store_id : str, product_id : str) -> Response[None]:
		raise NotImplementedError

	#4.1
	@abstractmethod
	def change_product_quantity(self, store_id : str, product_id : str, new_quantity : int) -> Response[None]:
		raise NotImplementedError

	#4.1
	@abstractmethod
	def edit_product_details(self, store_id : str, product_id : str, new_name: str, new_price : float) -> Response[None]:
		raise NotImplementedError

	#4.3
	@abstractmethod
	def appoint_owner(self, store_id : str, user : IUser) -> Response[None]:
		raise NotImplementedError

	#4.5
	@abstractmethod
	def appoint_manager(self, store_id : str, user : IUser) -> Response[None]:
		raise NotImplementedError

	#4.6
	@abstractmethod
	def add_manager_permission(self, store_id : str, username : str, permission : Permission) -> Response[None]:
		raise NotImplementedError

	#4.6
	@abstractmethod
	def remove_manager_permission(self, store_id : str, username : str, permission : Permission) -> Response[None]:
		raise NotImplementedError

	#4.4, 4.7
	@abstractmethod
	def remove_appointment(self, store_id : str, username : str) -> Response[None]:
		raise NotImplementedError

	#4.9
	@abstractmethod
	def get_store_appointments(self, store_id : str) -> Response[Responsibility]:
		raise NotImplementedError

	#4.11
	@abstractmethod
	def get_store_purchases_history(self, store_id : str) -> Response[ParsableList[PurchaseDetails]]:
		raise NotImplementedError

	#System Manager
	#====================

	#6.4
	@abstractmethod
	def get_any_user_purchase_history(self, username : str) -> Response[ParsableList[PurchaseDetails]]:
		raise NotImplementedError

	#6.4
	@abstractmethod
	def get_any_store_purchase_history(self, store_id : str) -> Response[ParsableList[PurchaseDetails]]:
		raise NotImplementedError

	
	# Inter component functions
	#====================

	@abstractmethod
	def is_appointed(self, store_id : str) -> bool:
		raise NotImplementedError
	
	@abstractmethod
	def get_username(self) -> str:
		raise NotImplementedError

	@abstractmethod
	def change_state(self, new_state : UserState) -> None:
		raise NotImplementedError
	
