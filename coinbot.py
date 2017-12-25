from bittrex import Bittrex
from coinbase import Coinbase


if __name__ == '__main__':
    coinbase = Coinbase(
        'cf3a26182673f04a6c14b525cf486538',
        'b/gZLAP70oEiGzmSPA998WWTXUY0X+Ip3eDPPNTRVlx+G9Tdv/cLBIQ8mLp3Le/7VzTgFPp/+8SrQtqBp0NoVQ==',
        'Ss132465798'
    )
    bittrex = Bittrex(
        "c439546abe26493ebb52cce3d9a4eeac",
        "ee05e7bde1ed461c806793a9289d370b"
    )

    USD_gdax = coinbase.getUSDBalance()
    print USD_gdax

    USD_bittrex = bittrex.get_USD_balance(coinbase.getPrice('BTC'))
    print USD_bittrex
    
    out = 3768 + 2000 + 8888 + 2100         # 2100 in gate.io
    total = USD_bittrex + USD_gdax + out

    print total

    # print 'Bittrex: ' + str(USD_bittrex) + ' ' + str(100 - int(USDT * 100 / USD_bittrex)) + '%'
    # print 'GDAX:    ' + str(USD_gdax)    + ' ' + str(100 - int(USD * 100 / USD_gdax)) + '%'
    # print 'out:     ' + str(out)   
    # print 'Total:   ' + str(total)       + ' ' + str(100 - int((USDT + USD) * 100 / (total - (3768 + 2000 + 8888 + 10000)))) + '%'















