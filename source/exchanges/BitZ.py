import Const
from Exchange import Exchange
import requests

class BitZ(Exchange):

	def __init__(self):
		super().__init__('BitZ', 'https://www.bit-z.com')
		supported = [Const.ETH, Const.BCH, Const.ETC, Const.LTC, 
					 Const.ZEC, Const.DASH, Const.DGB, Const.DOGE, 
					 Const.OMG, Const.TRX, Const.EOS, Const.QTUM, 
					 Const.BTG, Const.LSK]
		for c in supported :
			self.prices[c] = None

	def update_prices(self):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		ticker = requests.get(self.api_base+'/api_v1/tickerall', headers=headers)
		if ticker.status_code is 200 :
			ticker = ticker.json() 
		else :
			print(Const.BOLD+Const.FAIL+'Unable to reach '+self.name+' API'+Const.ENDC)
			return
		for c in self.get_coins() :
			self.prices[c] = float(ticker['data'][c.lower()+'_'+Const.BTC.lower()]['buy'])
