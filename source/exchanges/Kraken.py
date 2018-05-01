import Const
from Exchange import Exchange
import requests

class Kraken(Exchange):

	def __init__(self):
		super().__init__('Kraken', 'https://api.kraken.com')
		self.prices = {}
		self.pairs = {'DASHBTC':'DASHXBT', 'ETHBTC':'XETHXXBT', 'BCHBTC':'BCHXBT',
					  'XRPBTC':'XXRPXXBT', 'ETCBTC':'XETCXXBT', 'LTCBTC':'XLTCXXBT',
					  'XMRBTC':'XXMRXXBT', 'ZECBTC':'XZECXXBT', 'REPBTC':'XREPXXBT',
					  'EOSBTC':'EOSXBT', 'XLMBTC':'XXLMXXBT'}

	def update_coins(self):
		self.prices.clear()
		coins = requests.get(self.api_base+'/0/public/AssetPairs')
		if coins.status_code is Const.SC_OK :
			coins = coins.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for supported in Const.COINS :
			if supported+Const.BTC in self.pairs and self.pairs[supported+Const.BTC] in coins['result'] :
				self.prices[supported] = {}

	def update_prices(self):
		param = ''
		for c in self.get_coins() :
			param += self.pairs[c+Const.BTC]+','
		param = param[:-1]
		ticker = requests.get(self.api_base+'/0/public/Ticker?pair='+param)
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			self.prices[c]['bid'] = float(ticker['result'][self.pairs[c+Const.BTC]]['b'][0])
			self.prices[c]['ask'] = float(ticker['result'][self.pairs[c+Const.BTC]]['a'][0])
			self.prices[c]['last'] = float(ticker['result'][self.pairs[c+Const.BTC]]['c'][0])
