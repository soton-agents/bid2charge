import json
import logging
import math
import re
import sys
import traceback

from django.contrib.auth import authenticate, login
import django.contrib.auth
from django.contrib.auth.views import logout
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import Context
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

import auction
from game_settings import KWH_PER_KM, DEFAULT_AVAILABLE_UNITS, SIMPLE_BIDS
from generator_factory import GeneratorFactory
from optimal.db_populator import ORCHID_SHOWCASE
import utils
from webapp import game_settings
from webapp.game_settings import TRIAL_2_QUESTIONS, SIMPLE_BIDS_TRIAL_2
from webapp.models import Task, ShortestPath, Day, EVUser, AccountEvent, \
	TaskClickEvent, AuctionEvent, PerformEvent, DayHistory, AuctionHistory, \
	TasksAvailableLog, QuizHistory, Survey, Completion, InstructionView, Treatment, \
	Experiment
from webapp.payment_calculator import get_profit, get_bonus_payment, \
	get_total_payment
from webapp.utils import getRandomUniqueUsername, generateRandomString, isInt


SECOND_TRIAL_GAMES = 3

def do_login(request):
	logger = logging.getLogger("console_logger")
	logger.debug(request)

	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			# Login the user under the current session
			login(request, user)

			# Store the login event
			AccountEvent.log(AccountEvent.LOGIN_EVENT, request)

			# Redirect to the home page
			return HttpResponseRedirect("/webapp/home/")
		else:
			# Return 'disabled account' error message
			return HttpResponse('Your account has been disabled')
	else:
		# Return an 'invalid login' error message
		# return HttpResponse('Invalid Credentials')
		request.session["login_error"] = True
		return HttpResponseRedirect("/accounts/login/")

def aamas(request):
	request.session["aamas"] = True
	request.session["trial_2"] = True
	return HttpResponseRedirect("/start")	

def go(request):
	request.session["trial_2"] = True
	return HttpResponseRedirect("/start")	

def go2(request):
	logout(request)
	return HttpResponseRedirect("/go")

def home(request):
	
	if not request.user.is_authenticated():
		if "orchid" in request.session:
			if request.session["orchid"]:
				return HttpResponseRedirect("/orchid")
	
	
	# Do a number of things if the user is turker
	if request.user.is_turker:
		# Have we done the quiz yet?
		if len(QuizHistory.objects.filter(user=request.user,correct=True)) == 0:
			# No!
			return HttpResponseRedirect("/webapp/rules")
		# Are we done yet?
		elif request.user.current_day > request.user.treatment.getNumberOfDays() * SECOND_TRIAL_GAMES \
				or (not request.user.is_turker_trial_2 and request.user.current_day > request.user.treatment.getNumberOfDays()):
			
			if len(Survey.objects.filter(user=request.user)) == 0:
				# No
				return HttpResponseRedirect("/webapp/survey")
			else:
				return HttpResponseRedirect("/webapp/hit_done")

	
	# Check if the game is complete (and not EV Guru)
	if request.user.current_day > request.user.treatment.getNumberOfDays() and not request.user.ev_guru_mode and not request.user.is_turker and not request.user.is_orchid:
		return HttpResponseRedirect("/webapp/game_complete")
	
	# Check if the auction has already taken place 
	elif request.user.auction_done_today: 
		return HttpResponseRedirect ("/webapp/delivery")

	# Otherwise proceed with the dashboard page
	else:	
		json_serializer = serializers.get_serializer("json")()

		# Task objects containing: description, reward and xy coordinates
		tasks = json_serializer.serialize(Task.objects.all().order_by("description"))

		# Array containing the shortest paths for any possible subset of tasks
		shortest_paths = json_serializer.serialize(ShortestPath.objects.all())
		
		# Let's shorten progressive bids if appropriate
#		last_progressive_bids = re.findall("[0-9.]+",request.user.last_progressive_bids)
#		last_progressive_kwhs = re.findall("[0-9.]+",request.user.last_progressive_kwhs)
#		
#		last_index = len(last_progressive_bids)
#		
#		for i in range(len(last_progressive_bids)):
#			kwh = int(last_progressive_kwhs[i])
#			if kwh + request.user.energy_units > request.user.treatment.battery_capacity:
#				last_index = i
#				break
#		
#		last_progressive_bids = str(last_progressive_bids[0:last_index])
#		last_progressive_kwhs = str(last_progressive_kwhs[0:last_index])
		
		# if not request.user.ev_guru_mode:
		
		# Day properties: available energy units and <task, p>
		index =  ((request.user.current_day - 1) % request.user.treatment.getNumberOfDays()) + 1
		current_day = Day.objects.filter(treatment = request.user.treatment, day_index = index)[0]
		available_energy_units = current_day.units_available
		task_probabilities = current_day.task_probabilities_str()

		show_tutorial = False
		if not request.user.completed_tutorial:
			show_tutorial = True
			request.user.completed_tutorial = True
			request.user.save()
		
		c = Context({	
						"tasks": tasks, 
						"task_probabilities": task_probabilities,
						"shortest_paths": shortest_paths,
						"available_energy_units": available_energy_units,
						"kwh_per_km": KWH_PER_KM,
						"last_progressive_bids": request.user.last_progressive_bids,
						"last_progressive_kwhs": request.user.last_progressive_kwhs,
						"show_tutorial" : show_tutorial,
					})

		# if the user is EV Guru, then build default / random distributions
		
		# SEB: I have disabled this for now, as it's not logging probabilities, and some tasks overlap. After AAMAS, may restructure, and re-decide. For now, EV Guru mode will simply repeat the same game again.
		
#		else:
#			cstm_units_available = DEFAULT_AVAILABLE_UNITS
#			rndm_task_probabilities = Day.getRandomTaskDistributionStr(request.user)
#
#			c = Context({	
#							"tasks": tasks, 
#							"task_probabilities": rndm_task_probabilities,
#							"shortest_paths": shortest_paths,
#							"available_energy_units": cstm_units_available,
#							"kwh_per_km": KWH_PER_KM,
#							"last_progressive_bids": request.user.last_progressive_bids,
#							"last_progressive_kwhs": request.user.last_progressive_kwhs,
#						})


		# Return the dashboard (step1) view
		return render(request, "step1.html", c)


def instructions(request):
	if request.user.is_authenticated() and request.user.is_turker:
		
		 # Has the user passed the initial test yet?
		if len(QuizHistory.objects.filter(user=request.user,correct=True)) == 0:
			return HttpResponseRedirect("/webapp/rules")
		
		record = InstructionView()
		record.user = request.user
		record.date_time = timezone.now()
		record.save()
		
		return render(request,"turk_instructions_2.html", Context(_getPaymentContext()))
	
	record = InstructionView()
	record.user = request.user
	record.date_time = timezone.now()
	record.save()
	return render(request, "turk_instructions_2.html")


def run_simple_auction(request):
	
	# Already done?
	events = AuctionEvent.objects.filter(user=request.user,day=request.user.current_day)
	
	if request.user.auction_done_today == True and len(events) > 0:
		# Yes!
		return HttpResponse(json.dumps({
									"auctionResult": events[0].result,
									"totalSpent": events[0].total_pay,
									"allocatedKwh": events[0].allocated_units}), 
									content_type="application_json")
	
	
	marginal_generator = GeneratorFactory.getInstance(request.user.treatment.price_vector_generator)
	
	if not request.user.ev_guru_mode:
		day = utils.getDay(request.user.current_day, request.user.treatment)
	else: 
		day = Day()
		day.units_available = DEFAULT_AVAILABLE_UNITS

	
	# Generate the vector of marginal prices
	mp = marginal_generator.generate_marginal_price_vector(day, request.user)
	
	# Build the vector of marginal values from the user's input
	bidType = request.POST["bidType"]
	
	mv = auction.generate_simple_values_vector(bidType, request.user)
	
	# Run the auction
	result = auction.run_auction(mp, mv)

	# Log the Auction Event 
	AuctionEvent.log(request, mp, mv, result)

	# Update User Details
	allocatedKwh = len(result)
	totalSpent = sum(result)
	
	request.user.energy_units += allocatedKwh
	request.user.balance -= totalSpent
	request.user.auction_done_today = True
	request.user.save()

	# Save the auction result in Auction History
	auctionHistory = AuctionHistory()
	auctionHistory.user = request.user
	auctionHistory.day = request.user.current_day
	
	if request.user.treatment.treatment_name == "Simple_AAAI_3":
		bids = SIMPLE_BIDS_TRIAL_2
	else:
		bids = SIMPLE_BIDS
	
	
	
	auctionHistory.bid = bids[bidType] * len(mv)
	auctionHistory.total_spent = totalSpent
	auctionHistory.kwh_won = allocatedKwh
	auctionHistory.recorded = timezone.now()
	auctionHistory.save()

	return HttpResponse(json.dumps({
									"auctionResult": result,
									"totalSpent": totalSpent,
									"allocatedKwh": allocatedKwh}), 
									content_type="application_json")
	

def run_progressive_auction(request):
	
	# Already done?
	events = AuctionEvent.objects.filter(user=request.user,day=request.user.current_day)
	
	if request.user.auction_done_today == True and len(events) > 0:
		# Yes!
		return HttpResponse(json.dumps({
									"auctionResult": events[0].result,
									"totalSpent": events[0].total_pay,
									"allocatedKwh": events[0].allocated_units}), 
									content_type="application_json")
	
	marginal_generator = GeneratorFactory.getInstance(request.user.treatment.price_vector_generator)

	if not request.user.ev_guru_mode:
		day = utils.getDay(request.user.current_day, request.user.treatment)
	else: 
		day = Day()
		day.units_available = DEFAULT_AVAILABLE_UNITS

	# Generate the vector of marginal prices
	mp = marginal_generator.generate_marginal_price_vector(day, request.user)

	# Build the vector of marginal values from the user's input
	kwhs = request.POST.getlist("kwhs[]")
	bids = request.POST.getlist("bids[]")

	request.user.last_progressive_kwhs = [int(x) for x in kwhs]
	request.user.last_progressive_bids = [float(x) for x in bids]

	mv = auction.generate_progressive_values_vector(kwhs, bids)

	# Run the auction
	result = auction.run_auction(mp, mv)

	# Log the Auction Event 
	AuctionEvent.log(request, mp, mv, result)

	# Update User Details
	allocatedKwh = len(result)
	totalSpent = sum(result)

	request.user.energy_units += allocatedKwh
	request.user.balance -= totalSpent
	request.user.auction_done_today = True
	request.user.save()


	# Save the auction result in Auction History
	auctionHistory = AuctionHistory()
	auctionHistory.user = request.user
	auctionHistory.day = request.user.current_day
	auctionHistory.bid = bids[len(bids) - 1]
	auctionHistory.total_spent = totalSpent
	auctionHistory.kwh_won = allocatedKwh
	auctionHistory.recorded = timezone.now()
	auctionHistory.save()


	return HttpResponse(json.dumps({
									"auctionResult": result,
									"totalSpent": totalSpent,
									"allocatedKwh": allocatedKwh}), 
									content_type="application_json")



def run_uniform_auction(request):
	
	# Already done?
	events = AuctionEvent.objects.filter(user=request.user,day=request.user.current_day)
	
	if request.user.auction_done_today == True and len(events) > 0:
		# Yes!
		return HttpResponse(json.dumps({
									"auctionResult": events[0].result,
									"totalSpent": events[0].total_pay,
									"allocatedKwh": events[0].allocated_units}), 
									content_type="application_json")
	
	marginal_generator = GeneratorFactory.getInstance(request.user.treatment.price_vector_generator)
	
	if not request.user.ev_guru_mode:
		day = utils.getDay(request.user.current_day, request.user.treatment)
	else: 
		day = Day()
		day.units_available = DEFAULT_AVAILABLE_UNITS

	# Generate the vector of marginal prices
	mp = marginal_generator.generate_marginal_price_vector(day, request.user)
	
	# Build the vector of marginal values from the user's input
	max_kwh = request.POST["max_kwh"]
	bid_per_unit = request.POST["bid_per_unit"]
	mv = auction.generate_marginal_values_vector(int(max_kwh), float(bid_per_unit))

	# Run the auction
	result = auction.run_auction(mp, mv)

	# Log the Auction Event 
	AuctionEvent.log(request, mp, mv, result)

	# Update User Details
	allocatedKwh = len(result)
	totalSpent = sum(result)

	request.user.energy_units += allocatedKwh
	request.user.balance -= totalSpent
	request.user.auction_done_today = True
	request.user.save()

	# Save the auction result in Auction History
	auctionHistory = AuctionHistory()
	auctionHistory.user = request.user
	auctionHistory.day = request.user.current_day
	auctionHistory.bid = (float)(bid_per_unit) * (int)(max_kwh)
	auctionHistory.total_spent = totalSpent
	auctionHistory.kwh_won = allocatedKwh
	auctionHistory.recorded = timezone.now()
	auctionHistory.save()

	dump = json.dumps({"auctionResult": result,
					   "requestedKwh": max_kwh,
					   "totalSpent": totalSpent,
					   "allocatedKwh": allocatedKwh})
	

	return HttpResponse(dump, content_type="application/json")

def auction_result(request):
	c = Context({
					"auction_result": request.session["auction_result"],
					"result_length": len(request.session["auction_result"]),
					"total_spent": sum(request.session["auction_result"]),
					"kwh_requested": request.session["kwh_requested"]
				})
	return render(request, "step2.html", c)



def delivery(request):
	# If the user did not participate in an auction today, redirect to home page
	if not request.user.auction_done_today: 
		return HttpResponseRedirect ("/webapp/home")
	
	# Get the tasks to be performed on this particular day by user
	taskList = request.user.getTasksToPerform()

	#TasksAvailableLog.log(request.user, taskList)

	if len(taskList) > 0:

		# Create the Selection String (task descritpion separated by semicolon)
		taskSelectionString = ";".join("{0}{1}".format(t.description, "") for t in taskList)
		TasksAvailableLog.log(request.user, taskSelectionString)

		# Get the matrix of optimal Task Sets 
		# This will have the following format: [ [shortestPathSolution, totalReward, totalCost], [A;B;D, 12, 5], ...]
		optimalTaskSets = ShortestPath.findOptimalTaskSets(taskSelectionString, request.user.energy_units)
		# To be used in Javascript
		optimalTaskSetsJS = json.dumps(optimalTaskSets)

		# Add the groups of optimal tasks to the context - to be available on the template html page
		c = Context({ 
						"taskList": taskList,
						"optimalTaskSets": optimalTaskSets, 
						"optimalTaskSetsJS": optimalTaskSetsJS 
					})

	else: 
		TasksAvailableLog.log(request.user, "")
		c = Context({
					"taskList": [],
					"optimalTaskSets": [],
					"optimalTaskSetsJS": []

					})

	return render(request, "step2.html", c)



def getTasksToPerform(request):
	json_serializer = serializers.get_serializer("json")()
	task_list = json_serializer.serialize(request.user.getTasksToPerform())

	return HttpResponse(task_list, content_type="application/json")


def findOptimalTaskSet(request):
	availableEnergy = request.user.energy_units - int(request.POST["energyToSpare"])
	taskList = json.loads(request.POST["taskList"])
	taskSelectionString = ";".join("{0}{1}".format(t["description"], "") for t in taskList)
	optimalPath = ShortestPath.findOptimalPath(taskSelectionString, availableEnergy)
	optimalPathTasks = optimalPath.getShortestPathTasks()

	json_serializer = serializers.get_serializer("json")()
	optimalPathTasksJson = json_serializer.serialize(optimalPathTasks)

	return HttpResponse(json.dumps({"shortestPath": optimalPathTasksJson,
									"totalCost": optimalPath.total_cost,
									"totalReward": optimalPath.total_reward}),
									content_type="application_json")


def getOptimalTaskSets(request):
	taskList = json.loads(request.POST["taskList"])
	taskSelectionString = ";".join("{0}{1}".format(t["description"], "") for t in taskList)

	optimalTaskSets = ShortestPath.findOptimalTaskSets(taskSelectionString, request.user.energy_units)

	return HttpResponse(json.dumps({"optimalTaskSets": optimalTaskSets}), content_type="application/json")


@csrf_protect
def getShortestPath(request):
	# Task List as a dict object
	taskList = json.loads(request.POST["taskList"])

	# Build the list of task descriptions (semicolon separated). E.g: "B;D;E"
	taskSelectionString = ";".join("{0}{1}".format(t["description"], "") for t in taskList)

	# Get the Shortest Path for the specified tasks - String of semicolon separated task descritpions. E.g: "D;B;E"
	shortestPath = ShortestPath.objects.filter(task_selection = taskSelectionString)[0]

	# Build the actual list of Task objects forming the shortest path. E.g: [<Task: D>, <Task: B>, <Task: E>]
	shortestPathTasks = shortestPath.getShortestPathTasks()

	# Serialize and return the list of tasks as JSON 
	json_serializer = serializers.get_serializer("json")()
	shortestPathJson = json_serializer.serialize(shortestPathTasks)

	logger = logging.getLogger("console_logger")

	return HttpResponse(json.dumps({"shortestPath": shortestPathJson, 
									"totalCost": shortestPath.total_cost, 
									"totalReward": shortestPath.total_reward}),
									content_type="application_json")

def updateUserToNextDay(request):
	
	# Make sure that we're in the correct state
	if not request.user.auction_done_today: 
		
		return HttpResponseRedirect ("/webapp/home")
	
	gainedReward = float(request.POST["gainedReward"])
	consumedEnergy = float(request.POST["consumedEnergy"])
	otherOptions = request.POST["otherOptions"]

	# Log the performing of the tasks
	PerformEvent.log(request, gainedReward, consumedEnergy, otherOptions)
	
	request.user.balance += gainedReward
	request.user.energy_units -= consumedEnergy
	# Save this day History (overwrite existing entries)
	DayHistory.log(request)	

	request.user.current_day += 1
	request.user.auction_done_today = False
	request.user.saved_current_day_history = False
	request.user.save()
	
	# Check if user needs to be reset
	# Users get reset whenever they finish a cycle (each cycle lasts for the number of days
	# defined in their treatment). For instance, if the treatment currently has 30 days, 
	# users' balance should be reset at day 31, 61, 91, etc.
	test_day =  request.user.current_day - 1
		
	if (test_day % request.user.treatment.getNumberOfDays()) == 0:
		if request.user.is_orchid:
			return HttpResponse("orchidNewGame")

			
		# If necessary, show progress to turkers in second trial
		if request.user.is_turker_trial_2:
			if (test_day < request.user.treatment.getNumberOfDays() * SECOND_TRIAL_GAMES):
				return HttpResponse("resetBalancePage")
			else:
				# Let home handle end of the game
				return HttpResponse("home")
				
		
		elif request.user.best_monthly_score == 0: 
			request.user.best_monthly_score = request.user.balance
			request.user.save()
			return HttpResponse("home")
		elif request.user.balance > request.user.best_monthly_score:
			request.user.best_monthly_score = request.user.balance
			request.user.save()
		return HttpResponse("resetBalancePage")
	else:
		return HttpResponse("home")

def resetBalancePage(request):
	if request.user.is_turker_trial_2:
		# Special treatment if trial 2:
		
		test_day= request.user.current_day - 1
		game = test_day / request.user.treatment.getNumberOfDays()
		total_profit = get_profit(request.user)
		bonus_so_far = get_bonus_payment(total_profit)
		games_left = SECOND_TRIAL_GAMES - game
		
		c = Context({ 
					"game": game,
					"total_profit": total_profit,
					"bonus_so_far" : bonus_so_far,
					"games_left" : games_left,
					})
		
		#request.user.balance = request.user.treatment.user_initial_balance
		request.user.energy_units = request.user.treatment.user_initial_energy_units
		request.user.save()
		return render(request, "reset_page_trial_2.html",c)
	
	else:
		c = Context({ "monthly_score": DayHistory.objects.filter(user_id = request.user.pk, day = (request.user.current_day - 1))[0].balance })
		request.user.balance = request.user.treatment.user_initial_balance
		request.user.energy_units = request.user.treatment.user_initial_energy_units
		request.user.save()
		return render(request, "reset_page.html", c)

	

def skipAuction(request):
	AuctionEvent.log(request, [], [], [])
	request.user.auction_done_today = True
	request.user.save()
	return HttpResponse("")


def gameComplete(request):
	# Redirect to Home if the user has not completed all days 
	if request.user.current_day <= request.user.treatment.getNumberOfDays(): 
		return HttpResponseRedirect ("/webapp/home/")
	
	return render(request, "game-complete.html")

def auctionTookPlaceToday(request):
	return HttpResponse(True) if request.user.auction_done_today else HttpResponse(False)

def logTaskClickEvent(request):
	TaskClickEvent.log(request)
	return HttpResponse("")

def becomeEvGuru(request):
	request.user.ev_guru_mode = True
	request.user.balance = request.user.treatment.user_initial_balance
	request.user.save()
	return HttpResponseRedirect("/webapp/home")

def leaderboard(request):
	
	if request.user.is_authenticated() and request.user.is_orchid:
		return HttpResponseRedirect("/webapp/orchidLeaderboard")

	users = EVUser.objects.filter(treatment = request.user.treatment, is_admin = 0, is_turker = 0).exclude(current_day = 1, experiment__experiment_name = ORCHID_SHOWCASE).order_by("-best_monthly_score", "-balance", "current_day", "username")
	c = Context({ "users": users })
	return render(request, "leaderboard.html", c)

def history(request):
	# auctionEvents = AuctionEvent.objects.filter(user = request.user).order_by("date_time")
	dayHistory = DayHistory.objects.filter(user = request.user).order_by("day").reverse()[0:request.user.current_day].reverse()	
	auctionHistory = AuctionHistory.objects.filter(user = request.user).order_by("day").reverse()[0:request.user.current_day].reverse()

	c = Context({	
					"dayHistory": dayHistory,
					"auctionHistory": auctionHistory,
				})
	return render(request, "history.html", c)

def settings(request):
	return render(request, "settings.html")


def survey(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/webapp/rules")

 
 	if not (request.user.current_day > request.user.treatment.getNumberOfDays() * SECOND_TRIAL_GAMES \
 				or (not request.user.is_turker_trial_2 and request.user.current_day > request.user.treatment.getNumberOfDays())):
 		return HttpResponseRedirect("/webapp/home")


	profit = get_profit(request.user)
	bonus_payment = get_bonus_payment(profit)
	total_payment = get_total_payment(profit)
	questions = TRIAL_2_QUESTIONS
	
	if request.method == "GET":
		if request.user.is_turker_trial_2:
			return render(request,"turk_survey_trial_2.html",Context(locals()))
		else:
			return render(request,"turk_survey.html",Context(locals()))
	
	survey = Survey()
	survey.date_time = timezone.now()
	survey.user = request.user
	
	valid = True
	
	print request.POST
	
	if "genderRadio" not in request.POST:
		valid = False
	else:
		genderRadio = request.POST["genderRadio"]
		survey.gender = genderRadio
		
	
	if "ageRadio" not in request.POST:
		valid = False
	else:
		ageRadio = request.POST["ageRadio"]
		survey.age = ageRadio	
		
	if "educationRadio" not in request.POST:
		valid = False
	else:
		educationRadio = request.POST["educationRadio"]
		survey.education =	 educationRadio
		
	if "residence" not in request.POST or request.POST["residence"] == "":
		valid = False
	else:
		residence = request.POST["residence"]
		survey.country = residence
	
	if "carRadio" not in request.POST:
		valid = False
	else:
		carRadio = request.POST["carRadio"]
		if carRadio == "Yes":
			survey.car_owner = True
		else:
			survey.car_owner = False

	if "evRadio" not in request.POST:
		valid = False
	else:
		evRadio = request.POST["evRadio"]
		if evRadio == "Yes":
			survey.driven_ev = True
		else:
			survey.driven_ev = False	

	if "strategy" in request.POST:
		strategy = request.POST["strategy"]
		survey.strategy = strategy
		
	if "strategy_change" in request.POST:
		strategy_change = request.POST["strategy_change"]
		survey.strategy_change = strategy_change

	if "comments" in request.POST:
		comments = request.POST["comments"]
		survey.comments = comments
		
	if request.user.is_turker_trial_2:
		# Evaluate usability questions
		answers = []
		total_score = 0
		usability_valid = True
		for (question,question_id,positive) in TRIAL_2_QUESTIONS:
			if question_id not in request.POST :
				usability_valid = False
				answers.append(-1)
			else:
				value = request.POST[question_id]
				if isInt(value,1,5):
					as_int = int(value)
					answers.append(as_int)
					if positive:
						total_score +=  as_int - 1
					else:
						total_score += (5-as_int)
				else:
					usability_valid = False
					answers.append(-1)
		
		if usability_valid:
			survey.usability_answers = ",".join(str(x) for x in answers)
			survey.usability_score = total_score
		else:
			valid = False 
	
	
	#for i in range(1,len(questions)+1):
	#	print "%s) %s" % (i,questions[i-1][0] )
	
	questions = [(a,b,c,d) for ((a,b,c),d) in zip(questions,answers)]
	
	#print answers
	#print questions
	
	if valid:
		survey.save()
		
		completion = Completion()
		completion.base_payment = game_settings.TURK_BASE_PAYMENT
		completion.bonus_payment = bonus_payment
		completion.date_time = timezone.now()
		completion.paid = False
		completion.user = request.user
		completion.save()
		
		return HttpResponseRedirect("/webapp/hit_done")
		
	else:
		
		anchor = "input_missing"
		input_error = True
		if request.user.is_turker_trial_2:
			return render(request,"turk_survey_trial_2.html",Context(locals()))
		else:
			return render(request,"turk_survey.html",locals())


def hitDone(request):
	profit = get_profit(request.user)
	total_payment = get_total_payment(profit)
	return render(request,"turk_complete.html",locals())
	

def _getPaymentContext():
	
	bonus_per_profit = '%.2f' % game_settings.TURK_BONUS_PER_PROFIT
	max_bonus = '%.2f' % game_settings.TURK_MAX_BONUS
	bonus_example = '%.2f' % (50 * game_settings.TURK_BONUS_PER_PROFIT)
	base_payment = '%.2f' % game_settings.TURK_BASE_PAYMENT
	
	return { "bonus_example" : bonus_example, "bonus_per_profit" : bonus_per_profit, 'base_payment' : base_payment , "max_bonus" : max_bonus}

def quiz(request):
	
	isAAMAS = "aamas" in request.session.keys() and request.session["aamas"] == True
	
	isTrial2 = "trial_2" in request.session.keys() and request.session["trial_2"] == True
	
	if request.user.is_authenticated() and not request.user.is_turker:
		logout(request)
	
	# Check if we need to create a new user (from MTurk)
	if not request.user.is_authenticated():
		code = getRandomUniqueUsername(10)
		password = generateRandomString(10)
		email = code + "@turker.com"
		user = EVUser.objects.create_user(email, code, password)
		user.is_turker = True
		if isTrial2:
			user.is_turker_trial_2 = True
		user.save()
		user = authenticate(username=code,password=password)
		login(request, user)
	
	if isAAMAS and not request.user.is_aamas:
		request.user.is_aamas = True
		request.user.save()
	
	if request.method == "GET":
		
		c = Context(_getPaymentContext())
		return render(request,"turk_instructions_1.html",c)
	
	if "goalRadio" in request.POST:
		goalAnswer = request.POST["goalRadio"]
	else:
		goalAnswer = "Blank"
	
	if "planRadio" in request.POST:
		planAnswer = request.POST["planRadio"]
	else:
		planAnswer = "Blank"
		
	if "auctionRadio" in request.POST:
		auctionAnswer = request.POST["auctionRadio"]
	else:
		auctionAnswer = "Blank"
	
	if "consent_check" in request.POST and request.POST["consent_check"] == "on":
		consentAnswer = True
	else:
		consentAnswer = False
	
	correct = goalAnswer == "option2" and planAnswer == "option5" and auctionAnswer == "option3"
	
	QuizHistory.log(request.user,goalAnswer,planAnswer,auctionAnswer,consentAnswer,correct)
	
	if not consentAnswer:
		c1 = _getPaymentContext()
		c1.update({"consent_error" : True, "anchor" : "consent", "goalAnswer" : goalAnswer, "planAnswer" : planAnswer, "auctionAnswer" : auctionAnswer})
		c = Context(c1)
		return render(request,"turk_instructions_1.html",c)
	
	if not correct:
		c1 = _getPaymentContext()
		c1.update({"consent_given" : True, "quiz_error" : True, "anchor" : "quiz", "goalAnswer" : goalAnswer, "planAnswer" : planAnswer, "auctionAnswer" : auctionAnswer })
		c = Context(c1)
		return render(request,"turk_instructions_1.html",c)
	
	
	# Continue to game here...
	return HttpResponseRedirect ("/webapp/home/")
	

def updateSettings(request):
	username = request.POST["username"]
	agree_emails = request.POST["agreeToEmails"]
	request.user.username = username
	request.user.agree_to_receive_email = agree_emails
	request.user.save()

	c = Context({ "saved_ok": 1 })

	return render(request, "settings.html", c)


def aamasSkipQuiz(request):
	if not request.user.is_aamas:
		return HttpResponseRedirect ("/webapp/home/")
	existing = QuizHistory.objects.filter(user=request.user,correct=True,consentAnswer=True)
	if len(existing) == 0:
		QuizHistory.log(request.user,"skipped","skipped","skipped",True,True)
	return HttpResponseRedirect ("/webapp/home/")

def aamasResetGame(request):
	logout(request)
	return HttpResponseRedirect ("/jair/")


def aamasChangeExperiment(request):
	
	if not request.user.is_aamas:
		return HttpResponseRedirect ("/webapp/home/")
	
	if request.user.current_day > 10:
		return HttpResponseRedirect ("/jair/")
	
	
	if request.user.treatment.treatment_name == "Simple_AAAI":
		request.user.treatment = Treatment.objects.get(treatment_name="Simple")
		request.user.is_turker_trial_2 = False
	elif request.user.treatment.treatment_name == "Simple_AAAI_3":
		request.user.treatment = Treatment.objects.get(treatment_name="Simple")
		request.user.is_turker_trial_2 = False
	elif request.user.treatment.treatment_name == "Uniform_AAAI":
		request.user.treatment = Treatment.objects.get(treatment_name="Uniform")
		request.user.is_turker_trial_2 = False
	elif request.user.treatment.treatment_name == "Expressive_AAAI":
		request.user.treatment = Treatment.objects.get(treatment_name="Expressive")
		request.user.is_turker_trial_2 = True
	elif request.user.treatment.treatment_name == "Simple":
		request.user.treatment = Treatment.objects.get(treatment_name="Simple_AAAI")
		request.user.is_turker_trial_2 = True
	elif request.user.treatment.treatment_name == "Uniform":
		request.user.treatment = Treatment.objects.get(treatment_name="Uniform_AAAI")
		request.user.is_turker_trial_2 = True
	elif request.user.treatment.treatment_name == "Expressive":
		request.user.treatment = Treatment.objects.get(treatment_name="Expressive_AAAI")
		request.user.is_turker_trial_2 = True
		
	request.user.save()
	print "left %s" % request.user.treatment
	if len(QuizHistory.objects.filter(user=request.user,correct=True,consentAnswer=True)) == 0:
		return HttpResponseRedirect ("/jair/")
	else:
		return HttpResponseRedirect ("/webapp/instructions/")

def aamasChangeMechanism(request):

	if not request.user.is_aamas:
		return HttpResponseRedirect ("/webapp/home/")
	
	if request.user.treatment.treatment_name == "Simple_AAAI":
		request.user.treatment = Treatment.objects.get(treatment_name="Simple_AAAI_3")
	elif request.user.treatment.treatment_name == "Simple_AAAI_3":
		request.user.treatment = Treatment.objects.get(treatment_name="Uniform_AAAI")
	elif request.user.treatment.treatment_name == "Uniform_AAAI":
		request.user.treatment = Treatment.objects.get(treatment_name="Expressive_AAAI")
	elif request.user.treatment.treatment_name == "Expressive_AAAI":
		request.user.treatment = Treatment.objects.get(treatment_name="Simple_AAAI")
	elif request.user.treatment.treatment_name == "Simple":
		request.user.treatment = Treatment.objects.get(treatment_name="Uniform")
	elif request.user.treatment.treatment_name == "Uniform":
		request.user.treatment = Treatment.objects.get(treatment_name="Expressive")
	elif request.user.treatment.treatment_name == "Expressive":
		request.user.treatment = Treatment.objects.get(treatment_name="Simple")
	
	request.user.save()
	print "left %s" % request.user.treatment
	if len(QuizHistory.objects.filter(user=request.user,correct=True,consentAnswer=True)) == 0:
		return HttpResponseRedirect ("/jair/")
	else:
		return HttpResponseRedirect ("/webapp/instructions/")
	
	
def orchid(request):
	
	if request.user.is_authenticated():
		logout(request)
		
	request.session["orchid"] = True
	return render(request, "orchid_start.html")

ORCHID_PASSWORD = "0rch1d_5h0wca5e"
ORCHID_EMAIL = "orchid@xiaoba.co.uk"

def orchidNewPlayer(request):
	if request.user.is_authenticated():
		logout(request)
	
	if request.method == "GET":
		return render(request, "orchid_new_player.html")
	else:
		# Get submitted name
		if "username" in request.POST:
			username = request.POST["username"]
			
			if len(username) == 0:
				return render(request,"orchid_new_player.html", Context({"error_message": "Error: Please provide a name."}))
			
			if len(username) > 254:
				return render(request,"orchid_new_player.html", Context({"error_message": "Error: Name can't be longer than 254 characters."}))
			
			if len(EVUser.objects.filter(username=username)):
				return render(request,"orchid_new_player.html", Context({"error_message": "Error: A user with this name already exists."}))
			
			if "leaderboard" in request.POST and request.POST["leaderboard"] == "on":
				leaderboard_allowed = True
			else:
				leaderboard_allowed = False
				
			if "research" in request.POST and request.POST["research"] == "on":
				research_allowed = True
			else:
				research_allowed = False
			
			user = EVUser.objects.create_user(ORCHID_EMAIL, username, ORCHID_PASSWORD)
			user.experiment = Experiment.objects.get(experiment_name=ORCHID_SHOWCASE)
			user.research_allowed = research_allowed
			user.leaderboard_allowed = leaderboard_allowed
			user.reassign_treatment()
			user.completed_tutorial = False
			user.save()
			user = authenticate(username=username,password=ORCHID_PASSWORD)
			login(request, user)
			return HttpResponseRedirect ("/webapp/home/")
				
		else:
			return render(request,"orchid_new_player.html", Context({"error_message": "Error: Please provide a name."}))
			

def orchidExistingPlayer(request):
	if request.user.is_authenticated():
		logout(request)
	
	users = EVUser.objects.filter(experiment__experiment_name=ORCHID_SHOWCASE)
	
	if request.method == "GET":
		
		users = sorted(users,key=lambda user:user.username)
		
		return render(request,"orchid_existing_player.html", Context({"users" : users}))
	
	else:
		
		if "user" in request.POST:
			username = request.POST["user"]
			try:
				user = authenticate(username=username,password=ORCHID_PASSWORD)
				login(request, user)
				return HttpResponseRedirect ("/webapp/home/")
			except:
				return render(request,"orchid_existing_player.html", Context({"users" : users,"error_message" : "Something went wrong. Try again."}))
		else:
			return render(request,"orchid_existing_player.html", Context({"users" : users,"error_message" : "Please select a user."}))	

def orchidNewGame(request):
		
		
		previousBest = request.user.best_monthly_score
		profit = request.user.balance - request.user.treatment.user_initial_balance
		
		game = request.user.current_day / request.user.treatment.getNumberOfDays()
		
		if profit > previousBest or game == 1:
			request.user.best_monthly_score = profit
			c = Context({"new_best" : profit, "game":game })
		else:
			c = Context({"old_best" : previousBest,"profit" : profit, "game":game })
			
		request.user.energy_units = request.user.treatment.user_initial_energy_units
		request.user.balance = request.user.treatment.user_initial_balance
		request.user.save()
		
		return render(request, "reset_page_orchid.html",c)

def orchidLeaderboard(request):
	users = EVUser.objects.filter(is_admin = 0, is_turker = 0, experiment__experiment_name = ORCHID_SHOWCASE, leaderboard_allowed = 1).exclude(current_day = 1).exclude(best_monthly_score = 0).order_by("-best_monthly_score", "-balance", "current_day", "username")
	c = Context({ "users": users })
	return render(request, "orchid_leaderboard.html", c)

def orchidPerformance(request):
#	users = EVUser.objects.filter(is_admin = 0, is_turker = 0, experiment__experiment_name = ORCHID_SHOWCASE, leaderboard_allowed = 1).exclude(current_day = 1).exclude(best_monthly_score = 0).order_by("-best_monthly_score", "-balance", "current_day", "username")
	#c = Context({ "users": users })
	return render(request, "treatment_performance.html")
