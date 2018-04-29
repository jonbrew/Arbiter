import Const
from Exchange import Exchange
import requests

class Huobi(Exchange):

	def __init__(self):
		super().__init__('Huobi', 'https://api.huobipro.com')
		self.prices = {}

	def update_coins(self):
		# TODO (This exchange postponed because it is not available in US)
		pass

	def update_prices(self):
		for c in self.get_coins() :
			ticker = requests.get(self.api_base+'/market/trade?symbol='+c.lower()+Const.BTC.lower())
			if ticker.status_code is Const.SC_OK :
				ticker = ticker.json()
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c] = float(ticker['tick']['data'][0]['price'])
