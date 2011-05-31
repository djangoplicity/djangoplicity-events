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
from djangoplicity.archives import ArchiveOptions
from djangoplicity.archives.contrib.browsers import NormalBrowser, \
	SerializationBrowser
from djangoplicity.archives.contrib.queries import AllPublicQuery
from djangoplicity.archives.contrib.serialization import XMPEmitter, JSONEmitter
from djangoplicity.archives.views import SerializationDetailView
from djangoplicity.events.models import EventSerializer
from djangoplicity.events.queries import SiteQuery
	
class EventOptions( ArchiveOptions ):
	urlname_prefix = "events"
	
	detail_views = (
		{ 'url_pattern' : 'api/(?P<serializer>json)/', 'view' : SerializationDetailView( serializer=EventSerializer, emitters=[JSONEmitter] ), 'urlname_suffix' : 'serialization', },
	)
	
	class Queries(object):
		default = AllPublicQuery( browsers = ( 'json', ), verbose_name = "Events and meetings" )
		site = SiteQuery( browsers = ('json',), verbose_name = "Events and meetings" )
		
	class Browsers(object):
		json = SerializationBrowser( serializer=EventSerializer, emitter=JSONEmitter, paginate_by=100, display=False, verbose_name=_("JSON") )