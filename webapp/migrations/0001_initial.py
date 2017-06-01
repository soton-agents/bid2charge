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
            ('user_initial_balance', self.gf('django.db.models.fields.FloatField')(default=10.0)),
            ('user_initial_energy_units', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('battery_capacity', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('random_seed', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('price_vector_generator', self.gf('django.db.models.fields.CharField')(default='random_gen', max_length=50)),
            ('bidding_strategy', self.gf('django.db.models.fields.CharField')(default='simple_bidding', max_length=50)),
        ))
        db.send_create_signal(u'webapp', ['Treatment'])

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
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
            ('current_day', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('auction_done_today', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ev_guru_mode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('treatment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Treatment'], null=True)),
            ('last_progressive_bids', self.gf('django.db.models.fields.CharField')(default='[]', max_length=200)),
            ('last_progressive_kwhs', self.gf('django.db.models.fields.CharField')(default='[]', max_length=200)),
            ('saved_current_day_history', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('agree_to_receive_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
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
            ('task_selection', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('solution', self.gf('django.db.models.fields.CharField')(max_length=20)),
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
            ('recorded', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
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
            ('recorded', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
        ))
        db.send_create_signal(u'webapp', ['AuctionHistory'])

        # Adding model 'AccountEvent'
        db.create_table(u'webapp_accountevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('http_host', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('http_referer', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='login', max_length=50)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
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
            ('user_marginal_values', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('marginal_prices', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('result', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('allocated_units', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_pay', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
        ))
        db.send_create_signal(u'webapp', ['AuctionEvent'])

        # Adding model 'TaskClickEvent'
        db.create_table(u'webapp_taskclickevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('treatment_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='select', max_length=50)),
            ('task_description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('task_reward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_reward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_km', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('task_selection_before', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('task_selection_after', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
        ))
        db.send_create_signal(u'webapp', ['TaskClickEvent'])

        # Adding model 'TasksAvailableLog'
        db.create_table(u'webapp_tasksavailablelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.EVUser'], null=True)),
            ('treatment_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('available_tasks', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
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
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 6, 0, 0))),
        ))
        db.send_create_signal(u'webapp', ['PerformEvent'])


    def backwards(self, orm):
        # Deleting model 'Treatment'
        db.delete_table(u'webapp_treatment')

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


    models = {
        u'webapp.accountevent': {
            'Meta': {'object_name': 'AccountEvent'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
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
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'energy_units_before_auction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marginal_prices': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'sliders_used': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_pay': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'}),
            'user_marginal_values': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'})
        },
        u'webapp.auctionhistory': {
            'Meta': {'object_name': 'AuctionHistory'},
            'bid': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwh_won': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recorded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'total_spent': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
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
            'recorded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'task_distribution': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.evuser': {
            'Meta': {'object_name': 'EVUser'},
            'agree_to_receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auction_done_today': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'best_monthly_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'current_day': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'energy_units': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ev_guru_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_progressive_bids': ('django.db.models.fields.CharField', [], {'default': "'[]'", 'max_length': '200'}),
            'last_progressive_kwhs': ('django.db.models.fields.CharField', [], {'default': "'[]'", 'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'saved_current_day_history': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'treatment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Treatment']", 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '254'})
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
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'energy_used': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_tasksets': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'taskset_reward': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.shortestpath': {
            'Meta': {'object_name': 'ShortestPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'task_selection': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_reward': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
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
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': "'select'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'task_reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_selection_after': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'task_selection_before': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'total_km': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.tasksavailablelog': {
            'Meta': {'object_name': 'TasksAvailableLog'},
            'available_tasks': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 6, 0, 0)'}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'treatment_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']", 'null': 'True'})
        },
        u'webapp.treatment': {
            'Meta': {'object_name': 'Treatment'},
            'battery_capacity': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'bidding_strategy': ('django.db.models.fields.CharField', [], {'default': "'simple_bidding'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_vector_generator': ('django.db.models.fields.CharField', [], {'default': "'random_gen'", 'max_length': '50'}),
            'random_seed': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'treatment_name': ('django.db.models.fields.CharField', [], {'default': "'New Treatment'", 'max_length': '50'}),
            'user_initial_balance': ('django.db.models.fields.FloatField', [], {'default': '10.0'}),
            'user_initial_energy_units': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['webapp']