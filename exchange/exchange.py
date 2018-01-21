class Exchange:
    def __init__(self, name):
        self.name = name

    def connect_success(self):
        print('connected %s' % self.name)

    def get_BTC_price(self):
        pass

    def get_price(self, coin, base='BTC'):
        pass

    def get_coin_balance(self):
        pass

    def get_trading_pairs(self):
        pass
