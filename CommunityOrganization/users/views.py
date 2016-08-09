from django.shortcuts import render

def users(request):
	context = {}
	return render(request, 'users/users.html', context)