from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Event
from users.models import UserData, UserDonation, UserAttending
from .utils import event_donation_total, event_donation_list
from django.contrib import messages
from notifications.signals import notify
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

"""
Display all Events
TODO: don't display past events
"""
def event_list_view(request):
    event_list = Event.objects.order_by('-start_date')
    donation_list = event_donation_list(event_list)
    data_list = zip(event_list, donation_list)
    notify_list = request.user.notifications.unread()[:5]

    # SEARCH FUNCTION
    query = request.GET.get("q")
    if query:
        event_list = event_list.filter(
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

        #test if user is attending or volunteering for the event
        data = UserData.objects.get(user=request.user)
        is_attending = Event.objects.filter(userattending__user=data, id=event_id).exists()
        is_volunteering = Event.objects.filter(userdata__user=request.user).exists()

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {
        'event': event,
        'donation': donation,
        'user': request.user,
        'is_attending': is_attending,
        'is_volunteering': is_volunteering,
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
                #notify user and committee members
                notify.send(request.user, recipient=request.user, verb='You are attending ', target=event)
                for committee_member in list(User.objects.filter(is_staff=True)):
                    #don't norify an attending committee member twice
                    if committee_member is not request.user:
                        notify.send(request.user, recipient=committee_member, verb=u' is attending ', target=event)

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

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

        except UserData.DoesNotExist:
            raise Http404("Missing user data! what?!")

    event_list = Event.objects.order_by('-start_date')[:5]

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

        except Event.DoesNotExist:
            raise Http404("Event does not exist")

    event_list = Event.objects.order_by('-start_date')[:5]
    
    return redirect('/events/')

"""
Display a list of all volunteers
"""
def event_volunteer_list_view(request, event_id):
    #get event specified in url
    try:
        volunteers = User.objects.filter(userdata__events_volunteering__id=event_id)
        # Testing
        messages.success(request, 'Hello world.')

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {
        'user_list': volunteers,
        'user': request.user,
    }

    return render(request, 'events/eventUsers.html', context)

"""
Display a list of all attendees
"""
def event_attendee_list_view(request, event_id):

    try:
        attending = User.objects.filter(userdata__userattending__event__id=event_id)

    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    context = {
        'user_list': attending,
        'user': request.user,
    }

    return render(request, 'events/eventUsers.html', context)

"""
Mark all user notifications as read
"""
@csrf_exempt
def event_mark_all_view(request):

    mark_all = request.POST.get('view_all', False)

    if mark_all:

        request.user.notifications.unread().mark_all_as_read()
        
    else:

        print("fuck:")

    return HttpResponse(simplejson.dumps(response))




