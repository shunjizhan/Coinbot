import pprint as pp
import json

from bittrex.bittrex import Bittrex
from coinbase.coinbase import Coinbase
from binance.binance import Binance


def show_coins(coins, full=False):
    for coinName, info in coins.items():
        info['BTC'] = round(info['BTC'], 2)
        info['USD'] = int(info['USD'])
        if coinName not in {'total', 'cang'}:
            info['num'] = int(info['num'])

    # print the result
    if full:
        total_USD = coins['total']['USD']
        print ' '
        coinslist = sorted(coins.items(), key=lambda kv: kv[1]['USD'], reverse=True)
        for coin, info in coinslist:
            if info['USD'] > 0:
                info['ratio'] = round(info['USD'] * 100.0 / total_USD, 1)
                print coin, info
    else:
        print coins['total']['USD'],
    print cang(coins)


def connect_success(exchange):
    print 'connected %s' % exchange


def cang(coins):
    cash_ratio = round(coins['USD']['USD'] * 100.0 / coins['total']['USD'], 1)
    coin_ratio = str(100 - cash_ratio)
    return coin_ratio + '%'


def get_gate_coins():
    with open('gate/gate.json') as gate:
        return json.load(gate)


# combine two dicts with format {coinName: {'BTC': BTC_value, 'USD': USD_value, 'num': coin_num}}
def combine(d1, d2):
    for coin, info in d2.items():
        if coin in d1:
            for attribute in d1[coin]:
                d1[coin][attribute] += info[attribute]
        else:
            d1[coin] = info
    return d1


'''
combine two markets with format {
    'BTC': {'ETH', 'EOS'},
    'ETH': {'NEO', 'EOS'}},
    ...
}
'''
def combine_markets(m1, m2):
    assert(m1.keys() == m2.keys())
    for base in m1.keys():
        m1[base] |= m2[base]
    return m1


class Coinbot:
    def __init__(self):
        self.connect_exchanges()
        self.BTC_price = self.coinbase.get_BTC_price()
        self.dontTouch = {'XRP', 'XEM', 'BTC', 'DOGE', 'SC', 'NEO', 'ZEC', 'BTG', 'MONA', 'WINGS', 'USDT', 'IOTA', 'EOS', 'QTUM', 'ADA', 'XLM', 'LSK', 'BTS', 'XMR', 'DASH', 'SNT', 'BCC', 'BCH', 'SBTC', 'BCX', 'ETF', 'LTC', 'ETH'}

    def connect_exchanges(self):
        print ' '
        self.coinbase = Coinbase(
            'ad8327c971400a583a511c8b44153c3b',
            '4oc5G42pHNRGf6fxBhL+JE3bwKH54SothrVzCVwgBD7dxdj/PLWz2rrBYx3f9V3/lh3Cj2vLzMfsXIvmv5W1mg==',
            '5rngcof6sug'
        )
        connect_success('coinbase')

        self.bittrex = Bittrex(
            "f4a53cc750174691bb8a26adf5b9d732",
            "74cdede4f6a34ae88e782b339fdf2830"
        )
        connect_success('bittrex')

        self.binance = Binance(
            'N0VUiMGmgZRXsEJyEEyXNITGZAELNfPIZyzzcTOSwV7q9MhZt6Mt7SFFdzERZgB5',
            '7A6ZwSIwsfdWVnTSgK0Gc2JzAU2k5snEHf9DQuyM7VCNC4FykC14qxNxQmmyUhDU'
        )
        connect_success('binance')

        print ' '

    # --------------------------------------------------------------------------------------------- #
    # ------------------------------------------ View --------------------------------------------- #
    # --------------------------------------------------------------------------------------------- #
    def get_all_profit_rate(self):
        bases = {'BTC', 'ETH', 'USDT'}
        all_markets = {}
        cur_markets = {}
        for base in bases:
            cur_markets[base] = set()
            bittrex_markets = self.bittrex.get_markets()['result']
            for info in bittrex_markets:
                if info['BaseCurrency'] == base:
                    cur_markets[base].add(info['MarketCurrency'])
            all_markets[base] = cur_markets[base]

            cur_markets[base] = set()
            binance_markets = self.binance.client.get_products()['data']
            for info in binance_markets:
                if info['quoteAsset'] == base:
                    cur_markets[base].add(info['baseAsset'])
            all_markets[base] &= cur_markets[base]

        # pp.pprint(all_markets)

        while True:
            for base, markets in all_markets.items():
                for coin in markets:
                    self.get_profit_rate(coin, base)

    def get_profit_rate(self, coin, base, _type=1):
        # need more accurate calculation with bids and asks price
        price_binance = self.binance.get_price(coin, base, _type)
        price_bittrex = self.bittrex.get_price(coin, base, _type)
        prices = {price_binance, price_bittrex}
        if 0 in prices:
            return 0

        big, small = max(prices), min(prices)
        diff = (big - small) / big if big > 0 else 0
        if diff > 0.01:
            print '%s-%s %.2f' % (coin, base, diff * 100) + '%'

    def get_all_coins(self, full=False):
        all_coins = {}

        gate_coins = get_gate_coins()
        combine(all_coins, gate_coins)
        print 'GateIO:  ',
        show_coins(gate_coins)

        coinbase_coins = self.coinbase.get_coin_balance()
        combine(all_coins, coinbase_coins)
        print 'Coinbase:',
        show_coins(coinbase_coins)

        bittrex_coins = self.bittrex.get_coin_balance()
        combine(all_coins, bittrex_coins)
        print 'Bittrex: ',
        show_coins(bittrex_coins)

        binance_coins = self.binance.get_coin_balance()
        combine(all_coins, binance_coins)
        print 'Binance: ',
        show_coins(binance_coins)

        print 'Total:   ',
        show_coins(all_coins, full=full)

    def get_bittrex_profit_ratio(self, base=200):
        coins = self.bittrex.get_coin_balance()
        for coin, count in coins.items():
            ticker = self.bittrex.get_ticker('BTC-' + coin)['result']
            percent_sum, coin_count = 0.0, 0
            if (ticker is not None and ticker['Last'] is not None):
                percent = count * float(ticker['Last']) * self.BTC_price / base
                percent_sum += percent
                coin_count += 1
                print coin, '%.2f' % percent
        print percent_sum / coin_count

    # --------------------------------------------------------------------------------------------- #
    # ----------------------------------------- Trade --------------------------------------------- #
    # --------------------------------------------------------------------------------------------- #
    def buy_all_bittrex(self, USD_total=200.0):
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

                        print name, int(USD),
                        # break

    def sell_all_bittrex(self):
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

                        print name, int(USD),
                        print '%.2f' % percent
                        # break
        print total, total / count

    def buy_all_binance(self, USD_total=200.0):
        dontTouch = self.dontTouch
        balances = self.binance.client.get_account()['balances']

        # pp.pprint(balances)
        for coin in balances:
            coinName = coin['asset']
            if coinName not in dontTouch:
                num = float(coin['free']) + float(coin['locked'])
                if num == 0:
                    pair = coinName + 'BTC'
                    print coinName,
                    info = self.binance.client.get_symbol_info(pair)
                    if info:
                        # print info
                        ticker = self.binance.client.get_order_book(symbol=pair)
                        if (ticker is not None and ticker['asks']):
                            # print ticker['asks']
                            price = float(ticker['asks'][0][0]) * 1.03
                            BTC_total = USD_total / self.BTC_price * 1.03
                            quantity = int(BTC_total / price)
                            print price, quantity
                            result = self.binance.client.order_market_buy(symbol=pair, quantity=quantity)

    def sell_all_binance(self):
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
                    print coinName, sell_quantity
                    result = self.binance.client.order_market_sell(symbol=pair, quantity=sell_quantity)

















