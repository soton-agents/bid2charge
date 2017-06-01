from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete, post_init
from django.dispatch import receiver
from itertools import combinations
from models import Task, ShortestPath, MarginalPriceVector, EVUser, Treatment, Day, DayHistory, AuctionHistory, TasksAvailableLog
from django.db import transaction


import game_settings as gsettings
import numpy as np
import utils
import tsp
import math
import logging
from django.utils import timezone
from webapp.game_settings import ROUND_ROBIN_TREATMENTS

@receiver(user_signed_up)
def user_signed_up(request, user, sociallogin = None, **kwargs):
    if hasattr(sociallogin, 'account') and sociallogin.account.provider == 'facebook':
        # Retrieve the first name and the last name from the facebook account 
        # Build the username by concatenating the two names, with dot [.] between them
        first_name = sociallogin.account.extra_data['first_name'].lower()
        last_name = sociallogin.account.extra_data['last_name'].lower()
        username = first_name + '.' + last_name

        # Ensure username is unique
        user.username = utils.getUniqueUsername(username)

        # Save the new username on the user's account
        user.save()




@receiver(pre_save, sender=EVUser)
def apply_treatment(sender, instance, **kwargs):

    if instance.treatment is None:
        
        if instance.experiment:
            treatments = instance.experiment.getTreatments()
        else:
            treatments = Treatment.objects.filter(active=True)
        
        if not ROUND_ROBIN_TREATMENTS:
            min_num = -1
            min_treatment = None
            
            for t in treatments:
                number = len(EVUser.objects.filter(treatment=t))
                if not min_treatment or number < min_num:
                    min_num = number
                    min_treatment = t
            
            treatment = min_treatment
            
        else:
            treatments = sorted(treatments, key=lambda treatment: treatment.pk)
            # Last selected
            all = EVUser.objects.all().exclude(username=instance.username)
            
            if len(all) == 0:
                treatment = treatments[0]
            else:
                latest_user = all.latest('created')
                
                last = latest_user.treatment
                
                found = False
                for t in range(len(treatments)):
                    
                    if treatments[t] == last:
                        treatment = treatments[(t+1) % len(treatments)]
                        found = True
                        break
                if not found:
                    treatment = treatments[0]
                    
        instance.treatment = treatment
            
        # logger.debug("Treatment " + instance.treatment.treatment_name + " has been applied")
        instance.balance =  treatment.user_initial_balance
        instance.energy_units =  treatment.user_initial_energy_units
        instance.created = timezone.now()


@receiver(pre_save, sender=Task)
def validate_task(sender, instance, **kwargs):
    instance.full_clean()



# @receiver(post_save, sender=Task)
def update_shortest_paths(sender, instance, **kwargs):
    # Delete all existent precomputed Shortest Paths
    ShortestPath.objects.all().delete()

    # Retrieve the complete list of tasks from the database
    tasks_db = Task.objects.all()
    
    for i in range(len(tasks_db)):
        for task_selection in combinations(tasks_db, i + 1):
            # Create the Home Task
            home = Task()
            home.description = "Home"
            home.x = 0.5
            home.y = 0.5

            # Transform to list, sort and insert the home task as the first in the list
            task_selection = list(task_selection)
            task_selection = sorted(task_selection, key=lambda task: task.description)
            task_selection.insert(0, home)

            # Get the shortest path by solving TSP
            path = tsp.solve_tsp(task_selection)
            total_cost = math.floor(tsp.total_distance(path))

            # Remove the first Task (the Home Task added at the beginning)
            path.pop(0)

            # Create a new ShortestPath object to be persisted in db
            shortest_path = ShortestPath()
            
            # Build the Task Selection string by concatenatig
            # all task names (description) from the initial task 
            # selection array, separated by a set separator symbol 
            shortest_path.task_selection = ";".join("{0}{1}".format(t.description, "") for t in task_selection)

            # for task in task_selection:
            #     shortest_path.task_selection += task.description + ";"
            # shortest_path.task_selection = shortest_path.task_selection[:-1]

            # Build the Solution string by concatenating all 
            # task names (description) from the computed tsp 
            # problem, separated by a set seaparator symbol.
            # Calculate the total probability of the tour.
            shortest_path.solution = ";".join("{0}{1}".format(t.description, "") for t in path)
            shortest_path.total_reward = sum(t.reward for t in path)

            # for task in path:
            #     shortest_path.solution += task.description + ";"
            #     shortest_path.total_reward += task.reward
            # shortest_path.solution = shortest_path.solution[:-1]

            # Assign the Shortest Path Cost
            shortest_path.total_cost = total_cost

            # Save the new shortest path discovered
            shortest_path.save()

def recompute_all_shortest_paths():
    ShortestPath.objects.all().delete()
    
    days = Day.objects.all()
    
    for d in days:
        create_shortest_path_for_day(d)


def create_shortest_path_for_day(day):
    # Compute shortest paths if necessary
    tasks = Task.objects.all()
    these_tasks = []
    for t in tasks:
        if t.description in day.task_probabilities and day.task_probabilities[t.description] > 0.0:
            these_tasks.append(t)
    
    
    for i in range(len(these_tasks)):
        for task_selection in combinations(these_tasks, i + 1):


            # Transform to list, sort and insert the home task as the first in the list
            task_selection = list(task_selection)
            task_selection = sorted(task_selection, key=lambda task: task.description)
            
            # Build the Task Selection string by concatenatig
            # all task names (description) from the initial task 
            # selection array, separated by a set separator symbol
            string_key = ";".join("{0}{1}".format(t.description, "") for t in task_selection)
            
            if len(ShortestPath.objects.filter(task_selection=string_key)) == 0:
                
                # Create the Home Task
                home = Task()
                home.description = "Home"
                home.x = 0.5
                home.y = 0.5
                
                # Need to compute shortest path
                task_selection.insert(0, home)
    
                # Get the shortest path by solving TSP
                path = tsp.solve_tsp(task_selection)
                total_cost = math.floor(tsp.total_distance(path))
    
                # Remove the first Task (the Home Task added at the beginning)
                path.pop(0)
    
                # Create a new ShortestPath object to be persisted in db
                shortest_path = ShortestPath()
                
                shortest_path.task_selection = string_key
    
                # for task in task_selection:
                #     shortest_path.task_selection += task.description + ";"
                # shortest_path.task_selection = shortest_path.task_selection[:-1]
    
                # Build the Solution string by concatenating all 
                # task names (description) from the computed tsp 
                # problem, separated by a set seaparator symbol.
                # Calculate the total probability of the tour.
                shortest_path.solution = ";".join("{0}{1}".format(t.description, "") for t in path)
                shortest_path.total_reward = sum(t.reward for t in path)
    
                # for task in path:
                #     shortest_path.solution += task.description + ";"
                #     shortest_path.total_reward += task.reward
                # shortest_path.solution = shortest_path.solution[:-1]
    
                # Assign the Shortest Path Cost
                shortest_path.total_cost = total_cost
    
                # Save the new shortest path discovered
                shortest_path.save()

@receiver(post_save, sender=Day)
def add_day_index(sender, instance, **kwargs):
    if instance.day_index == 0:
        instance.day_index = len(Day.objects.filter(treatment = instance.treatment))
        instance.save()
    create_shortest_path_for_day(instance)
    
@receiver(post_delete, sender=Day)
def reindex(sender, instance, **kwargs):
    logger = logging.getLogger("console_logger")

    days = Day.objects.filter(treatment = instance.treatment)
        
    for i in range(0, len(days)):
        days[i].day_index = i + 1
        days[i].save()

    days = Day.objects.filter(treatment = instance.treatment)
    for day in days:
        logger.debug(day)


@receiver(pre_save, sender=Treatment)
def prepare_treatment(sender, instance, **kwargs):
    # Assure the name of the treatment is unique.
    if instance.pk is None:
        instance.treatment_name = utils.getUniqueTreatmentName(instance.treatment_name)
        

@receiver(pre_save, sender=DayHistory)
def deleteConflictingDayRecords(sender, instance, **kwargs):
    history = DayHistory.objects.filter(user = instance.user, day = instance.day)
    if history:
        history.delete()

@receiver(pre_save, sender=AuctionHistory)
def deleteConflictingAuctionRecords(sender, instance, **kwargs):
    history = AuctionHistory.objects.filter(user = instance.user, day = instance.day)
    if history:
        history.delete()

@receiver(pre_save, sender=TasksAvailableLog)
def deleteConflictingTasksAvailableLogs(sender, instance, **kwargs):
    history = TasksAvailableLog.objects.filter(user = instance.user, day = instance.day, treatment_id = instance.treatment_id)
    if history:
        history.delete()
