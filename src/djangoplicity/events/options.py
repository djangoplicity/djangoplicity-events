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
from django.utils.translation import ugettext as _
from djangoplicity.archives.options import ArchiveOptions
from djangoplicity.archives.contrib.browsers import ListBrowser, SerializationBrowser
from djangoplicity.archives.contrib.queries import YearQuery
from djangoplicity.archives.contrib.serialization import JSONEmitter, ICalEmitter
from djangoplicity.archives.views import SerializationDetailView
from djangoplicity.events.serializers import EventSerializer, ICalEventSerializer
from djangoplicity.events.queries import SiteQuery, AllEventsQuery, IndustryEventsQuery


class EventOptions( ArchiveOptions ):
    urlname_prefix = "events"

    #title = ugettext_noop("Events and Meetings")

    detail_views = (
        { 'url_pattern': 'api/(?P<serializer>json)/', 'view': SerializationDetailView( serializer=EventSerializer, emitters=[JSONEmitter] ), 'urlname_suffix': 'serialization', },
    )

    search_fields = (
        'location__name', 'series__name', 'title', 'speaker', 'affiliation', 'abstract',
    )

    class Queries(object):
        default = AllEventsQuery( browsers=( 'html', 'json', 'ical' ), verbose_name = "Seminars and Colloquia" )
        site = SiteQuery( browsers=( 'html', 'json', 'ical' ), verbose_name = "Seminars and Colloquia" )
        conf = AllEventsQuery( browsers=( 'html', 'json', 'ical' ), verbose_name = "Conferences and Workshops" )
        year = YearQuery( browsers=( 'html', 'json', 'ical' ), datetime_feature='start_date', verbose_name = "Seminars and Colloquia %d")
        site_embed = SiteQuery( browsers=( 'html_embed', 'json', 'ical' ), verbose_name = "Seminars and Colloquia" )
        conf_embed = AllEventsQuery( browsers=( 'html_conf_embed', 'json', 'ical' ), verbose_name = "Conferences and Workshops" )
        industry = IndustryEventsQuery( browsers=( 'html_industry', 'json', 'ical' ), verbose_name = "Industry Events" )

    class Browsers(object):
        html = ListBrowser( verbose_name='HTML', paginate_by=1000 )
        html_embed = ListBrowser( verbose_name='HTML', paginate_by=1000, index_template='index_list_embed.html' )
        html_conf_embed = ListBrowser( verbose_name='HTML', paginate_by=1000, index_template='index_list_embed.html' )
        html_industry = ListBrowser( verbose_name='HTML', paginate_by=1000, index_template='index_list_industry.html' )
        json = SerializationBrowser( serializer=EventSerializer, emitter=JSONEmitter, paginate_by=100, display=False, verbose_name=_( "JSON" ) )
        ical = SerializationBrowser( serializer=ICalEventSerializer, emitter=ICalEmitter, paginate_by=100, display=True, verbose_name=_( "iCal" ) )
