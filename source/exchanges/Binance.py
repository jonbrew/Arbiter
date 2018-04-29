import Const
from Exchange import Exchange
import requests

class Binance(Exchange):

	def __init__(self):
		super().__init__('Binance', 'https://api.binance.com')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/api/v1/exchangeInfo')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins['symbols'] :
				if c['symbol'] == supported+Const.BTC and c['status'] == 'TRADING' :
					self.prices[supported] = None

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api/v3/ticker/price')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for i in ticker :
				if i['symbol'] == c+Const.BTC:
					self.prices[c] = float(i['price'])
					break
