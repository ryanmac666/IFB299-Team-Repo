from django.http import Http404
from django.shortcuts import render, redirect
from .models import Event
from users.models import UserData, UserDonation, UserAttending

def eventsIndex(request):
	#get the 5 most resent events
	event_list = Event.objects.order_by('-start_date')[:5]
	context = {'event_list': event_list}
	return render(request, 'events/eventIndex.html', context)

def event(request, eventID):
	#get event specified in url
	try:
		event = Event.objects.get(id=eventID)
	except Event.DoesNotExist:
		raise Http404("Event does not exist")

	context = {'event': event}
	return render(request, 'events/eventPage.html', context)

def eventJoin(request, eventID):
	if not request.user.is_authenticated:
		return redirect('/users/login')
	else:
		try:
			event = Event.objects.get(id=eventID)
			user = UserData.objects.get(user=request.user)
			#make sure user is not already attending this event
			if UserAttending.objects.filter(user=user, event=event).exists():
				raise Http404("already in event! p.s this is for debuging only. make a page!")
			else:
				attendingUser = UserAttending(user=user, event=event, family=0)
				attendingUser.save()

		except Event.DoesNotExist:
			raise Http404("Event does not exist")
		except UserData.DoesNotExist:
			raise Http404("Missing user data! what?!")

	event_list = Event.objects.order_by('-start_date')[:5]
	context = {'event_list': event_list}
	return render(request, 'events/eventIndex.html', context)


def eventVolunteer(request, eventID):
	if not request.user.is_authenticated:
		return redirect('/users/login')
	else:
		try:
			event = Event.objects.get(id=eventID)
			#make sure user is not already volunteer for the event this event
			if Event.objects.filter(id=eventID, userdata__user=request.user).exists():
				raise Http404("already volunteering! p.s this is for debuging only. make a page!")
			else:
				userVoluntee = UserData.objects.get(user=request.user)
				userVoluntee.eventsVolunteering.add(event)
				userVoluntee.save()

		except Event.DoesNotExist:
			raise Http404("Event does not exist")

	event_list = Event.objects.order_by('-start_date')[:5]
	context = {'event_list': event_list}
	return render(request, 'events/eventIndex.html', context)





