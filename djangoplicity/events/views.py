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
from collections import defaultdict
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from djangoplicity.events.models import Event, INTERNAL_AUDIENCE_KEY
from datetime import datetime, timedelta
from djangoplicity.archives.views import GenericDetailView
from django.views.generic import ListView
import calendar
from django.utils.formats import date_format
from djangoplicity.events.utils import check_internal_password


class EventEmbedDetailView(GenericDetailView):
    """
    Archive detail view for embed Event

    Will just use detail_embed.html to render the event instead of detail.html

    The view is installed in options.py
    """

    def vary_on(self, request, model, obj, state, admin_rights, **kwargs):
        return ['embed', ]

    def select_template(self, model, obj, **kwargs):
        return super(EventEmbedDetailView, self).select_template(model, obj, suffix='_embed')


def defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: defaultdict_to_dict(v) for k, v in d.items()}
    return d


class CalendarView(ListView):
    model = Event
    template_name = 'events/calendar.html'  # Cambia esto por el nombre de tu template
    paginate_by = 10
    today = datetime.today()
    first_day_of_month = None
    year = None
    site_embed = False
    site_internal = False
    period = 'upcoming'
    pw = None

    def sanitize_slug(self, value):  # noqa
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

    def get_queryset(self):
        queryset = super().get_queryset()
        today = datetime.today()

        self.site_embed = self.request.GET.get('siteEmbed', 'false') == 'true'
        self.site_internal = self.request.GET.get('siteInternal', 'false') == 'true'
        self.period = self.request.GET.get('period', 'upcoming')
        self.year = int(self.request.GET.get('year', today.year))

        if self.site_internal:
            if check_internal_password(self.request):
                queryset = queryset.filter(audience=INTERNAL_AUDIENCE_KEY)
                self.pw = self.request.GET.get('pw', None)
            else:
                return []
        else:
            queryset = queryset.exclude(audience=INTERNAL_AUDIENCE_KEY)

        month = int(self.request.GET.get('month', today.month))
        online = self.request.GET.get('online', 'false') == 'true'

        # Params with All default option
        audience_type = self.request.GET.get('audienceType', 'all')
        access = self.request.GET.get('accessType', 'all')
        event_type = self.sanitize_slug(self.request.GET.get('type', 'all'))
        series = self.sanitize_slug(self.request.GET.get('series', 'all'))
        time_of_day = self.request.GET.get('timeOfDay', 'all')
        country = self.request.GET.get('country', 'all')
        state = self.request.GET.get('state', 'all')
        city = self.request.GET.get('city', 'all')

        # First day of the month
        self.first_day_of_month = datetime(self.year, month, 1)

        # Get the current filters, month and year, ect. You can modify this to allow users to change the month/year.
        if self.period == 'past':
            queryset = queryset.filter(
                Q(end_date__lte=today, end_date__isnull=False) |
                Q(start_date__lte=today, end_date__isnull=True)
            )
        elif self.period == 'since':
            queryset = queryset.filter(
                Q(end_date__gte=self.first_day_of_month) |
                Q(start_date__gte=self.first_day_of_month)
            )
        else:
            queryset = queryset.filter(
                Q(end_date__gte=today, end_date__isnull=False) |
                Q(start_date__gte=today, end_date__isnull=True)
            )

        if event_type != 'all':
            queryset = queryset.filter(type=event_type)

        if audience_type != 'all':
            queryset = queryset.filter(audience=audience_type)

        if access != 'all':
            queryset = queryset.filter(access=access)

        if series != 'all':
            queryset = queryset.filter(series__slug=series)

        if time_of_day != 'all':
            queryset = queryset.filter(time_of_day=time_of_day)

        if online:
            queryset = queryset.filter(location__name__icontains='online')
        else:
            if country != 'all':
                queryset = queryset.filter(location__country=country)
                if state != 'all':
                    queryset = queryset.update(location__state=state)
                    if city != 'all':
                        queryset = queryset.filter(location__city=city)

        if self.period == 'past':
            queryset = queryset.order_by('-start_date')
        else:
            queryset = queryset.order_by('start_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Prepare the query for the calendar here
        events = self.get_queryset()

        # Pagination
        p = Paginator(events, self.paginate_by)
        page = self.request.GET.get('page')
        events_page = p.get_page(page)

        events_by_year_month_day = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(list)
            )
        )

        # Check if the URL path contains 'site_embed' and add password
        context['event_detail_url'] = 'events_detail_embed' if self.site_embed else 'events_detail'
        if self.pw:
            context['pw'] = self.pw

        # sort events by year, month, day
        for event in events_page:
            # Calculate the duration of the event
            duration = (event.end_date - event.start_date).days

            # Extract the year, month, and day
            _year = event.start_date.year
            _month = date_format(event.start_date, 'F')

            if duration > 0:
                # Check if the event spans multiple months or years
                if event.start_date.month != event.end_date.month or event.start_date.year != event.end_date.year:
                    # Event spans different months or years
                    _day = f"{date_format(event.start_date, 'l, j F')} - {date_format(event.end_date, 'l, j F Y')}"
                else:
                    # Event spans multiple days but within the same month and year
                    _day = f"{date_format(event.start_date, 'l, j')} - {date_format(event.end_date, 'l, j F Y')}"
            else:
                # Event starts and ends on the same day
                _day = date_format(event.start_date, 'l, j F Y')

            # Add the event to the data structure
            events_by_year_month_day[_year][_month][_day].append(event)

        context['events_by_year_month_day'] = defaultdict_to_dict(events_by_year_month_day)
        context['current_month'] = date_format(self.first_day_of_month, 'F')
        context['current_year'] = self.year
        context['total_pages'] = p.num_pages
        return context
