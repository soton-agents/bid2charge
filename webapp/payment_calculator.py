'''
Created on 2 Sep 2015

@author: user
'''
import math

from webapp import game_settings
from webapp.models import DayHistory


def get_profit(user):
#    if user.is_turker_trial_2:
#        # Special treatment, accumulate previous games first
#        days = user.treatment.getNumberOfDays()
#        day = days
#        profit = 0
#        while day < user.current_day:
#            histories = DayHistory.objects.filter(user=user,day=day)
#            profit += histories[0].balance - user.treatment.user_initial_balance
#            day += days  
#        if user.current_day > day:
#            profit += user.balance - user.treatment.user_initial_balance
#        return profit
#    else:
        return user.balance - user.treatment.user_initial_balance

def get_bonus_payment(profit):
    bonus_payment = max(0,math.ceil(100 *profit * game_settings.TURK_BONUS_PER_PROFIT)/100)
    bonus_payment = min(bonus_payment, game_settings.TURK_MAX_BONUS)
    return bonus_payment
    

def get_total_payment(profit):
    return game_settings.TURK_BASE_PAYMENT + get_bonus_payment(profit)