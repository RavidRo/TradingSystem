from Backend.response import Response
from Backend.response import ParsableList
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product
class SearchEngine:

	#2.6
	# kwargs = You can search for a product by additional key words
	def search_products(product_name : str, category : str, min_price : float, max_price : float, *keywords) -> Response[ParsableList[product]]:
		# For now we don't have kewwords and categories fo the products
		all_products = StoresManager.get_products()

		def filter_predicate(product : product) -> bool:
			price = product.get_price()
			name = product.get_name()

			if min_price and min_price > price:
				return False
			if max_price and max_price < price:
				return False
			if product_name not in name:
				return False
				
			return True

		filtered_products = filter(filter_predicate, all_products)
		return Response(True, ParsableList(filtered_products))

	
		

