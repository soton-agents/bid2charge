'''
Created on 10 Oct 2014

@author: ss2
'''

import math
import itertools

from webapp import game_settings
from webapp import tsp
from webapp.game_settings import DISTANCE_MULTIPLIER, KWH_PER_KM

# First some data containers (mirror some of the classes in Django model, but we want
# this to work as a self-contained app


class ProblemDescription:
    
    def __init__(self, days, parameters, compute_options=True):
        self.days = days
        self.parameters = parameters
        if compute_options:
            self.computeAllOptions()
    
    # Computes all options for every days
    def computeAllOptions(self):
        for d in self.days:
            d.computeOptions(self.parameters)
        

class DayDescription:
    
    def __init__(self, tasks):
        self.tasks = tasks
        
    def __transform_to_coordinates(self, tasks):
        return [x.coordinates for x in tasks]
    
    # This works out the possible outcomes for each day
    def computeOptions(self, parameters):
        
        self.options = []
        
        # Store values of previously computed shortest path solutions here
        cache = {}
        
        # Set this to true, so it uses the distance_to method
        tsp.use_distance_method = True
        
        # For all combinations of tasks
        for available in itertools.product((False, True), repeat=len(self.tasks)):
            # Available is true / false for each task, to indicate if task is available.
            # Build array of actual tasks
            chosen_tasks = []
            counter = 0
            probability = 1
            for included in available:
                if included:
                    chosen_tasks.append(self.tasks[counter])
                    probability = probability * self.tasks[counter].probability
                else:
                    probability = probability * (1 - self.tasks[counter].probability)
                counter = counter + 1
            
            #print(chosen_tasks)
                
            # Work out shortest path for this exact subset
            shortest = parameters.km_per_unit * tsp.total_distance(tsp.solve_tsp([parameters.home_coordinates] + self.__transform_to_coordinates(chosen_tasks)))
            
            # Round down to mirror behaviour of server
            shortest = math.floor(shortest) 
            value = sum([x.value for x in chosen_tasks])

            # Round up final cost
            shortest = int(math.ceil(shortest * parameters.kWh_per_km))

            # Save this result            
            cache[str(chosen_tasks)] = (shortest, value)
            
            # print (tsp.total_distance(shortest),value)
            
            # Now work out subsets of tasks to do
            subsets = []
            for i in range(len(chosen_tasks) + 1):
                combinations = itertools.combinations(chosen_tasks, r=i)
                this_subset = []
                for p in combinations:
                    attributes = cache[str(list(p))]
                    this_subset.append((p, attributes))
                #print this_subset
                this_subset.sort(key=lambda x : x[1][1], reverse=True)
                #print this_subset
                
                j = 0
                while j < len(this_subset) - 1:
                    # Check if one is clearly dominated
                    dominated = -1
                    if this_subset[j][1][1] >= this_subset[j + 1][1][1]:
                        if this_subset[j][1][0] <= this_subset[j + 1][1][0]:
                            dominated = j + 1
                    elif this_subset[j][1][1] <= this_subset[j + 1][1][1]:
                        if this_subset[j][1][0] >= this_subset[j + 1][1][0]:
                            dominated = j
                    if dominated != -1:
                        removed = this_subset.pop(dominated)
                        #print "removed %s" % str(removed)
                    else:
                        j = j + 1
                
                subsets = subsets + this_subset
            
            # Now record options for this case
            self.options.append((probability, subsets))
        
        #print "Final options:"
        #for o in self.options:
        #    print o

    

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distance_to(self, other):
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
        return distance

class Parameters:
    def __init__(self, kWh_per_km, km_per_unit, max_battery, initial_battery, home_coordinates, battery_discharge):
        self.kWh_per_km = kWh_per_km
        self.km_per_unit = km_per_unit
        self.max_battery = max_battery
        self.initial_battery = initial_battery
        self.home_coordinates = home_coordinates
        self.battery_discharge = battery_discharge

class TaskDescription:
    
    counter = 1
    
    
    def __init__(self, probability, value, coordinates, name=None):
        self.probability = probability
        self.value = value
        self.coordinates = coordinates
        if name == None:
            self.name = "T%s (%s,%s)" % (TaskDescription.counter, value, probability)
            TaskDescription.counter = TaskDescription.counter + 1 
        else:
            self.name = "%s (%s, %s)" % (name, value, probability)
    
    def __repr__(self):
        return self.name
        

def generate_parameters_from_game(home_x=0.5, home_y=0.5):
    home_coordinates = Coordinates(home_x, home_y)
    
    kWh_per_km = game_settings.KWH_PER_KM
    km_per_unit = game_settings.DISTANCE_MULTIPLIER
    initial_battery = game_settings.DEFAULT_USER_ENERGY_UNITS
    max_battery = game_settings.DEFAULT_BATTERY_CAPACITY
    
    return Parameters(kWh_per_km, km_per_unit, max_battery, initial_battery, home_coordinates, 0)
    
    
def create_simple_training_day():
    task = TaskDescription(1, 5, Coordinates(0.5, 0.75), "Close")
    return DayDescription([task])

def create_simple_training_day_2():
    task = TaskDescription(1, 15, Coordinates(0.9, 0.9), "Far")
    return DayDescription([task])



top_left_far = Coordinates(0.1, 0.1)
top_left = Coordinates(0.25, 0.25)
top_left_close = Coordinates(0.35, 0.35)

top_far = Coordinates(0.5, 0.1)
top = Coordinates(0.5, 0.25)
top_close = Coordinates(0.5, 0.3)

top_right_far = Coordinates(0.8, 0.1)
top_right = Coordinates(0.75, 0.25)
top_right_close = Coordinates(0.65, 0.35)

left_far = Coordinates(0.1, 0.5)
left = Coordinates(0.25, 0.5)

right_far = Coordinates(0.9, 0.5)
right = Coordinates(0.75, 0.5)

bottom_left_far = Coordinates(0.1, 0.8)
bottom_left = Coordinates(0.25, 0.75)

bottom_far = Coordinates(0.5, 0.8)
bottom = Coordinates(0.5, 0.75)

bottom_right_far = Coordinates(0.9, 0.8)
bottom_right = Coordinates(0.75, 0.75)

home = Coordinates(0.5,0.5)

VALUES = [10,5,5,5,10,5,10,15,15]
COORDINATES = [top_left,top_left,top_close,top_right_close,bottom_left,bottom,bottom_right,bottom_left_far,bottom_right_far] 

VALUES_AAAI = [5,5,10,5,15,15,5,15,15]
COORDINATES_AAAI = [top_close,top_right_close,bottom_left,bottom,bottom_right_far,top_right,top_left_far,top_right_close,top_far] 

def create_simple_aaai_raw():
    dayList = []
    
    dayList.append([(0,1.0)]) 
    
    dayList.append([(0,1.0),(1,0.5)])
    dayList.append([(0,1.0),(1,0.5)])
    
    dayList.append([(0,1.0),(1,0.5),(2,0.5)])
    dayList.append([(0,1.0),(1,0.5),(2,0.5)])
    
    dayList.append([(2,0.5),(3,0.5),(4,0.25)])
    dayList.append([(2,0.5),(3,0.5),(4,0.25)])
    
    dayList.append([(0,1.0),(2,0.5),(3,0.5),(4,0.25),(5,0.75)])
    dayList.append([(0,1.0),(2,0.5),(3,0.5),(4,0.25),(5,0.75)])
    
    dayList.append([(2,0.3),(3,0.3),(5,0.25)])

    return (dayList,VALUES_AAAI,COORDINATES_AAAI)

def create_simple_aaai_2_raw():
    dayList = []
    
    dayList.append([(0,1.0)])
    
    dayList.append([(0,1.0),(1,0.5)])
    dayList.append([(6,1.0)])
    
    dayList.append([(5,0.5),(8,0.5)])
    dayList.append([(5,0.5),(8,0.5)])
    
    dayList.append([(2,0.5),(3,0.25),(4,0.25)])
    dayList.append([(2,0.5),(3,0.25),(4,0.25)])
    
    dayList.append([(0,1.0),(2,0.5),(3,0.5),(4,0.25),(5,0.75)])
    dayList.append([(0,1.0),(2,0.5),(3,0.5),(4,0.25),(5,0.75)])
    
    dayList.append([(2,0.3),(3,0.3),(5,0.25)])

    return (dayList,VALUES_AAAI,COORDINATES_AAAI)


def create_simple_aaai_3_raw():
    dayList = []
    
    dayList.append([(0,1.0)])
    
    dayList.append([(0,1.0),(1,0.5)])
    dayList.append([(6,1.0)])
    
    dayList.append([(5,0.5),(8,0.5)])
    dayList.append([(5,0.5),(8,0.5)])
    
    dayList.append([(2,0.5),(0,0.5),(4,0.2)])
    dayList.append([(2,0.5),(0,0.5),(4,0.2)])
    
    dayList.append([(0,1.0),(2,0.5),(3,0.5),(4,0.25),(5,0.5)])
    dayList.append([(0,1.0),(2,0.5),(3,0.5),(4,0.25),(5,0.5)])
    
    dayList.append([(2,0.3),(5,0.25)])

    return (dayList,VALUES_AAAI,COORDINATES_AAAI)


def create_simple_aaai_4_raw():
    dayList = []
    
    dayList.append([(0,1.0)])
    
    dayList.append([(0,1.0),(1,0.75)])
    dayList.append([(6,1.0),(2,0.25)])
    
    dayList.append([(4,0.75),(8,0.5)])
    dayList.append([(4,0.75),(8,0.5)])
    
    dayList.append([(2,0.5),(0,0.5),(4,0.2)])
    #dayList.append([(2,0.5),(0,0.5),(4,0.2)])
    dayList.append([(6,1.0),(2,0.25)])
    
    dayList.append([(2,0.5),(3,1),(4,0.5),(8,0.25)])
    dayList.append([(2,0.5),(3,1),(4,0.5),(8,0.25)])
    
    dayList.append([(2,0.3),(4,0.5)])
    
    return (dayList,VALUES_AAAI,COORDINATES_AAAI)


def create_simple_orchid_raw_TEST():
    dayList = []
    
    dayList.append([(0,1.0)])
    
    dayList.append([(0,1.0),(1,0.8)])
    
    dayList.append([(0,1.0),(1,0.8),(2,0.9)])
    
    dayList.append([(3,1.0),(4,1.0)])
    
    dayList.append([(0,0.8),(1,0.8),(3,0.8)])
    
    dayList.append([(5,0.8),(4,0.8),(2,1.0),(0,1.0)])
    
    dayList.append([(5,0.8),(4,0.8),(2,1.0),(0,1.0)])
    
    return (dayList,VALUES_AAAI,COORDINATES_AAAI)


def create_simple_orchid_raw():
    dayList = []
    
    dayList.append([(0,1.0)])
    
    dayList.append([(0,1.0),(1,1.0)])
    
    dayList.append([(3,1.0),(4,1.0)])
    
    dayList.append([(0,0.8),(1,0.8),(3,0.8)])
    
    dayList.append([(5,0.8),(4,0.8),(6,1.0),(0,1.0)])
    
    return (dayList,VALUES_AAAI,COORDINATES_AAAI)

# Just for visualisation:
def create_single_full_day_raw():
    dayList = [[(i,1.0) for i in range(len(VALUES))]]
    return (dayList, VALUES, COORDINATES)


def create_final_raw_data():
    # First 2 days - easy, get used to game - 1 task, sure
    dayList = []
    
    task1 = (2,1.0)
    
    for i in range(2):
        dayList.append([task1])
        
    # Next day - one extra task
    
    task2 = (3,0.8)
    
    for i in range(1):
        dayList.append([task1,task2])
    
    # 2 days: Add third task, further away, higher value
    
    task3 = (6,0.75)
    
    for i in range(2):
        dayList.append([task1,task2,task3])
        
    # 3 days: Three tasks
    
    task4 = (4,0.5)
    task5 = (8,0.5)
    task6 = (1,0.8)
    
    for i in range(3):
        dayList.append([task4, task5, task6])
    
    # 3 days: one high one low
        
    task7 = (1,0.5)
    task8 = (4,1)
    
    for i in range(3):
        dayList.append([task7, task8])
    
    # Days 14, 15, 16: Adding high-value, far
    
    task9 = (8,0.5)
    
    for i in range(2):
        dayList.append([task7, task9])
        
    # Days 17, 18, 19: Another high-value, far
    
    task10 = (7,0.5)
    
    for i in range(2):
        dayList.append([task7, task9, task10])
    
    # Days 20, 21, 22: Replace 2 uncertain high-value by 1 certain:
    
    task11 = (7,1)
     
    
    for i in range(2):
        dayList.append([task11, task7])
        
    # Days 23, 24, 25: Many uncertain tasks
    
    task14 = (3,0.4)
    task15 = (0,0.25)
    task16 = (5,0.25)
    task17 = (4,0.25)
    task18 = (8,0.2)
    
    for i in range(3):
        dayList.append([task14, task15, task16, task17, task18])
        
    # Days 26, 27, 28: Few tasks
    
    task19 = (1,0.5)
    task20 = (5,0.5)
    
    for i in range(2):
        dayList.append([task19, task20])
    
    # Days  29, 30: Many tasks
    
    task21 = (8,0.4)
    task22 = (7,0.4)
    task23 = (0,0.6)
    task24 = (5,0.8)
    task25 = (6,0.5)
    task26 = (2,0.5)
    
    for i in range(4):
        dayList.append([task21, task22, task23, task24, task25, task26])
   
    # Few tasks again
    
    for i in range(2):
        dayList.append([task19, task20])
    
    # Give out bonus to those paying attention
    for i in range(2):
        dayList.append([task7, task8])
    
    return (dayList,VALUES,COORDINATES)


def create_simple_raw_data():
    
    dayList = []
    
    task1 = (2,1.0)
    
    dayList.append([task1])
        
    # Next day - one extra task
    
    task2 = (3,0.8)
    
    for i in range(1):
        dayList.append([task1,task2])
    
    # 2 days: Add third task, further away, higher value
    
    task3 = (6,0.75)
    
    for i in range(2):
        dayList.append([task1,task2,task3])
        
    # 3 days: Three tasks
    
    task4 = (4,0.5)
    task5 = (8,0.5)
    task6 = (1,0.8)
    
    for i in range(3):
        dayList.append([task4, task5, task6])
    
    # 3 days: one high one low
        
    task7 = (1,0.5)
    task8 = (4,1)
    
    for i in range(3):
        dayList.append([task7, task8])
    
    # Days 14, 15, 16: Adding high-value, far
    
    task9 = (8,0.5)
    
    for i in range(2):
        dayList.append([task7, task9])
        
    # Days 17, 18, 19: Another high-value, far
    
    task10 = (7,0.5)
    
    for i in range(2):
        dayList.append([task7, task9, task10])
    
    # Days 20, 21, 22: Replace 2 uncertain high-value by 1 certain:
    
    task11 = (7,1)
     
    
    for i in range(2):
        dayList.append([task11, task7])
        
    # Days 23, 24, 25: Many uncertain tasks
    
    task14 = (3,0.4)
    task15 = (0,0.25)
    task16 = (5,0.25)
    task17 = (4,0.25)
    task18 = (8,0.2)
    
    for i in range(3):
        dayList.append([task14, task15, task16, task17, task18])
        
    # Days 26, 27, 28: Few tasks
    
    task19 = (1,0.5)
    task20 = (5,0.5)
    
    for i in range(2):
        dayList.append([task19, task20])
    
    # Days  29, 30: Many tasks
    
    task21 = (8,0.4)
    task22 = (7,0.4)
    task23 = (0,0.6)
    task24 = (5,0.8)
    task25 = (6,0.5)
    task26 = (2,0.5)
    
    for i in range(4):
        dayList.append([task21, task22, task23, task24, task25, task26])
   
    # Few tasks again
    
    for i in range(2):
        dayList.append([task19, task20])
    
    # Give out bonus to those paying attention
    for i in range(2):
        dayList.append([task7, task8])
    
    return (dayList,VALUES,COORDINATES)


def generate_aaai_problem():
    return convert_from_raw(*create_simple_aaai_raw())

def generate_aaai_2_problem():
    return convert_from_raw(*create_simple_aaai_2_raw())

def generate_aaai_3_problem():
    return convert_from_raw(*create_simple_aaai_3_raw())

# This was used for AAAI paper:
def generate_aaai_4_problem():
    return convert_from_raw(*create_simple_aaai_4_raw())


def generate_orchid_problem():
    return convert_from_raw(*create_simple_orchid_raw())

# This was used for original paper:
def generate_final_problem():
    return convert_from_raw(*create_final_raw_data()) 

def convert_from_raw(dayList,values,coordinates):
    real_days = []
    
    for tasks in dayList:
        day = []
        for (task,prob) in tasks:
            day.append(TaskDescription(prob, values[task], coordinates[task]))
        real_days.append(DayDescription(day))
    
    return ProblemDescription(real_days, generate_parameters_from_game())
    
def generate_longer_problem():
    task1 = TaskDescription(0.8, 5, Coordinates(0.5, 0.75), "A")
    task2 = TaskDescription(0.5, 10, Coordinates(0.8, 0.45), "B")
    task3 = TaskDescription(0.1, 15, Coordinates(0.2, 0.2), "C")
    task4 = TaskDescription(0.1, 15, Coordinates(0.7, 0.2), "D")
    
    task5 = TaskDescription(0.5, 5, Coordinates(0.9, 0.1), "E")
    task6 = TaskDescription(0.5, 30, Coordinates(0.8, 0.8), "F")
    
    taskSimple = TaskDescription(1.0, 5, Coordinates(0.5, 0.25), "Start")
    
    taskHigh = TaskDescription(0.7, 15, Coordinates(0.25, 0.75), "High")
    
    taskMedium = TaskDescription(0.8, 10, Coordinates(0.75, 0.75), "Medium")
    
    parameters = generate_parameters_from_game()
    
    dayList = []
    
    for i in range(2):
        dayList.append(DayDescription([taskSimple]))
    
    for i in range(2):
        dayList.append(DayDescription([taskHigh]))
        
    for i in range(2):
        dayList.append(DayDescription([taskSimple, taskMedium]))
        
    for i in range(2):
        dayList.append(DayDescription([taskMedium, taskHigh]))
    
    for i in range(5):
        dayList.append(DayDescription([task1, task2, task3]))
        
    for i in range(5):
        dayList.append(DayDescription([task1]))
        
    for i in range(5):
        dayList.append(DayDescription([task1, task2, task6]))
    
    for i in range(5):
        dayList.append(DayDescription([task1, task2]))
        
    for i in range(5):
        dayList.append(DayDescription([task1, task2, task6]))
        
    for i in range(5):
        dayList.append(DayDescription([task1, task2]))
        
        
    return ProblemDescription(dayList, parameters)

def generate_simple_problem(days=30):
    task1 = TaskDescription(0.8, 5, Coordinates(0.5, 0.75), "A")
    task2 = TaskDescription(0.4, 10, Coordinates(0.8, 0.45), "B")
    task3 = TaskDescription(0.1, 15, Coordinates(0.2, 0.2), "C")
    task4 = TaskDescription(0.1, 15, Coordinates(0.7, 0.2), "D")

    tasks = [task1, task2, task3, task4]

    parameters = generate_parameters_from_game()
    dayList = []
    
    for i in range(days):
        dayList.append(DayDescription(tasks))
    
    return ProblemDescription(dayList, parameters)

def print_table(exp1,coords,values,letters):
    for (i,l) in zip(range(len(exp1)),exp1):
        s =  "Day %d " % (i+1)
        for (t,p) in l:
            s += "& %c(%d,%.2f) " % ( letters[AAMAS_coords[t]], values[t], p)
        for _ in range(len(l),6):
            s += "& "
        s += "\\\\"
        print s
    
      

if __name__ == '__main__':
    #simple = generate_simple_problem(10)
    #simple = generate_final_problem()
    
    
    #          0      1         2       3                4         5         6             7              8                9         10          11
    coords = [home,top_left,top_close,top_right_close,bottom_left,bottom,bottom_right,bottom_left_far, bottom_right_far,top_right,top_left_far,top_far]
    
    
    AAMAS = [top_left,top_left,top_close,top_right_close,bottom_left,bottom,bottom_right,bottom_left_far,bottom_right_far]
    AAMAS_coords = [1,1,2,3,4,5,6,7,8] 

    AAAI = [top_close,top_right_close,bottom_left,bottom,bottom_right_far,top_right,top_left_far,top_right_close,top_far]
    AAAI_coords = [ 2,3,4,5,8,9,10,3,11 ] 

    tasks = len(coords)
    letters = [chr(ord("A")+i) for i in range(tasks)]
    
    for i in range(tasks):
        for j in range(tasks):
            x1 = coords[i].x
            y1 = coords[i].y
            x2 = coords[j].x
            y2 = coords[j].y
            distance = math.sqrt((x1 - x2)**2 + (y1-y2)**2) * DISTANCE_MULTIPLIER
            
            print "%d -> %d : %f km" % (i,j,distance)
    
    
    print " table: "
    
    for i in range(tasks):
        print "\t%d & %.2f & %.2f \\\\" % (i,coords[i].x * DISTANCE_MULTIPLIER, (1-coords[i].y) * DISTANCE_MULTIPLIER)
    
    print " Exp 1: "
    
    (exp1,values,coordinates) = create_final_raw_data()
    print_table(exp1,AAMAS_coords,values,letters)
    
    print " Exp 2: "
    
    (exp1,values,coordinates) = create_simple_aaai_4_raw()
    print_table(exp1,AAAI_coords,values,letters)
    
    
    
    
    
    #day = simple.days[0]
    #day.computeOptions(simple.parameters)
