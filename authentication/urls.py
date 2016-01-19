from django.conf.urls import url, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^login/*', auth_views.login, {'template_name': 'authentication/login.html',
      'redirect_field_name': 'signup_complete'}, name='login'),
    url('^signup/', views.signup, name='signup'),
    url('^google_calendar/', views.google_calendar, name='google_calendar'),
    url('^oauth2callback', views.auth_return, name='auth_return'),
]
