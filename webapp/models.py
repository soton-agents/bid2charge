from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from json import dumps
from game_settings import *
from generator_factory import *
from http_utils import *
from jsonfield import JSONField, JSONCharField
from validators import *
import collections
import itertools
import logging
import math
import random
import re







# Model class Treatment. The game can have a number of treatments, each presenting a different set
# of configurations to the end user. Each treatment is associated with a number of tasks (task foreign 
# key pointing to treatment), each task having a list of probabilities for a number of days. Other
# settings such as the initial starting balance can be configured differently for each Treatment. 
class Treatment(models.Model):

	# Constant Names - Marginal Price Vector Generators
	RANDOM_PRICE_VECTOR_GEN = "random_gen"
	DB_PRICE_VECTOR_GEN = "db_gen"
	FILE_PRICE_VECTOR_GEN = "file_gen"

	# Constant Names - Bidding Strategies
	SIMPLE_BIDDING_STRATEGY = "simple_bidding"
	UNIFORM_BIDDING_STRATEGY = "uniform_bidding"
	PROGRESSIVE_BIDDING_STRATEGY = "progressive_bidding"

	# Choices for Marginal Price Vector Generators (admin view)
	MARGINAL_PRICE_VECTOR_CHOICES = (
		(RANDOM_PRICE_VECTOR_GEN, "Random Price Vectors"),
		(DB_PRICE_VECTOR_GEN, "DB Price Vectors"),
		(FILE_PRICE_VECTOR_GEN, "File Price Vectors"),
	)

	# Choices for Bidding Strategies
	BIDDING_STRATEGY_CHOICES = (
		(SIMPLE_BIDDING_STRATEGY, "Simple Bidding Format"),
		(UNIFORM_BIDDING_STRATEGY, "Uniform Bidding Format"),
		(PROGRESSIVE_BIDDING_STRATEGY, "Progressive Bidding Format"),
	)

	# Fields
	treatment_name = models.CharField(max_length = 50, default = "New Treatment")
	experiment = models.ForeignKey("Experiment",null=True,default=None)
	user_initial_balance = models.FloatField(default = DEFAULT_USER_BALANCE)
	user_initial_energy_units = models.IntegerField(default = DEFAULT_USER_ENERGY_UNITS)
	battery_capacity = models.IntegerField(default = DEFAULT_BATTERY_CAPACITY)
	random_seed = models.IntegerField(default = DEFAULT_SEED)
	active = models.BooleanField(default = False)

	price_vector_generator = models.CharField(	max_length = 50, 
												choices = MARGINAL_PRICE_VECTOR_CHOICES, 
												default = RANDOM_PRICE_VECTOR_GEN)

	bidding_strategy = models.CharField(max_length = 50, 
										choices = BIDDING_STRATEGY_CHOICES,
										default = SIMPLE_BIDDING_STRATEGY)

	def getNumberOfDays(self):
		return len(Day.objects.filter(treatment = self))

	@property
	def numberOfDays(self):
		return self.getNumberOfDays()

	def getUnitsAuctionedOnDay(self, day):
		return eval(self.daily_energy_units)[day - 1]

	def getVectorPriceForDay(self, day):
		generator = GeneratorFactory.getInstance(self.price_vector_generator)
		return generator.generate_marginal_price_vector(self, day)

	def __unicode__(self):
		return self.treatment_name



class Experiment(models.Model):
	experiment_name = models.CharField(max_length = 255)
	
	def getTreatments(self,only_active=True):
		mappings = ExperimentTreatment.objects.filter(experiment=self)
		treatments = []
		for m in mappings:
			if (not only_active) or m.active: 
				treatments.append(m.treatment)
		return treatments
	
	def __unicode__(self):
		return "%s -> %s" % (self.experiment_name,self.getTreatments(only_active=False))

class ExperimentTreatment(models.Model):
	experiment = models.ForeignKey(Experiment)
	treatment = models.ForeignKey("Treatment")
	active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return "%s -> %s" % (self.experiment.experiment_name, self.treatment.treatment_name)
	

class Task(models.Model):
	
	# Constant Task Icon Paths
	LOW_REWARD_ICON = "/static/webapp/img/low-reward-task-icon.png"
	MEDIUM_REWARD_ICON = "/static/webapp/img/medium-reward-task-icon.png"
	HIGH_REWARD_ICON = "/static/webapp/img/high-reward-task-icon.png"

	# Choices for Task Image
	TASK_ICON_CHOICES = (
		(LOW_REWARD_ICON, "Low Reward Icon"),
		(MEDIUM_REWARD_ICON, "Medium Reward Icon"),
		(HIGH_REWARD_ICON, "High Reward Icon"),
	)

	description = models.CharField(max_length = 45)
	reward = models.FloatField(default = 0.00, validators = [MinValueValidator(0)])
	task_icon = models.CharField(	max_length = 50,
									choices = TASK_ICON_CHOICES,
									default = LOW_REWARD_ICON)

	# Coordinates XY for displaying the task on the viewport (0 <= xy <= 1)
	x = models.FloatField(default = 0.00)
	y = models.FloatField(default = 0.00)

	def __unicode__(self):
		return self.description



class Day(models.Model):
	
	@staticmethod
	def getNewTaskProbabilities(p):
		# Build a dict object with all defined tasks, 
		# initialized with probability p
		task_dict = {}
		
		for task in Task.objects.all():
			task_dict[str(task.description)] = p

		return task_dict

	day_index = models.IntegerField(default = 0, verbose_name = "#")
	treatment = models.ForeignKey(Treatment)
	units_available = models.IntegerField(default = 30)
	task_probabilities = JSONField(default = "")
	
	marginal_prices = models.CharField(	max_length = 500, 
										validators = [marginal_prices_validator], 
										null = True,
										blank = True, 
										verbose_name = "Price Vector")


	def task_probabilities_str(self):
		return re.sub("u'|'", '"', str(self.task_probabilities))

	@staticmethod
	def getTaskDistributionStr(user):
		index = ((user.current_day - 1) % user.treatment.getNumberOfDays()) + 1
		day = Day.objects.filter(treatment = user.treatment, day_index = index)[0]
		return day.task_probabilities_str()

	@staticmethod
	def getRandomTaskDistributionStr(user):
		random.seed((user.pk * RNDM_PK_MULTIPLIER + user.current_day) * RNDM_TASK_DISTRIBUTION_CNST)

		allTasks = Task.objects.all()
		taskDescriptions = [ t.description for t in allTasks ]
		taskProbabilities = [ random.random() for i in range(0, len(taskDescriptions))]

		taskDistributionStr = '{'
		for i in range(0, len(taskDescriptions)):
			taskDistributionStr += '"' + taskDescriptions[i] + '":' + '{0:.2f}'.format(taskProbabilities[i]) + ','

		taskDistributionStr = taskDistributionStr[:-1] + "}"

		return taskDistributionStr

	@staticmethod
	def getRandomTaskDistributionProbabilitiesOnly(user):
		random.seed((user.pk * RNDM_PK_MULTIPLIER + user.current_day) * RNDM_TASK_DISTRIBUTION_CNST)

		allTasks = Task.objects.all()
		taskDescriptions = [t.description for t in allTasks ]
		return [ random.random() for i in range(0, len(taskDescriptions))]


	def getTaskProbability(self, task_description):
		return self.task_probabilities[task_description]

	def __unicode__(self):
		return "Day " + str(self.day_index) if self.day_index > 0 else "New Day"


class EVUserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		
		if not username:
			raise ValueError('Users must have a username')
		
		user = self.model(email = EVUserManager.normalize_email(email), username = username,)
		user.set_password(password)
		user.created = timezone.now()
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(email, username, password)
		user.is_admin = True
		user.save(using=self._db)
		return user



class EVUser(AbstractBaseUser):
	username = models.CharField(max_length = 254, unique = True)
	email = models.EmailField(blank = True)

	is_active = models.BooleanField(default = True)
	is_admin = models.BooleanField(default = False)

	created = models.DateTimeField()
	current_day = models.IntegerField(default = 1)
	auction_done_today = models.BooleanField(default = False)
	ev_guru_mode = models.BooleanField(default = False)
	treatment = models.ForeignKey(Treatment, null = True)
	last_progressive_bids = models.CharField(max_length = 200, default = "[]")
	last_progressive_kwhs = models.CharField(max_length = 200, default = "[]")
	saved_current_day_history = models.BooleanField(default = False)
	agree_to_receive_email = models.BooleanField(default = True)
	
	is_turker = models.BooleanField(default = False)
	is_aamas = models.BooleanField(default = False)
	experiment= models.ForeignKey(Experiment,default=None,null=True)
	
	# Whether this is a Turker for the second trial
	is_turker_trial_2 = models.BooleanField(default = False)
	
	# ORCHID Showcase specific:
	leaderboard_allowed = models.BooleanField(default = True)
	research_allowed = models.BooleanField(default = True)
	completed_tutorial = models.BooleanField(default=True)
	
	
	# Will get initiated by the EVUserManager based on the chosen game configuration
	balance = models.FloatField(default = 0)
	best_monthly_score = models.FloatField(default = 0)
	energy_units = models.IntegerField(default = 0)

	

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	# Use UserManager to get the create_user method, etc.
	objects = EVUserManager()

	def getTasksToPerform(self):
		'''Potential Issue: the random seed might not be consistent for many users accessing the
		method concurrently. The bug could not be replicated for now.
		'''
		# Check if a set of tasks has already been logged in the database for the current day
		existingLog = TasksAvailableLog.objects.filter(user = self, day = self.current_day, treatment_id = self.treatment.pk)
		
		if existingLog:
			# Build a task list based on the existing log, by 
			# retrieving tasks matching each description and adding them to the task_list array 
			task_list = []
			
			for description in (existingLog[0].available_tasks).split(';'):
				if description != '':
					task_list.append(Task.objects.filter(description = description)[0])
			
			# Return the sorted list of tasks
			return sorted(task_list, key = lambda x: x.description)
		else:
			# Generate a fresh list of tasks and log it in the database

			# Set the random seed based on the user's PK, current day and other constants
			random.seed((self.pk * RNDM_PK_MULTIPLIER + self.current_day) * RNDM_TASK_PERFORM_CNST)
			task_list = []

			# If the user is NOT an EV Guru, use the task distribution existent for the current day
			#if not self.ev_guru_mode:
			
			index =  ((self.current_day - 1) % self.treatment.getNumberOfDays()) + 1
			
			day = Day.objects.filter(day_index = index, treatment = self.treatment)[0]
			
			# For each task description, compare its probability with a new random number
			# and decide whether the task appears or not. If yes, add it to the list
			for task_description in day.task_probabilities:
				if day.task_probabilities[task_description] >= random.random():
					task = Task.objects.filter(description = task_description)[0]
					task_list.append(task)

			# Return the sorted list of tasks
			return sorted(task_list, key = lambda x: x.description)

			# If the user IS an EV Guru, get all tasks existent in the  
			# database and generate a random task distribution set

#			else:
#				allTasks = Task.objects.all()
#				taskDescriptions = [ t.description for t in allTasks ]
#				taskProbabilities = Day.getRandomTaskDistributionProbabilitiesOnly(self)
#
#				for i in range(0, len(taskDescriptions)):
#					if taskProbabilities[i] >= random.random():
#						task = Task.objects.filter(description = taskDescriptions[i])[0]
#						task_list.append(task)
#
#				# Log the tasks available 
#				taskListDescriptionStr = "" 
#				for task in task_list:
#					taskListDescriptionStr += task.description + ","
#				taskListDescriptionStr = taskListDescriptionStr[:-1]
#				TasksAvailableLog.log(self, taskListDescriptionStr)

#				return sorted(task_list, key = lambda x: x.description)

	def __unicode__(self):
		return self.username

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	def reassign_treatment(self):
		self.treatment = None
		self.save()
			
	
	@property
	def is_orchid(self):
		if not self.experiment:
			return False
		else:
			if self.experiment.experiment_name == ORCHID_SHOWCASE:
				return True
			else:
				return False

	@property
	def is_staff(self):
		return self.is_admin
	


class MarginalPriceVector(models.Model):
	treatment = models.ForeignKey(Treatment, null = True )
	day = models.IntegerField(default = 0)
	marginal_prices = models.CharField(max_length = 500, validators = [marginal_prices_validator], null = True, verbose_name = "Price Vector")	

	class Meta:
		ordering = ['treatment', 'day']

	def __unicode__(self):
		return self.marginal_prices



class ShortestPath(models.Model):
	task_selection = models.CharField(max_length = 1000)
	solution = models.CharField(max_length = 1000)
	total_cost = models.FloatField(default = 0.00)
	total_reward = models.FloatField(default = 0.00)

	def getShortestPathTasks(self):
		return [Task.objects.filter(description = t)[0] for t in self.solution.split(";")]

	@staticmethod
	def findOptimalPath(totalTaskSelection, availableEnergy):
		optimalPath = ""
		max_reward = 0

		totalTaskSelection = totalTaskSelection.split(";")
		for i in range(1, len(totalTaskSelection) + 1):
			for taskSubset in itertools.combinations(totalTaskSelection, i):
				taskSelectionString = ";".join("{0}{1}".format(t, "") for t in taskSubset)

				tmpShortestPath = ShortestPath.objects.filter(task_selection = taskSelectionString)[0]
				if tmpShortestPath.total_cost <= availableEnergy and tmpShortestPath.total_reward >= max_reward:
					max_reward = tmpShortestPath.total_reward
					optimalPath = tmpShortestPath

		return optimalPath

	@staticmethod
	def findOptimalTaskSets(totalTaskSelection, availableEnergy):
		totalTaskSelection = totalTaskSelection.split(";")
		totalTasks = len(totalTaskSelection)

		# Create a matrix consisting of 2^totalTasks rows and 4 columns
		# On each row of this matrix, we will store a subset of tasks
		# Column 0 represents the shortest path for that particular task selection
		# Column 1 represents the total reward for those tasks
		# Column 2 represents the total cost (km) 
		# Column 3 represents the required kwh
		pathMatrix = [[0 for x in range(5)] for x in range(2 ** totalTasks)]
		rowIndex = 0

		for i in range(1, len(totalTaskSelection) + 1):
			for taskSubset in itertools.combinations(totalTaskSelection, i):
				taskSelectionString = ";".join("{0}{1}".format(t, "") for t in taskSubset)
				tmpShortestPath = ShortestPath.objects.filter(task_selection = taskSelectionString)[0]

				tmpShortestPathKWHCost = int(math.ceil(tmpShortestPath.total_cost * KWH_PER_KM))

				if tmpShortestPathKWHCost <= availableEnergy:
					pathMatrix[rowIndex][0] = tmpShortestPath.solution
					pathMatrix[rowIndex][1] = tmpShortestPath.total_reward
					pathMatrix[rowIndex][2] = tmpShortestPath.total_cost
					pathMatrix[rowIndex][3] = tmpShortestPathKWHCost
					rowIndex += 1

		# Sort the matrix by the reward column
		pathMatrix.sort(key=lambda x: (x[1],-x[3]), reverse=True)

		# Iterate through the matrix and remove the rows where the cost column element (index 2)
		# is higher than the cost column element at the previous row
		i = 1
		while i < len(pathMatrix):
			if pathMatrix[i][3] >= pathMatrix[i - 1][3]:
				pathMatrix.remove(pathMatrix[i])
			else: 
				i += 1

		# Add the Actual List of Task objects on the last column of each row
		for i in range(len(pathMatrix) - 1):
			taskList = []
			taskDescriptions = pathMatrix[i][0].split(";")
			for description in taskDescriptions:
				taskList.append(Task.objects.filter(description = description)[0].task_icon)

			pathMatrix[i][4] = taskList

		return pathMatrix

	def __unicode__(self):
		return self.task_selection + " -> " + self.solution


class DayHistory(models.Model):
	user = models.ForeignKey(EVUser, null = True)
	day = models.IntegerField(default = 0)
	balance = models.FloatField(default = 0.00)
	kwh = models.FloatField(default = 0.00)
	recorded = models.DateTimeField()
	task_distribution = models.CharField(max_length = 500, default = "")

	def __unicode__(self):
		return "User: %s, completed day %s with %s kWh, %s balance" % (self.user,self.day,self.kwh,self.balance)


	@staticmethod
	def log(request):
		if not request.user.saved_current_day_history:
			dayHistory = DayHistory()
			dayHistory.recorded = timezone.now()
			dayHistory.user = request.user
			dayHistory.day = request.user.current_day
			dayHistory.balance = request.user.balance
			dayHistory.kwh = request.user.energy_units

			# Get the task distribution depending on whether the user is an EV Guru or not
			# For EV Guru users, the task distribution is randomly generated based on their day 
			# Normal users have a predefined task distribution
			if request.user.ev_guru_mode:
				dayHistory.task_distribution = Day.getRandomTaskDistributionStr(request.user)
			else: 
				dayHistory.task_distribution = Day.getTaskDistributionStr(request.user)

			# Mark the user's day as saved and save the user
			request.user.saved_current_day_history = True
			request.user.save()

			# Save the day History log
			dayHistory.save()


class AuctionHistory(models.Model):
	user = models.ForeignKey(EVUser, null = True)
	day = models.IntegerField(default = 0)
	bid = models.FloatField(default = 0.00)
	total_spent = models.FloatField(default = 0.00)
	kwh_won = models.IntegerField(default = 0)
	recorded = models.DateTimeField()
	
class QuizHistory(models.Model):
	user = models.ForeignKey(EVUser, null = True)
	date_time = models.DateTimeField()
	goalAnswer = models.CharField(max_length = 50, default="")
	planAnswer = models.CharField(max_length = 50, default="")
	auctionAnswer = models.CharField(max_length = 50, default="")
	consentAnswer = models.BooleanField()
	correct = models.BooleanField()

	def __unicode__(self):
		return "User: %s, correct: %s, consent: %s, at %s" % (self.user,self.correct,self.consentAnswer,self.date_time)

	
	@staticmethod
	def log(user,goalAnswer,planAnswer,auctionAnswer,consentAnswer,correct):
		history = QuizHistory()
		history.user = user
		history.date_time = timezone.now()
		history.goalAnswer = goalAnswer
		history.planAnswer = planAnswer
		history.auctionAnswer = auctionAnswer
		history.consentAnswer = consentAnswer
		history.correct = correct
		history.save()

class AccountEvent(models.Model):
	# Constant Names 
	LOGIN_EVENT = "login"
	LOGOUT_EVENT = "logout"
	SIGNUP_EVENT = "signup"
	CHANGE_PASSWORD_EVENT = "change_password"
	FORGOT_PASSWORD_EVENT = "forgot_password"

	user = models.ForeignKey(EVUser, null = True)
	ip = models.CharField(max_length = 50)
	http_host = models.CharField(max_length = 50, default="")
	user_agent = models.CharField(max_length = 500, default="")
	http_referer = models.CharField(max_length = 500, default="")
	event_type = models.CharField(max_length=50, default = LOGIN_EVENT)
	date_time = models.DateTimeField()

	@staticmethod
	def log(eventType, request):
		accEvent = AccountEvent()
		accEvent.user = request.user
		accEvent.ip = get_client_ip(request)
		accEvent.remote_host = get_remote_host(request)
		accEvent.http_host = get_http_host(request)
		accEvent.user_agent = get_user_agent(request)
		accEvent.http_referer = get_http_referer(request)
		accEvent.event_type = eventType
		accEvent.date_time = timezone.now()
		accEvent.save()


class AuctionEvent(models.Model):
	user = models.ForeignKey(EVUser, null = True)
	treatment_id = models.IntegerField(default = 0)
	day = models.IntegerField(default = 0)
	bidding_strategy = models.CharField(max_length = 50, default = "")
	sliders_used = models.IntegerField(null = True)
	balance_before_auction = models.FloatField(default = 0.00)
	energy_units_before_auction = models.IntegerField(default = 0)
	user_marginal_values = models.CharField(max_length = 1000, default = "")
	marginal_prices = models.CharField(max_length = 1000, default = "")
	result = models.CharField(max_length = 500, default = "")
	allocated_units = models.IntegerField(default = 0)
	total_pay = models.FloatField(default = 0.00)
	date_time = models.DateTimeField()


	def __unicode__(self):
		return "User: %s, received %s for %s" % (self.user,self.allocated_units,self.total_pay)

	@staticmethod
	def log(request, marginalPrices, userMarginalValues, result):
		auctionEvent = AuctionEvent()
		auctionEvent.user = request.user
		auctionEvent.date_time = timezone.now()
		auctionEvent.treatment_id = request.user.treatment.pk
		auctionEvent.bidding_strategy = request.user.treatment.bidding_strategy
		auctionEvent.day = request.user.current_day
		auctionEvent.balance_before_auction = request.user.balance
		auctionEvent.energy_units_before_auction = request.user.energy_units
		auctionEvent.marginal_prices = marginalPrices
		auctionEvent.user_marginal_values = userMarginalValues
		auctionEvent.result = result
		auctionEvent.allocated_units = len(result)
		auctionEvent.total_pay = sum(result)
		if "sliders" in request.POST:
			auctionEvent.sliders_used = (int)(request.POST["sliders"])
		auctionEvent.save()


class TaskClickEvent(models.Model):
	# Constant Names
	SELECT_TASK_EVENT = "select"
	CLEAR_TASK_SELECTION_EVENT = "deselect"

	user = models.ForeignKey(EVUser, null = True)
	treatment_id = models.IntegerField(default = 0)
	day = models.IntegerField(default = 0)
	event_type = models.CharField(max_length = 100, default = SELECT_TASK_EVENT)
	task_description = models.CharField(max_length = 100)
	task_reward = models.IntegerField(default = 0)
	total_reward = models.IntegerField(default = 0)
	total_km = models.FloatField(default = 0.00)
	task_selection_before = models.CharField(max_length = 1000, default = "")
	task_selection_after = models.CharField(max_length = 1000, default = "")
	date_time = models.DateTimeField()

	def __unicode__(self):
		return "User: %s clicked %s for %s at %s" % (self.user,self.task_selection_after, self.total_reward,self.date_time)

	@staticmethod
	def log(request):
		taskEvent = TaskClickEvent()
		taskEvent.user = request.user
		taskEvent.date_time = timezone.now()
		taskEvent.treatment_id = request.user.treatment.pk
		taskEvent.day = request.user.current_day
		taskEvent.task_description = request.POST["taskDescription"]
		taskEvent.task_reward = request.POST["taskReward"]
		taskEvent.task_selection_before = request.POST["taskSelectionBefore"]
		taskEvent.task_selection_after = request.POST["taskSelectionAfter"]
		taskEvent.event_type = request.POST["eventType"]
		taskEvent.total_reward = request.POST["total_reward"]
		taskEvent.total_km = request.POST["total_km"]
		taskEvent.save()

class TasksAvailableLog(models.Model):
	user = models.ForeignKey(EVUser, null = True)
	treatment_id = models.IntegerField(default = 0)
	day = models.IntegerField(default = 0)
	available_tasks = models.CharField(max_length = 1000, default = "")
	date_time = models.DateTimeField()

	def __unicode__(self):
		return "User: %s day %s available: %s" % (self.user,self.day, self.available_tasks)


	@staticmethod
	def log(user, taskDescriptionList):
		tasksAvailableLog = TasksAvailableLog()
		tasksAvailableLog.user = user
		tasksAvailableLog.treatment_id = user.treatment.pk
		tasksAvailableLog.day = user.current_day
		tasksAvailableLog.available_tasks = taskDescriptionList
		tasksAvailableLog.date_time = timezone.now()
		tasksAvailableLog.save()


class PerformEvent(models.Model):
	user = models.ForeignKey(EVUser, null = True)
	treatment_id = models.IntegerField(default = 0)
	day = models.IntegerField(default = 0)
	taskset_reward = models.FloatField(default = 0)
	energy_used = models.FloatField(default = 0)
	other_tasksets = models.CharField(max_length = 1000)
	date_time = models.DateTimeField()
	
	def __unicode__(self):
		return "User: %s, received %s reward, used %s kWh" % (self.user,self.taskset_reward,self.energy_used)


	@staticmethod
	def log(request, totalReward, energyUsed, otherTasksets):
		performEvent = PerformEvent()
		performEvent.date_time = timezone.now()
		performEvent.user = request.user
		performEvent.treatment_id = request.user.treatment.pk
		performEvent.day = request.user.current_day
		performEvent.taskset_reward = totalReward
		performEvent.energy_used = energyUsed
		performEvent.other_tasksets = otherTasksets
		performEvent.save()

class Completion(models.Model):
	user = models.ForeignKey(EVUser)
	base_payment = models.FloatField()
	bonus_payment = models.FloatField()
	date_time = models.DateTimeField(default=timezone.now())
	paid = models.BooleanField(default = False)
	approved = models.BooleanField(default = True)
	worker_id = models.CharField(max_length = 100, default = None, null = True)
	assignment_id = models.CharField(max_length = 100, default = None, null = True)
	hit_id = models.CharField(max_length = 100, default = None, null = True)
	
	def __unicode__(self):
		return "User: %s (%s), completed on %s. Payment %s + bonus %s. Paid: %s" % (self.user,self.user.treatment,self.date_time, self.base_payment, self.bonus_payment,self.paid)


class InstructionView(models.Model):
	user = models.ForeignKey(EVUser)
	date_time = models.DateTimeField(default=timezone.now())
	
	def __unicode__(self):
		return "User: %s viewed instructions on %s" % (self.user,self.date_time)



class Survey(models.Model):
	
	# Constant Task Icon Paths
	POSITIVE = 1
	NEUTRAL = 2
	NEGATIVE = 3

	# Choices for Task Image
	SENTIMENT_CHOICE = (
		(POSITIVE, "Positive"),
		(NEUTRAL, "Neutral"),
		(NEGATIVE, "Negative"),
	)
	
	
	user = models.ForeignKey(EVUser)
	date_time = models.DateTimeField()
	gender = models.CharField(max_length = 10)
	age = models.CharField(max_length = 10)
	education = models.CharField(max_length = 20)
	country = models.TextField()
	car_owner = models.BooleanField()
	driven_ev = models.BooleanField()
	strategy = models.TextField()
	strategy_change = models.TextField()
	comments = models.TextField()
	sentiment = models.IntegerField(default=NEUTRAL, choices=SENTIMENT_CHOICE)
	usability_answers = models.TextField(default="")
	usability_score = models.IntegerField(default=-1)
	
	def __unicode__(self):
		return "User: %s, received %s" % (self.user,self.date_time)
