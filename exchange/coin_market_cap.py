from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class CoinMarketCap:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'b277b774-a848-4d0d-87a6-86540d03e015',    # free key anyways
        }

    def get_price(self, coin):
        parameters = {
            'symbol': coin,
        }

        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(self.url, params=parameters)
            data = json.loads(response.text)
            price = data['data'][coin]['quote']['USD']['price']
            return price
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)