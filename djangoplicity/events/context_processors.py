# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from djangoplicity.events.utils import is_internal, get_url_secret_param


def internal_request( request ):
    """
    Sets a context variable to check if a request is an internal request
    """
    return {
        'SECRET_PARAM': get_url_secret_param(request),
        'EVENT_INTERNAL_REQUEST': is_internal(request)
        }
