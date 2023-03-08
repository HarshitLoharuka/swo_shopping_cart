import json
import abc



class AbstractPriceList(abc.ABC):

    MANDATORY_KEYS = ('price', 'currency',)

    @abc.abstractmethod
    def get_price_list(self):
        pass

class DefaultPriceList(AbstractPriceList):

    DEFAULT_PRICE_LIST = {
        'apple': {'price': 1.0, 'currency': '€'},
        'banana': {'price': 1.1, 'currency': '€'},
        'kiwi': {'price': 3.0, 'currency': '€'}
    }

    def get_price_list(self):
        return self.DEFAULT_PRICE_LIST

class JsonPriceList(AbstractPriceList):

    def __init__(self, filepath):
        self._filepath = filepath

    def get_price_list(self):
        with open(self._filepath, 'r') as f:
            price_list = json.load(f)

        self.validate_price_list(price_list)

        return price_list

    def validate_price_list(self, price_list):
        for product_code, price_details in price_list.items():

            for key in self.MANDATORY_KEYS:
                if key not in price_details:
                    raise Exception(f"Invalid price list. Key not present: {key}")
