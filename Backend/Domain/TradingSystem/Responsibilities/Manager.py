from .Responsibility import Permission, Responsibility
from .Owner import Owner
from ..User import User



class Manager(Owner):

	def __init__(self, user_state: UserState, store: Store) -> None:
		self.permissions = {
			Permission.MANAGE_PRODUCTS: False,
			Permission.GET_APPOINTMENTS: False,
			Permission.APPOINT_MANAGER: False,
			Permission.REMOVE_MANAGER: False,
			Permission.GET_HISTORY : False,
		}
		super().__init__(user_state, store)
	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, name : str, price : float):
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().create_product(name, price)

		raise Exception("No permission to manage products")

	#4.1
	def add_products(self, product_id : str, quantity : int):
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().add_products(product_id, quantity)

		raise Exception("No permission to manage products")

	#4.1
	def remove_products(self, product_id : str, quantity : int):
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().remove_products(product_id, quantity)

		raise Exception("No permission to manage products")

	#4.1
	def set_product_price(self, product_id : str, new_price : float):
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().set_product_price(product_id, new_price)

		raise Exception("No permission to manage products")

	#4.3
	def appoint_owner(self, user : User):
		raise Exception("Managers can't appoint owners")

	#4.5
	def appoint_manager(self, user : User):
		if(self.permissions[Permission.APPOINT_MANAGER]):
			return super().appoint_manager(user)

		raise Exception("No permission to appoint managers")
		
	#4.6
	def add_manager_permission(self, user : User, permission):
		if(self.permissions[Permission.APPOINT_MANAGER]):
			return super().add_manager_permission(user, permission)

		raise Exception("No permission to manage managers")
		
	#4.6
	def remove_manager_permission(self, user : User, permission):
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().remove_manager_permission(user, permission)

		raise Exception("No permission to manage managers")
		
	#4.4, 4.7
	def remove_appointment(self, user : User):
		if(self.permissions[Permission.REMOVE_MANAGER]):
			return super().remove_appointment(user)

		raise Exception("No permission to remove managers")
		
	#4.9
	def get_store_appointments(self) -> Responsibility:
		if(self.permissions[Permission.GET_APPOINTMENTS]):
			return super().get_store_appointments()

		raise Exception("No permission to view appointments")
		
	#4.11
	def get_store_purchases_history(self) -> list[PurchaseDetails]: #TODO import Purchase Details
		if(self.permissions[Permission.GET_HISTORY]):
			return super().get_store_purchases_history()

		raise Exception("No permission to view purchase history")
		

	def _add_permission(self, username : str, permission : Permission):
		if self.user_state.username == username :
			self.permissions[permission] = True
			return True

		return super()._add_permission(username, permission)

	def _remove_permission(self, username : str, permission : Permission):
		if self.user_state.username == username :
			self.permissions[permission] = False
			return True

		return super()._remove_permission(username, permission)