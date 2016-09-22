from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Event
from users.models import UserData, UserDonation, UserAttending
from .utils import event_donation_total, event_donation_list, event_notify
from django.contrib import messages

"""
Display all Events
TODO: don't display past events
"""
def event_list_view(request):
    event_list = Event.objects.order_by('-start_date')
    donation_list = event_donation_list(event_list)
    data_list = zip(event_list, donation_list)
    notify_list = None
    notify_unread = None

    #ensure user is not anonymous when getting notifications
    if request.user.is_authenticated:
        notify_list = request.user.notifications.unread()[:5]



    # SEARCH FUNCTION
    query = request.GET.get("q")
    if query:
        event_list = event_list.filter(
            Q(start_date__icontains=query) |
            Q(end_date__icontains=query) |
            Q(event_name__icontains=query) |
            Q(event_location__icontains=query)
        ).distinct()
        donation_list = event_donation_list(event_list)
        data_list = zip(event_list, donation_list)

    context = {
        'data_list': data_list,
        'user': request.user,
        'notify_list': notify_list,
    }

    return render(request, 'events/eventIndex.html', context)

"""
Display all information about an event 
"""
def event_view(request, event_id):
    #get event specified in url
    try:
        event = Event.objects.get(id=event_id)
        donation = event_donation_total(event)
        is_attending = None
        is_volunteering = None
        notify_list = None
        notify_unread = None

        #ensure user is not anonymous
        if request.user.is_authenticated:
            #test if user is attending or volunteering for the event
            data = UserData.objects.get(user=request.user)
            is_attending = Event.objects.filter(userattending__user=data, id=event_id).exists()
            is_volunteering = Event.objects.filter(userdata__user=request.user).exists()
            #get notifications
            notify_list = request.user.notifications.unread()[:5]

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {
        'event': event,
        'donation': donation,
        'user': request.user,
        'is_attending': is_attending,
        'is_volunteering': is_volunteering,
        'notify_list': notify_list,
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
                raise Http404("Already in event! p.s this is for debuging only. make a page!")

            else:
                attendingUser = UserAttending(user=user, event=event, family=amount)
                attendingUser.save()
                event_notify(request, event, "You are attending", "is attending")

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

        except UserData.DoesNotExist:
            raise Http404("Missing user data! what?!")

    event_list = Event.objects.order_by('-start_date')[:5]

    return redirect('/events/')

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
            event_notify(request, event, "You are donating to", "is donating to")

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

        except UserData.DoesNotExist:
            raise Http404("Missing user data! what?!")

    #event_list = Event.objects.order_by('-start_date')[:5]

    return redirect('/events/')

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
                event_notify(request, event, "You are volunteering for", "is volunteering for")

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

    #event_list = Event.objects.order_by('-start_date')[:5]
    
    return redirect('/events/')

"""
Display a list of all volunteers
"""
def event_volunteer_list_view(request, event_id):
    notify_list = None

    #get event specified in url
    try:
        volunteers = User.objects.filter(userdata__events_volunteering__id=event_id)

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    #ensure user is not anonymous when getting notifications
    if request.user.is_authenticated:
        notify_list = request.user.notifications.unread()[:5]

    context = {
        'user_list': volunteers,
        'user': request.user,
        'notify_list': notify_list,
    }

    return render(request, 'events/eventUsers.html', context)

"""
Display a list of all attendees
"""
def event_attendee_list_view(request, event_id):
    notify_list = None

    try:
        attending = User.objects.filter(userdata__userattending__event__id=event_id)

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    #ensure user is not anonymous when getting notifications
    if request.user.is_authenticated:
        notify_list = request.user.notifications.unread()[:5]

    context = {
        'user_list': attending,
        'user': request.user,
        'notify_list': notify_list,
    }

    return render(request, 'events/eventUsers.html', context)

"""
Mark all user notifications as read
"""
def event_mark_all_view(request):
    #ensure request is a post request
    if request.method == 'POST':
        request.user.notifications.unread().mark_all_as_read()

    return redirect('/events/')




