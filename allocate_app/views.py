from django.shortcuts import render, render_to_response
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from oauth2client.django_orm import Storage
from . import models
from authentication import models as authentication_models
from django.core.urlresolvers import reverse
from algs import allocator
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

@login_required
def home(request):
  if request.method == 'GET':
    companies = request.user.manager_of.all()
    if companies:
      return render_to_response('allocate_app/manager.html',
                                {'user': request.user, 'companies': companies})
    companies = request.user.employee_of.all()
    if companies:
      return render_to_response('allocate_app/employee.html',
                                {'user': request.user, 'companies': companies})
    return render_to_response('allocate_app/thankyou.html')

@login_required
def event_handler(request):
  if request.method == 'POST' or request.method == 'PUT':
    event_models = serializers.deserialize('json', '[' + request.body + ']')
    for obj in event_models:
        obj.save()
    return HttpResponse('{}')

@login_required
def project_handler(request):
  if request.method == 'POST' or request.method == 'PUT':
    obj = json.loads(request.body)
    fields = obj['fields']
    fields['user'] = request.user
    fields['id'] = obj['pk'] if 'pk' in obj else None
    models.ProjectModel.objects.update_or_create(**fields)

    return HttpResponse('{}')
