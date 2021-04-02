from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, ParsableList

class StoreStub():

	def __init__(self) -> None:
		self.product_added = False
		self.product_removed = False
		self.product_quantity_changed = False
		self.product_details_changed = False

	#4.1
	#Creating a new product a the store
	def add_product(self, name : str, price: float, quantity : int) -> Response[None]:
		self.product_added = True
		return Response(True)

	#4.1
	def remove_product(self, product_id : str) -> Response[None]:
		self.product_removed = True
		return Response(True)

	#4.1
	def change_product_quantity(self, product_id : str, quantity : int) -> Response[None]:
		self.product_quantity_changed = True
		return Response(True)

	#4.1
	def edit_product_details(self, product_id : str, new_name: str, new_price : float) -> Response[None]:
		self.product_details_changed = True
		return Response(True)
	
	def get_id(self):
		return 0

	def get_name(self):
		return "store"

	#4.9
	def get_responsibilities(self) -> Response[Responsibility]:
		return Response(True)

	#4.11
	def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
		return Response(True, ParsableList([]))
		
