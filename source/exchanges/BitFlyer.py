import Const
from Exchange import Exchange
import requests

class Poloniex(Exchange):

	def __init__(self):
		super().__init__('Poloniex', 'https://poloniex.com')
		ticker = requests.get(self.api_base+'/public?command=returnTicker').json()
		supported = [Const.BTC, Const.ETH, Const.STR, Const.BCH, Const.XRP, Const.ETC, 
					Const.LTC, Const.XMR, Const.NXT, Const.ZEC, Const.DASH, Const.REP]
		for c in supported :
			self.prices[c] = ticker[Const.USDT+'_'+c]['highestBid']

	def update_prices(self):
		ticker = requests.get(self.api_base+'/public?command=returnTicker').json()
		for c in self.get_currencies() :
			self.prices[c] = ticker[Const.USDT+'_'+c]['highestBid']
