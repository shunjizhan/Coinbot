import requests

from ..exchange import Exchange


class Dew(Exchange):
    def __init__(self):
        self.api = Cmk()
        super().__init__('dew')
        self.connect_success()

    def get_price(self, coin, base='BTC'):
        return self.api.get_price(coin, base)

    def get_full_balance(self, allow_zero=False):
        balances = self.get_all_coin_balance()
        coins = {
            'total': {'BTC': 0, 'USD': 0, 'num': 0},
            'USD': {'BTC': 0, 'USD': 0, 'num': 0}
        }
        for coinName, num in balances.items():
            if allow_zero or num > 0:
                BTC_value = self.get_price(coinName, base='BTC') * num
                USD_value = self.get_price(coinName, base='USD') * num

                # update info
                coins[coinName] = {
                    'num': num,
                    'BTC': BTC_value,
                    'USD': USD_value
                }
                coins['total']['BTC'] += BTC_value
                coins['total']['USD'] += USD_value
        return coins

    def get_all_coin_balance(self, allow_zero=False):
        return {'DEW': 2688}
