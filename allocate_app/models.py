from __future__ import unicode_literals
from django.contrib.auth import models as auth_models
from django.db import models
from django.forms import ModelForm

class ProjectModel(models.Model):
  user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  client_name = models.CharField(max_length=200)
  project_name = models.CharField(max_length=200)
  # http://stackoverflow.com/questions/2930182/regex-to-not-match-any-characters
  pattern = models.CharField(max_length=200, default='(?!.*)') # don't match anything

class GoogleCalendarEventModel(models.Model):
  event_id = models.CharField(max_length=500)
  user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  project = models.ForeignKey(ProjectModel, null=True, blank=True, default=None)
  calendar_id = models.CharField(max_length=100)
  summary = models.CharField(max_length=500)
  organizer_email = models.CharField(max_length=500, default='')
  start = models.DateTimeField()
  end = models.DateTimeField()
  class Meta:
    unique_together = ('user', 'event_id')

