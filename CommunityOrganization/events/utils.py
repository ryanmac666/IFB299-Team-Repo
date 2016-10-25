from .models import Event
from users.models import UserData, UserDonation, UserAttending
from notifications.signals import notify
from django.contrib.auth.models import User

"""
Calculate total donation amounts for an event
"""
def event_donation_total(event):
	donations = 0

	for event_donation in UserDonation.objects.filter(event=event):
		donations += event_donation.donation

	return donations


def event_user_donation_total(event, user):
        donations = 0
        for event_donation in UserDonation.objects.filter(event=event).filter(user=user):
                donations += event_donation.donation

        return donations

"""
Calculate total donation amounts for a list of events
"""
def event_donation_list(event_list):

	donations_list = [];


	for event in event_list:
		donations_list.append(event_donation_total(event))

	return donations_list

def event_user_donation_list(event_list, user):

	donations_list = [];


	for event in event_list:
		donations_list.append(event_user_donation_total(event, user))

	return donations_list

def event_attendee_donation_list(event, user_list):

	donations_list = [];


	for user in user_list:
		donations_list.append(event_user_donation_total(event, user))

	return donations_list

"""
Get a list of family members attending for all attending members
"""
def event_user_family(event, attending):

	family_list = []

	for user in attending:
		family_list.append(UserAttending.objects.get(user=user, event=event).family)

	return family_list

"""
Notify the user and committee members
verb1 is the message to the user
verb2 is the message to the committee members
"""
def event_notify(request, event, verb1, verb2):
	#notify user and committee members
    notify.send(request.user, recipient=request.user, verb=verb1 + ' ', target=event)
    for committee_member in list(User.objects.filter(is_staff=True)):
        #don't norify an attending committee member twice
            if committee_member is not request.user:
                notify.send(request.user, recipient=committee_member, verb= ' ' + verb2 + ' ', target=event)
