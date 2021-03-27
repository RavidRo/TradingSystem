from .responsibility import permission, responsibility
from .owner import owner
from Backend.Domain.TradingSystem.user_states import member
from Backend.Domain.TradingSystem.user import user
from Backend.Domain.TradingSystem.purchase_details import purchase_details
from Backend.Domain.TradingSystem.store import store
from Backend.response import Response



class Manager(owner):

	def __init__(self, user_state: member, store: store) -> None:
		self.permissions = {
			permission.MANAGE_PRODUCTS: False,
			permission.GET_APPOINTMENTS: True,
			permission.APPOINT_MANAGER: False,
			permission.REMOVE_MANAGER: False,
			permission.GET_HISTORY : False,
		}
		super().__init__(user_state, store)
	
	def __create_no_permission_Response(self, permission : permission) -> Response:
		return Response(False, msg=f"{self.user_state.username} does not have permission to {permission.name}") 

	#4.1
	#Creating a new product a the store
	def add_product(self, product_id : str, name : str, price: float, quantity : int) -> Response[None]:
		if(self.permissions[permission.MANAGE_PRODUCTS]):
			return super().add_product(product_id, name, price, quantity)

		return self.__create_no_permission_Response(permission.MANAGE_PRODUCTS)

	#4.1
	def remove_product(self, product_id : str) -> Response[None]:
		if(self.permissions[permission.MANAGE_PRODUCTS]):
			return super().remove_product(product_id, product_id)

		return self.__create_no_permission_Response(permission.MANAGE_PRODUCTS)

	#4.1
	def change_product_quantity(self, product_id : str, quantity : int) -> Response[None]:
		if(self.permissions[permission.MANAGE_PRODUCTS]):
			return super().change_product_quantity(product_id, quantity)

		return self.__create_no_permission_Response(permission.MANAGE_PRODUCTS)

	#4.1
	def edit_product_details(self, product_id : str, new_name: str, new_price : float) -> Response[None]:
		if(self.permissions[permission.MANAGE_PRODUCTS]):
			return super().edit_product_details(product_id, new_name, new_price)

		return self.__create_no_permission_Response(permission.MANAGE_PRODUCTS)

	#4.3
	def appoint_owner(self, user : user) -> Response[None]:
		return Response(msg=f"Managers can't appoint owners")


	#4.5
	def appoint_manager(self, user : user) -> Response[None]:
		if(self.permissions[permission.APPOINT_MANAGER]):
			return super().appoint_manager(user)

		return self.__create_no_permission_Response(permission.APPOINT_MANAGER)
		
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
		if(self.permissions[permission.REMOVE_MANAGER]):
			return super().remove_appointment(username)

		return self.__create_no_permission_Response(permission.REMOVE_MANAGER)
		
	#4.9
	def get_store_appointments(self) -> Response[responsibility]:
		if(self.permissions[permission.GET_APPOINTMENTS]):
			return super().get_store_appointments()

		return self.__create_no_permission_Response(permission.GET_APPOINTMENTS)

	#4.11
	def get_store_purchases_history(self) -> Response[list[purchase_details]]: #TODO import Purchase Details
		if(self.permissions[permission.GET_HISTORY]):
			return super().get_store_purchases_history()

		return self.__create_no_permission_Response(permission.GET_HISTORY)

	def _add_permission(self, username : str, permission : permission) -> bool:
		if self.user_state.username == username :
			self.permissions[permission] = True
			return True

		return super()._add_permission(username, permission)

	def _remove_permission(self, username : str, permission : permission) -> bool:
		if self.user_state.username == username :
			self.permissions[permission] = False
			return True

		return super()._remove_permission(username, permission)