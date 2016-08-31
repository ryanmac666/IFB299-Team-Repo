from django.db import models
from django.contrib.auth.models import User

import events

"""
UserData Table:

Small comment here
"""
class UserData(models.Model):
	events_volunteering = models.ManyToManyField('events.Event')
	user               = models.OneToOneField(User, null=True)

"""
UserDonation Table:

Small comment here
"""
class UserDonation(models.Model):
	user     = models.ForeignKey(UserData)
	event    = models.ForeignKey('events.Event')
	donation = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

"""
UserAttending Table:

Small comment here
"""
class UserAttending(models.Model):
	user = models.ForeignKey(UserData)
	event = models.ForeignKey('events.Event')
	family = models.IntegerField(default=0)

