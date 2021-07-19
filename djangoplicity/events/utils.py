from django.contrib.auth.models import User
from djangoplicity.events.models import INTERNAL_AUDIENCE_KEY

def is_internal(request):
    """
    Check if a request is an internal request
    """
    try:
        user = User.objects.get(username='internal')
        pw = request.GET.get('pw', None)
        if pw and user.check_password(pw):
            return True
    except:
        pass

    return False

def get_url_secret_param(request):
    """
    Return url secret param
    """
    if is_internal(request):
        return '?pw=' + request.GET.get('pw', None)
    else:
        return ''
