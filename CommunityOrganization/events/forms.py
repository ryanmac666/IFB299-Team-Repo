from django import forms
from .models import Event

class EventCreateForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ("event_name", "event_location", "event_cost", "event_estemated_interrest", "start_date", "end_date")
	def __init__(self, *args, **kwargs):
		super(EventCreateForm, self).__init__(*args, **kwargs)
		self.fields['start_date'].widget = widgets.AdminDateTime()