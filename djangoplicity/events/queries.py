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

from datetime import date, datetime, timedelta
from pytz import timezone

from django.core import validators
from django.core.exceptions import ValidationError
from django.db.models import Q

from djangoplicity.archives.contrib.queries import ForeignKeyQuery, AllPublicQuery  # pylint: disable=no-name-in-module

from djangoplicity.events.models import EventSite


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
        - year: return only events from the given year (or past event for the
          current year if given witout value
        """
        (qs, query_data) = super(SiteQuery, self).queryset(model, options, request, **kwargs)

        # Possible get parameters for the site_query
        type = [ self._sanitize_slug(t).upper() for t in request.GET.getlist('type', '') ]
        series = self._sanitize_slug(request.GET.get('series', ''))
        audience = [ self._sanitize_slug(t).upper() for t in request.GET.getlist('audience', '') ]
        calendar = request.GET.get('calendar', None)  # 0 for past, 1 for future
        video_only = 'video' in request.GET

        if 'year' in request.GET:
            try:
                year = int(request.GET.get('year', None))
            except (ValueError, TypeError):
                # No year or invalid year, we use the current year
                year = date.today().year
        else:
            year = None

        try:
            upcoming = int(request.GET.get('upcoming', None))  # 0 for past, 1 for future
        except (ValueError, TypeError):
            if year:
                upcoming = None
            else:
                upcoming = 1

        qs = qs.select_related('location', 'series')

        now = datetime.now()

        # Get selected site
        site = EventSite.objects.get(slug=kwargs['stringparam'])

        # Get "now" in the timezone of the selected site
        # TODO: This is a hack as we use naive timestamp in the database,
        # we should really use aware timestamps and do this cleanly
        now = datetime.now(timezone(site.timezone)).replace(tzinfo=None)

        if type:
            qs = qs.filter(type__in=type)
        if series:
            qs = qs.filter(series__slug=series)
        if audience:
            qs = qs.filter(audience__in=audience)
        if upcoming is not None and year is None:
            if upcoming == 0:
                qs = qs.filter(Q(end_date__lte=now, end_date__isnull=False) | Q(start_date__lte=now, end_date__isnull=True))
            elif upcoming == 1:
                qs = qs.filter(Q(end_date__gte=now, end_date__isnull=False) | Q(start_date__gte=now, end_date__isnull=True))
        if calendar and upcoming is None:
            qs = qs.filter(Q(end_date__gte=(now - timedelta(weeks=8)), end_date__isnull=False) | Q(start_date__gte=(now - timedelta(weeks=8)), end_date__isnull=True))
        if video_only:
            qs = qs.exclude(video_url='')

        if year:
            qs = qs.filter(
                start_date__year=year, start_date__lte=now
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
        now = datetime.now()
        (qs, query_data) = super(AllEventsQuery, self).queryset(model, options, request, **kwargs)
        # Possible get parameters for the site_query
        type = [self._sanitize_slug(t).upper() for t in request.GET.getlist('type', '')]
        series = self._sanitize_slug(request.GET.get('series', ''))
        audience = [self._sanitize_slug(t).upper() for t in request.GET.getlist('audience', '')]
        calendar = request.GET.get('calendar', None)  # 0 for past, 1 for future
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        video_only = 'video' in request.GET

        period = request.GET.get('period', 'default')
        access = request.GET.get('accessType', '')
        audience_type = request.GET.get('audienceType', '')
        time_of_day = request.GET.get('timeOfDay', None)
        online = request.GET.get('online', 'false') == 'true'
        country = request.GET.get('country', '')
        state = request.GET.get('state', '')
        city = request.GET.get('city', '')

        try:
            upcoming = int(request.GET.get('upcoming', None))  # 0 for past, 1 for future
            if upcoming >= 1:
                period = 'upcoming'
            elif period == 0:
                period = 'past'
        except (ValueError, TypeError):
            upcoming = None

        # Additional filters for 'access', 'time of day', 'location', and 'online' status
        if access and access != 'all':
            qs = qs.filter(access=access)
        if time_of_day and time_of_day != 'all':
            qs = qs.filter(time_of_day=time_of_day)
        if online:
            qs = qs.filter(location__name__icontains='online')
        else:
            if country and country != 'all':
                qs = qs.filter(location__country__iexact=country)
                if state and state != 'all':
                    qs = qs.filter(location__state__iexact=state)
                    if city and city != 'all':
                        qs = qs.filter(location__city__iexact=city)

        try:
            type.remove('ALL')
        except ValueError:
            pass

        if type:
            qs = qs.filter(type__in=type)
        if series and series != 'all':
            qs = qs.filter(series__slug=series)

        if audience:
            qs = qs.filter(audience__in=audience)
        elif audience_type and audience_type != 'all':
            qs = qs.filter(audience=audience_type)

        if calendar and upcoming is None:
            qs = qs.filter(
                Q(end_date__gte=(now - timedelta(weeks=8)), end_date__isnull=False) |
                Q(start_date__gte=(now - timedelta(weeks=8)), end_date__isnull=True)
            )
        if video_only:
            qs = qs.exclude(video_url='')

        if year and not month:
            qs = qs.filter(start_date__year=year, start_date__lte=now)

        if period:
            if period == 'upcoming':
                qs = qs.filter(
                    Q(end_date__gte=now, end_date__isnull=False) |
                    Q(start_date__gte=now, end_date__isnull=True))
            elif period == 'past':
                qs = qs.filter(
                    Q(end_date__lte=now, end_date__isnull=False) |
                    Q(start_date__lte=now, end_date__isnull=True))
            elif period == 'since' and year is not None and month is not None:
                try:
                    first_day_of_month = datetime(
                        year=int(year),
                        month=int(month),
                        day=1
                    )
                    qs = qs.filter(
                        Q(end_date__gte=first_day_of_month, end_date__isnull=False) |
                        Q(start_date__gte=first_day_of_month, end_date__isnull=True)
                    )
                except (TypeError, ValueError):
                    pass
            else:
                upcoming_events = qs.filter(
                    Q(end_date__gte=now, end_date__isnull=False) |
                    Q(start_date__gte=now, end_date__isnull=True))

                if upcoming_events:
                    qs = upcoming_events
                else:
                    # workaround if there are no future events send past event
                    period = 'past'
                    qs = qs.filter(
                        Q(end_date__lte=now, end_date__isnull=False) |
                        Q(start_date__lte=now, end_date__isnull=True))

        if period == 'past':
            qs = qs.order_by('-start_date')

        return (qs, query_data)


class IndustryEventsQuery(AllEventsQuery):
    def queryset(self, model, options, request, **kwargs):
        (qs, query_data) = super(IndustryEventsQuery, self).queryset(model, options, request, **kwargs)
        qs = qs.filter(Q(series__slug='industry-day') | Q(audience='IN'))
        qs = qs.order_by('-start_date')
        return (qs, query_data)
