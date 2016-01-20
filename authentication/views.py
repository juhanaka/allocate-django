from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout, models as user_models
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . import models
from django.conf import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
import httplib2
from apiclient.discovery import build
from oauth2client.django_orm import Storage
from datetime import datetime

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://app.getallocate.in/authentication/oauth2callback')

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      user = authenticate(username=request.POST['username'],
                          password=request.POST['password1'])
      login(request, user)
      return HttpResponseRedirect(reverse('index'))
  else:
    form = UserCreationForm()
  token = {}
  token.update(csrf(request))
  token['form'] = form
  return render_to_response('authentication/signup.html', token)

@login_required
def index(request):
  storage = Storage(models.CredentialsModel, 'id', request.user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return render_to_response('authentication/index.html', {'auth_url': authorize_url, 'authorized': False})
  return render_to_response('authentication/index.html', {'authorized': True})

@login_required
def google_calendar(request):
  storage = Storage(models.CredentialsModel, 'id', request.user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)
  else:
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("calendar", "v3", http=http)
    all_entries = []
    page_token = None
    while True:
      calendar_list = service.events().list(calendarId='primary', timeMin=datetime.utcnow().isoformat() + 'Z').execute()
      for calendar_list_entry in calendar_list['items']:
        all_entries.append({'time': calendar_list_entry['start'],
                            'description': calendar_list_entry['summary']})
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    return render_to_response('authentication/calendar.html', {'entries':all_entries})

@login_required
def auth_return(request):
  if not xsrfutil.validate_token(settings.SECRET_KEY, str(request.GET['state']),
                                 request.user):
    return HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.GET)
  storage = Storage(models.CredentialsModel, 'id', request.user, 'credential')
  storage.put(credential)
  return HttpResponseRedirect("index")
