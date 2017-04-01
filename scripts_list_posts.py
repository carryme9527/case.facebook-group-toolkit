import re
import json
import utils
import settings
import requests
import facebook_util

access_token = utils.get_token()

path = '/{0}/feed'.format(settings.facebook_group_id)
params = { 'limit': 100 }

last_until = None
while True:
    resp = facebook_util.request(path, access_token, params)
    until = re.search('until=([0-9]+)', resp['paging']['next']).groups()[0]
    for post in resp['data']:
        print post['id']
    if until == last_until:
        break
    params['until'] = last_until = until
