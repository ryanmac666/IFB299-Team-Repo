from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

from .forms import UserCreateForm

def users(request):
	context = {}
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

def logoutUser(request):
    logout(request)