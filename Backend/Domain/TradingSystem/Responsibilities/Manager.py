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
	
	def __create_no_permission_response(self, permission : Permission) -> response:
		return response(msg=f"{self.user_state.username} does not have permission to {permission.name}") 

	#4.1
	# Creating a new product a the store and setting its quantity to 0
	def create_product(self, name : str, price : float) -> response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().create_product(name, price)

		return self.__create_no_permission_response(Permission.MANAGE_PRODUCTS)

	#4.1
	def add_products(self, product_id : str, quantity : int) -> response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().add_products(product_id, quantity)

		return self.__create_no_permission_response(Permission.MANAGE_PRODUCTS)

	#4.1
	def remove_products(self, product_id : str, quantity : int) -> response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().remove_products(product_id, quantity)

		return self.__create_no_permission_response(Permission.MANAGE_PRODUCTS)

	#4.1
	def set_product_price(self, product_id : str, new_price : float) -> response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().set_product_price(product_id, new_price)

		return self.__create_no_permission_response(Permission.MANAGE_PRODUCTS)

	#4.3
	def appoint_owner(self, user : User) -> response[None]:
		return response(msg=f"Managers can't appoint owners")


	#4.5
	def appoint_manager(self, user : User) -> response[None]:
		if(self.permissions[Permission.APPOINT_MANAGER]):
			return super().appoint_manager(user)

		return self.__create_no_permission_response(Permission.APPOINT_MANAGER)
		
	#4.6
	def add_manager_permission(self, user : User, permission) -> response[None]:
		if(self.permissions[Permission.APPOINT_MANAGER]):
			return super().add_manager_permission(user, permission)

		return self.__create_no_permission_response(Permission.APPOINT_MANAGER)
		
	#4.6
	def remove_manager_permission(self, user : User, permission) -> response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().remove_manager_permission(user, permission)

		return self.__create_no_permission_response(Permission.MANAGE_PRODUCTS)
		
	#4.4, 4.7
	def remove_appointment(self, user : User) -> response[None]:
		if(self.permissions[Permission.REMOVE_MANAGER]):
			return super().remove_appointment(user)

		return self.__create_no_permission_response(Permission.REMOVE_MANAGER)
		
	#4.9
	def get_store_appointments(self) -> response[Responsibility]:
		if(self.permissions[Permission.GET_APPOINTMENTS]):
			return super().get_store_appointments()

		return self.__create_no_permission_response(Permission.GET_APPOINTMENTS)

	#4.11
	def get_store_purchases_history(self) -> response[list[PurchaseDetails]]: #TODO import Purchase Details
		if(self.permissions[Permission.GET_HISTORY]):
			return super().get_store_purchases_history()

		return self.__create_no_permission_response(Permission.GET_HISTORY)

	def _add_permission(self, username : str, permission : Permission) -> bool:
		if self.user_state.username == username :
			self.permissions[permission] = True
			return True

		return super()._add_permission(username, permission)

	def _remove_permission(self, username : str, permission : Permission) -> bool:
		if self.user_state.username == username :
			self.permissions[permission] = False
			return True

		return super()._remove_permission(username, permission)