# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-04 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_event_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_estemated_interrest',
            field=models.IntegerField(default=100),
        ),
    ]
