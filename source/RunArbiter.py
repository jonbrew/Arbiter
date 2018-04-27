#!/usr/bin/env python3
from exchanges import *
import time

if __name__ == "__main__":
	p = Poloniex()
	print(p.get_prices())
	