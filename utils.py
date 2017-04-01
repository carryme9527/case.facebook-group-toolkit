import settings
from datetime import datetime, timedelta

def get_token():
    access_token = ''
    with open(settings.data_token_filename) as fh:
        access_token = fh.read()
    return access_token

def set_token(access_token):
    with open(settings.data_token_filename, 'w') as fh:
        fh.write(access_token)

def time_limit(hours=24):
    now = datetime.now()
    time_limit = now - timedelta(hours=hours)
    return time_limit

def parse_time(created_time):
    time = datetime.strptime(created_time[:-5], '%Y-%m-%dT%H:%M:%S')
    time += timedelta(hours=8)
    return time

def is_in_24_hours(created_time, hours=24):
    return parse_time(created_time) > time_limit(hours)

def is_owner(comment):
    return comment['from']['id'] == settings.facebook_user_id
