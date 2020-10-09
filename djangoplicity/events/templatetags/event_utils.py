from django import template
from djangoplicity.events.models import EVENT_TYPES, AUDIENCE_TYPES

register = template.Library()

@register.inclusion_tag('audience_options.html', takes_context=True)
def show_event_audiences(context):
    choices = AUDIENCE_TYPES
    audience = context.request.GET['audience'] if 'audience' in context.request.GET else None

    # Get current url params
    event_type = context.request.GET['type'] if 'type' in context.request.GET else None
    current_params = '&type=%s' % event_type if event_type else ''

    # All
    all_audiences = '?type=%s' % event_type if event_type else '.'

    return {
        'choices': choices,
        'current_params': current_params,
        'audience': audience,
        'all': all_audiences
        }

@register.inclusion_tag('event_type_options.html', takes_context=True)
def show_event_types(context):
    choices = EVENT_TYPES
    event_type = context.request.GET['type'] if 'type' in context.request.GET else None

    # Get current url params
    audience = context.request.GET['audience'] if 'audience' in context.request.GET else None
    current_params = '&audience=%s' % audience if audience else ''

    # All
    all_types = '?audience=%s' % audience if audience else '.'

    return {
        'choices': choices,
        'current_params': current_params,
        'type': event_type,
        'all': all_types
        }
