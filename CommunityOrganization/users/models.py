from django.db import models

import events

class UserData(models.Model):
	events_confirmed = models.ManyToManyField('events.Event')
