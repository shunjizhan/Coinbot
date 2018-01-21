import pprint as pp
import sys

from coinbot import Coinbot


def p(x):
    pp.pprint(x)


if __name__ == '__main__':
    bot = Coinbot()
    if len(sys.argv) == 1:
        bot.get_all_coins(full=False)
    elif sys.argv[1] == 'full':
        bot.get_all_coins(full=True)
    elif sys.argv[1] == 'diff':
        bot.get_all_diff_rate(min_diff=0.03)
    elif sys.argv[1] == 'test':
        p(bot.dew.get_BTC_price())
    else:
        print('nothing to do...')
