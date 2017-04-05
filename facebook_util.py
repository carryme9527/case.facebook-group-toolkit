import requests
import json
from settings import facebook_domain, facebook_view, facebook_api_version

def api_url(path):
  return facebook_domain + facebook_api_version + path

def group_post_url(gid, pid):
    return '{0}/groups/{1}/permalink/{2}' \
        .format(facebook_view, gid, pid)

def group_comment_url(gid, pid, cid):
    return '{0}/?comment_id={1}' \
        .format(group_post_url(gid, pid), cid)

def user_url(uid):
    return '{0}/{1}'.format(facebook_view, uid)

def get_comments_order_by_time(path, access_token):
  url = api_url(path)
  params = { 'fields': 'message,comments.order(reverse_chronological)' }
  resp = requests.get(url, params = params).text
  return request(path, access_token, params)

def request(path, access_token, params = {}):
  p = {
    'access_token': access_token,
    'limit': 50,
  }
  p.update(params)
  resp = requests.get(api_url(path), params=p).text
  return json.loads(resp)
