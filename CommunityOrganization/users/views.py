from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import UserCreateForm
from .models import UserData, UserDonation, UserAttending
from events.models import Event

def users(request):

	if not request.user.is_authenticated:
		return redirect('/users/login')
	else:
		#get all events the user is atteneding or volunteering
		data = UserData.objects.get(user=request.user)
		attending_list = Event.objects.filter(userattending__user=data)
		volunteering_list = Event.objects.filter(userdata__user=request.user)
		context = {
			'attending_list': attending_list,
			'volunteering_list': volunteering_list,
			}
		return render(request, 'users/users.html', context)

def signup(request):

	if request.method == 'POST':
		form = UserCreateForm(request.POST)

		if form.is_valid():
			form.save()
			return users(request)

	form = UserCreateForm()
	context = {'form': form}

	return render(request, 'users/signup.html', context)

def loginUser(request):
	context = {}
	#context.update(csrf(request))
	return render(request, 'users/login.html', {})

def authUser(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = authenticate(username=username, password=password)

	if user is not None:
		login(request, user)
		return redirect('/events')
	else:
		return redirect('/users/login')

def logoutUser(request):
    logout(request)
    return redirect('/users/login')