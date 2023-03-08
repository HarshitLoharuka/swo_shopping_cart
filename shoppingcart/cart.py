import typing
from collections import OrderedDict

from abstract_shopping_cart import ShoppingCart as AbstractShoppingCart
from price_list_sources import *


class ShoppingCart(AbstractShoppingCart):

    def __init__(self, price_list_source=DefaultPriceList):
        self._items = OrderedDict()
        self._price_list = self._get_price_list(price_list_source)

    def _get_price_list(self, price_list_source):
        return price_list_source.get_price_list()


    def add_item(self, product_code: str, quantity: int):
        try:
            self._items[product_code] += quantity
        except KeyError:
            self._items[product_code] = quantity


    def print_receipt(self) -> typing.List[str]:
        lines = []
        item_totals = {}

        for item, quantity in self._items.items():
            item_totals[item] = self._get_product_price(item) * quantity

            price_string = self._get_price_string(item, item_totals[item])
            lines.append(f"{item} - {quantity} - {price_string}")

        lines.append(f"Total - {sum(item_totals.values())}")
        return lines

    def _get_product_price(self, product_code: str) -> float:
        try:
            return self._price_list['product_code']['price']
        except KeyError:
            raise Exception(f"Could not find item {product_code} in price list")

    def _get_product_price_currency(self, product_code: str):
        try:
            return self._price_list['product_code']['currency']
        except KeyError:
            raise Exception(f"Could not find item {product_code} in price list")

    def _get_price_string(self, item, total_price_for_item):
        formatted_price_string = f"{total_price_for_item:.2f}"
        return f"{self._get_product_price_currency(item)}{formatted_price_string}"