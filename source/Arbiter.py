import sys
import Const
from exchanges import *
from threading import Thread
from Utils import pct_inc

class Arbiter():

	def __init__(self):
		self.exchanges = [Binance(), Bitfinex(), Bitstamp(), Bittrex(), CexIO(),
						  GDAX(), GateIO(), HitBTC(), Kraken(), Poloniex()]
		self.bot_exchanges = [Binance(), Bitfinex(), Bitstamp(), Bittrex(), 
						      GDAX(), GateIO(), HitBTC(), Kraken(), Poloniex()]
		print(Const.HEADER+'Building thread pool...'+Const.ENDC)
		thread_pool = [Thread(target=e.update,name=e.name) for e in self.exchanges]
		print(Const.HEADER+'Getting exchange price data...'+Const.ENDC)
		for t in thread_pool :
			t.start()
		for t in thread_pool :
			t.join()

		self.price_table = {}
		for c in Const.COINS :
			self.price_table[c] = {}
			for e in self.exchanges :
				if c in e.prices :
					self.price_table[c][e.name] = e.prices[c]

	def calculate(self, verbose):
		print(Const.HEADER+'Calculating arbitrage opportunities...'+Const.ENDC)
		buy_exchange = None
		sell_exchange = None
		coin = None
		percent = -1
		for c in Const.COINS :
			supported_exchanges = [e for e in self.exchanges if c in e.prices and e.prices[c]]
			if len(supported_exchanges) is 0 :
				continue
			min_ask = sys.float_info.max
			for e in supported_exchanges :
				if e.prices[c]['ask'] < min_ask :
					min_ask = e.prices[c]['ask']
			spreads = sorted(supported_exchanges, key=lambda e,c=c,min_ask=min_ask: pct_inc(min_ask,e.prices[c]['bid']), reverse=True)
			diff = pct_inc(spreads[-1].prices[c]['ask'],spreads[0].prices[c]['bid'])
			if diff > percent :
				buy_exchange = spreads[-1]
				sell_exchange = spreads[0]
				coin = c
				percent = diff
			if verbose :
				print('+---------------+---------------+----------+')
				print('|'+Const.YELL+c.center(42)+Const.ENDC+'|')
				print('+---------------+---------------+----------+')
				for i,e in enumerate(spreads) :
					price = "{0:.8f}".format(e.prices[c]['last'])
					pct = "{0:.2f}".format(pct_inc(min_ask,e.prices[c]['bid']))+'%'
					print('| '+e.name.ljust(14)+'| '+price.ljust(14)+'| ', end='')
					if i is 0 :
						print(Const.OK+pct.ljust(9)+Const.ENDC+'|')
					else :
						print(pct.ljust(9)+'|')
				print('+---------------+---------------+----------+\n')
		if verbose :
			pct = "{0:.2f}".format(percent)
			print('Buy '+coin+' from '+buy_exchange.name+' at '+str(buy_exchange.prices[coin]['ask'])+
				   '. Sell to '+sell_exchange.name+' at '+str(sell_exchange.prices[coin]['bid'])+' for '+Const.OK+pct+'%'+Const.ENDC)
			print()
