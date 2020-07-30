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

from django.db import models
from django.utils import dateformat, formats
from django.utils.translation import ugettext_lazy as _
from djangoplicity.utils.datetimes import timezone
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import make_aware
from django_countries.fields import CountryField
import pytz

from djangoplicity.archives.base import ArchiveModel
from djangoplicity.media.models import Image
from djangoplicity.events import tasks


EVENT_TYPES = (
    ( 'C', 'Conference' ),
    ( 'E', 'Event' ),
    ( 'EX', 'Exhibitions' ),
    ( 'L', 'Lecture' ),
    ( 'M', 'Meeting' ),
    ( 'PE', 'Press Event' ),
    ( 'T', 'Talk' ),
    ( 'W', 'Workshop' ),
)

AUDIENCE_TYPES = (
    ( 'I', 'Internal' ),
    ( 'P', 'Public' ),
    ( 'IN', 'Industry' ),
    ( 'S', 'Science' ),
    ( 'SI', 'Science Internal' ),
)

EVENTSITE_TZS = [( tz, tz ) for tz in pytz.all_timezones]


class EventSite( models.Model ):
    """ Defines a given site - e.g. Garching, Santiago or Paranal"""
    name = models.CharField( max_length=255 )
    slug = models.SlugField()
    timezone = models.CharField( max_length=40, default='Europe/Berlin', choices=EVENTSITE_TZS )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = ('name',)


class EventSeries( models.Model ):
    """ Defines series of talks - e.g Astronomy for non-astronomers """
    name = models.CharField( max_length=255 )
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = _( 'event series' )
        ordering = ('name',)

    def __unicode__( self ):
        return self.name


class EventLocation( models.Model ):
    """ Defines a room at a given site """
    name = models.CharField( max_length=255 )
    slug = models.SlugField()
    country = CountryField(default='DE')
    site = models.ForeignKey( EventSite, blank=True, null=True )

    def __unicode__( self ):
        s = self.name
        if self.site:
            s += ' | %s' % self.site
        return s

    class Meta:
        ordering = ('site__name', 'name')


class Event( ArchiveModel, models.Model ):
    """ Defines an event or meeting """
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey( EventLocation, blank=True, null=True )
    series = models.ForeignKey( EventSeries, blank=True, null=True )
    type = models.CharField( max_length=2, db_index=True, choices=EVENT_TYPES, default='T', help_text="The event and meeting type is used to control where the event is displayed on the website." )
    audience = models.CharField( max_length=2, db_index=True, choices=AUDIENCE_TYPES, default='P', help_text="The event and meeting audience is used to control which audience is targetted." )
    title = models.CharField( max_length=255 )
    speaker = models.CharField( max_length=255, blank=True )
    affiliation = models.CharField( max_length=255, blank=True, help_text="Affiliation of the speaker - please keep short if possible." )
    abstract = models.TextField( blank=True )
    image = models.ForeignKey( Image, blank=True, null=True, help_text="Image id of image to display together with this event." )
    webpage_url = models.URLField( verbose_name="Webpage URL", blank=True, null=True, max_length=255, help_text="Link to webpage of this event if it exists." )
    video_url = models.URLField( verbose_name="Video URL", blank=True, null=True, max_length=255, help_text="Link to flash video (.flv) of this event if it exists." )
    slides_url = models.URLField( verbose_name="Slides URL", blank=True, null=True, max_length=255, help_text="Link to slides for this event if any." )
    additional_information = models.CharField( max_length=255, blank=True, help_text="Short additional information to be displayed on reception screen." )
    gcal_key = models.CharField( max_length=255, blank=True, null=True, )

    def __unicode__( self ):
        return "%s: %s (%s, %s)" % ( self.get_type_display(), self.title, self.location, self.start_date )

    def _get_date_tz( self, date ):
        if not date:
            return None
        # Datetimes are currently "naive", and stored in the DB using the default
        # TIME_ZONE: Europe/Berlin, this works fine from Garching as events are
        # always added in the DB in the local timezon, but from Chile the dates
        # are entered as Chile local time and saved as Garching time.
        # So if we have a site timezone for the event which is different than
        # the local one we first convert it to a local time aware date
        if self.location and self.location.site and self.location.site.timezone:
            tz = pytz.timezone(self.location.site.timezone)
        else:
            tz = pytz.timezone(settings.TIME_ZONE)
        return tz.localize(date)

    def get_dates( self ):
        if self.end_date and self.start_date:
            if self.end_date.year != self.start_date.year:
                return "%s - %s" % ( formats.date_format( self.start_date ), formats.date_format( self.end_date ) )
            elif self.end_date.month != self.start_date.month:
                return "%s - %s %s" % ( dateformat.format( self.start_date, "j F" ), dateformat.format( self.end_date, "j F" ), self.start_date.year )
            elif self.end_date.day != self.start_date.day:
                return "%s - %s %s" % ( dateformat.format( self.start_date, "j" ), dateformat.format( self.end_date, "j" ), dateformat.format( self.start_date, "F Y" ) )
            else:
                return formats.date_format( self.start_date )
        else:
            return formats.date_format( self.start_date )

    def get_calendar(self):
        '''
        Return the calendarId for the event based on its audience and site
        '''
        calendarId = None
        try:
            event_site = self.location.site.slug
        except AttributeError:
            event_site = ''

        for site, calendar in settings.GCAL_CALENDAR[self.audience].items():
            if site == event_site:
                calendarId = calendar

        if not calendarId and 'default' in settings.GCAL_CALENDAR[self.audience]:
            calendarId = settings.GCAL_CALENDAR[self.audience]['default']

        return calendarId

    def _get_start_date_tz( self ):
        return self._get_date_tz( self.start_date )

    def _get_end_date_tz( self ):
        return self._get_date_tz( self.end_date )

    start_date_tz = property( _get_start_date_tz )
    end_date_tz = property( _get_end_date_tz )

    class Archive:
        class Meta:
            release_date = False
            start_date = True
            start_date_fieldname = 'start_date'
            embargo_date = False
            last_modified = True
            created = True
            published = True
            sort_fields = ( 'start_date', )

    class Meta:
        verbose_name = _( 'event or meeting' )
        verbose_name_plural = _( 'events and meetings' )
        ordering = ( 'start_date', )


@receiver(pre_save, sender=Event)
def event_pre_save(sender, instance, **kwargs):
    # storing these values for use in post_save
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        obj = instance

    instance._old_audience = obj.audience
    try:
        instance._old_site_slug = obj.location.site.slug
    except AttributeError:
        instance._old_site_slug = ''


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, **kwargs):
    update_fields = kwargs['update_fields']
    if not update_fields or not(len(update_fields) == 1 and 'gcal_key' in update_fields):
        # don't sync if we're only saving the 'gcal_key'
        # tasks.google_calendar_sync.delay(instance)
        tasks.google_calendar_sync.delay(instance.id, instance._old_audience, instance._old_site_slug)


@receiver(post_delete, sender=Event)
def event_post_delete(sender, instance, **kwargs):
    calendarId = instance.get_calendar()
    tasks.google_calendar_delete.delay(instance.gcal_key, calendarId)