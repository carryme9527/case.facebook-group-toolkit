import os
import utils
import pickle
import datetime
import facebook_util

access_token = utils.get_token()

folder = 'history/post/'
filename = folder + os.listdir(folder)[-1]

results = []
for pid in pickle.load(open(filename)):
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
        results.append((pid, resp['message'], comment['id'], comment['from']['id'], comment['created_time']))

pickle.dump(results, open('history/comment/%s.pkl' % datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 'w'))
