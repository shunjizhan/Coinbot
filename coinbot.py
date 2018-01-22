import pprint as pp
import json

from utils import p, show_coins, combine_coins, combine_markets
from exchange.bittrex.bittrex import Bittrex
from exchange.coinbase.coinbase import Coinbase
from exchange.binance.binance import Binance
from exchange.gate.gate import Gate
from exchange.dew.dew import Dew


class Coinbot:
    def __init__(self):
        self.connect_exchanges()
        # BTC_price might need to keep updating if the program keep running
        self.BTC_price = self.coinbase.get_BTC_price()
        self.dontTouch = {'XRP', 'XEM', 'BTC', 'DOGE', 'SC', 'NEO', 'ZEC', 'BTG', 'MONA', 'WINGS', 'USDT', 'IOTA', 'EOS', 'QTUM', 'ADA', 'XLM', 'LSK', 'BTS', 'XMR', 'DASH', 'SNT', 'BCC', 'BCH', 'SBTC', 'BCX', 'ETF', 'LTC', 'ETH'}

    def connect_exchanges(self):
        with open('./keys.json') as key_file:
            keys = json.load(key_file)
        key_coinbase = keys['coinbase']
        key_bittrex = keys['bittrex']
        key_binance = keys['binance']
        key_gate = keys['gate']

        print('')

        self.gate = Gate(
            key_gate['key'],
            key_gate['secret'],
        )

        self.coinbase = Coinbase(
            key_coinbase['key'],
            key_coinbase['secret'],
            key_coinbase['pass']
        )

        self.bittrex = Bittrex(
            key_bittrex['key'],
            key_bittrex['secret']
        )

        self.binance = Binance(
            key_binance['key'],
            key_binance['secret']
        )

        self.dew = Dew()

        self.all_exchanges = {
            'gate': self.gate,
            'dew': self.dew,
            'coinbase': self.coinbase,
            'binance': self.binance,
            'bittrex': self.bittrex,
        }

        self.trading_exchanges = {
            'gate': self.gate,
            'binance': self.binance,
            'bittrex': self.bittrex,
        }

        print('')

    # --------------------------------------------------------------------------------------------- #
    # ------------------------------------------ View --------------------------------------------- #
    # --------------------------------------------------------------------------------------------- #
    def get_all_diff_rate(self, min_diff=0.03):
        all_markets = {}
        for ex_name, exchange in self.trading_exchanges.items():
            all_markets = combine_markets(
                all_markets,
                exchange.get_trading_pairs()
            )
        pp.pprint(all_markets)

        while True:
            print('----------------------------------------')
            for base, markets in all_markets.items():
                for coin in markets:
                    self.get_diff_rate(coin, base, min_diff)

    def get_diff_rate(self, coin, base, min_diff, _type=0):
        # set up bijection between exchange and price
        exchange_price = {}
        for ex_name, exchange in self.trading_exchanges.items():
            exchange_price[ex_name] = exchange.get_price(coin, base, _type)
        price_exchange = {v: k for k, v in exchange_price.items()}

        prices = exchange_price.values()
        if 0 in prices:
            return 0

        high, low = max(prices), min(prices)
        diff = (high - low) / high if high > 0 else 0
        if diff >= min_diff:
            # need more accurate diff calculation with bids and asks price
            print('%s-%s %.1f' % (coin, base, diff * 100) + '%  ' + '%s > %s' % (price_exchange[high], price_exchange[low]))
        # else:
        #     print('%s-%s X' % (coin, base))

    def get_all_coins(self, full=False):
        USD_out = 2000 + 8888 + 8338
        all_coins = {
            'total': {
                'BTC': USD_out / self.BTC_price,
                'USD': USD_out,
                'num': 0
            }
        }

        for ex_name, exchange in self.all_exchanges.items():
            coins = exchange.get_coin_balance()
            combine_coins(all_coins, coins)
            p(ex_name + ': '),
            show_coins(coins)

        print('Out:     ' + str(USD_out) + ' 100%'),

        p('Total:   '),
        show_coins(all_coins, full=full, USD_out=USD_out)

    def get_bittrex_profit_ratio(self, base=200):
        # *** not updated ***
        coins = self.bittrex.get_coin_balance()
        for coin, count in coins.items():
            ticker = self.bittrex.get_ticker('BTC-' + coin)['result']
            percent_sum, coin_count = 0.0, 0
            if (ticker is not None and ticker['Last'] is not None):
                percent = count * float(ticker['Last']) * self.BTC_price / base
                percent_sum += percent
                coin_count += 1
                print(coin, '%.2f' % percent)
        print(percent_sum / coin_count)

    # --------------------------------------------------------------------------------------------- #
    # ----------------------------------------- Trade --------------------------------------------- #
    # --------------------------------------------------------------------------------------------- #
    def buy_all_bittrex(self, USD_total=200.0):
        # *** not updated ***
        dontTouch = self.dontTouch
        allCoins = self.bittrex.get_balances()['result']

        for coin in allCoins:
            name = coin['Currency']
            if (name not in dontTouch):
                market = 'BTC-' + name
                ticker = self.bittrex.get_ticker(market)['result']
                if (ticker is not None and ticker['Ask'] is not None):
                    price = float(ticker['Ask']) * 1.05
                    BTC_total = USD_total / self.BTC_price * 1.01
                    quantity = BTC_total / price
                    result = self.bittrex.buy_limit(market, quantity, price)
                    if result is not None and result['result'] is not None:
                        details = self.bittrex.get_order(result['result']['uuid'])
                        USD = float(details['result']['Price']) * self.BTC_price

                        print(name, int(USD)),
                        # break

    def sell_all_bittrex(self):
        # *** not updated ***
        dontTouch = self.dontTouch
        allCoins = self.bittrex.get_balances()['result']

        count = 0
        total = 0
        for coin in allCoins:
            name = coin['Currency']
            balance = coin['Balance']
            if (name not in dontTouch and balance > 0):
                market = 'BTC-' + name
                ticker = self.bittrex.get_ticker(market)['result']
                if (ticker is not None and ticker['Bid'] is not None):
                    price = float(ticker['Bid']) * 0.95
                    result = self.bittrex.sell_limit(market, balance, price)
                    if result is not None and result['result'] is not None:
                        details = self.bittrex.get_order(result['result']['uuid'])
                        USD = float(details['result']['Price']) * self.BTC_price
                        percent = USD / 40.0

                        count += 1
                        total += USD

                        print(name, int(USD)),
                        print('%.2f' % percent)
                        # break
        print(total, total / count)

    def buy_all_binance(self, USD_total=200.0):
        # *** not updated ***
        dontTouch = self.dontTouch
        balances = self.binance.client.get_account()['balances']

        # pp.pprint(balances)
        for coin in balances:
            coinName = coin['asset']
            if coinName not in dontTouch:
                num = float(coin['free']) + float(coin['locked'])
                if num == 0:
                    pair = coinName + 'BTC'
                    print(coinName),
                    info = self.binance.client.get_symbol_info(pair)
                    if info:
                        # print info
                        ticker = self.binance.client.get_order_book(symbol=pair)
                        if (ticker is not None and ticker['asks']):
                            # print ticker['asks']
                            price = float(ticker['asks'][0][0]) * 1.03
                            BTC_total = USD_total / self.BTC_price * 1.03
                            quantity = int(BTC_total / price)
                            print(price, quantity)
                            result = self.binance.client.order_market_buy(symbol=pair, quantity=quantity)

    def sell_all_binance(self):
        # *** not updated ***
        dontTouch = self.dontTouch
        all_coins = self.binance.get_coin_balance()

        for coinName, quantity in all_coins.items():
            if coinName not in dontTouch:
                pair = coinName + 'BTC'
                price = float(self.binance.client.get_order_book(symbol=pair)['bids'][0][0])
                BTC_value = price * quantity
                extra_value = BTC_value - 0.01190112    # 200 USD
                sell_quantity = int(extra_value / price)
                if sell_quantity > 0:
                    print(coinName, sell_quantity)
                    result = self.binance.client.order_market_sell(symbol=pair, quantity=sell_quantity)

















