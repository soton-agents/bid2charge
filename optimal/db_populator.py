'''
Created on Nov 13, 2014

@author: user
'''
from collections import Counter
from optimal import problem
from webapp import game_settings
from webapp.game_settings import ORCHID_SHOWCASE
from webapp.models import Day, Task, Survey, Treatment, Experiment, \
    ExperimentTreatment
import simplejson




def delete_db():
    # First delete data
    Day.objects.all().delete()
    Task.objects.all().delete()

def populate_db(problem_tuple=None,treatment_names=None,task_prefix="T"):
    if not problem_tuple:
        dayList,values,coordinates = problem.create_final_raw_data()
    else:
        dayList,values,coordinates = problem_tuple
    
    tasks = []
    
    # Now re-create tasks
    for i in range(len(values)):
        task = Task()
        task.reward = values[i]
        
        if task.reward == 5:
            task.task_icon = Task.LOW_REWARD_ICON
        elif task.reward == 10:
            task.task_icon = Task.MEDIUM_REWARD_ICON
        else:
            task.task_icon = Task.HIGH_REWARD_ICON
        task.x = coordinates[i].x
        task.y = coordinates[i].y
        task.description = "%s%s(%s,%s,%s)" % (task_prefix,(i+1), task.reward, task.x, task.y)
        
        task.save()
        tasks.append(task)
        print "Done with task %s" % task

    #tasks = Task.objects.all()

    if not treatment_names:
        treatments = Treatment.objects.all()
    else:
        treatments = Treatment.objects.filter(treatment_name__in=treatment_names)

    # Re-create days:
    for i in range(len(dayList)):
        day_tasks = dayList[i]
        
        probabilities = [0.0 for x in range(len(tasks))]
        for (task, probability) in day_tasks:
            probabilities[task] = probability
        
        for treatment in treatments:
            day = Day()
            day.day_index = i + 1
            day.treatment = treatment
            day.units_available = game_settings.DEFAULT_AVAILABLE_UNITS
            
            taskDistributionStr = '{'
            for j in range(0, len(tasks)):
                taskDistributionStr += '"' + str(tasks[j]) + '":' + '{0:.2f}'.format(probabilities[j]) + ','
            taskDistributionStr = taskDistributionStr[:-1] + "}"
            
            day.task_probabilities = simplejson.loads(taskDistributionStr)
            day.save()
            
            print "Done with day %s" % day

def populate_all():
    delete_db()
    # Trial 1:
    populate_db( problem.create_final_raw_data(),["Simple", "Uniform" , "Expressive"],"T")
    # Trial 2:
    populate_db(problem.create_simple_aaai_4_raw(),["Simple_AAAI", "Simple_AAAI_3","Uniform_AAAI" , "Expressive_AAAI"],"AAAI_T")
    # ORCHID Trial:
    # First experiment & treatments:
    exps = Experiment.objects.filter(experiment_name=ORCHID_SHOWCASE)
    orchid_treatments = ["Simple_ORCHID", "Uniform_ORCHID" , "Expressive_ORCHID"]
    interfaces = [Treatment.SIMPLE_BIDDING_STRATEGY,Treatment.UNIFORM_BIDDING_STRATEGY,Treatment.PROGRESSIVE_BIDDING_STRATEGY]
    
    if len(exps) == 0:
        # Create
        exp = Experiment(experiment_name=ORCHID_SHOWCASE)
        exp.save()
        # Create treatments
        counter= 10
        for (t,i) in zip(orchid_treatments,interfaces):
            treatment = Treatment(treatment_name=t)
            treatment.experiment = exp
            treatment.battery_capacity = 10
            treatment.random_seed = counter 
            counter += 1
            treatment.active = False
            treatment.bidding_strategy = i
            treatment.save()
            et = ExperimentTreatment(experiment=exp,treatment=treatment,active=True)
            et.save()
    else:
        exp = exps[0]
        
    populate_db(problem.create_simple_orchid_raw(),orchid_treatments,"ORCHID_T")
    
    
        
    
    
    