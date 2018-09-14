import Const
from Exchange import Exchange
import requests

# Removed due to bad API and no withdraw endpoint
class BitZ(Exchange):

	def __init__(self):
		super().__init__('BitZ', 'https://www.bit-z.com')
		self.prices = {}
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/api_v1/tickerall', headers=self.headers)
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			if supported.lower()+'_'+Const.BTC.lower() in coins['data'] :
				self.prices[supported] = {}

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api_v1/tickerall', headers=self.headers)
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			self.prices[c] = float(ticker['data'][c.lower()+'_'+Const.BTC.lower()]['buy'])
