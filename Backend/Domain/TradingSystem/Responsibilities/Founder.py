from .Responsibility import Permission, Responsibility
from .Manager import Manager
from .Owner import Owner
from ..User import User



class Founder(Responsibility):
	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, name : str, price : float):
		return self.store.create_product(name, price)

	#4.1
	def add_products(self, product_id : str, quantity : int):
		return self.store.add_products(product_id, quantity)

	#4.1
	def remove_products(self, product_id : str, quantity : int):
		return self.store.remove_products(product_id, quantity)

	#4.1
	def set_product_price(self, product_id : str, new_price : float):
		return self.store.set_product_price(self, product_id, new_price)

	#4.3
	def appoint_owner(self, user : User):
		if(not user.isAppointed(self.store.id)):
			newResponsibility = Owner(user.state, self.store)
			self.appointed.append(newResponsibility)
			# TODO: Return a success message here
		else:
			# TODO: Return an error message here
			pass

	#4.5
	def appoint_manager(self, user : User):
		if(not user.isAppointed(self.store.id)):
			newResponsibility = Manager(user.state, self.store)
			self.appointed.append(newResponsibility)
			# TODO: Return a success message here
		else:
			# TODO: Return an error message here
			pass

	#4.6
	# recursively call children function until the child is found and the permission is added
	def add_manager_permission(self, user : User, permission : Permission) -> bool:
		return self._add_permission(user.get_user_name(), permission)

	#4.6
	def remove_manager_permission(self,  user : User, permission : Permission) -> bool:
		return self._remove_permission(user.get_user_name(), permission)

	#4.4, 4.7
	def remove_appointment(self, user : User) -> bool:
		return self._remove_appointment(user)

	#4.9
	def get_store_appointments(self) -> Responsibility:
		return self.store.responsibilities

	#4.11
	def get_store_purchases_history(self) -> List[PurchaseDetails]: #TODO import Purchase Details
		self.store.purchase_history
		
