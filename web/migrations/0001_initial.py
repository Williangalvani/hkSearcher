# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Motor'
        db.create_table('web_motor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kv', self.gf('django.db.models.fields.IntegerField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')(max_length=20, null=True, blank=True)),
            ('img', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('bigimg', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('page', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('maxCurrent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('resistance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('maxThrust', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('power', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('maxVoltage', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=3000)),
        ))
        db.send_create_signal('web', ['Motor'])

        # Adding model 'Battery'
        db.create_table('web_battery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('page', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('heigth', self.gf('django.db.models.fields.FloatField')()),
            ('width', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('crating', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cchargerating', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('capacity', self.gf('django.db.models.fields.FloatField')()),
            ('cells', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=3000)),
        ))
        db.send_create_signal('web', ['Battery'])


    def backwards(self, orm):
        
        # Deleting model 'Motor'
        db.delete_table('web_motor')

        # Deleting model 'Battery'
        db.delete_table('web_battery')


    models = {
        'web.battery': {
            'Meta': {'object_name': 'Battery'},
            'capacity': ('django.db.models.fields.FloatField', [], {}),
            'cchargerating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cells': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'crating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            'heigth': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'web.motor': {
            'Meta': {'object_name': 'Motor'},
            'bigimg': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'kv': ('django.db.models.fields.IntegerField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'maxCurrent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'maxThrust': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'maxVoltage': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'power': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'resistance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['web']
