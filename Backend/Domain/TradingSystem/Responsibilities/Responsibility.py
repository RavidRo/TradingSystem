from ..User import User

import enum
class Permission(enum.Enum):
	MANAGE_PRODUCTS = 1
	GET_APPOINTMENTS = 2
	APPOINT_MANAGER = 3
	REMOVE_MANAGER = 4
	GET_HISTORY = 5

class Responsibility:
	ERROR_MESSAGE = "Responsibility is an interface, function not implemented"

	# TODO import Store and Member
	def __init__(self, user_state : Member, store : Store) -> None:
		self.user_state = user_state;
		user_state.add_responsibility(self)
		self.store = store;
		self.appointed : list[Responsibility] = [];

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, name : str, price : float):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.1
	def add_products(self, product_id : str, quantity : int):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.1
	def remove_products(self, product_id : str, quantity : int):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.1
	def set_product_price(self, product_id : str, new_price : float):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.3
	def appoint_owner(self, user : User):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.5
	def appoint_manager(self, user : User):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.6
	# Returns true if and only if self.user appointed user and user is a manager
	def add_manager_permission(self, user : User, permission : Permission) -> bool:
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.6
	def remove_manager_permission(self, user : User, permission : Permission):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.4, 4.7
	def remove_appointment(self, user : User):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.9
	def get_store_appointments(self):
		raise Exception(Responsibility.ERROR_MESSAGE)

	#4.11
	def get_store_purchases_history(self) -> list[PurchaseDetails]: #TODO import Purchase Details
		raise Exception(Responsibility.ERROR_MESSAGE)

	
	def _add_permission(self, username : str, permission : Permission) -> bool:
		if not self.appointed:
			# if self.user never appointed anyone
			return False
		# returns true if any one of the children returns true
		return any(map(self.appointed.appointed, lambda worker : worker._add_permission(username, permission)))
	
	def _remove_permission(self, username : str, permission : Permission) -> bool:
		if not self.appointed:
			# if self.user never appointed anyone
			return False
		# returns true if any one of the children returns true
		return any(map(self.appointed.appointed, lambda worker : worker._remove_permission(username, permission)))
	
	def _remove_appointment(self, user : User):
		if not self.appointed:
			# if self.user never appointed anyone
			return False
			
		for appointment in self.appointed:
			appointment.user_state.username == user.get_username()
			self.appointed.remove(appointment)
			return True

		return any(map(self.appointed.appointed, lambda worker : worker._remove_appointment(user)))
	
			