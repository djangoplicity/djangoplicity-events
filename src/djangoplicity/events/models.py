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

EVENT_TYPES = ( 
	( 'E', 'Event' ),
	( 'M', 'Meeting' ),
 )

class EventSite( models.Model ):
	""" Defines a given site - e.g. Garching, Santiago or Paranal"""
	name = models.CharField( max_length=255 )
	slug = models.SlugField()

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
	type = models.CharField( max_length=1, db_index=True, choices=EVENT_TYPES, default='M' )
	title = models.CharField( max_length=255 )
	speaker = models.CharField( max_length=255, blank=True )
	affiliation = models.CharField( max_length=255, blank=True )
	abstract = models.TextField( blank=True )
	image = models.ForeignKey( Image, blank=True, null=True )

	def __unicode__( self ):
		return "%s: %s (%s, %s)" % ( self.get_type_display(), self.title, self.location, self.start_date )

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
		'start_date', 
		'end_date', 
		'location',
	)
	
	def get_type_value( self, obj ):
		return obj.get_type_display()
	