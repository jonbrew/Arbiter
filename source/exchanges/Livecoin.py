import Const
from Exchange import Exchange
import requests

class Livecoin(Exchange):

	def __init__(self):
		super().__init__('Livecoin', 'https://api.livecoin.net')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/info/coinInfo')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins['info'] :
				if c['symbol'] == supported and c['walletStatus'] == 'normal' :
					self.prices[supported] = {}
					break

	def update_prices(self):
		ticker = requests.get(self.api_base+'/exchange/ticker')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for t in ticker :
				if t['symbol'] == c+'/'+Const.BTC :
					self.prices[c]['bid'] = float(t['best_bid'])
					self.prices[c]['ask'] = float(t['best_ask'])
					self.prices[c]['last'] = float(t['last'])
					break
