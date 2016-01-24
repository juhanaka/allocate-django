from django.conf.urls import url, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', views.home, name='authentication_home'),
    url('^login/*', auth_views.login, {'template_name': 'authentication/login.html',
      'redirect_field_name': 'signup_complete'}, name='authentication_login'),
    url('^signup/', views.signup, name='authentication_signup'),
    url('^oauth2callback', views.auth_return, name='authentication_return'),
]
