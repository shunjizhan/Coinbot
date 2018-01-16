import requests
import hmac
import hashlib
import base64
from requests.auth import AuthBase


class CoinbaseAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(requests.get('https://api.gdax.com/time').json()['epoch'])
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class Coinbase:
    def __init__(self, api_key, secret_key, passphrase):
        self.api_base_url = 'https://api.gdax.com/'
        self.auth = CoinbaseAuth(api_key, secret_key, passphrase)

    def get_price(self, coin):
        if coin not in {'BTC', 'ETH', 'BCH', 'LTC'}:
            raise Exception('this coin (%s) is not in GDAX!' % coin)

        api_url = self.api_base_url + 'products/%s-USD/book?level=1' % coin
        return float(requests.get(api_url, auth=self.auth).json()['bids'][0][0])

    def get_BTC_price(self):
        return self.get_price('BTC')

    def get_coin_balance(self):
        account = requests.get(self.api_base_url + 'accounts', auth=self.auth).json()

        BTC_price = self.get_BTC_price()
        coins = {'total': {'BTC': 0, 'USD': 0}}
        for acc in account:
            coinName = acc['currency']
            num = float(acc['balance'])
            if coinName == 'USD':
                USD_value = num
            else:
                USD_value = self.get_price(coinName) * num
            BTC_value = USD_value / BTC_price

            # update info
            coins[coinName] = {
                'num': num,
                'BTC': BTC_value,
                'USD': USD_value
            }
            coins['total']['BTC'] += BTC_value
            coins['total']['USD'] += USD_value
        return coins














