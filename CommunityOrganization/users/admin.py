from django.contrib import admin
from .models import UserData, UserDonation, UserAttending

admin.site.register(UserData)

class DonationDetailAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "donation")
admin.site.register(UserDonation, DonationDetailAdmin)

class AttendingDetailAdmin(admin.ModelAdmin):
    list_display = ("user", "event")
admin.site.register(UserAttending, AttendingDetailAdmin)
