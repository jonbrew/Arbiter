import Const
from Exchange import Exchange
import requests

class GateIO(Exchange):

	def __init__(self):
		super().__init__('GateIO', 'http://data.gate.io')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/api2/1/pairs')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins :
				if c == supported.lower()+'_'+Const.BTC.lower() :
					self.prices[supported] = {}
	
	def update_prices(self):
		ticker = requests.get(self.api_base+'/api2/1/tickers')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			pair = c.lower()+'_'+Const.BTC.lower()
			self.prices[c]['bid'] = float(ticker[pair]['highestBid'])
			self.prices[c]['ask'] = float(ticker[pair]['lowestAsk'])
			self.prices[c]['last'] = float(ticker[pair]['last'])
			