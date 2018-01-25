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
        bot.get_full_balance(full=True)
    elif sys.argv[1] == 'diff':
        bot.get_all_diff_rate(min_diff=0.01)
    elif sys.argv[1] == 'coins':
        bot.get_all_coin_balance()
    elif sys.argv[1] == 'test':
        # res = bot.bittrex.market_sell_everything()
        # p(res)
        # print (bot.bithumb.api.place_market_sell(0.01, 'ETH'))
        # print(bot.bithumb.get_price('BTC'))
        # print(bot.bithumb.get_price('ETH'))
        # print(bot.bithumb.get_price('BTC', 'ETH'))
        print(bot.bithumb.get_price('QTUM', 'EOS'))
        # print (bot.bithumb.api.get_ticker())
        # print (bot.bithumb.api.get_order_book())
        # print (bot.bithumb.api.get_recent_transactions())
        # print (bot.bithumb.api.get_account())
        # print (bot.bithumb.api.get_my_ticker())
        # # print (bot.bithumb.api.get_my_orders())
        # print (bot.bithumb.api.get_my_transactions())
    else:
        print('nothing to do...')
