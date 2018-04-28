import Const
from Exchange import Exchange
import requests

class Binance(Exchange):

	def __init__(self):
		super().__init__('Binance', 'https://api.binance.com')
		supported = [Const.ETH, Const.XRP, Const.ETC, Const.LTC, Const.XMR, 
					 Const.ZEC, Const.DASH, Const.GNT, Const.OMG, Const.XEM, 
					 Const.TRX, Const.EOS, Const.ICX, Const.XVG, Const.XLM, 
					 Const.ADA, Const.VEN, Const.QTUM, Const.BTG, Const.LSK, 
					 Const.STEEM, Const.BTS]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api/v3/ticker/price')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for i in ticker :
				if i['symbol'] == c+Const.BTC:
					self.prices[c] = float(i['price'])
					break
