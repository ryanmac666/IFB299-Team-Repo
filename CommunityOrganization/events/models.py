from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.urlresolvers import reverse


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_location = models.CharField(max_length=500)
    event_cost = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    event_estemated_interrest = models.IntegerField(default=100)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        return self.event_name

    # return true if start date is within 3 days
    def is_upcoming(self):
        return self.start_date >= timezone.now() - timedelta(days=3)

    # the url to the Django admin interface for the model instance
    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))
