from .Responsibility import Permission, Responsibility
from .Manager import Manager
from .Owner import Owner
from ..User import User



class Founder(Responsibility):
	#4.1
	#Creating a new product a the store
	def add_product(self, product_id : str, name : str, price: float, quantity : int) -> response[None]:
		return self.store.add_product(self, product_id, name, price, quantity)

	#4.1
	def remove_product(self, product_id : str) -> response[None]:
		return self.store.remove_product(self, product_id)

	#4.1
	def change_product_quantity(self, product_id : str, quantity : int) -> response[None]:
		return self.store.change_product_quantity(self, product_id, quantity)

	#4.1
	def edit_product_details(self, product_id : str, new_name: str, new_price : float) -> response[None]:
		return self.store.edit_product_details(self, product_id, new_name, new_price)
	
	#4.3
	def appoint_owner(self, user : User) -> response[None]:
		if user.isAppointed(self.store.id):
			return respons(False, msg = f"{user.get_username()} is already appointed to {self.store.get_name()}")	
		
		# Success
		newResponsibility = Owner(user.state, self.store)
		self.appointed.append(newResponsibility)
		return response(True)			

	#4.5
	def appoint_manager(self, user : User) -> response[None]:
		if user.isAppointed(self.store.id):
			return respons(False, msg = f"{user.get_username()} is already appointed to {self.store.get_name()}")	

		# Success
		newResponsibility = Manager(user.state, self.store)
		self.appointed.append(newResponsibility)
		return response(True)	

	#4.6
	# recursively call children function until the child is found and the permission is added
	def add_manager_permission(self, username : str, permission : Permission) -> response[None]:
		if not self._add_permission(username, permission):
			return response(False, msg = f"{self.user_state.username} never appointed {username} as a manager")
		return response(True)

	#4.6
	def remove_manager_permission(self, username : str, permission : Permission) -> response[None]:
		if not self._remove_permission(username, permission):
			return response(False, msg = f"{self.user_state.username} never appointed {username} as a manager")
		return response(True)

	#4.4, 4.7
	def remove_appointment(self, username : str) -> response[None]:
		if not self._remove_appointment(username):
			return response(False, msg = f"{self.user_state.username} never appointed {username}")
		return response(True)

	#4.9
	def get_store_appointments(self) -> response[Responsibility]:
		return self.store.get_responsibilities()

	#4.11
	def get_store_purchases_history(self) -> response[list[PurchaseDetails]]: #TODO import Purchase Details
		return self.store.get_purchase_history()
		
