import Const
from Exchange import Exchange
import requests

class CexIO(Exchange):

	def __init__(self):
		super().__init__('CexIO', 'https://cex.io')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/api/tickers/BTC')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins['data'] :
				if c['pair'] == supported+':'+Const.BTC :
					self.prices[supported] = None

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api/tickers/BTC')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for d in ticker['data'] :
				if d['pair'] == c+':'+Const.BTC :
					self.prices[c] = float(d['last'])
					break
