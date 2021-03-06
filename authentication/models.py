from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import models as auth_models
from oauth2client.django_orm import FlowField, CredentialsField

def get_user_by_id(user_id):
  try:
    user = auth_models.User.objects.get(id=user_id)
  except auth_models.User.DoesNotExist:
    user = None
  return user

class CompanyModel(models.Model):
  name = models.CharField(max_length=200, unique=True)
  employees = models.ManyToManyField(auth_models.User, related_name="employee_of")
  managers = models.ManyToManyField(auth_models.User, related_name="manager_of")

class FlowModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True, on_delete=models.CASCADE)
  flow = FlowField()

class CredentialsModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True, on_delete=models.CASCADE)
  credential = CredentialsField()

class RescuetimeTokenModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True, on_delete=models.CASCADE)
  token = models.CharField(max_length=1000)

class OutlookCredentialsModel(models.Model):
  id = models.ForeignKey(auth_models.User, primary_key=True, on_delete=models.CASCADE)
  server = models.CharField(max_length=1000)
  email_address = models.CharField(max_length=1000)
  password = models.CharField(max_length=1000)
