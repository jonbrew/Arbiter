import Const
from Exchange import Exchange
import requests

class Poloniex(Exchange):

	def __init__(self):
		super().__init__('Poloniex', 'https://poloniex.com')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/public?command=returnCurrencies')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			if supported in coins and coins[supported]['disabled'] == 0 :
				self.prices[supported] = {}

	def update_prices(self):
		ticker = requests.get(self.api_base+'/public?command=returnTicker')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			self.prices[c]['bid'] = float(ticker[Const.BTC+'_'+c]['highestBid'])
			self.prices[c]['ask'] = float(ticker[Const.BTC+'_'+c]['lowestAsk'])
			self.prices[c]['last'] = float(ticker[Const.BTC+'_'+c]['last'])
