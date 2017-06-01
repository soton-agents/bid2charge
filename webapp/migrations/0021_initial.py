# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Treatment'
        db.create_table(u'webapp_treatment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('treatment_name', self.gf('django.db.models.fields.CharField')(default='New Treatment', max_length=50)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['webapp.Experiment'], null=True)),
            ('user_initial_balance', self.gf('django.db.models.fields.FloatField')(default=100.0)),
            ('user_initial_energy_units', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('battery_capacity', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('random_seed', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price_vector_generator', self.gf('django.db.models.fields.CharField')(default='random_gen', max_length=50)),
            ('bidding_strategy', self.gf('django.db.models.fields.CharField')(default='simple_bidding', max_length=50)),
        ))
        db.send_create_signal(u'webapp', ['Treatment'])

        # Adding model 'Experiment'
        db.create_table(u'webapp_experiment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'webapp', ['Experiment'])

        # Adding model 'ExperimentTreatment'
        db.create_table(u'webapp_experimenttreatment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Experiment'])),
            ('treatment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Treatment'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'webapp', ['ExperimentTreatment'])

        # Adding model 'Task'
        db.create_table(u'webapp_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('reward', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('task_icon', self.gf('django.db.models.fields.CharField')(default='/static/webapp/img/low-reward-task-icon.png', max_length=50)),
            ('x', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('y', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'webapp', ['Task'])

        # Adding model 'Day'
        db.create_table(u'webapp_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day_index', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('treatment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Treatment'])),
            ('units_available', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('task_probabilities', self.gf('jsonfield.fields.JSONField')(default='')),
            ('marginal_prices', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'webapp', ['Day'])

        # Adding model 'EVUser'
        db.create_table(u'webapp_evuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=254)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_day', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('auction_done_today', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ev_guru_mode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('treatment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Treatment'], null=True)),
            ('last_progressive_bids', self.gf('django.db.models.fields.CharField')(default='[]', max_length=200)),
            ('last_progressive_kwhs', self.gf('django.db.models.fields.CharField')(default='[]', max_length=200)),
            ('saved_current_day_history', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('agree_to_receive_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_turker', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_aamas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['webapp.Experiment'], null=True)),
            ('is_turker_trial_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('leaderboard_allowed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('research_allowed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('completed_tutorial', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('best_monthly_score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('energy_units', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'webapp', ['EVUser'])

        # Adding model 'MarginalPriceVector'
        db.create_table(u'webapp_marginalpricevector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('treatment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Treatment'], null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('marginal_prices', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
        ))
        db.send_create_signal(u'webapp', ['MarginalPriceVector'])

        # Adding model 'ShortestPath'
        db.create_table(u'webapp_shortestpath', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_selection', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('solution', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('total_cost', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('total_reward', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'webapp', ['ShortestPath'])

        # Adding model 'DayHistory'
        db.create_table(u'webapp_dayhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('kwh', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('recorded', self.gf('django.db.models.fields.DateTimeField')()),
            ('task_distribution', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
        ))
        db.send_create_signal(u'webapp', ['DayHistory'])

        # Adding model 'AuctionHistory'
        db.create_table(u'webapp_auctionhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bid', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('total_spent', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('kwh_won', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recorded', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'webapp', ['AuctionHistory'])

        # Adding model 'QuizHistory'
        db.create_table(u'webapp_quizhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('goalAnswer', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('planAnswer', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('auctionAnswer', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('consentAnswer', self.gf('django.db.models.fields.BooleanField')()),
            ('correct', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'webapp', ['QuizHistory'])

        # Adding model 'AccountEvent'
        db.create_table(u'webapp_accountevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('http_host', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('http_referer', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='login', max_length=50)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'webapp', ['AccountEvent'])

        # Adding model 'AuctionEvent'
        db.create_table(u'webapp_auctionevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('treatment_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bidding_strategy', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('sliders_used', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('balance_before_auction', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('energy_units_before_auction', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user_marginal_values', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('marginal_prices', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('result', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('allocated_units', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_pay', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'webapp', ['AuctionEvent'])

        # Adding model 'TaskClickEvent'
        db.create_table(u'webapp_taskclickevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('treatment_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='select', max_length=100)),
            ('task_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('task_reward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_reward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_km', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('task_selection_before', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('task_selection_after', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'webapp', ['TaskClickEvent'])

        # Adding model 'TasksAvailableLog'
        db.create_table(u'webapp_tasksavailablelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('treatment_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('available_tasks', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'webapp', ['TasksAvailableLog'])

        # Adding model 'PerformEvent'
        db.create_table(u'webapp_performevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('treatment_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('taskset_reward', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('energy_used', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('other_tasksets', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'webapp', ['PerformEvent'])

        # Adding model 'Completion'
        db.create_table(u'webapp_completion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'])),
            ('base_payment', self.gf('django.db.models.fields.FloatField')()),
            ('bonus_payment', self.gf('django.db.models.fields.FloatField')()),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 6, 1, 0, 0))),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('worker_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('assignment_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('hit_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
        ))
        db.send_create_signal(u'webapp', ['Completion'])

        # Adding model 'InstructionView'
        db.create_table(u'webapp_instructionview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 6, 1, 0, 0))),
        ))
        db.send_create_signal(u'webapp', ['InstructionView'])

        # Adding model 'Survey'
        db.create_table(u'webapp_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.TextField')()),
            ('car_owner', self.gf('django.db.models.fields.BooleanField')()),
            ('driven_ev', self.gf('django.db.models.fields.BooleanField')()),
            ('strategy', self.gf('django.db.models.fields.TextField')()),
            ('strategy_change', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('sentiment', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('usability_answers', self.gf('django.db.models.fields.TextField')(default='')),
            ('usability_score', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal(u'webapp', ['Survey'])


    def backwards(self, orm):
        # Deleting model 'Treatment'
        db.delete_table(u'webapp_treatment')

        # Deleting model 'Experiment'
        db.delete_table(u'webapp_experiment')

        # Deleting model 'ExperimentTreatment'
        db.delete_table(u'webapp_experimenttreatment')

        # Deleting model 'Task'
        db.delete_table(u'webapp_task')

        # Deleting model 'Day'
        db.delete_table(u'webapp_day')

        # Deleting model 'EVUser'
        db.delete_table(u'webapp_evuser')

        # Deleting model 'MarginalPriceVector'
        db.delete_table(u'webapp_marginalpricevector')

        # Deleting model 'ShortestPath'
        db.delete_table(u'webapp_shortestpath')

        # Deleting model 'DayHistory'
        db.delete_table(u'webapp_dayhistory')

        # Deleting model 'AuctionHistory'
        db.delete_table(u'webapp_auctionhistory')

        # Deleting model 'QuizHistory'
        db.delete_table(u'webapp_quizhistory')

        # Deleting model 'AccountEvent'
        db.delete_table(u'webapp_accountevent')

        # Deleting model 'AuctionEvent'
        db.delete_table(u'webapp_auctionevent')

        # Deleting model 'TaskClickEvent'
        db.delete_table(u'webapp_taskclickevent')

        # Deleting model 'TasksAvailableLog'
        db.delete_table(u'webapp_tasksavailablelog')

        # Deleting model 'PerformEvent'
        db.delete_table(u'webapp_performevent')

        # Deleting model 'Completion'
        db.delete_table(u'webapp_completion')

        # Deleting model 'InstructionView'
        db.delete_table(u'webapp_instructionview')

        # Deleting model 'Survey'
        db.delete_table(u'webapp_survey')


    models = {
        u'webapp.accountevent': {
            'Meta': {'object_name': 'AccountEvent'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': "'login'", 'max_length': '50'}),
            'http_host': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'http_referer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'})
        },
        u'webapp.auctionevent': {
            'Meta': {'object_name': 'AuctionEvent'},
            'allocated_units': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'balance_before_auction': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'bidding_strategy': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'energy_units_before_auction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marginal_prices': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'sliders_used': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_pay': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'}),
            'user_marginal_values': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
        },
        u'webapp.auctionhistory': {
            'Meta': {'object_name': 'AuctionHistory'},
            'bid': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwh_won': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recorded': ('django.db.models.fields.DateTimeField', [], {}),
            'total_spent': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.completion': {
            'Meta': {'object_name': 'Completion'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'assignment_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'base_payment': ('django.db.models.fields.FloatField', [], {}),
            'bonus_payment': ('django.db.models.fields.FloatField', [], {}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 6, 1, 0, 0)'}),
            'hit_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']"}),
            'worker_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'})
        },
        u'webapp.day': {
            'Meta': {'object_name': 'Day'},
            'day_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marginal_prices': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'task_probabilities': ('jsonfield.fields.JSONField', [], {'default': "''"}),
            'treatment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Treatment']"}),
            'units_available': ('django.db.models.fields.IntegerField', [], {'default': '30'})
        },
        u'webapp.dayhistory': {
            'Meta': {'object_name': 'DayHistory'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwh': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'recorded': ('django.db.models.fields.DateTimeField', [], {}),
            'task_distribution': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.evuser': {
            'Meta': {'object_name': 'EVUser'},
            'agree_to_receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auction_done_today': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'best_monthly_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'completed_tutorial': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'current_day': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'energy_units': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ev_guru_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['webapp.Experiment']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_aamas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_turker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_turker_trial_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_progressive_bids': ('django.db.models.fields.CharField', [], {'default': "'[]'", 'max_length': '200'}),
            'last_progressive_kwhs': ('django.db.models.fields.CharField', [], {'default': "'[]'", 'max_length': '200'}),
            'leaderboard_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'research_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saved_current_day_history': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'treatment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Treatment']", 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '254'})
        },
        u'webapp.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'experiment_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'webapp.experimenttreatment': {
            'Meta': {'object_name': 'ExperimentTreatment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'treatment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Treatment']"})
        },
        u'webapp.instructionview': {
            'Meta': {'object_name': 'InstructionView'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']"})
        },
        u'webapp.marginalpricevector': {
            'Meta': {'ordering': "['treatment', 'day']", 'object_name': 'MarginalPriceVector'},
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marginal_prices': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'treatment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Treatment']", 'null': 'True'})
        },
        u'webapp.performevent': {
            'Meta': {'object_name': 'PerformEvent'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'energy_used': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_tasksets': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'taskset_reward': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.quizhistory': {
            'Meta': {'object_name': 'QuizHistory'},
            'auctionAnswer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'consentAnswer': ('django.db.models.fields.BooleanField', [], {}),
            'correct': ('django.db.models.fields.BooleanField', [], {}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'goalAnswer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'planAnswer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.shortestpath': {
            'Meta': {'object_name': 'ShortestPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'task_selection': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_reward': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'webapp.survey': {
            'Meta': {'object_name': 'Survey'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'car_owner': ('django.db.models.fields.BooleanField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.TextField', [], {}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'driven_ev': ('django.db.models.fields.BooleanField', [], {}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sentiment': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'strategy': ('django.db.models.fields.TextField', [], {}),
            'strategy_change': ('django.db.models.fields.TextField', [], {}),
            'usability_answers': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'usability_score': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']"})
        },
        u'webapp.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reward': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'task_icon': ('django.db.models.fields.CharField', [], {'default': "'/static/webapp/img/low-reward-task-icon.png'", 'max_length': '50'}),
            'x': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'y': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'webapp.taskclickevent': {
            'Meta': {'object_name': 'TaskClickEvent'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': "'select'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task_reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_selection_after': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'task_selection_before': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'total_km': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.tasksavailablelog': {
            'Meta': {'object_name': 'TasksAvailableLog'},
            'available_tasks': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.treatment': {
            'Meta': {'object_name': 'Treatment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'battery_capacity': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'bidding_strategy': ('django.db.models.fields.CharField', [], {'default': "'simple_bidding'", 'max_length': '50'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['webapp.Experiment']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_vector_generator': ('django.db.models.fields.CharField', [], {'default': "'random_gen'", 'max_length': '50'}),
            'random_seed': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'treatment_name': ('django.db.models.fields.CharField', [], {'default': "'New Treatment'", 'max_length': '50'}),
            'user_initial_balance': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'user_initial_energy_units': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['webapp']