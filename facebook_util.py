import requests
import json
from settings import facebook_domain, facebook_api_version

def api_url(query):
  return facebook_domain + facebook_api_version + query

def group_post_url(gid, pid):
    return '{0}/groups/{1}/permalink/{2}' \
        .format(facebook_domain, gid, pid)

def group_comment_url(gid, pid, cid):
    return '{0}/?comment_id={1}' \
        .format(group_post_url(gid, pid), cid)

def user_url(uid):
    return '{0}/{1}'.format(facebook_domain, uid)

def get_comments_order_by_time(query, access_token):
  url = api_url(query)
  params = {
    'fields': 'comments.order(reverse_chronological)',
    'access_token': access_token,
    'limit': 50,
  }
  resp = requests.get(url, params = params).text
  return json.loads(resp)
