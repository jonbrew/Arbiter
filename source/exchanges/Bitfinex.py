import Const
from Exchange import Exchange
import requests

class Bitfinex(Exchange):

	def __init__(self):
		super().__init__('Bitfinex', 'https://api.bitfinex.com')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/v1/symbols')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins :
				if c == supported.lower()+Const.BTC.lower():
					self.prices[supported] = {}
					break

	def update_prices(self):
		for c in self.get_coins() :
			ticker = requests.get(self.api_base+'/v1/pubticker/'+c+Const.BTC)
			if ticker.status_code is Const.SC_OK :
				ticker = ticker.json()
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c]['bid'] = float(ticker['bid'])
			self.prices[c]['ask'] = float(ticker['ask'])
			self.prices[c]['last'] = float(ticker['last_price'])
