from .responsibility import Permission, Responsibility
from .owner import Owner
from Backend.Domain.TradingSystem.user_states import Member
from Backend.Domain.TradingSystem.user import User
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response, ParsableList



class Manager(Owner):

	def __init__(self, user_state: Member, store: Store) -> None:
		self.permissions = {
			Permission.MANAGE_PRODUCTS: False,
			Permission.GET_APPOINTMENTS: True,
			Permission.APPOINT_MANAGER: False,
			Permission.REMOVE_MANAGER: False,
			Permission.GET_HISTORY : False,
		}
		super().__init__(user_state, store)
	
	def __create_no_permission_Response(self, permission : Permission) -> Response:
		return Response(False, msg=f"{self.user_state.get_username()} does not have permission to {permission.name}") 

	#4.1
	#Creating a new product a the store
	def add_product(self, name : str, price: float, quantity : int) -> Response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().add_product(name, price, quantity)

		return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

	#4.1
	def remove_product(self, product_id : str) -> Response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().remove_product(product_id, product_id)

		return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

	#4.1
	def change_product_quantity(self, product_id : str, quantity : int) -> Response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().change_product_quantity(product_id, quantity)

		return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

	#4.1
	def edit_product_details(self, product_id : str, new_name: str, new_price : float) -> Response[None]:
		if(self.permissions[Permission.MANAGE_PRODUCTS]):
			return super().edit_product_details(product_id, new_name, new_price)

		return self.__create_no_permission_Response(Permission.MANAGE_PRODUCTS)

	#4.3
	def appoint_owner(self, user : User) -> Response[None]:
		return Response(msg=f"Managers can't appoint owners")


	#4.5
	def appoint_manager(self, user : User) -> Response[None]:
		if(self.permissions[Permission.APPOINT_MANAGER]):
			return super().appoint_manager(user)

		return self.__create_no_permission_Response(Permission.APPOINT_MANAGER)
		
	#4.6
	def add_manager_permission(self, username : str, permission) -> Response[None]:
		if(self.permissions[permission.APPOINT_MANAGER]):
			return super().add_manager_permission(username, permission)

		return self.__create_no_permission_Response(permission.APPOINT_MANAGER)
		
	#4.6
	def remove_manager_permission(self, username: str, permission) -> Response[None]:
		if(self.permissions[permission.MANAGE_PRODUCTS]):
			return super().remove_manager_permission(username, permission)

		return self.__create_no_permission_Response(permission.MANAGE_PRODUCTS)
		
	#4.4, 4.7
	def remove_appointment(self, username : str) -> Response[None]:
		if(self.permissions[Permission.REMOVE_MANAGER]):
			return super().remove_appointment(username)

		return self.__create_no_permission_Response(Permission.REMOVE_MANAGER)
		
	#4.9
	def get_store_appointments(self) -> Response[Responsibility]:
		if(self.permissions[Permission.GET_APPOINTMENTS]):
			return super().get_store_appointments()

		return self.__create_no_permission_Response(Permission.GET_APPOINTMENTS)

	#4.11
	def get_store_purchases_history(self) -> Response[ParsableList[PurchaseDetails]]: 
		if(self.permissions[Permission.GET_HISTORY]):
			return super().get_store_purchases_history()

		return self.__create_no_permission_Response(Permission.GET_HISTORY)

	def _add_permission(self, username : str, permission : Permission) -> bool:
		if self.user_state.get_username() == username :
			self.permissions[permission] = True
			return True

		return super()._add_permission(username, permission)

	def _remove_permission(self, username : str, permission : Permission) -> bool:
		if self.user_state.get_username() == username :
			self.permissions[permission] = False
			return True

		return super()._remove_permission(username, permission)