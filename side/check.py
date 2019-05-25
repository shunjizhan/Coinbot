import json
from pprint import pprint
from binance import Binance
from datetime import datetime


def get_profit_details(coin):
    coin_name = coin[:-3]

    # get all orders
    all_orders = binance.api.get_all_orders(symbol=coin)
    all_orders = list(filter(lambda x: x['status'] == 'FILLED', all_orders))

    # calculation
    position = {}
    all_trades = []
    for order in all_orders:
        side = order['side']
        price = float(order['price'])
        num = float(order['executedQty'])
        time = datetime.utcfromtimestamp(int(order['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        if side == 'BUY':
            position = {
                'buy_price': price,
                'buy_time': time,
                'num': num
            }
        else:
            buy_time = position['buy_time']
            buy_price = position['buy_price']
            profit = price - position['buy_price']
            cur_trade = {
                'coin_name': coin_name,
                'buy_time': buy_time,
                'sell_time': time,
                'buy_price': buy_price,
                'sell_price': price,
                'num': num,
                'profit': profit,
                'profit_rate': round(profit * 100 / buy_price, 2)
            }
            all_trades.append(cur_trade)

    return all_trades


if __name__ == '__main__':
    with open('../keys.json') as key_file:
        keys = json.load(key_file)
        key_binance = keys['binance2']

    # exchange instance
    binance = Binance(key_binance['key'], key_binance['secret'])

    # get all trading pairs
    all_tickers = binance.api.get_all_tickers()
    all_pairs = map(lambda x: x['symbol'], all_tickers)
    all_pairs = list(filter(lambda x: x[-3:] == 'BTC', all_pairs))

    # calculate all trade profits
    print('calculating ...')
    all_trades = []
    finished = 0
    task_count = len(all_pairs)
    target = 0.1
    for pair in all_pairs:
        # add all trades of this pair
        all_trades.extend(get_profit_details(pair))

        # print out some progress info
        finished += 1
        if (finished / task_count) >= target:
            print(str(int(target * 100)) + '%')
            target += 0.1

    pprint(all_trades)




