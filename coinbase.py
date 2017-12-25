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

    def getPrice(self, coin):
        if coin not in {'BTC', 'ETH', 'BCH', 'LTC'}:
            raise Exception('this coin (%s) is not in GDAX!' % coin)

        api_url = self.api_base_url + 'products/%s-USD/book?level=1' % coin
        return float(requests.get(api_url, auth=self.auth).json()['bids'][0][0])

    def getUSDBalance(self):
        account = requests.get(self.api_base_url + 'accounts', auth=self.auth).json()
        # pp.pprint(account)
        total_USD = 0
        cash = 0
        for acc in account:
            coin = acc['currency']
            num = float(acc['balance'])
            if (coin == 'BCH'):
                total_USD += num * 2888
            elif (coin == 'USD'):
                cash = num * 1
                total_USD += num * 1
            else:
                total_USD += num * self.getPrice(coin)

        return int(total_USD), int(cash)















