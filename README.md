## Introduction
Coinbot is a cryptocurrency trading operating system.<br>

Being a cryptocurrency lover and technology enthusiast, I implemented this smart bot for researching and learning purpose (also for fun!).<br>

Using it arbitrarily is risky, and could potentially lose real money! Don't import your API keys until you had examine the code and comfirmed it worked! If you are looking for a public library with more robust and comprehensive functionality, check [this](https://github.com/ccxt/ccxt) out!

## Functionalities

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


## Supported Exchanges
- Coinbase [U.S.]
- Bittrex [U.S.]
- Huobi [China]
- Binance [Japan]
- Gate [China]
- Dew [?]
- Bithumb [South Korea]
- Bifinex [British Virgin Islands] (coming soon)
- Kraken [U.S.] (coming soon)
- Okex [China] (coming soon)  


## Run
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

- start to command line interface<br>
`make run`

- other functionalities<br>
Makefile only wrapped some most commonly used operations, for other functionalities we can modify the code and call them directly!


# Author
Shunji Zhan
