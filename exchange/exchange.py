class Exchange:
    def __init__(self, name):
        self.name = name
        self.market_bases = {'BTC', 'ETH', 'USDT'}
        self.dontTouch = {'XRP', 'XEM', 'BTC', 'DOGE', 'SC', 'NEO', 'ZEC', 'BTG', 'MONA', 'WINGS', 'USDT', 'IOTA', 'EOS', 'QTUM', 'ADA', 'XLM', 'LSK', 'BTS', 'XMR', 'DASH', 'SNT', 'BCC', 'BCH', 'SBTC', 'BCX', 'ETF', 'LTC', 'ETH'}

    def connect_success(self):
        print('connected %s' % self.name)

    def get_pair(self, coin, base):
        # return a the specific pair format for that exchange
        pass

    def get_BTC_price(self):
        pass

    def get_price(self, coin, base='BTC'):
        pass

    def get_full_balance(self):
        '''
        return format {
            'total': {
                'BTC': BTC_value,
                'USD': USD_value,
                'num': coin_num
            },
            'USD': { ... },
            coinName1: { ... },
            coinName2: { ... },
            ...
        }
        '''
        pass

    def get_coin_balance(self, allow_zero):
        '''
        return format {
            coinName1: num1,
            coinName2: num2,
            ...
        }
        '''
        pass

    def get_trading_pairs(self):
        '''
        return format: {
            'BTC': {'ADA', 'BAT', 'BTG', ...},
            'ETH': {'BAT', 'BNT', 'DNT', 'ETC', ...},
            'USDT': {'NEO', 'BTC', 'LTC', ...}
            ...
        }
        '''
        pass

    def market_buy(self, coin, base, quantity):
        pass

    def market_sell(self, coin, base, quantity):
        pass

    def buy_all(self, USD_price):
        pass

    def sell_all(self):
        pass







