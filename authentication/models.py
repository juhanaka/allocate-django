from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import models as auth_models
from oauth2client.django_orm import FlowField, CredentialsField

class FlowModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True)
  flow = FlowField()

class CredentialsModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True)
  credential = CredentialsField()
