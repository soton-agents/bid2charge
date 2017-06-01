from errors import NegativeNumberError
from game_settings import SIMPLE_BIDS
from webapp.game_settings import SIMPLE_BIDS_TRIAL_2
import itertools
import logging


def run_auction(marginal_prices, marginal_values):
	
	logger = logging.getLogger("console_logger")

	for elem in itertools.chain(marginal_prices, marginal_values):
		if elem < 0: raise NegativeNumberError(elem)

	# Calculate the total willingness to pay
	max_pay = 0
	for mv in marginal_values:
		max_pay += mv

	max_units = min(len(marginal_values), len(marginal_prices))

	# Starting from the first element, iterate through the list of marginal prices
	# until the max_pay, max_units or average per unit are exceeded.
	i = 0
	total_marginal_value = 0
	total_marginal_cost = 0
	max_utility = 0
	max_utility_n = -1

	while i < max_units and total_marginal_cost <= max_pay:
		total_marginal_cost += marginal_prices[i]
		total_marginal_value += marginal_values[i]

		utility = total_marginal_value - total_marginal_cost
		
		if utility >= max_utility:
			max_utility = utility
			max_utility_n = i

		i = i + 1

	# This vector will hold the auction results
	marginal_results = []
	for i in range(0, max_utility_n + 1):
		marginal_results.append(marginal_prices[i])

	return marginal_results


def generate_simple_values_vector(bidType, user):
	# Changed this because we allow unlimited budget now: 
	#qty = (int)(min(user.treatment.battery_capacity - user.energy_units, user.balance / SIMPLE_BIDS[bidType]))
	qty = (int)(user.treatment.battery_capacity - user.energy_units)
	
	if user.treatment.treatment_name == "Simple_AAAI_3":
		bids = SIMPLE_BIDS_TRIAL_2
	else:
		bids = SIMPLE_BIDS
		
	return generate_marginal_values_vector(qty, bids[bidType])


def generate_progressive_values_vector(kwhs, bids):
	
	# List to hold marginal values (first element is value of first kWh, etc.)
	mv = []

	# First fill with zeros	
	for i in range((int)(kwhs[len(kwhs) - 1])):
		mv.append(0)

	# Now populate bids
	previousBid = 0

	# Calculate marginal values (bids represent absolute values)
	for i in range(len(kwhs)):
		mv[(int)(kwhs[i]) - 1] = (float)(bids[i]) - previousBid
		previousBid = (float)(bids[i])

	return mv


def generate_marginal_values_vector(max_kwh, bid_per_unit):
	mv = []
	for i in range(0, max_kwh):
		mv.append(bid_per_unit)
	return mv
