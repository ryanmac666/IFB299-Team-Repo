from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
            url(r'^$', views.users, name='users'),
            url(r'^signup', views.signup, name='signup'),
            url(r'^logout', views.logoutUser, name='logoutUser'),
            url(r'^login', views.loginUser, name='loginUser'),
            url(r'^auth', views.authUser, name='authUser'),
            ]