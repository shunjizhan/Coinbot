import pprint as pp
import json

from utils import p, show_coins, combine_coins, combine_markets
from exchange.bittrex.bittrex import Bittrex
from exchange.coinbase.coinbase import Coinbase
from exchange.binance.binance import Binance
from exchange.gate.gate import Gate
from exchange.dew.dew import Dew
from exchange.bithumb.bithumb import Bithumb


class Coinbot:
    def __init__(self):
        self.connect_exchanges()

    def connect_exchanges(self):
        with open('./keys.json') as key_file:
            keys = json.load(key_file)
        key_coinbase = keys['coinbase']
        key_bittrex = keys['bittrex']
        key_binance = keys['binance']
        key_gate = keys['gate']
        key_bithumb = keys['bithumb']

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

        self.bithumb = Bithumb(
            key_bithumb['key'],
            key_bithumb['secret'],
        )

        self.dew = Dew()

        self.all_exchanges = {
            'gate': self.gate,
            'dew': self.dew,
            'coinbase': self.coinbase,
            'binance': self.binance,
            'bittrex': self.bittrex,
            'bithumb': self.bithumb,
        }

        self.trading_exchanges = {
            'gate': self.gate,
            'binance': self.binance,
            'bittrex': self.bittrex,
            'bithumb': self.bithumb,
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
        ex_price = {}
        for ex_name, exchange in self.trading_exchanges.items():
            ex_price[ex_name] = exchange.get_price(coin, base, _type)
        price_ex = {v: k for k, v in ex_price.items()}

        prices = ex_price.values()
        if 0 in prices:
            return 0

        # calculate diff
        high, low = max(prices), min(prices)
        diff = (high - low) / high if low > 0 else 0
        if diff >= min_diff:
            ex_high = price_ex[high]
            ex_low = price_ex[low]
            bid = self.trading_exchanges[ex_high].get_price(coin, base, 0)
            ask = self.trading_exchanges[ex_low].get_price(coin, base, 1)
            real_diff = (bid - ask) / bid
            # if real_diff < 0:
            #     bid = self.trading_exchanges[ex_low].get_price(coin, base, 0)
            #     ask = self.trading_exchanges[ex_high].get_price(coin, base, 1)
            #     real_diff = (bid - ask) / bid

            # need more accurate diff calculation with market depth
            if real_diff >= min_diff:
                print('')
                print(
                    round(low * 1000, 4),
                    round(high * 1000, 4),
                    round(ask * 1000, 4),
                    round(bid * 1000, 4)
                )
                print('{:s}-{:s} {:.1f}% {:.1f}% {:s} > {:s}'.format(coin, base, diff * 100, real_diff * 100, ex_high, ex_low))

    def get_full_balance(self, full=False, allow_zero=False):
        BTC_price = self.coinbase.get_BTC_price()
        USD_out = 2000 + 8888 + 8338
        all_coins = {
            'total': {
                'BTC': USD_out / BTC_price,
                'USD': USD_out,
                'num': 0
            }
        }

        for ex_name, exchange in self.all_exchanges.items():
            coins = exchange.get_full_balance(allow_zero=allow_zero)
            combine_coins(all_coins, coins)
            p(ex_name + ': '),
            show_coins(coins)

        print('Out:     ' + str(USD_out) + ' 100%'),

        p('Total:   '),
        show_coins(all_coins, full=full, USD_out=USD_out)

    def get_all_coin_balance(self, allow_zero=False):
        pp.pprint(self.all_exchanges)
        for ex_name, exchange in self.all_exchanges.items():
            coins = exchange.get_all_coin_balance(allow_zero)
            print('--------------------------')
            print(ex_name)
            print(coins)

    def get_bittrex_profit_ratio(self, base=200):
        # *** not updated ***
        coins = self.bittrex.get_full_balance()
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


