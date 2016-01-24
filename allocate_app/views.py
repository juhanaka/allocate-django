from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from oauth2client.django_orm import Storage
from . import models
from authentication import models as authentication_models
from django.core.urlresolvers import reverse

@login_required
def home(request):
  storage = Storage(authentication_models.CredentialsModel, 'id', request.user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True:
    return HttpResponseRedirect(reverse('authentication_home'))
  return render_to_response('allocate_app/home.html')
