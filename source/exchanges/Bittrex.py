import Const
from Exchange import Exchange
import requests

class Bittrex(Exchange):

	def __init__(self):
		super().__init__('Bittrex', 'https://bittrex.com')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/api/v1.1/public/getcurrencies')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			for c in coins['result'] :
				if c['Currency'] == supported and c['IsActive'] :
					self.prices[supported] = {}
					break

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api/v1.1/public/getmarketsummaries')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for r in ticker['result'] :
				if r['MarketName'] == Const.BTC+'-'+c :
					self.prices[c]['bid'] = float(r['Bid'])
					self.prices[c]['ask'] = float(r['Ask'])
					self.prices[c]['last'] = float(r['Last'])
					break
