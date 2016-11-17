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

from datetime import date, timedelta
from djangoplicity.archives.contrib.queries import ForeignKeyQuery, AllPublicQuery
from django.core import validators
from django.core.exceptions import ValidationError
from django.db.models import Q


class SiteQuery(ForeignKeyQuery):
	"""
	Archive query for filtering events by location site (e.g. ESO Garching)
	"""

	def __init__(self, *args, **kwargs):
		super(SiteQuery, self).__init__('location__site__slug', *args, **kwargs)

	def _sanitize_slug(self, value):
		"""
		Make sure a request input value is actually slug. If not,
		the just return an empty string.
		"""
		if value:
			try:
				validators.validate_slug(value)
				return value
			except ValidationError:
				pass
		return ''

	def queryset(self, model, options, request, **kwargs):
		"""
		Allow extra get parameters to filter list of shown items.

		- type: filter by type
		- series: filter by series
		- upcoming (0/1): filter by past or future events
		- calendar: return only events no more than 8 weeks in the past and all in t
		- year: return only events from the given year
		"""
		(qs, query_data) = super(SiteQuery, self).queryset(model, options, request, **kwargs)

		# Possible get parameters for the site_query
		type = [ self._sanitize_slug(t).upper() for t in request.GET.getlist('type', '') ]
		series = self._sanitize_slug(request.GET.get('series', ''))
		audience = [ self._sanitize_slug(t).upper() for t in request.GET.getlist('audience', '') ]
		calendar = request.GET.get('calendar', None)  # 0 for past, 1 for future
		video_only = 'video' in request.GET

		try:
			year = int(request.GET.get('year', None))  # 0 for past, 1 for future
		except (ValueError, TypeError):
			year = None

		try:
			upcoming = int(request.GET.get('upcoming', None))  # 0 for past, 1 for future
		except (ValueError, TypeError):
			if year:
				upcoming = None
			else:
				upcoming = 1

		qs = qs.select_related('location', 'series')

		if type:
			qs = qs.filter(type__in=type)
		if series:
			qs = qs.filter(series__slug=series)
		if audience:
			qs = qs.filter(audience__in=audience)
		if upcoming is not None and year is None:
			if upcoming == 0:
				qs = qs.filter(Q(end_date__lte=date.today(), end_date__isnull=False) | Q(start_date__lte=date.today(), end_date__isnull=True))
			elif upcoming == 1:
				qs = qs.filter(Q(end_date__gte=date.today(), end_date__isnull=False) | Q(start_date__gte=date.today(), end_date__isnull=True))
		if calendar and upcoming is None:
			qs = qs.filter(Q(end_date__gte=(date.today() - timedelta(weeks=8)), end_date__isnull=False) | Q(start_date__gte=(date.today() - timedelta(weeks=8)), end_date__isnull=True))
		if video_only:
			qs = qs.exclude(video_url='')

		if year:
			qs = qs.filter(
				start_date__year=year, start_date__lte=date.today()
			).order_by('-start_date')

		return (qs, query_data)


class AllEventsQuery(AllPublicQuery):
	"""
	Archive query for filtering events by location site (e.g. ESO Garching)
	"""

	def _sanitize_slug(self, value):
		"""
		Make sure a request input value is actually slug. If not,
		the just return an empty string.
		"""
		if value:
			try:
				validators.validate_slug(value)
				return value
			except ValidationError:
				pass
		return ''

	def queryset(self, model, options, request, **kwargs):
		"""
		Allow extra get parameters to filter list of shown items.

		- type: filter by type
		- series: filter by series
		- upcoming (0/1): filter by past or future events
		- calendar: return only events no more than 8 weeks in the past and all in t
		- year: return only events from the given year
		"""
		(qs, query_data) = super(AllEventsQuery, self).queryset(model, options, request, **kwargs)

		# Possible get parameters for the site_query
		type = [ self._sanitize_slug(t).upper() for t in request.GET.getlist('type', '') ]
		series = self._sanitize_slug(request.GET.get('series', ''))
		audience = [ self._sanitize_slug(t).upper() for t in request.GET.getlist('audience', '') ]
		calendar = request.GET.get('calendar', None)  # 0 for past, 1 for future
		year = request.GET.get('year', None)
		video_only = 'video' in request.GET

		try:
			upcoming = int(request.GET.get('upcoming', None))  # 0 for past, 1 for future
		except (ValueError, TypeError):
			upcoming = None

		if type:
			qs = qs.filter(type__in=type)
		if series:
			qs = qs.filter(series__slug=series)
		if audience:
			qs = qs.filter(audience__in=audience)
		if upcoming is not None and year is None:
			# We only filter by upcoming is year is not set
			if upcoming == 0:
				qs = qs.filter(Q(end_date__lte=date.today(), end_date__isnull=False) | Q(start_date__lte=date.today(), end_date__isnull=True))
			elif upcoming == 1:
				qs = qs.filter(Q(end_date__gte=date.today(), end_date__isnull=False) | Q(start_date__gte=date.today(), end_date__isnull=True))
		if calendar and upcoming is None:
			qs = qs.filter(Q(end_date__gte=(date.today() - timedelta(weeks=8)), end_date__isnull=False) | Q(start_date__gte=(date.today() - timedelta(weeks=8)), end_date__isnull=True))
		if video_only:
			qs = qs.exclude(video_url='')

		if year:
			qs = qs.filter(start_date__year=year, start_date__lte=date.today())

		return (qs, query_data)


class IndustryEventsQuery(AllEventsQuery):
	def queryset(self, model, options, request, **kwargs):
		(qs, query_data) = super(IndustryEventsQuery, self).queryset(model, options, request, **kwargs)
		qs = qs.filter(Q(series__slug='industry-day') | Q(audience='IN'))
		qs = qs.order_by('-start_date')
		return (qs, query_data)
