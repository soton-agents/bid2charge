from django.test import TestCase
from webapp.models import EVUser, Treatment
from errors import NegativeNumberError

import auction

class AuctionTestCase(TestCase):
	const_marginal_values = [1.05, 1.05, 1.05, 1.05, 1.05, 1.05]

	def setUp(self):
		pass

	def test_constant_marginal_values(self):
		marginal_prices = [0.5, 0.7, 1, 0.9, 1.7, 0.2, 1.6, 1.7, 1.6, 1.5, 1.5, 1.5, 0.2]
		self.assertEqual(auction.run_auction(marginal_prices, self.const_marginal_values), marginal_prices[0:6])

		marginal_prices = [100, 0.7, 1, 0.9, 1.7, 0.2, 1.6, 1.7, 1.6, 1.5, 1.5, 1.5, 0.2]
		self.assertEqual(auction.run_auction(marginal_prices, self.const_marginal_values), marginal_prices[0:0])

		marginal_prices = [0.5, 100, 1, 0.9, 1.7, 0.2, 1.6, 1.7, 1.6, 1.5, 1.5, 1.5, 0.2]
		self.assertEqual(auction.run_auction(marginal_prices, self.const_marginal_values), marginal_prices[0:1])

		marginal_prices = self.const_marginal_values
		self.assertEqual(auction.run_auction(marginal_prices, self.const_marginal_values), self.const_marginal_values)

		marginal_prices = [0.5, 0.7, 1, 0.9, 1.7]
		marginal_values = [2, 2, 2, 2, 2, 2]
		self.assertEqual(auction.run_auction(marginal_prices, marginal_values), [0.5, 0.7, 1, 0.9, 1.7])

	def test_different_marginal_values(self):
		marginal_prices = [0.5, 0.7, 1, 0.9, 1.7, 0.2, 1.6, 1.7, 1.6, 1.5, 1.5, 1.5, 0.2]
		marginal_values = [0.1, 0.5, 0.6, 10, 0.2, 2, 1]
		self.assertEqual(auction.run_auction(marginal_prices, marginal_values), [0.5, 0.7, 1, 0.9, 1.7, 0.2])

		marginal_prices = [0.5, 0.7, 1, 0.9, 1.7]
		marginal_values = [2, 2, 2, 2, 2, 1]
		self.assertEqual(auction.run_auction(marginal_prices, marginal_values), [0.5, 0.7, 1, 0.9, 1.7])

		marginal_prices = [0.5, 0.7, 1, 0.9, 1.7]
		marginal_values = []
		self.assertEqual(auction.run_auction(marginal_prices, marginal_values), marginal_values)

	def test_negative_values(self):
		marginal_prices = [1, 1, 1, -2]
		marginal_values = [1, 1, 1, 1]
		self.assertRaises(NegativeNumberError, lambda: auction.run_auction(marginal_prices, marginal_values))