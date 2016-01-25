from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.home, name='app_home'),
    url('^project$', views.project_handler, name='project_handler'),
    url('^event$', views.event_handler, name='event_handler')
]
