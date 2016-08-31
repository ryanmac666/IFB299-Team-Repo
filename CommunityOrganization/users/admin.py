from django.contrib import admin
from .models import UserData, UserDonation, UserAttending

admin.site.register(UserData)
admin.site.register(UserDonation)
admin.site.register(UserAttending)
