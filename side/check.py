import json
from pandas import DataFrame
from pprint import pprint
from binance import Binance
from datetime import datetime


def timestamp_to_real_time(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')


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
        time = int(order['time'])

        if side == 'BUY':
            position = {
                'buy_price': price,
                'buy_time': time,
                'num': num
            }
        else:
            buy_time = position['buy_time']
            buy_price = position['buy_price']
            profit = float(price - position['buy_price'])
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


def convert_to_panda_readable(all_trades, columns):
    res = {}
    for p in columns:
        res[p] = []

    for trade in all_trades:
        for p in columns:
            res[p].append(trade[p])

    return res


if __name__ == '__main__':
    with open('keys.json') as key_file:
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

    # sort by sell time
    all_trades = sorted(all_trades, key=lambda x: x['sell_time'])

    # convert time stamp to be readable
    def _convert_timestamp(x):
        x['sell_time'] = timestamp_to_real_time(x['sell_time'])
        x['buy_time'] = timestamp_to_real_time(x['buy_time'])
        return x

    all_trades = map(_convert_timestamp, all_trades)

    # convert to panda data frame
    columns = [
        'coin_name',
        'buy_time',
        'sell_time',
        'buy_price',
        'sell_price',
        'num',
        'profit',
        'profit_rate'
    ]
    all_trades = convert_to_panda_readable(all_trades, columns)
    df = DataFrame(all_trades)
    print('finished! => results.csv\n' + '-' * 50)

    # write to results
    df.to_csv('results.csv', columns=columns)




