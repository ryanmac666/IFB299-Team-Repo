from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.eventsIndex, name='eventsIndex'),
            url(r'^(?P<eventID>[0-9]+)/$', views.event, name='event'),
            url(r'^(?P<eventID>[0-9]+)/join/$', views.eventJoin, name='joinEvent'),
            url(r'^(?P<eventID>[0-9]+)/volunteer/$', views.eventVolunteer, name="volunteerEvent"),
            ]