import re
import utils
import pickle
import datetime
import settings
import facebook_util

access_token = utils.get_token()

path = '/{0}/feed'.format(settings.facebook_group_id)
params = { 'limit': 100 }

results = []

last_until = None
while True:
    resp = facebook_util.request(path, access_token, params)
    until = re.search('until=([0-9]+)', resp['paging']['next']).groups()[0]
    for post in resp['data']:
        results.append(post['id'])
    if until == last_until:
        break
    params['until'] = last_until = until

pickle.dump(results, open('history/post/%s.pkl' % datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 'w'))
