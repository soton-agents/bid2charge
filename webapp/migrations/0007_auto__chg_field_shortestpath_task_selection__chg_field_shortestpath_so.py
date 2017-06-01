# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ShortestPath.task_selection'
        db.alter_column(u'webapp_shortestpath', 'task_selection', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Changing field 'ShortestPath.solution'
        db.alter_column(u'webapp_shortestpath', 'solution', self.gf('django.db.models.fields.CharField')(max_length=1000))

    def backwards(self, orm):

        # Changing field 'ShortestPath.task_selection'
        db.alter_column(u'webapp_shortestpath', 'task_selection', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'ShortestPath.solution'
        db.alter_column(u'webapp_shortestpath', 'solution', self.gf('django.db.models.fields.CharField')(max_length=20))

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
            'base_payment': ('django.db.models.fields.FloatField', [], {}),
            'bonus_payment': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.EVUser']"})
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
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'current_day': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'energy_units': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ev_guru_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_turker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'strategy': ('django.db.models.fields.TextField', [], {}),
            'strategy_change': ('django.db.models.fields.TextField', [], {}),
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
            'battery_capacity': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'bidding_strategy': ('django.db.models.fields.CharField', [], {'default': "'simple_bidding'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_vector_generator': ('django.db.models.fields.CharField', [], {'default': "'random_gen'", 'max_length': '50'}),
            'random_seed': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'treatment_name': ('django.db.models.fields.CharField', [], {'default': "'New Treatment'", 'max_length': '50'}),
            'user_initial_balance': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'user_initial_energy_units': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['webapp']