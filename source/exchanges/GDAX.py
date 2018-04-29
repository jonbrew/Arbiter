import Const
from Exchange import Exchange
import requests

class GDAX(Exchange):

	def __init__(self):
		super().__init__('GDAX', 'https://api.gdax.com')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/products')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins :
				if c['id'] == supported+'-'+Const.BTC and c['status'] == 'online' :
					self.prices[supported] = None
	
	def update_prices(self):
		for c in self.get_coins() :
			ticker = requests.get(self.api_base+'/products/'+c+'-'+Const.BTC+'/ticker')
			if ticker.status_code is Const.SC_OK :
				ticker = ticker.json()
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c] = float(ticker['price'])
