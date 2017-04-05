import os
import utils
import helpers
import pickle
import datetime
import facebook_util

access_token = utils.get_token()

folder = 'history/post/'
filename = folder + os.listdir(folder)[-1]

results = {}
for pid in pickle.load(open(filename)):
    pid = pid.strip()
    group_id, post_id = pid.split('_')
    post_url = facebook_util.group_post_url(group_id, post_id)

    path = '/{0}'.format(pid)
    resp = facebook_util.get_comments_order_by_time(path, access_token)
    if 'comments' not in resp.keys():
        continue

    returned = []
    for comment in resp['comments']['data'][:2]:
        if utils.is_owner(comment):
            continue
        if not utils.is_in_24_hours(comment['created_time']):
            continue

        from_name = comment['from']['name']
        user_url = facebook_util.user_url(comment['from']['id'])
        message = comment['message']
        comment_url = facebook_util.group_comment_url(group_id, post_id, comment['id'])

        time = utils.parse_time(comment['created_time'])
        returned.append((from_name, user_url, message, time, comment_url))

    if len(returned) > 0:
        results[(post_url, resp['message'], len(returned) + 1)] = returned

pickle.dump(results, open('history/comment/%s.pkl' % datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 'w'))
