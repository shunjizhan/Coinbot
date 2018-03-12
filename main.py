import pprint as pp
import sys

from coinbot import Coinbot


def p(x):
    pp.pprint(x)


if __name__ == '__main__':
    bot = Coinbot()
    if len(sys.argv) == 1:
        bot.get_full_balance(full=False)
    elif sys.argv[1] == 'full':
        bot.get_full_balance(full=True, allow_zero=False)
    elif sys.argv[1] == 'diff':
        bot.get_all_diff_rate(min_diff=0.001)
    elif sys.argv[1] == 'coins':
        bot.get_all_coin_balance()
    elif sys.argv[1] == 'test':
        pp.pprint(bot.gate.markets)
        pp.pprint(bot.gate.get_full_balance())
        # res = bot.bittrex.market_sell_everything()
        # p(res)
        # print (bot.bithumb.api.place_market_sell(0.01, 'ETH'))
        # print(bot.bithumb.get_price('BTC'))
        # print(bot.bithumb.get_price('ETH'))
        # print(bot.bithumb.get_price('BTC', 'ETH'))
        # print(bot.huobi.api.get_market())
        # res = bot.binance.market_sell('ADA', quantity=888)
        # p(res)
        # market = bot.binance.api.get_symbol_info('BCHETH')
        # p(bot.binance.coins)
        # p(market)
        # print (bot.bithumb.api.get_ticker())
        # print (bot.bithumb.api.get_order_book())
        # print (bot.bithumb.api.get_recent_transactions())
        # print (bot.bithumb.api.get_account())
        # print (bot.bithumb.api.get_my_ticker())
        # # print (bot.bithumb.api.get_my_orders())
        # print (bot.bithumb.api.get_my_transactions())
    else:
        print('nothing to do...')
