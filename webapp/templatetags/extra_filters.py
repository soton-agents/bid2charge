'''
Created on 2 Sep 2015

@author: user
'''
from django import template

from webapp.views import SECOND_TRIAL_GAMES

register = template.Library()


@register.filter
def modulo(num,mod):
    return num % mod

@register.filter
def show_adjusted_day(user):
    if user.is_turker_trial_2 or user.is_orchid:
        return ((user.current_day - 1) % user.treatment.getNumberOfDays()) + 1
    else:
        return user.current_day

@register.filter
def get_game(user):
    return (user.current_day-1) / user.treatment.getNumberOfDays() + 1

@register.filter
def format_money(amount):
    if amount != int(amount):
        return ('%.2f' % amount)
    else:
        return ('%d' % amount)