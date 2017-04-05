# -*- coding: UTF-8 -*-

import os
import utils
import pickle
import settings
from helpers import get_data
from flask import Flask, render_template, request, redirect
app = Flask(__name__, static_folder=settings.server_static)

access_token = ''

@app.route('/')
def index():
  title = settings.website_title
  header = settings.website_sidebar_menu[request.path]
  return render_template('set_token.html', title=title, header=header)

@app.route('/', methods=['POST'])
def set_token():
  global access_token
  access_token = request.form['token']
  utils.set_token(access_token)
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

@app.route('/crontab')
def crontab():

  folder = 'history/comment/'
  fn = os.listdir(folder)[-1]
  filename = folder + fn
  title = settings.website_title
  header = settings.website_sidebar_menu[request.path] + '(%s)' % fn.split('.')[0]
  data = pickle.load(open(filename))
  size = len(data)
  return render_template('index.html',
                          title=title,
                          header=header,
                          size=size,
                          data=data)

if __name__ == '__main__':
    access_token = utils.get_token()

    app.run(
      host=settings.server_host,
      port=settings.server_post,
      debug=settings.server_debug)
