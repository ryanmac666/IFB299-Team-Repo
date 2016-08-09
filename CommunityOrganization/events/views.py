from django.shortcuts import render
from .models import Event

def events(request):
	event_list = Event.objects.order_by('-start_date')[:5]
	context = {'event_list': event_list}
	return render(request, 'events/events.html', context)
