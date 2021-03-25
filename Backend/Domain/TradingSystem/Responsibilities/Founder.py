from .Responsibility import Permission, Responsibility
from .Manager import Manager
from .Owner import Owner
from ..User import User



class Founder(Responsibility):
	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, name : str, price : float) -> response[None]:
		return self.store.create_product(name, price)

	#4.1
	def add_products(self, product_id : str, quantity : int) -> response[None]:
		return self.store.add_products(product_id, quantity)

	#4.1
	def remove_products(self, product_id : str, quantity : int) -> response[None]:
		return self.store.remove_products(product_id, quantity)

	#4.1
	def set_product_price(self, product_id : str, new_price : float) -> response[None]:
		return self.store.set_product_price(self, product_id, new_price)
	
	#4.3
	def appoint_owner(self, user : User) -> response[None]:
		if user.isAppointed(self.store.id):
			return respons(msg = f"{user.get_username()} is already appointed to {self.store.get_name()}")	
		
		# Success
		newResponsibility = Owner(user.state, self.store)
		self.appointed.append(newResponsibility)
		return response()			

	#4.5
	def appoint_manager(self, user : User) -> response[None]:
		if user.isAppointed(self.store.id):
			return respons(msg = f"{user.get_username()} is already appointed to {self.store.get_name()}")	

		# Success
		newResponsibility = Manager(user.state, self.store)
		self.appointed.append(newResponsibility)
		return response()	

	#4.6
	# recursively call children function until the child is found and the permission is added
	def add_manager_permission(self, user : User, permission : Permission) -> response[None]:
		if not self._add_permission(user.get_user_name(), permission):
			return response(msg = f"{self.user_state.username} never appointed {user.get_username()} as a manager")
		return response()

	#4.6
	def remove_manager_permission(self,  user : User, permission : Permission) -> response[None]:
		if not self._remove_permission(user.get_user_name(), permission):
			return response(msg = f"{self.user_state.username} never appointed {user.get_username()} as a manager")
		return response()

	#4.4, 4.7
	def remove_appointment(self, user : User) -> response[None]:
		if not self._remove_appointment(user):
			return response(msg = f"{self.user_state.username} never appointed {user.get_username()}")
		return response()

	#4.9
	def get_store_appointments(self) -> response[Responsibility]:
		return self.store.responsibilities

	#4.11
	def get_store_purchases_history(self) -> response[list[PurchaseDetails]]: #TODO import Purchase Details
		return self.store.purchase_history
		
