from typing import Union

from Backend.response import Response, ParsableTuple, PrimitiveParsable
from Backend.response import ParsableMap
from Backend.Domain.TradingSystem.stores_manager import StoresManager
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product
from Backend.response import ParsableList


class SearchEngine:

    # 2.6
    # kwargs = You can search for a product by additional key words
    @staticmethod
    def search_products(
            product_name: str = None, product_category: str = None, min_price: float = 0,
            max_price: float = float("inf"), keywords: list[str] = None
    ):
        # if (not product_name) and (not product_category) and (not keywords):
        #     return Response(False, msg="You must search for at least one of the following: 'product', 'category', "
        #                                "'keywords'")
        stores = StoresManager.get_stores_details().get_obj().values
        store_to_products = {PrimitiveParsable(store.get_id()): store.get_products_to_quantities().values() for store in stores}
        # return Response[ParsableList](True, ParsableList(store_to_products), msg="stores to products quantities")

        def filter_predicate(product_to_quantity) -> bool:
            product = product_to_quantity[0]
            price = product.get_price()
            name = product.get_name()
            category = product.get_category()

            if min_price and min_price > price:
                return False
            if max_price and max_price < price:
                return False

            if keywords:
                fit = True
                for keyword in keywords:
                    if keyword not in product.get_keywords():
                        return False

            if product_name and not product_name == name:
                return False
            if product_category and not product_category == category:
                return False

            return True

        for store in store_to_products:
            store_to_products[store] = ParsableTuple(tuple(map(lambda product_to_quantity: ParsableTuple((product_to_quantity[0], PrimitiveParsable(product_to_quantity[1]))), tuple(filter(filter_predicate, store_to_products[store])))))
        return Response(True, ParsableMap(store_to_products))
