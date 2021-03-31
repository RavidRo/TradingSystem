from .responsibility import permission, responsibility
from .manager import manager
from .owner import owner
from Backend.Domain.TradingSystem.user import user
from Backend.Domain.TradingSystem.purchase_details import purchase_details
from Backend.response import Response, ParsableList

class founder(responsibility):
	#4.1
	#Creating a new product a the store
	def add_product(self, name : str, price: float, quantity : int) -> Response[None]:
		return self.store.add_product(self, name, price, quantity)

	#4.1
	def remove_product(self, product_id : str) -> Response[None]:
		return self.store.remove_product(self, product_id)

	#4.1
	def change_product_quantity(self, product_id : str, quantity : int) -> Response[None]:
		return self.store.change_product_quantity(self, product_id, quantity)

	#4.1
	def edit_product_details(self, product_id : str, new_name: str, new_price : float) -> Response[None]:
		return self.store.edit_product_details(self, product_id, new_name, new_price)
	
	#4.3
	def appoint_owner(self, user : user) -> Response[None]:
		if user.isAppointed(self.store.get_id()):
			return Response(False, msg = f"{user.get_username()} is already appointed to {self.store.get_name()}")	
		
		# Success
		newResponsibility = owner(user.state, self.store)
		self.appointed.append(newResponsibility)
		return Response(True)			

	#4.5
	def appoint_manager(self, user : user) -> Response[None]:
		if user.isAppointed(self.store.get_id()):
			return Response(False, msg = f"{user.get_username()} is already appointed to {self.store.get_name()}")	

		# Success
		newResponsibility = manager(user.state, self.store)
		self.appointed.append(newResponsibility)
		return Response(True)	

	#4.6
	# recursively call children function until the child is found and the permission is added
	def add_manager_permission(self, username : str, permission : permission) -> Response[None]:
		if not self._add_permission(username, permission):
			return Response(False, msg = f"{self.user_state.get_username()} never appointed {username} as a manager")
		return Response(True)

	#4.6
	def remove_manager_permission(self, username : str, permission : permission) -> Response[None]:
		if not self._remove_permission(username, permission):
			return Response(False, msg = f"{self.user_state.get_username()} never appointed {username} as a manager")
		return Response(True)

	#4.4, 4.7
	def remove_appointment(self, username : str) -> Response[None]:
		if not self._remove_appointment(username):
			return Response(False, msg = f"{self.user_state.get_username()} never appointed {username}")
		return Response(True)

	#4.9
	def get_store_appointments(self) -> Response[responsibility]:
		return self.store.get_responsibilities()

	#4.11
	def get_store_purchases_history(self) -> Response[ParsableList[purchase_details]]: #TODO import Purchase Details
		return self.store.get_purchase_history()
		
