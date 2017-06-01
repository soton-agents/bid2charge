from django.core.exceptions import ValidationError

def daily_probabilities_validator(str):
	try:
		prob_list = eval(str)
	except (SyntaxError, NameError):
		raise ValidationError("The input must be a comma-separated list of numbers.")
	else:
		for p in prob_list:
			if (not isinstance (p, (int, float))):
				raise ValidationError("The input must be a comma-separated list of numbers.")
			if p < 0 or p > 1: 
				raise ValidationError("%d is not a correct probability. Input values between 0 and 1." % p)

def marginal_prices_validator(str):
	try:
		marginal_prices = eval(str)
	except (SyntaxError, NameError):
		raise ValidationError("The input must be a comma-separated list of numbers.")
	else:
		for p in marginal_prices:
			if (not isinstance(p, (int, float))):
				raise ValidationError("The input must be a comma-separated list of numbers.")
			if p < 0:
				raise ValidationError("%d is not a correct price. Only positive values accepted." % p)

def daily_energy_units_validator(str):
	try:
		energy_units = eval(str)
	except(SyntaxError, NameError):
		raise ValidationError("The input must be a comma-separated list of integer numbers.")
	else:
		if not type(energy_units) is int:
			for val in energy_units:
				if (not isinstance(val, (int))):
					raise ValidationError("The input must be a comma-separated list of integer numbers.")
				if (val <= 0):
					raise ValidationError("%d is not a valid amount of energy units. Only positive values accepted." % val)