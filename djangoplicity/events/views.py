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
from django.core.paginator import Paginator
from djangoplicity.events.models import Event
from datetime import datetime, timedelta
from djangoplicity.archives.views import GenericDetailView
from django.views.generic import ListView
import calendar
from django.utils.formats import date_format


class EventEmbedDetailView( GenericDetailView ):
    """
    Archive detail view for embed Event

    Will just use detail_embed.html to render the event instead of detail.html

    The view is installed in options.py
    """
    def vary_on( self, request, model, obj, state, admin_rights, **kwargs ):
        return ['embed', ]

    def select_template( self, model, obj, **kwargs ):
        return super( EventEmbedDetailView, self ).select_template( model, obj, suffix='_embed' )


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

    def get_queryset(self):
        query = {}
        today = datetime.today()
        queryset = super().get_queryset()

        # Get params
        audience_type = self.request.GET.get('audienceType', 'all')
        access = self.request.GET.get('accessType', 'all')
        period = self.request.GET.get('period', 'upcoming')
        month = int(self.request.GET.get('month', today.month))
        self.year = int(self.request.GET.get('year', today.year))
        series = self.request.GET.get('series', 'all')
        time_of_date = self.request.GET.get('timeOfDay', 'all')
        online = self.request.GET.get('online', 'false') == 'true'
        country = self.request.GET.get('country', 'all')
        state = self.request.GET.get('state', 'all')
        city = self.request.GET.get('city', 'all')

        # First day of the month
        self.first_day_of_month = datetime(self.year, month, 1)

        # Get the current filters, month and year, ect. You can modify this to allow users to change the month/year.

        if period == 'past':
            query.update({'start_date__lte': self.today})
        elif period == 'since':
            query.update({'start_date__gte': self.first_day_of_month})
        elif period == 'upcoming':
            query.update({'start_date__gte': self.today})

        if audience_type != 'all':
            query.update({'audience': audience_type})

        if access != 'all':
            query.update({'access': access})

        if series != 'all':
            query.update({'series': series})

        if time_of_date != 'all':
            query.update({'time_of_day': time_of_date})

        if online:
            query.update({'location__name__icontains': 'online'})
        else:
            if country != 'all':
                query.update({'location__country': country})
                if state != 'all':
                    query.update({'location__state': state})
                    if city != 'all':
                        query.update({'location__city': city})

        print(query)
        queryset = queryset.filter(**query)
        print(queryset.count())
        return queryset.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Prepare the query for the calendar here

        # Current month's events
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

        # sort events by year, month, day
        for event in events_page:
            # Calculate the duration of the event
            duration = (event.end_date - event.start_date).days

            # Iterate through each day of the event
            for day in range(duration + 1):
                current_date = event.start_date + timedelta(days=day)

                # Extract the year, month, and day
                _year = current_date.year
                _month = date_format(current_date, 'F')
                _day = date_format(current_date, 'l, j F Y')

                # Add the event to the data structure
                events_by_year_month_day[_year][_month][_day].append(event)

        context['events_by_year_month_day'] = defaultdict_to_dict(events_by_year_month_day)
        context['current_month'] = date_format(self.first_day_of_month, 'F')
        context['current_year'] = self.year
        return context


