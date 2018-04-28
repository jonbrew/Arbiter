import Const
from Exchange import Exchange
import requests

class Bitstamp(Exchange):

	def __init__(self):
		super().__init__('Bitstamp', 'https://www.bitstamp.net')
		supported = [Const.ETH, Const.BCH, Const.XRP, Const.LTC]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		for c in self.get_coins() :
			ticker = requests.get(self.api_base+'/api/v2/ticker/'+c.lower()+Const.BTC.lower())
			if ticker.status_code is 200 :
				ticker = ticker.json() 
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c] = float(ticker['last'])
