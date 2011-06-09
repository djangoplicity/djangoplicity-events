# -*- coding: utf-8 -*-
#
# djangoplicity-events
# Copyright (c) 2007-2011, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#	* Redistributions of source code must retain the above copyright
#	  notice, this list of conditions and the following disclaimer.
#
#	* Redistributions in binary form must reproduce the above copyright
#	  notice, this list of conditions and the following disclaimer in the
#	  documentation and/or other materials provided with the distribution.
#
#	* Neither the name of the European Southern Observatory nor the names 
#	  of its contributors may be used to endorse or promote products derived
#	  from this software without specific prior written permission.
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

from datetime import datetime, timedelta
from djangoplicity.archives.contrib.queries import ForeignKeyQuery 
from django.http import Http404
from django.core import validators
from django.core.exceptions import ValidationError

class SiteQuery( ForeignKeyQuery ):
	"""
	Archive query for filtering events by location site (e.g. ESO Garching)
	"""
	
	def __init__( self, *args, **kwargs ):
		super( SiteQuery, self ).__init__( 'location__site__slug', *args, **kwargs )

	def _sanitize_slug( self, value ):
		"""
		Make sure a request input value is actually slug. If not, 
		the just return an empty string.
		"""
		if value:
			try:
				validators.validate_slug( value )
				return value
			except ValidationError:
				pass
		return ''
				
	
	def queryset( self, model, options, request, **kwargs ):
		"""
		Allow extra get parameters to filter list of shown items.
		
		- type: filter by type
		- series: filter by series
		- upcoming (0/1): filter by past or future events
		- calendar: return only events no more than 8 weeks in the past and all in t
		"""
		( qs , query_data ) = super( SiteQuery, self ).queryset( model, options, request, **kwargs )
		
		# Possible get parameters for the site_query
		type = self._sanitize_slug( request.GET.get( 'type', '' ) )
		series = self._sanitize_slug( request.GET.get( 'series', '' ) )
		calendar = request.GET.get( 'calendar', None ) # 0 for past, 1 for future
		
		try: 
			upcoming = int( request.GET.get( 'upcoming', None ) ) # 0 for past, 1 for future
		except (ValueError, TypeError):
			upcoming = None
		
		if type:
			qs = qs.filter( type=type.upper() )
		if series:
			qs = qs.filter( series__slug=series )
		if upcoming is not None:
			if upcoming == 0:
				qs = qs.filter( end_date__lte=datetime.now() )
			elif upcoming == 1:
				qs = qs.filter( end_date__gte=datetime.now() )
		if calendar and upcoming is None:
			qs = qs.filter( end_date__gte=( datetime.now() - timedelta( weeks=8 ) ) )
			
		return ( qs , query_data )