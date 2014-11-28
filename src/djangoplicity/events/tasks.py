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

from celery.task import task

from django.conf import settings
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build


def _google_calendar_service():
	client_email = settings.GCAL_EMAIL
	private_key_file = settings.GCAL_PRIVATE_KEY
	with open(private_key_file) as f:
		private_key = f.read()
	credentials = SignedJwtAssertionCredentials(client_email, private_key, 'https://www.googleapis.com/auth/calendar')
	http_auth = credentials.authorize(Http())
	service = build(serviceName='calendar', version='v3', http=http_auth)
	return service


def _google_calendar_update(service, eventId, calendarId, oldCalendarId, body):
	from googleapiclient.http import HttpError
	if eventId:
		try:
			# retreive the existing event
			existing = service.events().get(eventId=eventId, calendarId=oldCalendarId).execute()
		except HttpError, err:
			if err.resp.status == 404:
				# if the event is not found, we will just create a new one
				existing = None

	if existing:
		if oldCalendarId != calendarId:
			result = service.events().move(eventId=eventId, calendarId=oldCalendarId, destination=calendarId).execute()
		# the iCal 'sequence' should be incresed, see http://www.kanzaki.com/docs/ical/sequence.html
		body['sequence'] = existing['sequence'] + 1
		result = service.events().update(eventId=eventId, calendarId=calendarId, body=body).execute()
	else:
		# We couldn't find the original event, so we just create a new one
		result = service.events().insert(calendarId=calendarId, body=body).execute()
	return result


@task()
# def google_calendar_sync(instance):
def google_calendar_sync(instance_id, _old_audience):
	from djangoplicity.events.models import Event

	instance = Event.objects.get(id=instance_id)
	service = _google_calendar_service()
	calendarId = settings.GCAL_CALENDAR[instance.audience]
	eventId = instance.gcal_key

	## code below retreives oldCalendarId when this function is called on pre_save
	# get previous calendar id; we might need to move the event to another calendar
	# if instance.id:
	# 	old_instance = type(instance).objects.get(pk=instance.pk)
	# 	oldCalendarId = settings.GCAL_CALENDAR[old_instance.audience]
	# else:
	# 	old_instance = None
	# 	oldCalendarId = calendarId

	# code below retreives oldCalendarId when this function is called on post_save
	# _old_audience is saved on post_init
	if eventId:
		# oldCalendarId = settings.GCAL_CALENDAR[instance._old_audience]
		oldCalendarId = settings.GCAL_CALENDAR[_old_audience]

	# create the event data
	data = {}
	data['summary'] = instance.title
	data['start'] = {'dateTime': instance.start_date_tz.isoformat(), 'timeZone': instance.start_date_tz.tzinfo.zone }
	data['end'] = {'dateTime': instance.end_date_tz.isoformat(), 'timeZone': instance.end_date_tz.tzinfo.zone }
	data['transparency'] = 'transparent'
	if instance.location:
		data['location'] = unicode(instance.location)
	# if instance.abstract:
	# 	data['description'] = instance.abstract

	if instance.published:
		if eventId:
			result = _google_calendar_update(service=service, eventId=eventId, calendarId=calendarId, oldCalendarId=oldCalendarId, body=data)
		else:
			result = service.events().insert(calendarId=calendarId, body=data).execute()
		instance.gcal_key = result['id']
		instance.save(update_fields=['gcal_key'])
	else:
		if eventId:
			service.events().delete(eventId=eventId, calendarId=oldCalendarId).execute()
			instance.gcal_key = None
			instance.save(update_fields=['gcal_key'])


@task()
def google_calendar_delete(eventId, audience):
	service = _google_calendar_service()
	# calendarId = settings.GCAL_CALENDAR[instance.audience]
	# eventId = instance.gcal_key
	calendarId = settings.GCAL_CALENDAR[audience]
	if eventId:
		result = service.events().delete(eventId=eventId, calendarId=calendarId).execute()
