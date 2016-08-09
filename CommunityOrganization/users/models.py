from django.db import models
from django.contrib.auth.models import User

import events

class UserData(models.Model):
	events_confirmed = models.ManyToManyField('events.Event')
	user = models.OneToOneField(User)
