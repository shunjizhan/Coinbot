import pprint as pp
from bittrex import Bittrex
from coinbase import Coinbase
from binance import Binance
from gate.GateIO import GateIO


def cang(cash, total):
    return str(100 - int(cash * 100 / total)) + '%'


if __name__ == '__main__':
    # coinbase = Coinbase(
    #     'cf3a26182673f04a6c14b525cf486538',
    #     'b/gZLAP70oEiGzmSPA998WWTXUY0X+Ip3eDPPNTRVlx+G9Tdv/cLBIQ8mLp3Le/7VzTgFPp/+8SrQtqBp0NoVQ==',
    #     'Ss132465798'
    # )

    # bittrex = Bittrex(
    #     "c439546abe26493ebb52cce3d9a4eeac",
    #     "ee05e7bde1ed461c806793a9289d370b"
    # )

    # binance = Binance(
    #     'N0VUiMGmgZRXsEJyEEyXNITGZAELNfPIZyzzcTOSwV7q9MhZt6Mt7SFFdzERZgB5',
    #     '7A6ZwSIwsfdWVnTSgK0Gc2JzAU2k5snEHf9DQuyM7VCNC4FykC14qxNxQmmyUhDU'
    # )

    gate = GateIO(
        '822FF026-1E61-47A7-92E0-780E0FD27268', 
        'c7b250bc2ddec59a059f782495123e60b4264207cbe6304a00e9b5d840ae88a7'
    )
    print (gate.balances())

    # out = 3768 + 2000 + 8888
    # print 'out:     %d' % out

    # USD_gdax, cash_gdax = coinbase.getUSDBalance()
    # print 'GDAX:    %s, %s' % (USD_gdax, cang(cash_gdax, USD_gdax))

    # USD_bittrex, cash_bittrex = bittrex.get_USD_balance(coinbase.getPrice('BTC'))
    # print 'Bittrex: %s, %s' % (USD_bittrex, cang(cash_bittrex, USD_bittrex))

    # USD_binance, cash_binance = binance.get_USD_balance()
    # print 'Binance: %s, %s' % (USD_binance, cang(cash_binance, USD_binance))

    # USD_gate, cash_gate = 2100, 0
    # print 'gate.io: %s, %s' % (USD_gate, cang(cash_gate, USD_gate))

    # real_total = USD_bittrex + USD_gdax + USD_gate
    # USD_total = real_total + out
    # cash_total = cash_gdax + cash_bittrex + cash_gate
    # print 'Total:   %s, %s' % (USD_total, cang(cash_total, real_total))

















