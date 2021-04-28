from Backend.response import Response, ParsableList
from Backend.response import ParsableMap
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product


class SearchEngine:

    # 2.6
    # kwargs = You can search for a product by additional key words
    @staticmethod
    def search_products(
        product_name: str = None, product_category: str = None, min_price: float = 0, max_price: float = float("inf"), search_by: str = None, *keywords
    ):
        # For now we don't have keywords and categories fo the products
        valid_search_by_values = ("name", "category")
        if search_by not in valid_search_by_values:
            return Response(False, msg="search by is not valid")
        stores = StoresManager.get_stores_details().get_obj().values
        store_to_products = {store: store.get_products().get_obj().values for store in stores}

        def filter_predicate(product) -> bool:
            price = product.get_price()
            name = product.get_name()
            category = product.get_category()

            if min_price and min_price > price:
                return False
            if max_price and max_price < price:
                return False

            if name and search_by == "name":
                return product_name == name
            elif category and search_by == "category":
                return product_category == category
            else:
                return False

        for store in store_to_products:
            store_to_products[store] = ParsableList(list(filter(filter_predicate, store_to_products[store])))
        return Response(True, ParsableMap(store_to_products))
