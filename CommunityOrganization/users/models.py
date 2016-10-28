from django.db import models
from django.contrib.auth.models import User

"""
UserData Table
"""

class UserData(models.Model):
    events_volunteering = models.ManyToManyField('events.Event')
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return self.user.username


"""
UserDonation Table
"""


class UserDonation(models.Model):
    user = models.ForeignKey(UserData)
    event = models.ForeignKey('events.Event', related_name='donated_to')
    donation = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.user.username + " Donated " + str(self.donation)
    
"""
UserAttending Table
"""


class UserAttending(models.Model):
    user = models.ForeignKey(UserData)
    event = models.ForeignKey('events.Event')
    family = models.IntegerField(default=0)

    def __str__(self):
        return self.user.user.username + " Attending " + self.event.event_name
