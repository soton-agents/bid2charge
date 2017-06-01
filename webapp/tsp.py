from game_settings import DISTANCE_MULTIPLIER
import itertools
import math

# Whether distance method of tasks should be used.
use_distance_method = False

# Generate all possible tours of the tasks and choose the shortest one
def solve_tsp(tasks):
	return shortest(alltours(tasks))

# Buld a list of tours, each a permutation of tasks
# Each permutation will start with the same task (Home task)
def alltours(tasks):
	home = tasks.pop(0)
	return [[home] + list(tour) for tour in itertools.permutations(tasks)]

# Get the tasks tour with the minimum total distance
def shortest(tasks):
	# min(collection, key=function) means: find the element x that 
	# is a memeber of collection s.t. function(x) is minimized.
	return min(tasks, key=total_distance)

# Calculate the total distance between each pair of consecutive
# tasks in the array of tasks passed as an argument
def total_distance(tasks):
	return sum(distance(tasks[i], tasks[i-1]) for i in range(len(tasks)))

# Get the first element of any collection
def first(collection):
	for element in collection: return element

# Function that calculates the distance between 2 points - includes a factor multiplication for better scaling
def distance(T1, T2):
	if use_distance_method:
		try:
			return T1.distance_to(T2)
		except:
			print "Could not use distance method."
	
	return math.sqrt(math.pow((T1.x - T2.x), 2) + math.pow((T1.y - T2.y), 2)) * DISTANCE_MULTIPLIER