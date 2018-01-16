import pprint as pp
from bittrex.bittrex import Bittrex
from coinbase.coinbase import Coinbase
from binance.binance import Binance

# from collections import defaultdict, OrderedDict


def show_coins(coins, full=False):
    for coinName, info in coins.items():
        info['BTC'] = round(info['BTC'], 2)
        info['USD'] = int(info['USD'])
        if coinName not in {'total', 'cang'}:
            info['num'] = int(info['num'])

    # print the result
    if full:
        print ' '
        coinslist = sorted(coins.items(), key=lambda kv: kv[1]['USD'], reverse=True)
        for coin, info in coinslist:
            print coin, info
    else:
        print coins['total']['USD'],
    print cang(coins)


def connect_success(exchange):
    print 'connected %s' % exchange


# def cang(cash, total):
#     return str(100 - int(cash * 100 / total)) + '%'

def cang(coins):
    cash_ratio = round(coins['USD']['USD'] * 100.0 / coins['total']['USD'], 1)
    coin_ratio = str(100 - cash_ratio)
    return coin_ratio + '%'


def getGateInfo():
    with open('gate/gate.txt') as f:
        return int(float(f.read()))


# combine two dicts with format {coinName: {'BTC': BTC_value, 'USD': USD_value, 'num': coin_num}}
def combine(d1, d2):
    for coin, info in d2.items():
        if coin in d1:
            for attribute in d1[coin]:
                d1[coin][attribute] += info[attribute]
        else:
            d1[coin] = info
    return d1


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
    def get_USD_balance(self):
        out = 2000 + 8888 + 8338
        print 'Out:     %d' % out

        USD_gate, cash_gate = getGateInfo(), 0
        print 'gate.io: %s, %s' % (USD_gate, cang(cash_gate, USD_gate))

        USD_gdax, cash_gdax = self.coinbase.get_USD_balance()
        # USD_gdax, cash_gdax = 60419, 60419
        print 'GDAX:    %s, %s' % (USD_gdax, cang(cash_gdax, USD_gdax))

        USD_bittrex, cash_bittrex = self.bittrex.get_USD_balance(self.BTC_price)
        print 'Bittrex: %s, %s' % (USD_bittrex, cang(cash_bittrex, USD_bittrex))

        USD_binance, cash_binance = self.binance.get_USD_balance()
        print 'Binance: %s, %s' % (USD_binance, cang(cash_binance, USD_binance))

        real_total = USD_bittrex + USD_gdax + USD_binance + USD_gate
        USD_total = int(real_total + out)
        cash_total = cash_gdax + cash_bittrex + cash_gate + cash_binance
        print 'Total:   %s, %s, %.3f' % (USD_total, cang(cash_total, real_total), USD_total / 38800.0)

    def get_all_coins(self):
        all_coins = {}

        coinbase_coins = self.coinbase.get_coin_balance()
        combine(all_coins, coinbase_coins)
        print 'Coinbase: ',
        show_coins(coinbase_coins)

        bittrex_coins = self.bittrex.get_coin_balance()
        combine(all_coins, bittrex_coins)
        print 'Bittrex: ',
        show_coins(bittrex_coins)

        binance_coins = self.binance.get_coin_balance()
        combine(all_coins, binance_coins)
        print 'Binance: ',
        show_coins(binance_coins)

        print 'Total: ',
        show_coins(all_coins, full=False)

    def get_bittrex_profit_ratio(self, base):
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

















