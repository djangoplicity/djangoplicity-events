import json
from datetime import datetime
from django.utils.formats import date_format
from djangoplicity.events.models import Event, PUBLIC_AUDIENCE_TYPES, EventLocation, EventSeries, EVENT_TYPES
from django_countries import countries


def event_constants(request):

    today = datetime.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    months = [(i, date_format(datetime(2024, i, 1), 'F')) for i in range(1, 13)]

    locations = EventLocation.objects.all().values('country', 'state', 'city').distinct()
    countries_data = {code: name for code, name in countries}

    locations_data = {}
    for location in locations:
        country_code = location['country']
        country_name = countries_data.get(country_code, country_code)
        state = location['state']
        city = location['city']

        if country_code and country_code not in locations_data:
            locations_data[country_code] = {'name': country_name, 'states': {}}

        if country_code and state and state not in locations_data[country_code]['states']:
            locations_data[country_code]['states'][state] = {'cities': []}

        if country_code and state and city and city not in locations_data[country_code]['states'][state]['cities']:
            locations_data[country_code]['states'][state]['cities'].append(city)

    return {
        'MONTHS': months,
        'YEARS': range(year - 10, year + 11),
        'CURRENT_YEAR': year,
        'CURRENT_MONTH': month,
        'CURRENT_MONTH_NAME': today.strftime('%B'),
        'DAY_TIMES': Event.TIME_OF_DAY_TYPES,
        'TYPES': EVENT_TYPES,
        'ACCESS_TYPES': Event.ACCESS_TYPES,
        'AUDIENCE_TYPES': PUBLIC_AUDIENCE_TYPES,
        'TIME_OF_DAY_TYPES': Event.TIME_OF_DAY_TYPES,
        'LOCATIONS': locations_data,
        'LOCATIONS_DATA': json.dumps(locations_data),
        'SERIES': EventSeries.objects.all().order_by('name')
    }
