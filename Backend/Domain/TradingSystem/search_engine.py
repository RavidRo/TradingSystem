from typing import Union

from Backend.response import Response, ParsableTuple, PrimitiveParsable
from Backend.response import ParsableMap
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product


class SearchEngine:

    # 2.6
    # kwargs = You can search for a product by additional key words
    @staticmethod
    def search_products(
            search_phrase: str = None, min_price: float = 0,
            max_price: float = float("inf"), search_by: Union[str, list[str]] = None, keywords: list[str] = None
    ):
        if keywords is None:
            keywords = []
        if isinstance(search_by, str):
            search_by = [search_by]
        search_by_name = "name" in search_by
        search_by_category = "category" in search_by
        search_by_keywords = "keywords" in search_by
        if not (search_by_name or search_by_category or search_by_keywords):
            return Response(False, msg="You must search for at least one of the following: 'product', 'category', "
                                       "'keywords'")
        stores = StoresManager.get_stores_details().get_obj().values
        store_to_products = dict({store: store.get_products_to_quantities().values() for store in stores})

        def filter_predicate(product_to_quantity) -> bool:
            product = product_to_quantity[0]
            price = product.get_price()
            name = product.get_name()
            category = product.get_category()

            if min_price and min_price > price:
                return False
            if max_price and max_price < price:
                return False

            if search_by_keywords:
                fit = True
                for keyword in keywords:
                    if keyword not in product.get_keywords():
                        fit = False
                        break
                if fit:
                    return True

            if search_by_name and (name and search_phrase == name):
                return True
            if search_by_category and (category and search_phrase == category):
                return True

            return False

        for store in store_to_products:
            store_to_products[store] = ParsableTuple(tuple(map(lambda product_to_quantity: ParsableTuple((product_to_quantity[0], PrimitiveParsable(product_to_quantity[1]))), tuple(filter(filter_predicate, store_to_products[store])))))
        return Response(True, ParsableMap(store_to_products))
