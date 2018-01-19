import pprint as pp
import sys

from coinbot import Coinbot


def p(x):
    pp.pprint(x)


if __name__ == '__main__':
    bot = Coinbot()
    if len(sys.argv) == 1:
        bot.get_all_coins(full=False)
    elif sys.argv[1] == 'diff':
        bot.get_all_diff_rate()
    elif sys.argv[1] == 'test':
        p(bot.gate.pairs())

    # bot.get_bittrex_profit_ratio(200.0)
    # bot.buy_all_binance()
