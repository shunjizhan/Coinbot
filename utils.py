import sys
import requests
from copy import deepcopy
from pprint import pprint


def p(*args):
    for x in args:
        if type(x) is not str:
            x = str(x)
        sys.stdout.write(x + ' ')


def show_coins(coins, full=False, USD_out=0, fixed_coins={}):
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

    coins = deepcopy(coins)

    # first need to deduct fixed coins from coins
    for coin, num in fixed_coins.items():
        assert(coin in coins)

        # calculate values to be deducted
        coin_info = coins[coin]
        deducted_ratio = (num / coin_info['num'])
        deducted_USD = coin_info['USD'] * deducted_ratio
        deducted_BTC = coin_info['BTC'] * deducted_ratio

        # deduct this coin num and value
        coin_info['num'] -= num
        coin_info['USD'] -= deducted_USD
        coin_info['BTC'] -= deducted_BTC

        # deduct total coin num and value
        coin_info = coins['total']
        coin_info['USD'] -= deducted_USD
        coin_info['BTC'] -= deducted_BTC

    # do some rounding
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
            if info['BTC'] != 0:
                info['ratio'] = round(info['USD'] * 100.0 / (total_USD - USD_out), 1)
                print(coin, info)
    else:
        p(coins['total']['USD'])

    # 仓位
    if (coins['total']['USD'] > 0) and ('USD' in coins):
        cash = coins['USD']['USD']
        real_balance = coins['total']['USD'] - USD_out      # real_balance = total_balance - USD_out
        cash_ratio = round(cash * 100.0 / real_balance, 1)
    else:
        cash_ratio = 0
    coin_ratio = str(100 - cash_ratio)
    print(coin_ratio + '%')
    print('-' * 70)


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
    d1, d2 = deepcopy(d1), deepcopy(d2)
    for coin, info in d2.items():
        if coin in d1:
            for attribute in d1[coin]:
                d1[coin][attribute] += info[attribute]
        else:
            d1[coin] = info

    return d1


def combine_markets(m1, m2):
    '''
    combine two markets with format {
        'BTC': {'ADA', 'BAT', 'BTG', ...},
        'ETH': {'BAT', 'BNT', 'DNT', 'ETC', ...},
        'USDT': {'NEO', 'BTC', 'LTC', ...}
        ...
    }
    '''
    if m1 == {}:
        return m2
    if m2 == {}:
        return m1

    assert(m1.keys() == m2.keys())
    for base in m2:
        m1[base] &= m2[base]
    return m1


def get_rate(currency, base):
    # *** this needs update
    key = '97d6041822759bd2b86a1f153329ed78'
    url = 'https://api.fixer.io/latest?access_key=%s&base=%s' % (key, base)
    pprint (requests.get(url).json())
    return requests.get(url).json()['rates'][currency]


if __name__ == '__main__':
    pprint(get_rate('krw','usd'))






















































