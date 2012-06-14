# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SiteState'
        db.create_table('carr_main_sitestate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='application_user', to=orm['auth.User'])),
            ('last_location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visited', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('carr_main', ['SiteState'])

        # Adding model 'SiteSection'
        db.create_table('carr_main_sitesection', (
            ('section_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pagetree.Section'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('carr_main', ['SiteSection'])

        # Adding M2M table for field sites on 'SiteSection'
        db.create_table('carr_main_sitesection_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sitesection', models.ForeignKey(orm['carr_main.sitesection'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('carr_main_sitesection_sites', ['sitesection_id', 'site_id'])

        # Adding model 'FlashVideoBlock'
        db.create_table('carr_main_flashvideoblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('carr_main', ['FlashVideoBlock'])

        # Adding model 'PullQuoteBlock_2'
        db.create_table('carr_main_pullquoteblock_2', (
            ('pullquoteblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pageblocks.PullQuoteBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('carr_main', ['PullQuoteBlock_2'])

        # Adding model 'PullQuoteBlock_3'
        db.create_table('carr_main_pullquoteblock_3', (
            ('pullquoteblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pageblocks.PullQuoteBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('carr_main', ['PullQuoteBlock_3'])


    def backwards(self, orm):
        
        # Deleting model 'SiteState'
        db.delete_table('carr_main_sitestate')

        # Deleting model 'SiteSection'
        db.delete_table('carr_main_sitesection')

        # Removing M2M table for field sites on 'SiteSection'
        db.delete_table('carr_main_sitesection_sites')

        # Deleting model 'FlashVideoBlock'
        db.delete_table('carr_main_flashvideoblock')

        # Deleting model 'PullQuoteBlock_2'
        db.delete_table('carr_main_pullquoteblock_2')

        # Deleting model 'PullQuoteBlock_3'
        db.delete_table('carr_main_pullquoteblock_3')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'carr_main.flashvideoblock': {
            'Meta': {'object_name': 'FlashVideoBlock'},
            'file_url': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'carr_main.pullquoteblock_2': {
            'Meta': {'object_name': 'PullQuoteBlock_2', '_ormbases': ['pageblocks.PullQuoteBlock']},
            'pullquoteblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pageblocks.PullQuoteBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'carr_main.pullquoteblock_3': {
            'Meta': {'object_name': 'PullQuoteBlock_3', '_ormbases': ['pageblocks.PullQuoteBlock']},
            'pullquoteblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pageblocks.PullQuoteBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'carr_main.sitesection': {
            'Meta': {'object_name': 'SiteSection', '_ormbases': ['pagetree.Section']},
            'section_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pagetree.Section']", 'unique': 'True', 'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'carr_main.sitestate': {
            'Meta': {'object_name': 'SiteState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'application_user'", 'to': "orm['auth.User']"}),
            'visited': ('django.db.models.fields.TextField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pageblocks.pullquoteblock': {
            'Meta': {'object_name': 'PullQuoteBlock'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Hierarchy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'base.html'", 'max_length': '50'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['carr_main']
