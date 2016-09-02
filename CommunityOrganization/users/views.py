from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import UserCreateForm
from .models import UserData, UserDonation, UserAttending

from events.models import Event
from events.utils import event_donation_list

"""
Display users attending and volunterring events
TODO: Display user information
"""
def user_view(request):

	if not request.user.is_authenticated:
		return redirect('/users/login')

	else:
		#get all events the user is atteneding or volunteering
		data = UserData.objects.get(user=request.user)

		attending_list = Event.objects.filter(userattending__user=data)
		attending_donation_list = event_donation_list(attending_list)
		attending_data = zip(attending_list, attending_donation_list)

		volunteering_list = Event.objects.filter(userdata__user=request.user)
		volunteering_donation_list = event_donation_list(volunteering_list)
		volunteering_data = zip(volunteering_list, volunteering_donation_list)

		context = {
			'attending_data': attending_data,
			'volunteering_data': volunteering_data,
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
			form.save()
			return users(request)

	form = UserCreateForm()
	context = {'form': form}

	return render(request, 'users/signup.html', context)

"""
Allow users to login
"""
def user_login_view(request):
	context = {}

	return render(request, 'users/login.html', context)

"""
Authenticate user login data for POST request
"""
def user_auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = authenticate(username=username, password=password)

	if user is not None:
		login(request, user)

		return redirect('/events')

	else:

		return redirect('/users/login')

"""
Log users out
"""
def user_logout_view(request):
    logout(request)

    return redirect('/users/login')