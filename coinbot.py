import pprint as pp
import requests

from bittrex import Bittrex
from coinbase import CoinbaseAuth


# ---------------------------------------- helpers ---------------------------------------- #
def utf8(d):
    return '{%s}' % ',\n'.join("'%s': '%s'" % pair for pair in d.iteritems())


def get(url):
    result = requests.get(api_url + url, auth=auth).json()
    for item in result:
        print (utf8(item))
        print (" ")
# ----------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    # ---------- bittrex ---------- #
    bittrex = Bittrex("c439546abe26493ebb52cce3d9a4eeac", "ee05e7bde1ed461c806793a9289d370b")
    balances = bittrex.get_balances()

    result = {}
    for coin in balances['result']:
        result[coin['Currency']] = coin['Balance']
    # pp.pprint(result)

    BTC_bittrex = 0
    total = len(result)
    current = 0
    USDT = 0
    for coin in result:
        current += 1
        if current == 10:
            break
        if (current % 20 == 0):
            print(str(current) + '/' + str(total))
        coinNum = float(result[coin])
        if (coin == 'BTC'):
            BTC_bittrex += coinNum
        elif coin == 'USDT':
            USDT = coinNum
        else:
            ticker = bittrex.get_ticker('BTC-' + coin)['result']
            if (ticker is not None and ticker['Last'] is not None):
                BTC_bittrex += float(ticker['Last']) * coinNum

    # ---------- GDAX ---------- #
    api_url = 'https://api.gdax.com/'
    API_KEY = 'cf3a26182673f04a6c14b525cf486538'
    API_SECRET = 'b/gZLAP70oEiGzmSPA998WWTXUY0X+Ip3eDPPNTRVlx+G9Tdv/cLBIQ8mLp3Le/7VzTgFPp/+8SrQtqBp0NoVQ=='
    API_PASS = 'Ss132465798'
    auth = CoinbaseAuth(API_KEY, API_SECRET, API_PASS)
    account = requests.get(api_url + 'accounts', auth=auth).json()
    # pp.pprint(account)
    for acc in account:
        coin = acc['currency']
        balance = float(acc['balance'])
        if (coin == 'BTC'):
            BTC = balance 
        if (coin == 'BCH'):
            BCH = balance        
        if (coin == 'LTC'):
            LTC = balance        
        if (coin == 'ETH'):
            ETH = balance
        if (coin == 'USD'):
            USD = balance

    BTCprice = float(requests.get(api_url + 'products/BTC-USD/book?level=1', auth=auth).json()['bids'][0][0])
    BCHprice = 3490
    ETHprice = float(requests.get(api_url + 'products/ETH-USD/book?level=1', auth=auth).json()['bids'][0][0])
    LTCprice = float(requests.get(api_url + 'products/LTC-USD/book?level=1', auth=auth).json()['bids'][0][0])

    # pp.pprint(account)

    USD_bittrex = BTC_bittrex * BTCprice + USDT
    USD_gdax = USD + LTC * LTCprice + BTC * BTCprice + ETH * ETHprice + BCH * BCHprice
    out = 3768 + 2000 + 8888
    total = USD_bittrex + USD_gdax + out

    print 'Bittrex: ' + str(USD_bittrex) + ' ' + str(100 - int(USDT * 100 / USD_bittrex)) + '%'
    print 'GDAX:    ' + str(USD_gdax)    + ' ' + str(100 - int(USD * 100 / USD_gdax)) + '%'
    print 'out:     ' + str(out)   
    print 'Total:   ' + str(total)       + ' ' + str(100 - int((USDT + USD) * 100 / (total - (3768 + 2000 + 8888 + 10000)))) + '%'















