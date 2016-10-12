from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.event_list_view, name='event_list_view'),
    url(r'^(?P<event_id>[0-9]+)/$', views.event_view, name='event_view'),
    url(r'^(?P<event_id>[0-9]+)/attend/$', views.event_attend_view, name='event_attend_view'),
    url(r'^(?P<event_id>[0-9]+)/donate/$', views.event_donate_view, name='event_donate_view'),
    url(r'^(?P<event_id>[0-9]+)/volunteer/$', views.event_volunteer_view, name='event_volunteer_view'),
    url(r'^(?P<event_id>[0-9]+)/attending/$', views.event_volunteer_list_view, name='event_volunteer_list_view'),
    url(r'^(?P<event_id>[0-9]+)/volunteering/$', views.event_attendee_list_view, name='event_attendee_list_view'),
    url(r'^(?P<event_id>[0-9]+)/event_notify_donations/$', views.event_notify_donations_view, name='event_notify_donations_view'),
    url(r'^create/$', views.event_create_view, name='event_create_view'),
    url(r'^mark_all_as_read/$', views.event_mark_all_view, name='event_mark_all_view'),
]
