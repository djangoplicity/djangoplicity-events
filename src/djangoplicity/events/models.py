# -*- coding: utf-8 -*-
#
# djangoplicity-events
# Copyright (c) 2007-2011, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the European Southern Observatory nor the names 
#      of its contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE
#

"""
Models for the djangoplicity event app. 
"""

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _
from djangoplicity import archives
from djangoplicity.archives.contrib.serialization import Serializer, \
	Serialization, SimpleSerializer
from djangoplicity.media.models import Image
import os
from pytz import all_timezones
from djangoplicity.utils.datetimes import timezone
from django.conf import settings

EVENT_TYPES = ( 
	( 'E', 'Event' ),
	( 'M', 'Meeting' ),
 )

EVENTSITE_TZS = [( tz, tz ) for tz in all_timezones]

class EventSite( models.Model ):
	""" Defines a given site - e.g. Garching, Santiago or Paranal"""
	name = models.CharField( max_length=255 )
	slug = models.SlugField()
	timezone = models.CharField( max_length=40, default='Europe/Berlin' )

	def __unicode__( self ):
		return self.name

class EventSeries( models.Model ):
	""" Defines series of talks - e.g Astronomy for non-astronomers """
	name = models.CharField( max_length=255 )
	slug = models.SlugField()

	class Meta:
		verbose_name_plural = _( 'event series' )

	def __unicode__( self ):
		return self.name

class EventLocation( models.Model ):
	""" Defines a room at a given site """
	name = models.CharField( max_length=255 )
	slug = models.SlugField()
	site = models.ForeignKey( EventSite, blank=True, null=True )

	def __unicode__( self ):
		return "%s, %s" % ( self.name, unicode( self.site ) )

class Event( archives.ArchiveModel, models.Model ):
	""" Defines an event or meeting """
	start_date = models.DateTimeField()
	end_date = models.DateTimeField( blank=True, null=True, )
	location = models.ForeignKey( EventLocation, blank=True, null=True )
	series = models.ForeignKey( EventSeries, blank=True, null=True )
	type = models.CharField( max_length=1, db_index=True, choices=EVENT_TYPES, default='M', help_text="The event and meeting type is used to control where the event is displayed on the website." )
	title = models.CharField( max_length=255 )
	speaker = models.CharField( max_length=255, blank=True )
	affiliation = models.CharField( max_length=255, blank=True, help_text="Affiliation of the speaker - please keep short if possible." )
	abstract = models.TextField( blank=True )
	image = models.ForeignKey( Image, blank=True, null=True, help_text="Image id of image to display together with this event." )
	video_url = models.URLField( blank=True, null=True, verify_exists=False, max_length=255, help_text="Link to flash video (.flv) of this event if exists." )

	def __unicode__( self ):
		return "%s: %s (%s, %s)" % ( self.get_type_display(), self.title, self.location, self.start_date )

	def _get_date_tz( self, date ):
		if not date:
			return None
		return timezone( date, tz=self.location.site.timezone if self.location.site.timezone else settings.TIME_ZONE )

	def _get_start_date_tz( self ):
		return self._get_date_tz( self.start_date )

	def _get_end_date_tz( self ):
		return self._get_date_tz( self.end_date )

	start_date_tz = property( _get_start_date_tz )
	end_date_tz = property( _get_end_date_tz )

	class Archive:
		class Meta:
			release_date = False
			embargo_date = False
			last_modified = True
			created = True
			published = True

	class Meta:
		verbose_name = _( 'event or meeting' )
		verbose_name_plural = _( 'events and meetings' )


class EventSerializer( SimpleSerializer ):
	fields = ( 
		'title',
		'speaker',
		'affiliation',
		'abstract',
		'series',
		'type',
		'image',
		'start_date_tz',
		'end_date_tz',
		'location',
		'video_url',
	)

	def get_type_value( self, obj ):
		return obj.get_type_display()

	def get_image_value( self, obj ):
		if obj.image and obj.image.resource_screen:
			return obj.image.resource_screen.url
		else:
			return ""


class ICalEventSerializer( SimpleSerializer ):
	"""
	Serialier responsible for converting events into 
	iCal data structure. 
	"""
	
	fields = ( 
		'summary',
		'description',
		'location',
		'dtstart',
		'dtend',
		'dtstamp',
	)

	def get_summary_value( self, obj ):
		return "%s: %s" % ( obj.series, obj.title ) if obj.series else obj.title
	
	def get_description_value( self, obj ):
		tmp = [obj.title]
		
		if obj.speaker:
			if obj.affiliation:
				tmp.append("")
				tmp.append( "Speaker: %s (%s)" % (obj.speaker, obj.affiliation) )
			else:
				tmp.append("")
				tmp.append( "Speaker: %s" % obj.speaker ) 
		
		if obj.series:
			tmp.append( "Series: %s" % obj.series )
		
		if obj.abstract:
			tmp.append("")
			tmp.append( "ABSTRACT: %s" % obj.abstract )
		
		return "\n".join( tmp )

	def get_location_value( self, obj ):
		return obj.location
	
	def get_dtstart_value( self, obj ):
		return obj.start_date_tz
	
	def get_dtend_value( self, obj ):
		return obj.obj.end_date_tz if obj.end_date_tz else obj.start_date_tz
	
	def get_dtstamp_value( self, obj ):
		return obj.obj.end_date_tz if obj.end_date_tz else obj.start_date_tz
