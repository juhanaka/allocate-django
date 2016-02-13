from django.shortcuts import render, render_to_response
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
    try:
      allocator_obj = allocator.GoogleAllocator(request.user)
      todays_events_json = allocator_obj.get_todays_events_json()
      #projects_json = allocator_obj.get_projects_json()
      return render_to_response('allocate_app/thankyou.html')
      #return render_to_response('allocate_app/home.html',
      #                          {'todays_events': todays_events_json,
      #                           'projects': projects_json})
    except allocator.CredentialsError:
      return HttpResponseRedirect(reverse('authentication_home'))

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
