#!/usr/bin/env python3
from exchanges import *
from Arbiter import Arbiter
import Const
import time
import ccxt

if __name__ == "__main__":
	print(Const.HEADER+'Getting exchange price data...'+Const.ENDC)
	arbiter = Arbiter()
	while(True) :
		print(Const.HEADER+'Calculating arbitrage opportunities...'+Const.ENDC)
		opportunities = arbiter.calculate()
		arbiter.log_opportunities(opportunities)
		arbiter.print_opportunities(opportunities)
		time.sleep(30)
		print(Const.HEADER+'Getting exchange price data...'+Const.ENDC)
		arbiter.update_exchange_prices()

