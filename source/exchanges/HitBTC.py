import Const
from Exchange import Exchange
import requests

class HitBTC(Exchange):

	def __init__(self):
		super().__init__('HitBTC', 'https://api.hitbtc.com')
		supported = [Const.STEEM, Const.DOGE, Const.DASH, Const.QTUM, 
					 Const.ETH, Const.BCH, Const.XRP, Const.ETC, Const.LTC, 
					 Const.XMR, Const.NXT, Const.ZEC, Const.REP, Const.DGB, 
					 Const.GNT, Const.OMG, Const.XEM, Const.TRX, Const.EOS, 
					 Const.ICX, Const.XVG, Const.XLM, Const.ADA, Const.VEN, 
					 Const.BTG, Const.LSK, Const.SC]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		ticker = requests.get(self.api_base+'/api/2/public/ticker')
		if ticker.status_code is Const.SC_OK :
			ticker = ticker.json()
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			for i in ticker :
				if i['symbol'] == c+Const.BTC:
					self.prices[c] = float(i['last'])
					break
