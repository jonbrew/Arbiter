from abc import ABC, abstractmethod

class Exchange(ABC):

	def __init__(self, name, api_base):
		self.name = name
		self.api_base = api_base
		self.prices = {}

	def get_name(self):
		return self.name

	def get_currencies(self):
		return list(self.prices.keys())

	def get_prices(self):
		return self.prices

	@abstractmethod
	def update_prices(self):
		pass
