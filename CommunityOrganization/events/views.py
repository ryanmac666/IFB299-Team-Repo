from django.shortcuts import render
from .models import Event

def index(request):
	event_list = Event.objects.order_by('-start_date')[:5]
	context = {'event_list': event_list}
	return render(request, 'index.html', context)
