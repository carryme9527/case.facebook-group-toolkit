# -*- coding: UTF-8 -*-

import json
import utils
import settings
import facebook_util
import requests

def get_post_content(raw_id, access_token):
  url = facebook_util.api_url('/' + raw_id)
  params = { 'access_token': access_token }
  resp = json.loads(requests.get(url, params=params).text)
  return resp['message']

def parse(data, access_token):
  results = {}
  data = filter(lambda x: 'comments' in x.keys(), data)

  for row in data:
    group_id, post_id = row['id'].split('_')
    post_url = facebook_util.group_post_url(group_id, post_id)
    comments = row['comments']['data']
    comments = filter(lambda x: not utils.is_owner(x), comments)

    returned = []
    for comment in comments:
      if not utils.is_in_24_hours(comment['created_time']):
          continue

      from_name = comment['from']['name']
      user_url = facebook_util.user_url(comment['from']['id'])
      message = comment['message']
      comment_url = facebook_util.group_comment_url(group_id, post_id, comment['id'])

      returned.append((from_name, user_url, message, time, comment_url))
    if len(returned) > 0:
      results[(post_url, get_post_content(row['id'], access_token), len(returned) + 1)] = returned
  return results

def get_data(access_token):
  path = '/{0}/feed'.format(settings.facebook_group_id)
  data = facebook_util.get_comments_order_by_time(path, access_token)['data']
  results = parse(data, access_token)
  return results
