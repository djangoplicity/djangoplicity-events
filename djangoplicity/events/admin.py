# -*- coding: utf-8 -*-
#
# djangoplicity-events
# Copyright (c) 2007-2011, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#   * Neither the name of the European Southern Observatory nor the names
#     of its contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
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

from django import forms
from django.contrib import admin
from djangoplicity.contrib.admin import DjangoplicityModelAdmin
from djangoplicity.events.models import Calendar, Event, EventLocation, EventSeries, \
    EventSite
from djangoplicity.archives.contrib.admin import view_link


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        cleaned_data = super(EventAdminForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if not start_date:
            self._errors['start_date'] = self.error_class([u'This field is required'])
        if not end_date:
            self._errors['end_date'] = self.error_class([u'This field is required'])

        if start_date and end_date and (end_date < start_date):
            msg = u'End date should be greater than start date.'
            self._errors['end_date'] = self.error_class([msg])
        return cleaned_data


class BaseAdmin( admin.ModelAdmin ):
    list_display = ('id', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ( 'name', 'slug' )
    fieldsets = (
        ( None, { 'fields': ( 'name', 'slug', ) }),
    )
    ordering = ('name',)
    prepopulated_fields = { 'slug': ('name', ) }


class EventLocationAdmin( BaseAdmin ):
    list_display = ( 'id', 'name', 'slug', 'country', 'site' )
    list_editable = ( 'name', 'slug', 'country', 'site' )
    search_fields = ( 'name', 'slug', 'country', 'site__name' )
    fieldsets = (
        ( None, { 'fields': ( 'name', 'slug', 'country', 'site' ) } ),
    )


class EventSiteAdmin( BaseAdmin ):
    list_display = ( 'id', 'name', 'slug', 'timezone' )
    list_editable = ( 'name', 'slug', 'timezone' )
    search_fields = ( 'name', 'slug', 'timezone' )
    fieldsets = (
        ( None, { 'fields': ( 'name', 'slug', 'timezone' ) } ),
    )


class EventSeriesAdmin( BaseAdmin ):
    pass


class EventAdmin( DjangoplicityModelAdmin ):
    list_display = ( 'title', 'speaker', 'start_date', 'end_date', 'location', 'series', 'type', 'audience', 'published', view_link('events'))
    list_filter = ( 'last_modified', 'published', 'type', 'series', 'audience', 'location', 'location__site' )
    search_fields = ( 'title', 'speaker', 'location__name', 'series__name', 'type', 'audience', 'affiliation', 'abstract', )
    richtext_fields = ( 'abstract', )
    form = EventAdminForm
    fieldsets = (
        ( 'Event or meeting', { 'fields': ( 'type', 'series', 'audience', 'title', 'speaker', 'affiliation', 'abstract', 'image', 'image_url', 'webpage_url', 'registration', 'video_url', 'slides_url', 'additional_information' ) } ),
        ( 'Location and date', { 'fields': ( 'start_date', 'end_date', 'location', ) } ),
        ( 'Publishing', {'fields': ( 'published', 'last_modified', 'created' ), } ),
    )
    readonly_fields = ( 'last_modified', 'created', )
    raw_id_fields = ( 'image', )
    ordering = ('-start_date',)

    def get_queryset(self, request):
        return super(EventAdmin, self).get_queryset(request).select_related('location__site', 'series')

    def formfield_for_dbfield(self, db_field, **kwargs):
        '''
        Cache the series choices to speed up admin list view
        '''
        request = kwargs['request']
        formfield = super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'series':
            series_choices_cache = getattr(request, 'series_choices_cache', None)
            if series_choices_cache is not None:
                formfield.choices = series_choices_cache
            else:
                request.series_choices_cache = formfield.choices
        return formfield

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('type', 'audience', 'url')


def register_with_admin( admin_site ):
    admin_site.register( EventLocation, EventLocationAdmin )
    admin_site.register( EventSite, EventSiteAdmin )
    admin_site.register( EventSeries, EventSeriesAdmin )
    admin_site.register( Event, EventAdmin )
    admin_site.register( Calendar, CalendarAdmin)

# Register with default admin site
register_with_admin( admin.site )
