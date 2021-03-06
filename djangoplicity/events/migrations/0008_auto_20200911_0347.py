# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-11 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20200910_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='video_url',
            field=models.URLField(blank=True, help_text=b"Link to flash video (.flv) of this event if it exists or YouTube's video URL in this format: https://www.youtube.com/watch?v=videoID.", max_length=255, null=True, verbose_name=b'Video URL'),
        ),
    ]
