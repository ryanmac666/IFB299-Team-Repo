# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_event_cost'),
        ('users', '0002_auto_20160810_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAttending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.RenameField(
            model_name='userdata',
            old_name='events_confirmed',
            new_name='eventsVolunteering',
        ),
        migrations.AddField(
            model_name='userattending',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserData'),
        ),
    ]