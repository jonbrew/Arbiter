#!/usr/bin/env python3
from exchanges import *
from Arbiter import Arbiter
import time
import ccxt

if __name__ == "__main__":
	arbiter = Arbiter()
	opps = arbiter.calculate()
	arbiter.print_opportunities(opps)

