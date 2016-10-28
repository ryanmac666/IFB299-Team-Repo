from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
            url(r'^$', views.user_view, name='user_view'),
            url(r'^signup', views.user_signup_view, name='user_signup_view'),
            url(r'^logout', views.user_logout_view, name='user_logout_view'),
            url(r'^login', views.user_login_view, name='user_login_view'),
            url(r'^splash', views.user_splash_view, name='user_splash_view')
            ]
