from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Event
from users.models import UserData, UserDonation, UserAttending
from .utils import event_donation_total, event_donation_list

"""
Display all Events
TODO: don't display past events
"""
def event_list_view(request):
    event_list = Event.objects.order_by('-start_date')
    donation_list = event_donation_list(event_list)
    data_list = zip(event_list, donation_list)

    context = {'data_list': data_list}

    return render(request, 'events/eventIndex.html', context)

"""
Display all information about an event 
"""
def event_view(request, event_id):
    #get event specified in url
    try:
        event = Event.objects.get(id=event_id)
        donation = event_donation_total(event)

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {
        'event': event,
        'donation': donation,
    }

    return render(request, 'events/eventPage.html', context)

"""
Add user to event attendee table
"""
def event_attend_view(request, event_id):
    amount = request.POST.get('amount', 0)

    if not request.user.is_authenticated:
        return redirect('/users/login')

    else:
        try:
            event = Event.objects.get(id=event_id)
            user = UserData.objects.get(user=request.user)
            #make sure user is not already attending this event
            if UserAttending.objects.filter(user=user, event=event).exists():
                raise Http404("already in event! p.s this is for debuging only. make a page!")

            else:
                attendingUser = UserAttending(user=user, event=event, family=amount)
                attendingUser.save()

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

        except UserData.DoesNotExist:
            raise Http404("Missing user data! what?!")

    event_list = Event.objects.order_by('-start_date')[:5]
    context = {'event_list': event_list}

    return render(request, 'events/eventIndex.html', context)

"""
Add a donation to the event
"""
def event_donate_view(request, event_id):
    amount = request.POST.get('amount', 0)

    if not request.user.is_authenticated:
        return redirect('/users/login')

    else:
        try:
            event = Event.objects.get(id=event_id)
            user = UserData.objects.get(user=request.user)

            donation = UserDonation(user=user, event=event, donation=amount)
            donation.save()

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

        except UserData.DoesNotExist:
            raise Http404("Missing user data! what?!")

    event_list = Event.objects.order_by('-start_date')[:5]
    context = {'event_list': event_list}

    return render(request, 'events/eventIndex.html', context)

"""
Add user to volunteer table
"""
def event_volunteer_view(request, event_id):
    if not request.user.is_authenticated:
        return redirect('/users/login')

    else:
        try:
            event = Event.objects.get(id=event_id)
            #make sure user is not already volunteer for the event this event
            if Event.objects.filter(id=event_id, userdata__user=request.user).exists():
                raise Http404("already volunteering! p.s this is for debuging only. make a page!")

            else:
                user_voluntee = UserData.objects.get(user=request.user)
                user_voluntee.events_volunteering.add(event)
                user_voluntee.save()

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

    event_list = Event.objects.order_by('-start_date')[:5]
    context = {'event_list': event_list}

    return render(request, 'events/eventIndex.html', context)

"""
Display a list of all volunteers
"""
def event_volunteer_list_view(request, event_id):
    #get event specified in url
    try:
        volunteers = User.objects.filter(userdata__events_volunteering__id=event_id)

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {'user_list': volunteers}

    return render(request, 'events/eventUsers.html', context)

"""
Display a list of all attendees
"""
def event_attendee_list_view(request, event_id):

    try:
        attending = User.objects.filter(userdata__userattending__event__id=event_id)

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {'user_list': attending}

    return render(request, 'events/eventUsers.html', context)




