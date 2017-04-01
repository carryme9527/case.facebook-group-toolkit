# -*- coding: UTF-8 -*-

import settings
from time import sleep
from helpers import get_data
from flask import Flask, render_template, request, redirect
app = Flask(__name__, static_folder=settings.server_static)

access_token = ''

@app.route('/')
def set_token():
  title = settings.website_title
  header = settings.website_sidebar_menu[request.path]
  return render_template('set_token.html', title=title, header=header)

@app.route('/', methods=['POST'])
def get_token():
  global access_token
  access_token = request.form['token']
  with open('token', 'w') as fh:
    fh.write(access_token)
  return redirect('/comments')

@app.route('/comments')
def comments():
  title = settings.website_title
  header = settings.website_sidebar_menu[request.path]
  data = get_data(access_token)
  size = len(data)
  return render_template('index.html',
                          title=title,
                          header=header,
                          size=size,
                          data=data)

if __name__ == '__main__':
    with open(settings.data_token_filename) as fh:
      access_token = fh.read()

    app.run(
      host=settings.server_host,
      port=settings.server_post,
      debug=settings.server_debug)
