import Const
from Exchange import Exchange
import requests

class Kucoin(Exchange):

	def __init__(self):
		super().__init__('Kucoin', 'https://api.kucoin.com')
		self.prices = {}

	def update_coins(self):
		self.prices.clear()
		for supported in Const.COINS :
			coins = requests.get(self.api_base+'/v1/market/open/coin-info?coin='+supported)
			if coins.status_code is Const.SC_OK :
				coins = coins.json()
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			if coins['success'] and coins['data']['enableWithdraw'] and coins['data']['enableDeposit'] :
				self.prices[supported] = {}

	def update_prices(self):
		ticker = requests.get(self.api_base+'/v1/open/tick')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for t in ticker['data'] :
				if t['symbol'] == c+'-'+Const.BTC :
					self.prices[c]['bid'] = float(t['buy'])
					self.prices[c]['ask'] = float(t['sell'])
					self.prices[c]['last'] = float(t['lastDealPrice'])
					break
