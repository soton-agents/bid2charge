from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from webapp.models import *


class EVUserView(admin.ModelAdmin):
    readonly_fields = ('created',)

    fieldsets = [
        (None,                      {'fields': ['username', 'email']}),
        ('Initial Configuration',   {'fields': ['treatment','experiment']}),
        ('Current Status',          {'fields': ['energy_units', 'balance', 'current_day', 'best_monthly_score', 'ev_guru_mode']}),
        ('Statistics',              {'fields': ['created']}),
        ('Properties',              {'fields': ['is_turker','is_turker_trial_2', 'is_aamas','leaderboard_allowed','research_allowed']})
    ]

    # Disable add permission
    def has_add_permission(self, request): return False

class TaskView(admin.ModelAdmin):
	fieldsets = [
		(None, 					{'fields': ['description', 'reward', 'task_icon']}),
        ("Positioning",         {'fields': ['x', 'y']}),
	]

	list_display = ('description',)

class ShortestPathView(admin.ModelAdmin):
    fields = ['task_selection', 'solution']

    list_display = ('task_selection',)

class MarginalPriceVectorView(admin.ModelAdmin):
    list_display = ('treatment', 'day', 'marginal_prices',)
    list_display_links = ('marginal_prices',)


class DayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DayForm, self).__init__(*args, **kwargs)
        self.initial['task_probabilities'] = self.instance.task_probabilities_str()

class DayInline(admin.TabularInline):
    extra = 0
    model = Day
    can_delete = False
    form = DayForm

    ordering = ['day_index']
    readonly_fields = ('day_index',)
    fields = ['units_available',  'task_probabilities', 'marginal_prices']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size' : 60})},
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 60})}
    }

class TreatmentView(admin.ModelAdmin):
    # inlines = [MarginalPriceVectorInline, ]
    inlines = [DayInline, ]

class DayView(admin.ModelAdmin):
    list_display = ('day_index', 'treatment')
    ordering = ('treatment', 'day_index')


class AuctionEventAdmin(admin.ModelAdmin):
    list_display = ('user','day','user_marginal_values','allocated_units','total_pay')
    list_filter = ('user',)

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user','date_time','gender','age','education','country','strategy','strategy_change', 'comments', 'sentiment')
    list_editable = ('sentiment',)
    

class CompletionAdmin(admin.ModelAdmin):
    list_display = ("user", "get_treatment","date_time","base_payment", "bonus_payment","paid","approved","worker_id","assignment_id")
    def get_treatment(self, obj):
        return obj.user.treatment
    get_treatment.short_description = 'Treatment'
    get_treatment.admin_order_field = 'user__treatment'
    
admin.site.register(EVUser, EVUserView)
admin.site.register(Task, TaskView)
admin.site.register(ShortestPath, ShortestPathView)
admin.site.register(MarginalPriceVector, MarginalPriceVectorView)
admin.site.register(Treatment, TreatmentView)
admin.site.register(Day, DayView)
admin.site.register(AuctionEvent, AuctionEventAdmin)
admin.site.register(AccountEvent)
admin.site.register(AuctionHistory)
admin.site.register(DayHistory)
admin.site.register(TaskClickEvent)
admin.site.register(TasksAvailableLog)
admin.site.register(PerformEvent)
admin.site.register(QuizHistory)
admin.site.register(Survey,SurveyAdmin)
admin.site.register(Completion,CompletionAdmin)
admin.site.register(InstructionView)
admin.site.register(Experiment)
admin.site.register(ExperimentTreatment)