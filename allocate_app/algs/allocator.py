import httplib2
from authentication import models as authentication_models
from oauth2client.django_orm import Storage
from apiclient.discovery import build
from datetime import datetime
from django.core import serializers
from allocate_app import models

class AllocatorError(Exception):
    pass

class CredentialsError(Exception):
    pass

class GoogleAllocator(object):
  def __init__(self, user):
    self.user = user
    self.credential = self.get_credential()

  @staticmethod
  def today_midnight():
    today = datetime.today()
    today = today.replace(hour=0, minute=0, second=0,
                          microsecond=0)
    return today

  @staticmethod
  def parse_google_datetime(datetime_str):
    return datetime.strptime(datetime_str[:18], '%Y-%m-%dT%H:%M:%S')

  def get_credential(self):
    storage = Storage(authentication_models.CredentialsModel,
                      'id', self.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        raise CredentialsError('Credentials not found or invalid.')
    return credential

  def get_calendar_events_for_today(self):
    if self.credential is None or self.credential.invalid:
        raise CredentialsError("Credentials not found or invalid.")
    http = httplib2.Http()
    http = self.credential.authorize(http)
    service = build("calendar", "v3", http=http)
    all_entries = []
    page_token = None
    while True:
      calendar_list = service.events().list(
        calendarId='primary',
        timeMin=self.today_midnight().isoformat() + '-07:00',
        timeMax=datetime.now().isoformat() + '-07:00',
        pageToken=page_token
      ).execute()
      all_entries += calendar_list['items']
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    print all_entries
    return all_entries

  def get_projects(self):
    user_projects = models.ProjectModel.objects.filter(user=self.user)
    return user_projects

  def get_existing_events_for_today(self):
    user_events = models.GoogleCalendarEventModel.objects.filter(
        user=self.user)
    return user_events

  def update_todays_events(self):
    all_events_from_google = self.get_calendar_events_for_today()
    existing_events = self.get_existing_events_for_today()
    for event in all_events_from_google:
        if existing_events.filter(event_id=event['id']).exists():
          continue

        start = self.parse_google_datetime(event['start']['dateTime'])
        end = self.parse_google_datetime(event['end']['dateTime'])
        event_model = models.GoogleCalendarEventModel(
            event_id=event['id'], user=self.user, calendar_id='primary',
            summary=event['summary'], start=start, end=end)
        event_model.save()

  def get_todays_events_json(self):
    self.update_todays_events()
    events = self.get_existing_events_for_today()
    return serializers.serialize('json', events)

  def get_projects_json(self):
    projects = self.get_projects()
    return serializers.serialize('json', projects)

