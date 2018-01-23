import requests

from ..exchange import Exchange


class Dew(Exchange):
    def __init__(self):
        super().__init__('dew')
        self.api = Cmk()
        self.connect_success()

    def get_price(self, coin, base='BTC'):
        return self.api.get_price(coin, base)

    def get_full_balance(self):
        balances = {
            'DEW': 5505,
        }

        coins = {
            'total': {'BTC': 0, 'USD': 0, 'num': 0},
            'USD': {'BTC': 0, 'USD': 0, 'num': 0}
        }
        for coinName, num in balances.items():
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


# ------------------------------------------------------------------ #
# --------------------------- API Wrapper -------------------------- #
# ------------------------------------------------------------------ #
class Cmk:
    def __init__(self):
        self.base_url = 'https://api.coinmarketcap.com/v1/'

    def get_price(self, coin, base):
        if base not in {'BTC', 'USD'}:
            return 0
        ticker_url = self.base_url + 'ticker/' + coin
        res = requests.get(ticker_url).json()[0]
        if base == 'BTC':
            return float(res['price_btc'])
        else:
            return float(res['price_usd'])
