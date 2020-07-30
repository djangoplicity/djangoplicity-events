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

"""
Serializers for Event models
"""

from djangoplicity.archives.contrib.serialization import SimpleSerializer


class EventSerializer( SimpleSerializer ):
    fields = (
        'title',
        'speaker',
        'affiliation',
        'abstract',
        'series',
        'type',
        'image',
        'start_date_tz',
        'end_date_tz',
        'location',
        'video_url',
        'additional_information',
    )

    def get_type_value( self, obj ):
        return obj.get_type_display()

    def get_image_value( self, obj ):
        if obj.image and obj.image.resource_screen:
            return obj.image.resource_wallpaper4.url
        else:
            return ""


class ICalEventSerializer( SimpleSerializer ):
    """
    Serialier responsible for converting events into
    iCal data structure.
    """

    fields = (
        'summary',
        'description',
        'location',
        'dtstart',
        'dtend',
        'dtstamp',
    )

    def get_summary_value( self, obj ):
        return "%s: %s" % ( obj.series, obj.title ) if obj.series else obj.title

    def get_description_value( self, obj ):
        tmp = [obj.title]

        if obj.additional_information:
            tmp.append("")
            tmp.append( obj.additional_information )

        if obj.speaker:
            if obj.affiliation:
                tmp.append("")
                tmp.append( "Speaker: %s (%s)" % (obj.speaker, obj.affiliation) )
            else:
                tmp.append("")
                tmp.append( "Speaker: %s" % obj.speaker )

        if obj.series:
            tmp.append( "Series: %s" % obj.series )

        if obj.abstract:
            tmp.append("")
            tmp.append( "ABSTRACT: %s" % obj.abstract )

        return "\n".join( tmp )

    def get_location_value( self, obj ):
        return obj.location

    def get_dtstart_value( self, obj ):
        return obj.start_date_tz

    def get_dtend_value( self, obj ):
        return obj.end_date_tz if obj.end_date_tz else obj.start_date_tz

    def get_dtstamp_value( self, obj ):
        return obj.end_date_tz if obj.end_date_tz else obj.start_date_tz