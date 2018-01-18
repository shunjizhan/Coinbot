from coinbot import Coinbot
import pprint as pp

if __name__ == '__main__':
    bot = Coinbot()
    # bot.get_all_coins(full=False)
    # pp.pprint(bot.binance.client.get_products()['data'])
    bot.get_all_profit_rate()
    # bot.get_bittrex_profit_ratio(200.0)
    # bot.buy_all_binance()
