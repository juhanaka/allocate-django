from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from oauth2client.django_orm import Storage
from . import models
from authentication import models as authentication_models
from django.core.urlresolvers import reverse
from algs import allocator

@login_required
def home(request):
  try:
    allocator_obj = allocator.GoogleAllocator(request.user)
    todays_events_json = allocator_obj.get_todays_events_json()
    return render_to_response('allocate_app/home.html', {'todays_events': todays_events_json})
  except allocator.CredentialsError:
    return HttpResponseRedirect(reverse('authentication_home'))
