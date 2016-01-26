import httplib2
import re
from authentication import models as authentication_models
from oauth2client.django_orm import Storage
from apiclient.discovery import build
from django.core import serializers
from allocate_app import models
from allocate_app.dateutils import parse_google_datetime, now_in_local, today_midnight

class AllocatorError(Exception):
    pass

class CredentialsError(Exception):
    pass

class GoogleAllocator(object):
  def __init__(self, user):
    self.user = user
    self.credential = self.get_credential()
          
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
        timeMin=today_midnight().isoformat(),
        timeMax=now_in_local().isoformat(),
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

  def get_projects_json(self):
    projects = self.get_projects()
    return serializers.serialize('json', projects)

  def get_existing_events_for_today(self):
    user_events = models.GoogleCalendarEventModel.objects.filter(
        user=self.user)
    return user_events

  def get_unallocated_events_for_today(self):
    unallocated_events = models.GoogleCalendarEventModel.objects.filter(
        user=self.user, project=None)
    return unallocated_events

  def update_todays_events(self):
    all_events_from_google = self.get_calendar_events_for_today()
    existing_events = self.get_existing_events_for_today()
    for event in all_events_from_google:
        if existing_events.filter(event_id=event['id']).exists():
          continue

        start = parse_google_datetime(event['start']['dateTime'])
        end = parse_google_datetime(event['end']['dateTime'])
        event_model = models.GoogleCalendarEventModel(
            event_id=event['id'], user=self.user, calendar_id='primary',
            summary=event['summary'], start=start, end=end)
        event_model.save()

  def allocate_and_save_event(self, event, projects):
    for project in projects:
      if re.search(project.pattern, event.summary):
          event.project = project
          event.save()

  def allocate_todays_unallocated_events(self):
    events = self.get_unallocated_events_for_today()
    projects = self.get_projects()
    for event in events:
        self.allocate_and_save_event(event, projects)

  def get_todays_events_json(self):
    self.update_todays_events()
    self.allocate_todays_unallocated_events()
    events = self.get_existing_events_for_today()
    return serializers.serialize('json', events)

