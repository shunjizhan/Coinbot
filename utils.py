import sys


def p(*args):
    for x in args:
        if type(x) is not str:
            x = str(x)
        sys.stdout.write(x + ' ')


def show_coins(coins, full=False, USD_out=0):
    '''
    print coins dict with format {
        coinName1: {
            'BTC': BTC_value,
            'USD': USD_value,
            'num': coin_num
        }
        coinName2: {} ...
    }
    '''
    for coinName, info in coins.items():
        info['BTC'] = round(info['BTC'], 2)
        info['USD'] = int(info['USD'])
        if coinName not in {'total', 'cang'}:
            info['num'] = int(info['num'])

    # print the result
    if full:
        total_USD = coins['total']['USD']
        coinslist = sorted(coins.items(), key=lambda kv: kv[1]['USD'], reverse=True)
        for coin, info in coinslist:
            if info['USD'] > 0:
                info['ratio'] = round(info['USD'] * 100.0 / total_USD, 1)
                print(coin, info)
    else:
        p(coins['total']['USD'])

    # 算仓位
    cash_ratio = round(coins['USD']['USD'] * 100.0 / (coins['total']['USD'] - USD_out), 1)
    coin_ratio = str(100 - cash_ratio)
    print(coin_ratio + '%')


def combine_coins(d1, d2):
    '''
    combine two dicts with format {
        coinName1: {
            'BTC': BTC_value,
            'USD': USD_value,
            'num': coin_num
        }
        coinName2: {} ...
    }
    '''
    for coin, info in d2.items():
        if coin in d1:
            for attribute in d1[coin]:
                d1[coin][attribute] += info[attribute]
        else:
            d1[coin] = info
    return d1
