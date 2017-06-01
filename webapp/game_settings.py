# DEFAULT_TREATMENT_DAYS = 15

DEFAULT_USER_BALANCE = 100.00
DEFAULT_USER_ENERGY_UNITS = 0
DEFAULT_BATTERY_CAPACITY = 10

DEFAULT_SEED = 10

DEFAULT_AVAILABLE_UNITS = 30

RNDM_MARGINAL_VALUES_SEED = 13567
RNDM_PK_MULTIPLIER = 58737
RNDM_TASK_PERFORM_CNST = 74123
RNDM_TASK_DISTRIBUTION_CNST = 15775

KWH_PER_KM = 0.2

PRICE_ROUNDING = 2

SIMPLE_BIDS = {
	"low": 1.00, 
	"medium": 2.00,
	"high": 4.00
}

SIMPLE_BIDS_TRIAL_2 = {
    "low": 1.00, 
    "medium": 2.00,
    "high": 3.00
}

DISTANCE_MULTIPLIER = 35

ROUND_ROBIN_TREATMENTS = True

TURK_BASE_PAYMENT = 2.50
TURK_BONUS_PER_PROFIT = 0.01
TURK_MAX_BONUS = 3.00


ORCHID_SHOWCASE = "orchid_showcase"


TRIAL_2_QUESTIONS = [
					("I would be happy to use this type of auction system for charging a real EV.","happyToUse",True),
					("I found the auction system unnecessarily complex.","complex",False),
					("I thought the auction system was easy to use.","easy",True),
					("I was successful in accomplishing what I was asked to do.","successful",True),
					("I had to work hard to achieve my level of performance.","hard",False),
					("I felt irritated, stressed or annoyed during the game.","stressed",False),
					("I needed to learn a lot of things before I could get going with this game.","learn",False),
					("I felt very confident in playing the game.","confident",True)
					]