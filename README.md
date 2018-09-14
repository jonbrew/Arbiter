# Arbiter

  A script for determining crypto arbitrage opportunities across 9 exchanges and 27 currencies. Arbitrage opportunities are printed to the console in sorted order and a log is kept of the top opportunities for each update. Updates are run every 30 seconds and the log can be found in `logs/log.txt`. Arbitrage opportunities are calculated using the minimum ask price compared to the highest bid price, so this reflects an immediate buying and selling opportunity and more beneficial spreads can be achieved through smarter trading. The goal of this project was to eventually create a trading bot, however this project as is reveals that arbitrage opportunities just aren't that great. 

### Supported Exchanges (Can be modified in the constructor of Arbiter.py)
* Binance
* Bitstamp
* Bittrex
* GDAX
* GateIO
* HitBTC
* Kraken
* Livecoin
* Poloniex

### Supported Currencies (Can be modified Const.py)
* STEEM
* DASH
* QTUM
* ETH	
* BCH	
* LTC	
* XRP	
* ETC	
* XMR	
* NXT	
* ZEC	
* BTS	
* REP	
* DGB	
* GNT	
* OMG	
* XEM	
* TRX	
* EOS	
* XVG	
* XLM	
* ADA	
* VEN	
* BTG	
* LSK	
* NEO	
* OAX	

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
Python 3.5
pip
virtualenv
```

### Installing

```
cd Arbiter/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running
 ```
 chmod+x source/RunArbiter.py
 make run
 ```

## Authors

* **Jon Brewer** (https://github.com/jonbrew)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
