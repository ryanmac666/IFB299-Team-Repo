from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail

from django.contrib.auth.forms import AuthenticationForm

from .forms import UserCreateForm
from .models import UserData, UserDonation, UserAttending

from events.models import Event
from events.utils import event_donation_list, event_user_donation_total, event_user_donation_list

"""
Display users attending and volunterring events
TODO: Display user information
"""
def user_view(request):
    #ensure user is loged in
    if not request.user.is_authenticated:
        return redirect('/users/login')

    else:
        # get all events the user is attending or volunteering
        data = UserData.objects.get(user=request.user)

        attending_list = Event.objects.filter(userattending__user=data)
        attending_donation_list = event_donation_list(attending_list)
        user_attending_donation_list = event_user_donation_list(attending_list, data)
        attending_data = zip(attending_list, attending_donation_list, user_attending_donation_list)

        volunteering_list = Event.objects.filter(userdata__user=request.user)
        volunteering_donation_list = event_donation_list(volunteering_list)
        user_volunteering_donation_list = event_user_donation_list(volunteering_list, data)
        volunteering_data = zip(volunteering_list, volunteering_donation_list, user_volunteering_donation_list)

        notify_list = request.user.notifications.unread()[:5]

        context = {
            'attending_data': attending_data,
            'volunteering_data': volunteering_data,
            'user': request.user,
            'notify_list': notify_list,
        }

        return render(request, 'users/users.html', context)


"""
Allow users to create an account
TODO: Ask for information such as first and last name
"""
def user_signup_view(request):

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save()
            send_mail(
                'Registration successful',
                'Thanks for registering',
                'ifb299dummyemail@gmail.com',
                ['ifb299dummyemail@gmail.com'],
                fail_silently=False,
            )

            if user is not None:
                login(request, user)
                return redirect('/events')
            else:
                return redirect('/users/login')
    else:
        form = UserCreateForm()

    notify_list = None

    #ensure user is not anonymous when getting notifications
    if request.user.is_authenticated:
        notify_list = request.user.notifications.unread()[:5]
        
    context = {
        'form': form,
        'user': request.user,
        'notify_list': notify_list,
    }

    return render(request, 'users/signup.html', context)


"""
Allow users to login
"""
def user_login_view(request):
    notify_list = None

    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST)

        if form.is_valid():
            login(request, form.get_user())

            return redirect('/events')

    else:
        form = AuthenticationForm()


    #ensure user is not anonymous when getting notifications
    if request.user.is_authenticated:
        notify_list = request.user.notifications.unread()[:5]

    context = {
        'form': form,
        'user': request.user,
        'notify_list': notify_list,
    }

    return render(request, 'users/login.html', context)


"""
Log users out
"""
def user_logout_view(request):
    logout(request)

    return redirect('/users/login')


"""
View Splash Page
"""
def user_splash_view(request):
    return render(request, 'users/splash.html')
