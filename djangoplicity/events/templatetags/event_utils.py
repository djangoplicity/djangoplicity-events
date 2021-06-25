from django import template
from djangoplicity.events.models import EVENT_TYPES, EDUCATIONAL_EVENT_TYPES, PUBLIC_AUDIENCE_TYPES, Calendar
from django.utils.translation import ugettext_lazy as _, ugettext

register = template.Library()

@register.inclusion_tag('audience_options.html', takes_context=True)
def show_event_audiences(context):
    choices = PUBLIC_AUDIENCE_TYPES
    audience = context.request.GET['audience'] if 'audience' in context.request.GET else None

    # Get current url params
    event_types = context.request.GET.getlist('type', [])
    upcoming = context.request.GET.get('upcoming', None)

    current_params = ''
    for event_type in event_types:
        if current_params == '':
            current_params += 'type=%s' % event_type
        else:
            current_params += '&type=%s' % event_type

    current_params += '&upcoming=%s' % upcoming if upcoming else ''

    # All
    all_audiences = '?%s' % current_params if current_params != '' else '.'

    if current_params != '':
        current_params = '&%s' % current_params

    return {
        'choices': choices,
        'current_params': current_params,
        'audience': audience,
        'all': all_audiences
        }

@register.inclusion_tag('event_type_options.html', takes_context=True)
def show_event_types(context):
    choices = EVENT_TYPES
    event_types = context.request.GET.getlist('type', [])

    # Get current url params
    audiences = context.request.GET.getlist('audience', [])
    upcoming = context.request.GET.get('upcoming', None)

    current_params = ''
    for audience in audiences:
        if current_params == '':
            current_params += 'audience=%s' % audience
        else:
            current_params += '&audience=%s' % audience

    current_params += '&upcoming=%s' % upcoming if upcoming else ''

    # All
    all_types = '?%s' % current_params if current_params != '' else '.'

    if current_params != '':
        current_params = '&%s' % current_params

    return {
        'choices': choices,
        'current_params': current_params,
        'types': event_types,
        'all': all_types
        }

@register.inclusion_tag('upcoming_options.html', takes_context=True)
def show_event_upcoming_options(context):
    choices = [
        ('1', 'Upcoming Events'),
        ('0', 'Past Events')
    ]
    upcoming = context.request.GET.get('upcoming', None)

    # Get current url params
    audiences = context.request.GET.getlist('audience', [])
    event_types = context.request.GET.getlist('type', [])


    current_params = ''
    for audience in audiences:
        if current_params == '':
            current_params += 'audience=%s' % audience
        else:
            current_params += '&audience=%s' % audience

    for event_type in event_types:
        if current_params == '':
            current_params += 'type=%s' % event_type
        else:
            current_params += '&type=%s' % event_type

    # All
    all_types = '?%s' % current_params if current_params != '' else '.'

    if current_params != '':
        current_params = '&%s' % current_params

    return {
        'choices': choices,
        'current_params': current_params,
        'upcoming': upcoming,
        'all': all_types
        }

@register.inclusion_tag('calendar_options.html', takes_context=True)
def show_calendars(context):
    calendars = Calendar.objects.all()
    return { 'calendars': calendars }

def is_educational_event(event_type):
    if not isinstance(event_type, str):
        return False
    for key, value in EDUCATIONAL_EVENT_TYPES:
        if key == event_type:
            return True
    return False

def request_contain_all_educational_events(event_types):
    """
    Return True when all educational events are request
    """
    if len(event_types) < 4:
        return False
    for key, value in EDUCATIONAL_EVENT_TYPES:
        if key not in event_types:
            return False
    return True

def cast_event_title(title):
    # not append events word
    if title.lower() in ['exhibition', 'talk', 'conference']:
        return title + 's'

    if title.lower().endswith("event"):
        title += 's'
    else:
        title += " Events"
    return title


@register.simple_tag(takes_context=True)
def event_title(context):
    event_types = context.request.GET.getlist('type', None)

    event_type = context.request.GET.get('type', None)
    upcoming = context.request.GET.get('upcoming', None)
    title = 'Events'

    if request_contain_all_educational_events(event_types):
        title = cast_event_title('Educational')
    else:
        for key, value in EVENT_TYPES:
            if key == event_type:
                # Special case when all educational types are request
                title = cast_event_title(value)

    if upcoming == '1':
        return ugettext('Upcoming %s' % title)
    elif upcoming == '0':
        return ugettext('Past %s' % title)

    return ugettext(title)
