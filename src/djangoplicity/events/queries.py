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

from datetime import datetime 
from djangoplicity.archives.contrib.queries import AllPublicQuery
from django.http import Http404


class ForeignKeyQuery( AllPublicQuery ):
	def __init__( self, fk_field, *args, **kwargs ):
		self.fk_field = fk_field
		super( ForeignKeyQuery, self ).__init__( *args, **kwargs )
	
	def queryset( self, model, options, request, stringparam=None, **kwargs ):
		if not stringparam:
			raise Http404
		
		( qs , query_data ) = super( ForeignKeyQuery, self ).queryset( model, options, request, **kwargs )
		qs = qs.filter( **{ self.fk_field : stringparam } )
		
		return ( qs , query_data )
	
	def url_args(self, model, options, request, stringparam=None, **kwargs ):
		"""
		Hook for query to specify extra reverse URL lookup arguments.
		"""
		return [ stringparam ]
	

class SiteQuery( ForeignKeyQuery ):
	def __init__( self, *args, **kwargs ):
		super( SiteQuery, self ).__init__( 'location__site__name', *args, **kwargs )