import Const
from Exchange import Exchange
import requests

class GDAX(Exchange):

	def __init__(self):
		super().__init__('GDAX', 'https://api.gdax.com')
		supported = [Const.ETH, Const.BCH, Const.LTC]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		for c in self.get_coins() :
			ticker = requests.get(self.api_base+'/products/'+c+'-'+Const.BTC+'/ticker')
			if ticker.status_code is Const.SC_OK :
				ticker = ticker.json()
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c] = float(ticker['price'])
