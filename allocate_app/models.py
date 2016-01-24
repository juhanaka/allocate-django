from __future__ import unicode_literals
from django.contrib.auth import models as auth_models
from django.db import models

class ProjectModel(models.Model):
  user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  client_name = models.CharField(max_length=200)
  project_name = models.CharField(max_length=200)

class EventModel(models.Model):
  user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  project = models.ForeignKey(ProjectModel)
