import json
from pprint import pprint
from binance import Binance


def get_profit_details(coin):
    # get all orders
    coin += 'BTC'
    all_orders = binance.api.get_all_orders(symbol=coin)
    all_orders = list(filter(lambda x: x['status'] == 'FILLED', all_orders))

    # calculation
    position = {}
    all_trades = []
    for order in all_orders:
        side = order['side']
        price = float(order['price'])
        num = float(order['executedQty'])
        time = order['time']

        if side == 'BUY':
            position = {
                'buy_price': price,
                'buy_time': time,
                'num': num
            }
        else:
            cur_trade = {
                'buy_time': position['buy_time'],
                'sell_time': time,
                'buy_price': position['buy_price'],
                'sell_price': price,
                'num': num,
                'profit': round((price - position['buy_price']) * 100/ price, 2)
            }
            all_trades.append(cur_trade)

    return all_trades


if __name__ == '__main__':
    with open('../keys.json') as key_file:
        keys = json.load(key_file)
        key_binance = keys['binance2']

    binance = Binance(key_binance['key'], key_binance['secret'])
    details = get_profit_details('APPC')


    pprint(details)