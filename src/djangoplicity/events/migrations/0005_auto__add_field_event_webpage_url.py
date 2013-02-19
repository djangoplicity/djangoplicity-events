# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.webpage_url'
        db.add_column('events_event', 'webpage_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.webpage_url'
        db.delete_column('events_event', 'webpage_url')


    models = {
        'events.event': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Event'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_information': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Image']", 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventLocation']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventSeries']", 'null': 'True', 'blank': 'True'}),
            'speaker': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1', 'db_index': 'True'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'webpage_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'events.eventlocation': {
            'Meta': {'ordering': "('site__name', 'name')", 'object_name': 'EventLocation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventSite']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'events.eventseries': {
            'Meta': {'ordering': "('name',)", 'object_name': 'EventSeries'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'events.eventsite': {
            'Meta': {'ordering': "('name',)", 'object_name': 'EventSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'Europe/Berlin'", 'max_length': '40'})
        },
        'media.color': {
            'Meta': {'ordering': "('upper_limit',)", 'object_name': 'Color'},
            'id': ('django.db.models.fields.SlugField', [], {'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'upper_limit': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'media.image': {
            'Meta': {'ordering': "['-priority', '-release_date']", 'object_name': 'Image'},
            'colors': ('djangoplicity.translation.fields.TranslationManyToManyField', [], {'to': "orm['media.Color']", 'through': "orm['media.ImageColor']", 'symmetrical': 'False'}),
            'contact_address': ('djangoplicity.metadata.archives.fields.AVMContactAddressField', [], {'default': "u'Karl-Schwarzschild-Strasse 2'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_city': ('djangoplicity.metadata.archives.fields.AVMContactCityField', [], {'default': "u'Garching bei M\\xfcnchen'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_country': ('djangoplicity.metadata.archives.fields.AVMContactCountryField', [], {'default': "u'Germany'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_postal_code': ('djangoplicity.metadata.archives.fields.AVMContactPostalCodeField', [], {'default': "u'D-85748'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'contact_state_province': ('djangoplicity.metadata.archives.fields.AVMContactStateProvinceField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('djangoplicity.metadata.archives.fields.AVMCreatorField', [], {'default': "u'European Southern Observatory'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'creator_url': ('djangoplicity.metadata.archives.fields.AVMCreatorURLField', [], {'default': "'http://www.eso.org'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credit': ('djangoplicity.metadata.archives.fields.AVMCreditField', [], {'default': "u'ESO'", 'blank': 'True'}),
            'description': ('djangoplicity.metadata.archives.fields.AVMDescriptionField', [], {'null': 'True', 'blank': 'True'}),
            'distance_ly': ('djangoplicity.metadata.archives.fields.AVMDistanceLyField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '1', 'blank': 'True'}),
            'distance_notes': ('djangoplicity.metadata.archives.fields.AVMDistanceNotesField', [], {'null': 'True', 'blank': 'True'}),
            'distance_z': ('djangoplicity.metadata.archives.fields.AVMDistanceZField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'embargo_date': ('djangoplicity.archives.fields.ReleaseDateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'file_size': ('djangoplicity.metadata.archives.fields.AVMFileSize', [], {'null': 'True', 'blank': 'True'}),
            'file_type': ('djangoplicity.metadata.archives.fields.AVMFileType', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'headline': ('djangoplicity.metadata.archives.fields.AVMHeadlineField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('djangoplicity.metadata.archives.fields.AVMFileDimensionHeight', [], {'null': 'True', 'blank': 'True'}),
            'id': ('djangoplicity.metadata.archives.fields.AVMIdField', [], {'max_length': '50', 'primary_key': 'True'}),
            'keep_newsfeature': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'long_caption_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'magnet_uri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'old_ids': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'press_release_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'print_layout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority': ('djangoplicity.archives.fields.PriorityField', [], {'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'publisher': ('djangoplicity.metadata.archives.fields.AVMPublisherField', [], {'default': "u'European Southern Observatory'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publisher_id': ('djangoplicity.metadata.archives.fields.AVMPublisherIdField', [], {'default': "u'eso'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'release_date': ('djangoplicity.archives.fields.ReleaseDateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'release_date_owner': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'rights': ('djangoplicity.metadata.archives.fields.AVMRightsField', [], {'default': "'Creative Commons Attribution 3.0 Unported license.'", 'null': 'True', 'blank': 'True'}),
            'source': ('djangoplicity.translation.fields.TranslationForeignKey', [], {'blank': 'True', 'related_name': "'translations'", 'null': 'True', 'only_sources': 'False', 'to': "orm['media.Image']"}),
            'spatial_coordinate_frame': ('djangoplicity.metadata.archives.fields.AVMSpatialCoordinateFrameField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'spatial_coordsystem_projection': ('djangoplicity.metadata.archives.fields.AVMSpatialCoordsystemProjectionField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'spatial_equinox': ('djangoplicity.metadata.archives.fields.AVMSpatialEquinoxField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'spatial_fits_header': ('djangoplicity.metadata.archives.fields.AVMSpatialNotesField', [], {'null': 'True', 'blank': 'True'}),
            'spatial_notes': ('djangoplicity.metadata.archives.fields.AVMSpatialNotesField', [], {'null': 'True', 'blank': 'True'}),
            'spatial_quality': ('djangoplicity.metadata.archives.fields.AVMSpatialQualityField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'spatial_reference_dimension': ('djangoplicity.metadata.archives.fields.AVMSpatialReferenceDimensionField', [], {'max_length': '47', 'null': 'True', 'blank': 'True'}),
            'spatial_reference_pixel': ('djangoplicity.metadata.archives.fields.AVMSpatialReferencePixelField', [], {'max_length': '47', 'null': 'True', 'blank': 'True'}),
            'spatial_reference_value': ('djangoplicity.metadata.archives.fields.AVMSpatialReferenceValueField', [], {'max_length': '47', 'null': 'True', 'blank': 'True'}),
            'spatial_rotation': ('djangoplicity.metadata.archives.fields.AVMSpatialRotationField', [], {'max_length': '23', 'null': 'True', 'blank': 'True'}),
            'spatial_scale': ('djangoplicity.metadata.archives.fields.AVMSpatialScaleField', [], {'max_length': '47', 'null': 'True', 'blank': 'True'}),
            'spectral_notes': ('djangoplicity.metadata.archives.fields.AVMSpectralNotesField', [], {'null': 'True', 'blank': 'True'}),
            'subject_category': ('djangoplicity.metadata.translation.fields.TranslationAVMSubjectCategoryField', [], {'symmetrical': 'False', 'to': "orm['metadata.TaxonomyHierarchy']", 'null': 'True', 'blank': 'True'}),
            'subject_name': ('djangoplicity.metadata.translation.fields.TranslationAVMSubjectNameField', [], {'symmetrical': 'False', 'to': "orm['metadata.SubjectName']", 'null': 'True', 'blank': 'True'}),
            'tagging_status': ('djangoplicity.translation.fields.TranslationManyToManyField', [], {'to': "orm['metadata.TaggingStatus']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('djangoplicity.metadata.archives.fields.AVMTitleField', [], {'max_length': '255', 'db_index': 'True'}),
            'translation_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('djangoplicity.metadata.archives.fields.AVMTypeField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'wallpapers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'width': ('djangoplicity.metadata.archives.fields.AVMFileDimensionWidth', [], {'null': 'True', 'blank': 'True'}),
            'zoomify': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'media.imagecolor': {
            'Meta': {'object_name': 'ImageColor'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Color']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('djangoplicity.translation.fields.TranslationForeignKey', [], {'to': "orm['media.Image']"}),
            'ratio': ('django.db.models.fields.FloatField', [], {})
        },
        'metadata.subjectname': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SubjectName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'simbad_compliant': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wiki_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'metadata.taggingstatus': {
            'Meta': {'ordering': "('name',)", 'object_name': 'TaggingStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'metadata.taxonomyhierarchy': {
            'Meta': {'unique_together': "(('top_level', 'level1', 'level2', 'level3', 'level4', 'level5'),)", 'object_name': 'TaxonomyHierarchy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level3': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level4': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level5': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'top_level': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'})
        }
    }

    complete_apps = ['events']