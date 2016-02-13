from datetime import datetime
from dateutil import parser
from events.utils.rfc3339 import parse_datetime, tzinfo, UTC_TZ

LOCAL_TZ = tzinfo(-8*60, '-08:00')

def to_local(dtm):
  return dtm.astimezone(LOCAL_TZ)

def now_in_local():
  now = to_local(datetime.utcnow().replace(tzinfo=UTC_TZ))
  return now

def today_midnight():
  today = now_in_local().replace(hour=0, minute=0, second=0, microsecond=0)
  return today

def parse_google_datetime(datetime_str):
  return to_local(parse_datetime(datetime_str))

def parse_email_datetime(datetime_str):
  return to_local(parser.parse(datetime_str))
