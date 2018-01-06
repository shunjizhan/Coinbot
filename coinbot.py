import pprint as pp
from bittrex.bittrex import Bittrex
from coinbase.coinbase import Coinbase
from binance.binance import Binance


def connect_success(exchange):
    print 'connected %s' % exchange


def cang(cash, total):
    return str(100 - int(cash * 100 / total)) + '%'


def getGateInfo():
    with open('gate/gate.txt') as f:
        return int(float(f.read()))


def combine(d1, d2):
    for coin, num in d2.items():
        if coin in d1:
            d1[coin] += num
        else:
            d1[coin] = num
    return d1


class Coinbot:
    def __init__(self):
        self.connect_exchanges()
        self.BTC_price = self.coinbase.get_BTC_price()

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
        out = 3768 + 2000 + 8888 + 8338
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
        coins = {}
        combine(coins, self.coinbase.get_coin_balance())
        combine(coins, self.bittrex.get_coin_balance())
        combine(coins, self.binance.get_coin_balance())

        pp.pprint(coins)

    # --------------------------------------------------------------------------------------------- #
    # ----------------------------------------- Trade --------------------------------------------- #
    # --------------------------------------------------------------------------------------------- #
    def buy_all_bittrex(self, USD_total=200.0):
        dontTouch = {'XRP', 'XEM', 'BTC', 'DOGE', 'SC', 'NEO', 'ZEC', 'BTG', 'MONA', 'WINGS', 'USDT'}
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
        dontTouch = {'XRP', 'XEM', 'BTC', 'DOGE', 'SC', 'NEO', 'ZEC', 'BTG', 'MONA', 'WINGS', 'USDT'}
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
                        print '%2f' % percent
                        # break
        print total, total / count


















