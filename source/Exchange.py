from abc import ABC, abstractmethod

class Exchange(ABC):

	def __init__(self, name, api_base):
		self.name = name
		self.api_base = api_base
		self.prices = {}

	def get_coins(self):
		return list(self.prices.keys())

	def update(self):
		self.update_coins()
		self.update_prices()

	@abstractmethod
	def update_coins(self):
		pass

	@abstractmethod
	def update_prices(self):
		pass
