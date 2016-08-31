from .models import Event
from users.models import UserDonation

"""
Calculate total donation amounts for an event
"""
def event_donation_total(event):
	donations = 0

	for event_donation in UserDonation.objects.filter(event=event):
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