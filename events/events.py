class BaseEvent(object):
  def __init__(self, **kwargs):
    self.source = kwargs.pop('source', None)
    self.title = kwargs.pop('title', None)
    self.timestamp = kwargs.pop('timestamp', None)
    self.duration = kwargs.pop('duration')

  @classmethod
  def get_all(cls, user_id, date):
    raise NotImplementedError

  def serialize_to_json(self):
    raise NotImplementedError

class CalendarEvent(object):
  def __init__(self, **kwargs):
    kwargs['source'] = 'calendar'
    super(CalendarEvent, self).__init__(kwargs)
    self.members = kwargs.pop('members', None)
    self.notes = kwargs.pop('notes', None)

class EmailEvent(object):
  pass

class RescuetimeEvent(object):
  pass

