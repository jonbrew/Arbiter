import Const
from Exchange import Exchange
import requests

class Poloniex(Exchange):

	def __init__(self):
		super().__init__('Poloniex', 'https://poloniex.com')
		supported = [Const.ETH, Const.BCH, Const.XRP, Const.ETC,
					 Const.LTC, Const.XMR, Const.NXT, Const.ZEC, Const.DASH, 
					 Const.REP, Const.SC, Const.DGB, Const.GNT, Const.DOGE, 
					 Const.OMG, Const.XEM]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		ticker = requests.get(self.api_base+'/public?command=returnTicker')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			self.prices[c] = float(ticker[Const.BTC+'_'+c]['highestBid'])
