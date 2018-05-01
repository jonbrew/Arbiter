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
					break
		# Manually remove deposit/withdraw paused coins
		self.prices.pop(Const.ADA)
	
	def update_prices(self):
		ticker = requests.get(self.api_base+'/api2/1/tickers')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			pair = c.lower()+'_'+Const.BTC.lower()
			ticker = requests.get(self.api_base+'/api2/1/orderBook/'+pair)
			if ticker.status_code is Const.SC_OK :
				ticker = ticker.json()
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c]['bid'] = float(ticker['bids'][0][0])
			self.prices[c]['ask'] = float(ticker['asks'][-1][0])
			self.prices[c]['last'] = float(ticker['bids'][0][0])
