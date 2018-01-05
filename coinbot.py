import pprint as pp
from bittrex import Bittrex
from coinbase import Coinbase
from binance import Binance


def cang(cash, total):
    return str(100 - int(cash * 100 / total)) + '%'


def getGateInfo():
    with open('gate.txt') as f:
        return int(float(f.read()))


if __name__ == '__main__':
    coinbase = Coinbase(
        'ad8327c971400a583a511c8b44153c3b',
        '4oc5G42pHNRGf6fxBhL+JE3bwKH54SothrVzCVwgBD7dxdj/PLWz2rrBYx3f9V3/lh3Cj2vLzMfsXIvmv5W1mg==',
        '5rngcof6sug'
    )

    bittrex = Bittrex(
        "f4a53cc750174691bb8a26adf5b9d732",
        "74cdede4f6a34ae88e782b339fdf2830"
    )

    binance = Binance(
        'N0VUiMGmgZRXsEJyEEyXNITGZAELNfPIZyzzcTOSwV7q9MhZt6Mt7SFFdzERZgB5',
        '7A6ZwSIwsfdWVnTSgK0Gc2JzAU2k5snEHf9DQuyM7VCNC4FykC14qxNxQmmyUhDU'
    )

    out = 3768 + 2000 + 8888 + 8338
    print 'Out:     %d' % out

    USD_gate, cash_gate = getGateInfo(), 0
    print 'gate.io: %s, %s' % (USD_gate, cang(cash_gate, USD_gate))

    # USD_gdax, cash_gdax = coinbase.getUSDBalance()
    USD_gdax, cash_gdax = 60419, 60419
    print 'GDAX:    %s, %s' % (USD_gdax, cang(cash_gdax, USD_gdax))

    USD_bittrex, cash_bittrex = bittrex.get_USD_balance(coinbase.getPrice('BTC'))
    print 'Bittrex: %s, %s' % (USD_bittrex, cang(cash_bittrex, USD_bittrex))

    USD_binance, cash_binance = binance.get_USD_balance()
    print 'Binance: %s, %s' % (USD_binance, cang(cash_binance, USD_binance))

    real_total = USD_bittrex + USD_gdax + USD_binance + USD_gate
    USD_total = int(real_total + out)
    cash_total = cash_gdax + cash_bittrex + cash_gate + cash_binance
    print 'Total:   %s, %s, %.3f' % (USD_total, cang(cash_total, real_total), USD_total / 38888.0)

















