class Exchange:
    def __init__(self, name):
        self.name = name
        self.market_bases = {'BTC', 'ETH', 'USDT'}

    def connect_success(self):
        print('connected %s' % self.name)

    def get_pair(self, coin, base):
        # return a the specific pair format for that exchange
        pass

    def get_BTC_price(self):
        pass

    def get_price(self, coin, base='BTC'):
        pass

    def get_coin_balance(self):
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







