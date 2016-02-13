import base64
import httplib2
import json
import datetime

from apiclient import discovery
from authentication import models as authentication_models
from utils import dateutils
from oauth2client import django_orm

class CredentialsException(Exception):
  pass


def get_google_credential(user_id):
  """Fetch the google oauth credential from db based on user_id.

  Args:
    user_id: Integer
  Returns:
    oauth2client.client.Credential object
  Raises:
    CredentialsException if credential not found or invalid.
  """
  user = authentication_models.get_user_by_id(user_id)
  if user is None:
    raise ValueError('No user found with id: {0}'.format(user_id))
  storage = django_orm.Storage(authentication_models.CredentialsModel,
                               'id', user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid:
      raise CredentialsException('Credentials not found or invalid.')
  return credential


class Event(object):
  """Base class for events.

  Attributes:
    id: Uniquely identifies Events with same type and source
    type: Type of the event, e.g. 'calendar'
    source: Source of the data, e.g. 'google'
    title: Title of the event, e.g. the subject line in email
    timestamp: Python datetime object. Start of the event.
    duration: Python timedelta object. Duration of the event.
  """
  def __init__(self, **kwargs):
    self.id = kwargs.pop('id', None)
    self.type = kwargs.pop('type', None)
    self.source = kwargs.pop('source', None)
    self.title = kwargs.pop('title', None)
    self.timestamp = kwargs.pop('timestamp', None)
    self.duration = kwargs.pop('duration', None)

  @classmethod
  def get_all(cls, user_id, date):
    """Get all events for user and date.

    Args:
      user_id: Integer corresponding to user id in django
      date: datetime.date object

    Returns:
      A list of Event subclass objects.
    """
    raise NotImplementedError


class CalendarEvent(Event):
  """Base class for calendar based events.

  Attributes:
    creator: The email of the creator.
    members: A list of emails.
    notes: string. Further description of the event.
    type: 'calendar'
  """
  def __init__(self, **kwargs):
    super(CalendarEvent, self).__init__(**kwargs)
    self.creator = kwargs.pop('creator', None)
    self.members = kwargs.pop('members', None)
    self.notes = kwargs.pop('notes', None)
    self.type = 'calendar'


class EmailEvent(Event):
  """Base class for email based events.

  Attributes:
    recipients: List of email addresses (including cc).
    sender: Sender email address.
    body: string.
    type: 'email'
  """
  def __init__(self, **kwargs):
    super(EmailEvent, self).__init__(**kwargs)
    self.recipients = kwargs.pop('recipients', None)
    self.sender = kwargs.pop('sender', None)
    self.body = kwargs.pop('body', None)
    self.type = 'email'


class GoogleCalendarEvent(CalendarEvent):
  def __init__(self, **kwargs):
    super(GoogleCalendarEvent, self).__init__(**kwargs)
    self.source = 'google'

  @classmethod
  def get_all(cls, user_id, date):
    """See base class."""
    credential = get_google_credential(user_id)
    http = httplib2.Http()
    http = credential.authorize(http)
    service = discovery.build("calendar", "v3", http=http)
    entries = []
    page_token = None

    while True:
      calendar_list = service.events().list(
          calendarId='primary',
          timeMin=dateutils.today_midnight().isoformat(),
          timeMax=dateutils.now_in_local().isoformat(),
          pageToken=page_token
      ).execute()
      entries.extend(calendar_list['items'])
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

    objects = [cls.create_object_from_entry(entry) for entry in entries]
    return objects

  @classmethod
  def create_object_from_entry(cls, entry):
    """Creates an object from a dictionary returned from client api."""
    start = dateutils.parse_google_datetime(entry['start']['dateTime'])
    end = dateutils.parse_google_datetime(entry['end']['dateTime'])
    if 'attendees' in entry:
      members = [member['email'] for member in entry['attendees']]
    else:
      members = None
    creator = entry['creator']['email'] if 'creator' in entry else None
    return cls(id=entry['id'], title=entry.get('summary'),
               timestamp=start, duration=end-start, creator=creator,
               members=members, notes=entry.get('description'))


class GoogleEmailEvent(EmailEvent):
  def __init__(self, **kwargs):
    super(GoogleEmailEvent, self).__init__(**kwargs)
    self.source = 'google'

  @classmethod
  def create_object_from_entry(cls, entry):
    """Creates an object from a dictionary returned from client api."""
    recipients = []
    sender = None
    subject = None
    body = None
    date = None
    for header in entry['payload']['headers']:
      if header['name'] == 'To' or header['name'] == 'Cc':
        recipients.append(header['value'])
      elif header['name'] == 'From':
        sender = header['value']
      elif header['name'] == 'Subject':
        subject = header['value']
      elif header['name'] == 'Date':
        date = dateutils.parse_email_datetime(header['value'])
    if 'data' in entry['payload']['body']:
      try:
        body = base64.b64decode(entry['payload']['body']['data'])
      except TypeError:
        body = entry['payload']['body']['data']
    return cls(id=entry['id'], sender=sender, recipients=recipients,
               title=subject, body=body, timestamp=date)

  @classmethod
  def get_all(cls, user_id, date):
    """See base class."""
    credential = get_google_credential(user_id)
    http = httplib2.Http()
    http = credential.authorize(http)
    service = discovery.build("gmail", "v1", http=http)
    entries = []
    page_token = None

    start=dateutils.today_midnight()
    end = start + datetime.timedelta(days=1)
    query_string = 'after:{0} before:{1}'.format(
        start.strftime('%Y/%m/%d'),
        end.strftime('%Y/%m/%d')
    )

    while True:
      email_list = service.users().messages().list(
          q=query_string,
          userId='me',
          pageToken=page_token
      ).execute()
      for ids in email_list['messages']:
        msg = service.users().messages().get(userId='me',
                                             id=ids['id']).execute()
        entries.append(msg)
      page_token = email_list.get('nextPageToken')
      if not page_token:
        break

    objects = [cls.create_object_from_entry(entry) for entry in entries]
    return objects

class RescuetimeEvent(object):
  pass
