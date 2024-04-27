from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def sanitize_slug(value):
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


def check_internal_password(request):
    """
    Check if a request is an internal request
    """
    try:
        user = User.objects.get(username='internal')
        pw = request.GET.get('pw', None)
        if pw and user.check_password(pw):
            return True
    except User.DoesNotExist:
        pass
    return False
