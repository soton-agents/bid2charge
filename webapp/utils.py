from django.utils import timezone
from models import EVUser, Treatment, Task, Day
import random
import string



def username_exists(username):
	# Check whether a username is already registered for a user.
	# Return true if the username already exists, false otherwise.
	ulist = EVUser.objects.all()
	for user in ulist:
		if user.username == username: return True



def treatment_name_exists(tname):
	# Check whether a treatment name is already registered on a treatment.
	# Return true if the treatment name exists, false otherwise.
	tlist = Treatment.objects.all()
	for t in tlist:
		if t.treatment_name == tname: return True



def getUniqueTreatmentName(tname):
	# Get the next available treatment name by appending 1 / 2 / etc until the name is unique.
	tmpName = tname
	i = 1
	while (treatment_name_exists(tmpName)):
		tmpName = tname + str(i)
		i += 1
	return tmpName


def isInt(str,min_int,max_int):
	try:
		as_int = int(str)
		return min_int <= as_int <= max_int
	except ValueError:
		return False


def getUniqueUsername(uname):
	# Get the next available username by appendin 1 / 2 / etc until the username is unique.
	tmpName = uname
	i = 1
	while (username_exists(tmpName)):
		tmpName = uname + str(i)
		i += 1
	return tmpName

def generateRandomString(length):
	result = ''
	for i in range(length):
		result += random.choice((string.digits + string.lowercase))
	return result

def getRandomUniqueUsername(length):
	trials = 100
	while True:
		for i in range(trials):
			randomSlug = generateRandomString(length)
			if EVUser.objects.filter(username=randomSlug).count() == 0:
				return randomSlug
		length = length + 1

def getDay(index, treatment):
	return Day.objects.filter(day_index = ((index-1) % treatment.getNumberOfDays())+1, treatment = treatment)[0]