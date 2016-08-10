from django.db import models
from django.contrib.auth.models import User

import events

class UserData(models.Model):
	events_confirmed = models.ManyToManyField('events.Event')
	user             = models.OneToOneField(User, null=True)

class UserDonation(models.Model):
	user     = models.ForeignKey(UserData)
	event    = models.ForeignKey('events.Event')
	donation = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

