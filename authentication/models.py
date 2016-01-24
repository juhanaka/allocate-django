from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import models as auth_models
from oauth2client.django_orm import FlowField, CredentialsField

class FlowModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True, on_delete=models.CASCADE)
  flow = FlowField()

class CredentialsModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True, on_delete=models.CASCADE)
  credential = CredentialsField()

class ProjectModel(models.Model):
  user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  client_name = models.CharField(max_length=200)
  project_name = models.CharField(max_length=200)

class EventModel(models.Model):
  user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  project = models.ForeignKey(ProjectModel)
