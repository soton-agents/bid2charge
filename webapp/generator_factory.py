from generators import *

class GeneratorFactory:

	@staticmethod
	def getInstance(gen_type):
		# Inline import - required to avoid circular imports 
		from webapp.models import Treatment

		if gen_type == Treatment.RANDOM_PRICE_VECTOR_GEN:
			return RandomGen()
		elif gen_type == Treatment.DB_PRICE_VECTOR_GEN:
			return DbGen()
		elif gen_type == Treatment.FILE_PRICE_VECTOR_GEN:
			return FileGen()