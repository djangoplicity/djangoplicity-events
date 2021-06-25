# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-24 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_calendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='type',
            field=models.CharField(choices=[(b'H', b'HTML'), (b'I', b'ICAL'), (b'X', b'XML')], max_length=1),
        ),
    ]
