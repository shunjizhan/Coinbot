# Introduction
Coinbot is a cryptocurrency trading bot, which aims to manage accounts across all exchanges, and provide efficient view/trade/monitor/transfer operations, ALL IN ONE PLACE. <br>

Based on these basic operations, we can conveniently build our own high level strategies, such as stop-limit order, batch buy/sell, hedging, and quantitative trading. <br>

# Note
Being a cryptocurrency lover and technology enthusiast, I implemented this cute bot for researching and learning purpose (also for fun ^_^). Using it arbitrarily could be risky, and could potentially lose real money, so be vigilant!<br>

If you are looking for a public library with more robust and comprehensive functionality, check [ccxt](https://github.com/ccxt/ccxt) out!

# Functionalities
### Basic
- view current exchange rate of any token pair in any exchange
- view quoted depths of any token pair in any exchange
- view any of your cryptocurrency balance in any exchange
- view your combined cryptocurrency balances in some/all exchanges
- calculate your fiat currency balance in any exchange
- calculate your combined fiat currency balances in some/all exchanges

### Advanced
- buy/sell any cryptocurrency in any exchange
- batch buy/sell cryptocurrencies in any exchange
- monitor price difference of any pair of tokens across some/all exchanges
- transfer your token from one exchange to another (highly risky! manual transfer recommended)

### Pro (alpha)
- interest arbitrage across some/all exchanges, with different strategies, such as "brick moving" (low efficiency) or hedging (high efficiency)
- quantitative trading in any exchange, with customized parameters


# Supported Exchanges
| Logo     | Exchange     | Location     | Fiat Currency Support | Remark   |
| :------: | :------: | :------: | :------: |:------: |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/gdax.jpg?raw=true) | Coinbase | U.S. | Yes  |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/bittrex.jpg?raw=true) | Bittrex | U.S. | No  |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/huobi.jpg?raw=true) | Huobi | China | No  |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/binance.jpg?raw=true) | Binance | Japan |  No |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/dew.jpg?raw=true) | Dew | ? | No  |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/bitfinex.jpg?raw=true) | Bitfinex | British Virgin Islands | Yes   | coming soon  |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/gate.jpg?raw=true) | Gate | China | No  |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/bithumb.jpg?raw=true) | Bithumb | South Korea | Yes  |    |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/kraken.jpg?raw=true) | Kraken | U.S. | Yes   | coming soon  |
| ![](https://raw.githubusercontent.com/shunjizhan/Coinbot/master/img/okex.jpg?raw=true) | Okex | China |  No  | coming soon  |

credit: some icons are from ccxt.



# Run
### import API keys
in root folder create a `keys.json` with format:
```
{
    "coinbase": {
        "key": "",
        "secret": "",
        "pass": ""
    },
    "bittrex": {
        "key": "",
        "secret": ""
    },
    "binance": {
        "key": "",
        "secret": ""
    },
    "gate": {
        "key": "",
        "secret": ""
    },
    "bithumb": {
        "key": "",
        "secret": ""
    },
    "huobi": {
        "key": "",
        "secret": ""
    }
}
```

### install
`make install`

### view/trade
- get USD balance in all exchanges<br>
`make`

- get detailed tokens and USD balances in all exchanges<br>
`make full`

- start to monitor price difference<br>
`make diff`

- start the command line interface<br>
`make run`

- other functionalities<br>
Makefile only wrapped some most commonly used operations, for other functionalities we can modify the code and call them directly!


# Author
Shunji Zhan
