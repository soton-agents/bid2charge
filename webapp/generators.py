from abc import ABCMeta, abstractmethod
import sys

from game_settings import RNDM_MARGINAL_VALUES_SEED, RNDM_PK_MULTIPLIER
import numpy.random as nprnd
from webapp.game_settings import PRICE_ROUNDING


class PriceVectorGen:
	__metaclass__ = ABCMeta

	@abstractmethod
	def generate_marginal_price_vector(self, day):
		pass



class RandomGen(PriceVectorGen):
	
	def old_generate_marginal_price_vector_from_seed(self,seed,units):
		if seed:
			nprnd.seed(seed)
		
		remaining = units

		length = (int)(nprnd.random() * min(4, remaining + 1))

		mmin = 0
		mmax = 1.0
		v1 = [round(elem, 2) for elem in (mmax - mmin) * nprnd.random(length) + mmin]

		remaining -= length
		length = (int)(nprnd.random() * min(4, remaining + 1))

		mmin = 0
		mmax = 2.0
		v2 = [round(elem, 2) for elem in (mmax - mmin) * nprnd.random(length) + mmin]

		remaining -= length

		mmin = 0.5
		mmax = 3.0
		v3 = [round(elem, 2) for elem in (mmax - mmin) * nprnd.random(remaining) + mmin]

		return v1 + v2 + v3
		
	
	def generate_marginal_price_vector_from_seed(self,seed,units,old_style=False):
		
		if seed:
			if old_style:
				nprnd.seed(int(seed))
			else:
				nprnd.seed(int(seed % 4294967295))
			
		
		prices = []
		
		min_start = 0
		min_increase = 0.2
		
		max_start = 1
		max_increase = 0.4
		
		for i in range(units):
			min_p = min_start + i * min_increase
			max_p = max_start + i * max_increase
			r = min_p + nprnd.random() * (max_p - min_p)
			r = round(r,PRICE_ROUNDING)
			
			prices.append(r)
		
		return prices

	def generate_marginal_price_vector(self, day, user,old_style=False):
		return self.generate_marginal_price_vector_pk(day.units_available, user.pk, user.current_day,old_style)
	
	def generate_marginal_price_vector_pk(self,units_available,user_pk,user_current_day,old_style=False):
		seed = (user_pk * RNDM_PK_MULTIPLIER + user_current_day) * RNDM_MARGINAL_VALUES_SEED
		return self.generate_marginal_price_vector_from_seed(seed, units_available,old_style)
		

class DbGen(PriceVectorGen):
	def generate_marginal_price_vector(self, treatment, day):
		# Inline import - required to avoid circular imports 
		from webapp.models import MarginalPriceVector

		vector_list = MarginalPriceVector.objects.all().filter(treatment = treatment.pk)
		return vector_list[day - 1]



class FileGen(PriceVectorGen):
	pass