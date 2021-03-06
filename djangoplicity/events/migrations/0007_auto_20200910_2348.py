# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-10 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20200505_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.URLField(blank=True, help_text=b'Alternative to display an image from this URL instead in case the image is not in the Images Archive.', max_length=255, null=True, verbose_name=b'Image URL'),
        ),
        migrations.AddField(
            model_name='event',
            name='registration',
            field=models.CharField(blank=True, help_text=b'Use this to add a registration URL or information about the registration to the event.', max_length=255, null=True, verbose_name=b'Registration'),
        ),
    ]
