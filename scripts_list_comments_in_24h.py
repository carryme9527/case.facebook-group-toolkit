import re
import json
import utils
import settings
import requests
import facebook_util

access_token = utils.get_token()

results = []
for pid in open('post_ids'):
    pid = pid.strip()
    path = '/{0}'.format(pid)
    resp = facebook_util.get_comments_order_by_time(path, access_token)
    if 'comments' not in resp.keys():
        continue
    for comment in resp['comments']['data'][:2]:
        if utils.is_owner(comment):
            continue
        if not utils.is_in_24_hours(comment['created_time']):
            continue
        results.append((pid, comment['id'], comment['from']['id'], comment['created_time']))

for r in results:
    pid, cid, uid, ct = r
    print pid, cid, uid, ct
