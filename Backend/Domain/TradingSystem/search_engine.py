from Backend.response import Response
from Backend.response import ParsableList
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product


class SearchEngine:

    # 2.6
    # kwargs = You can search for a product by additional key words
    @staticmethod
    def search_products(
        product_name: str, product_category: str, min_price: float, max_price: float, search_by, *keywords
    ) -> Response[ParsableList[product]]:
        # For now we don't have keywords and categories fo the products
        valid_search_by_values = ("name", "category")
        if search_by not in valid_search_by_values:
            return Response(False, msg="search by is not valid")
        response = StoresManager.get_products()
        if not response.succeeded():
            return response

        all_products = response.get_obj()

        def filter_predicate(product: product) -> bool:
            price = product.get_price()
            name = product.get_name()
            category = product.get_category()

            if min_price and min_price > price:
                return False
            if max_price and max_price < price:
                return False

            if search_by == "name":
                return product_name == name
            elif search_by == "category":
                return product_category == category
            else:
                return False

        filtered_products = list(filter(filter_predicate, all_products.values))
        return Response(True, ParsableList(filtered_products))
