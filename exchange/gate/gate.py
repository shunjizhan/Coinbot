#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from .HttpUtil import httpGet, httpPost
from ..exchange import Exchange


class Gate(Exchange):
    def __init__(self, apikey, secretkey):
        self.api = GateAPI(apikey, secretkey)
        super().__init__('gate')
        self.connect_success()

    def get_pair(self, coin, base):
        return '%s_%s' % (coin, base)

    def get_price(self, coin, base='BTC', _type=0):
        TYPES = {0: 'highestBid', 1: 'lowestAsk', 2: 'last'}
        pair = self.get_pair(coin, base)
        ticker = self.api.ticker(pair)[TYPES[_type]]
        return float(ticker) if ticker else 0

    def get_full_balance(self, allow_zero=False):
        balances = json.loads(self.api.balances())['available']
        ETH_price = float(self.api.ticker('eth_usdt')['last'])
        BTC_price = float(self.api.ticker('btc_usdt')['last'])

        coins = {
            'total': {'BTC': 0, 'USD': 0, 'num': 0},
            'USD': {'BTC': 0, 'USD': 0, 'num': 0}
        }
        for coinName in balances:
            num = float(balances[coinName])
            if allow_zero or num > 0:
                if coinName == 'USDT':
                    coinName = 'USD'
                    USD_value = num
                elif coinName == 'BTC':
                    USD_value = num / BTC_price
                elif coinName in {'FIL', 'ETH'}:
                    USD_value = num * float(self.api.ticker('FIL_usdt')['last'])
                else:
                    pair = '%s_eth' % coinName
                    price_in_USD = float(self.api.ticker(pair)['last']) * ETH_price
                    USD_value = price_in_USD * num
                BTC_value = USD_value / BTC_price

                # update info
                coins[coinName] = {
                    'num': num,
                    'BTC': BTC_value,
                    'USD': USD_value
                }
                coins['total']['BTC'] += BTC_value
                coins['total']['USD'] += USD_value
        return coins

    def get_all_coin_balance(self, allow_zero=False):
        balances = json.loads(self.api.balances())['available']
        coins = {}
        for coinName in balances:
            num = float(balances[coinName])
            if coinName == 'USDT':
                coinName = 'USD'
            if allow_zero or num > 0:
                coins[coinName] = num
        return coins

    def get_trading_pairs(self):
        markets = {}
        for base in self.market_bases:
            markets[base] = set()
            gate_markets = self.api.pairs()
            for pair in gate_markets:
                coin, gate_base = pair.split('_')
                if gate_base.upper() == base:
                    markets[base].add(coin.upper())
        return markets


# ------------------------------------------------------------------ #
# --------------------------- API Wrapper -------------------------- #
# ------------------------------------------------------------------ #
class GateAPI(Exchange):
    def __init__(self, apikey, secretkey):
        self.__url = 'data.gate.io'
        self.__apikey = apikey
        self.__secretkey = secretkey

    # 所有交易对
    def pairs(self):
        URL = "/api2/1/pairs"
        params = ''
        return httpGet(self.__url, URL, params)

    # 市场订单参数
    def marketinfo(self):
        URL = "/api2/1/marketinfo"
        params = ''
        return httpGet(self.__url, URL, params)

    # 交易市场详细行情
    def marketlist(self):
        URL = "/api2/1/marketlist"
        params = ''
        return httpGet(self.__url, URL, params)

    # 所有交易行情
    def tickers(self):
        URL = "/api2/1/tickers"
        params = ''
        return httpGet(self.__url, URL, params)

    # 单项交易行情
    def ticker(self, param):
        URL = "/api2/1/ticker"
        return httpGet(self.__url, URL, param)

    # 所有交易对市场深度
    def orderBooks(self):
        URL = "/api2/1/orderBooks"
        param = ''
        return httpGet(self.__url, URL, param)

    # 单项交易对市场深度
    def orderBook(self, param):
        URL = "/api2/1/orderBook"
        return httpGet(self.__url, URL, param)

    # 历史成交记录
    def tradeHistory(self, param):
        URL = "/api2/1/tradeHistory"
        return httpGet(self.__url, URL, param)

    # 获取帐号资金余额
    def balances(self):
        URL = "/api2/1/private/balances"
        param = {}
        return httpPost(self.__url, URL, param, self.__apikey, self.__secretkey)

    # 获取充值地址
    def depositAddres(self, param):
        URL = "/api2/1/private/depositAddress"
        params = {'currency': param}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 获取充值提现历史
    def depositsWithdrawals(self, start, end):
        URL = "/api2/1/private/depositsWithdrawals"
        params = {'start': start, 'end': end}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 买入
    def buy(self, currencyPair, rate, amount):
        URL = "/api2/1/private/buy"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 卖出
    def sell(self, currencyPair, rate, amount):
        URL = "/api2/1/private/sell"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 取消订单
    def cancelOrder(self, orderNumber, currencyPair):
        URL = "/api2/1/private/cancelOrder"
        params = {'orderNumber': orderNumber, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 取消所有订单
    def cancelAllOrders(self, type, currencyPair):
        URL = "/api2/1/private/cancelAllOrders"
        params = {'type': type, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 获取下单状态
    def getOrder(self, orderNumber, currencyPair):
        URL = "/api2/1/private/getOrder"
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 获取我的当前挂单列表
    def openOrders(self):
        URL = "/api2/1/private/openOrders"
        params = {}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 获取我的24小时内成交记录
    def mytradeHistory(self, currencyPair, orderNumber):
        URL = "/api2/1/private/tradeHistory"
        params = {'currencyPair': currencyPair, 'orderNumber': orderNumber}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 提现
    def withdraw(self, currency, amount, address):
        URL = "/api2/1/private/withdraw"
        params = {'currency': currency, 'amount': amount, 'address': address}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)
