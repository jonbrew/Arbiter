import sys
import time
import Const
from exchanges import *
from threading import Thread
from Utils import pct_inc

class Arbiter():

	def __init__(self):
		self.exchanges = [Binance(), Bitstamp(), Bittrex(), 
						  GDAX(), GateIO(), HitBTC(), Kraken(), 
						  Livecoin(), Poloniex()]
		thread_pool = [Thread(target=e.update,name=e.name) for e in self.exchanges]		
		for t in thread_pool :
			t.start()
		for t in thread_pool :
			t.join()

	def calculate(self):
		coin_opportunities = []
		for c in Const.COINS :
			supported_exchanges = [e for e in self.exchanges if c in e.prices and e.prices[c]]
			if len(supported_exchanges) is 0 :
				continue
			min_ask = sys.float_info.max
			for e in supported_exchanges :
				if e.prices[c]['ask'] < min_ask :
					min_ask = e.prices[c]['ask']
			spreads = sorted(supported_exchanges, key=lambda e,c=c,min_ask=min_ask: pct_inc(min_ask,e.prices[c]['bid']), reverse=True)
			coin_opportunities.append((c,spreads))				
		coin_opportunities = sorted(coin_opportunities, key=lambda o: pct_inc(o[1][-1].prices[o[0]]['ask'],o[1][0].prices[o[0]]['bid']), reverse=True)
		return coin_opportunities

	def print_opportunities(self, opportunities) :
		for spreads in reversed(opportunities) :
			c = spreads[0]
			exchanges = spreads[1]
			print('+---------------+---------------+----------+')
			print('|'+Const.YELL+c.center(42)+Const.ENDC+'|')
			print('+---------------+---------------+----------+')
			min_ask = exchanges[-1].prices[c]['ask']
			for i,e in enumerate(exchanges) :
				price = "{0:.8f}".format(e.prices[c]['ask']) if i == len(exchanges)-1 else "{0:.8f}".format(e.prices[c]['bid'])
				pct = "{0:.2f}".format(pct_inc(min_ask,e.prices[c]['bid']))+'%'
				print('| '+e.name.ljust(14)+'| '+price.ljust(14)+'| ', end='')
				if i is 0 :
					print(Const.OK+pct.ljust(9)+Const.ENDC+'|')
				else :
					print(pct.ljust(9)+'|')
			print('+---------------+---------------+----------+\n')
		coin = opportunities[0][0]
		buy_exchange = opportunities[0][1][-1]
		sell_exchange = opportunities[0][1][0]
		percent = "{0:.2f}".format(pct_inc(buy_exchange.prices[coin]['ask'],sell_exchange.prices[coin]['bid']))
		print('Buy '+coin+' from '+buy_exchange.name+' at '+str(buy_exchange.prices[coin]['ask'])+
			   '. Sell to '+sell_exchange.name+' at '+str(sell_exchange.prices[coin]['bid'])+' for '+Const.OK+percent+'%'+Const.ENDC)
		print()
	
	def log_opportunities(self, opportunities) :
		coin = opportunities[0][0]
		buy_exchange = opportunities[0][1][-1]
		sell_exchange = opportunities[0][1][0]
		percent = "{0:.2f}".format(pct_inc(buy_exchange.prices[coin]['ask'],sell_exchange.prices[coin]['bid']))
		log = open('../logs/log.txt','a+')
		log.write(time.strftime('%a %H:%M:%S')+': Buy '+coin+' from '+buy_exchange.name+' at '+str(buy_exchange.prices[coin]['ask'])+
			   '. Sell to '+sell_exchange.name+' at '+str(sell_exchange.prices[coin]['bid'])+' for '+percent+'%\n')
		log.close()

	def update_exchange_prices(self) :
		for e in self.exchanges :
			e.update_prices()

	def update_exchanges(self) :
		for e in self.exchanges :
			e.update()
