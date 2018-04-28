import Const
from Exchange import Exchange
import requests

class Bitfinex(Exchange):

	def __init__(self):
		super().__init__('Bitfinex', 'https://api.bitfinex.com')
		supported = [Const.ETH, Const.BCH, Const.XRP, Const.ETC, Const.LTC, 
					 Const.XMR, Const.ZEC, Const.REP, Const.GNT, Const.OMG, 
					 Const.TRX, Const.EOS, Const.BTG]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		for c in self.get_coins() :
			ticker = requests.get(self.api_base+'/v1/pubticker/'+c+Const.BTC)
			if ticker.status_code is 200 :
				ticker = ticker.json() 
			else :
				print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
				return
			self.prices[c] = float(ticker['ask'])
