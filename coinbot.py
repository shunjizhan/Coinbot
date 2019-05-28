import json
from pprint import pprint
from copy import deepcopy

from utils import p, show_coins, combine_coins, combine_markets
from exchange.bittrex.bittrex import Bittrex
from exchange.coinbase.coinbase import Coinbase
from exchange.binance.binance import Binance
from exchange.gate.gate import Gate
from exchange.dew.dew import Dew
from exchange.bithumb.bithumb import Bithumb
from exchange.huobi.huobi import Huobi


class Coinbot:
    def __init__(self):
        self.avail_exchanges = {
            # 'coinbase',
            # 'bittrex',
            'binance',
            # 'gate',
            # 'bithumb',
            'huobi',
            # 'dew'
        }
        self.connect_exchanges()

    def has_ex(self, ex_name):
        return ex_name in self.avail_exchanges

    def connect_exchanges(self):
        with open('./keys.json') as key_file:
            keys = json.load(key_file)
        key_coinbase = keys['coinbase']
        key_bittrex = keys['bittrex']
        key_binance = keys['binance']
        key_gate = keys['gate']
        key_bithumb = keys['bithumb']
        key_huobi = keys['huobi']

        print('')

        self.all_exchanges = {
            'huobi': Huobi(key_huobi['key'], key_huobi['secret']) if self.has_ex('huobi') else None,
            # 'bithumb': Bithumb(key_bithumb['key'], key_bithumb['secret']) if self.has_ex('bithumb') else None,
            # 'gate': Gate(key_gate['key'], key_gate['secret']) if self.has_ex('gate') else None,
            # 'dew': Dew() if self.has_ex('dew') else None,
            # 'coinbase': Coinbase(key_coinbase['key'], key_coinbase['secret'], key_coinbase['pass']) if self.has_ex('coinbase') else None,
            'binance': Binance(key_binance['key'], key_binance['secret']) if self.has_ex('binance') else None,
            # 'bittrex': Bittrex(key_bittrex['key'], key_bittrex['secret']) if self.has_ex('bittrex') else None,
        }

        print('')

    # --------------------------------------------------------------------------------------------- #
    # ------------------------------------------ View --------------------------------------------- #
    # --------------------------------------------------------------------------------------------- #
    def get_full_balance(self, full=False, allow_zero=False):
        # read all private variables
        with open('variables.json') as f:
            variables = json.load(f)

        # get BTC and EOS price for future use
        huobi = self.all_exchanges['huobi']
        BTC_price = huobi.get_BTC_price()
        EOS_price = huobi.get_price('EOS', 'USDT')

        # get cashed out amount
        USD_out = sum(variables['usd_out'])
        out_coins = {
            'total': {
                'BTC': USD_out / BTC_price,
                'USD': USD_out,
                'num': 0
            }
        }

        # combine coins in all exchanges
        all_coins = deepcopy(out_coins)
        for ex_name, exchange in self.all_exchanges.items():
            if exchange:
                coins = exchange.get_full_balance(allow_zero=allow_zero)
                # pprint(coins)
                all_coins = combine_coins(all_coins, coins)
                p('[' + ex_name + '] => '),
                show_coins(coins)

        # other long term coins
        tp_eos = variables['tp_eos']
        tp_usdt = tp_eos * EOS_price
        other_coins = {
            'EOS': {
                'BTC': tp_usdt / BTC_price,
                'USD': tp_usdt,
                'num': tp_eos
            },
            'total': {
                'BTC': tp_usdt / BTC_price,
                'USD': tp_usdt,
                'num': 0
            },
        }

        # print out cash out amount
        p('[Cash Out] =>'),
        show_coins(out_coins)

        # add other long term coins
        all_coins = combine_coins(all_coins, other_coins)

        print('[Total Long Term] =>')
        show_coins(all_coins, full=full, USD_out=USD_out)

        # calculate short term coins
        print('[Total Short Term] =>')
        fixed_coins = variables['fixed_coins']
        fixed_coins['EOS'] += tp_eos    # other coins is also long term
        show_coins(all_coins, full=full, USD_out=USD_out, fixed_coins=fixed_coins)

        # profit calculation
        p('Ratio:   ')
        base = variables['base']
        print(round(all_coins['total']['USD'] / base, 3))

    def get_all_coin_balance(self, allow_zero=False):
        pprint(self.all_exchanges)
        for ex_name, exchange in self.all_exchanges.items():
            coins = exchange.get_all_coin_balance(allow_zero)
            print('--------------------------')
            print(ex_name)
            print(coins)

    def get_all_diff_rate(self, min_diff=0.03):
        all_markets = {}
        for ex_name, exchange in self.trading_exchanges.items():
            all_markets = combine_markets(
                all_markets,
                exchange.get_trading_pairs()
            )
        pprint(all_markets)

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
            if real_diff >= min_diff:
                print('')
                print(
                    round(low * 1000, 4),
                    round(high * 1000, 4),
                    round(ask * 1000, 4),
                    round(bid * 1000, 4)
                )
                print('{:s}-{:s} {:.1f}% {:.1f}% {:s} > {:s}'.format(coin, base, diff * 100, real_diff * 100, ex_high, ex_low))


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
    def dingtou(self):
        # check password
        password = input('enter pass word: ')
        if not password == 'EOSGOGO':
            exit('password not correct')

        # market buy all of the coins
        huobi = self.all_exchanges['huobi']
        bases = {
            "EOS": 400,
            "ADA": 300,
            "BCH": 300,
            "AE": 200,
            "XRP": 200,
            "HT": 200,
            "ONT": 200,
            "ATOM": 200
        },
        for coin, usd in bases.items():
            res = huobi.market_buy(coin, 'usdt', usd)
            success = res['status'] == 'ok'

            # print out result
            if success:
                order_id = res['data']
                info = huobi.get_order_info(order_id)['data']
                price = float(info['field-cash-amount']) / float(info['field-amount'])
                print ('bought {} usd of {}, price: {}'.format(usd, coin, price))
            else:
                print ('bought {} failed!'.format(coin))















