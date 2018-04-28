import Const
from exchanges import *
from threading import Thread

class Arbiter():

	def __init__(self):
		self.exchanges = [Binance(), BitZ(), Bitfinex(), Bitstamp(), Bittrex(), 
						  CexIO(), GDAX(), HitBTC(), Huobi(), Poloniex()]
		print(Const.HEADER+'Building thread pool...'+Const.ENDC)
		thread_pool = [Thread(target=e.update_prices,name=e.name) for e in self.exchanges]
		print(Const.HEADER+'Getting exchange price data...'+Const.ENDC)
		for t in thread_pool :
			t.start()
		for t in thread_pool :
			t.join()

		self.coins = [Const.ETH, Const.BCH, Const.XRP, Const.ETC, 
					  Const.LTC, Const.XMR, Const.NXT, Const.ZEC, 
					  Const.DASH, Const.REP, Const.SC, Const.DGB, 
					  Const.GNT, Const.DOGE, Const.OMG, Const.XEM, 
					  Const.TRX, Const.EOS, Const.ICX, Const.XVG, 
					  Const.XLM, Const.ADA, Const.VEN, Const.QTUM, 
					  Const.BTG, Const.LSK, Const.STEEM, Const.BTS]

		self.price_table = {}
		for c in self.coins :
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
		for c in self.price_table.keys() :
			supported_exchanges = [e for e in self.exchanges if c in e.prices and e.prices[c] is not None]
			if len(supported_exchanges) is 0 :
				continue
			spreads = sorted(supported_exchanges, key=lambda e,c1=c: e.prices[c1], reverse=True)
			low = spreads[-1].prices[c]
			high = spreads[0].prices[c]
			diff = ((high-low)/low)*100
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
					price = "{0:.8f}".format(e.prices[c])
					pct = "{0:.2f}".format(((e.prices[c]-low)/low)*100) + '%'
					print('| '+e.name.ljust(14)+'| '+price.ljust(14)+'| ', end='')
					if i is 0 :
						print(Const.OK+pct.ljust(9)+Const.ENDC+'|')
					else :
						print(pct.ljust(9)+'|')
				print('+---------------+---------------+----------+\n')
		if verbose :
			pct = "{0:.2f}".format(percent)
			print('Buy '+coin+' from '+buy_exchange.name+' at '+str(buy_exchange.prices[coin])+
				   '. Sell to '+sell_exchange.name+' at '+str(sell_exchange.prices[coin])+' for '+Const.OK+pct+'%'+Const.ENDC)
			print()
