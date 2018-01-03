#!/usr/bin/env python
# coding=utf-8

import pprint as pp
from bittrex import Bittrex


def p(x):
    pp.pprint(x)


if __name__ == '__main__':
    bittrex = Bittrex(
        "c439546abe26493ebb52cce3d9a4eeac",
        "ee05e7bde1ed461c806793a9289d370b"
    )

    dontTouch = {'XRP', 'XEM', 'BTC', 'DOGE', 'SC', 'NEO', 'ZEC', 'BTG', 'MONA', 'WINGS', 'USDT'}
    allCoins = bittrex.get_balances()['result']

    for coin in allCoins:
        name = coin['Currency']
        if (name not in dontTouch):
            market = 'BTC-' + name
            ticker = bittrex.get_ticker(market)['result']
            if (ticker is not None and ticker['Ask'] is not None):
                price = float(ticker['Ask']) * 1.05
                quantity = 0.013 / price
                result = bittrex.buy_limit(market, quantity, price)
                if result is not None and result['result'] is not None:
                    details = bittrex.get_order(result['result']['uuid'])
                    USD = float(details['result']['Price']) * 15781

                    print name, int(USD), 
                    # break

    # count = 0
    # total = 0
    # for coin in allCoins:
    #     name = coin['Currency']
    #     balance = coin['Balance']
    #     if (name not in dontTouch and balance > 0):
    #         market = 'BTC-' + name
    #         ticker = bittrex.get_ticker(market)['result']
    #         if (ticker is not None and ticker['Bid'] is not None):
    #             price = float(ticker['Bid']) * 0.95
    #             result = bittrex.sell_limit(market, balance, price)
    #             if result is not None and result['result'] is not None:
    #                 details = bittrex.get_order(result['result']['uuid'])
    #                 USD = float(details['result']['Price']) * 15781
    #                 percent = USD / 40.0

    #                 count += 1
    #                 total += USD

    #                 print name, int(USD), 
    #                 print '%2f' % percent
    #                 # break
    # print total, total / count









