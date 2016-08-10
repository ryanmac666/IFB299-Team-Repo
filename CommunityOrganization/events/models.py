from django.db import models
from django.utils import timezone

class Event(models.Model):
	event_name     = models.CharField(max_length=100)
	event_location = models.CharField(max_length=500)
	event_cost	   = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
	start_date     = models.DateTimeField('start date')
	end_date       = models.DateTimeField('end date')

	def __str__(self):
		return self.event_name
	#return true if start date is within 3 days
	def is_upcoming(self):
            return self.start_date >= timezone.now() - datetime.timedelta(days=3)

