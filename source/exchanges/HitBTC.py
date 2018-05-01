import Const
from Exchange import Exchange
import requests

class HitBTC(Exchange):

	def __init__(self):
		super().__init__('HitBTC', 'https://api.hitbtc.com')
		self.prices = {}

	def build(self):
		self.update_coins()
		self.update_prices()

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/api/2/public/currency')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins :
				if c['id'] == supported and c['payoutEnabled'] and c['payinEnabled']:
					self.prices[supported] = {}
					break

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api/2/public/ticker')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for i in ticker :
				if i['symbol'] == c+Const.BTC:
					self.prices[c]['bid'] = float(i['bid'])
					self.prices[c]['ask'] = float(i['ask'])
					self.prices[c]['last'] = float(i['last'])
					break
