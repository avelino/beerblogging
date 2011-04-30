#coding: utf-8

from flask import Flask, g, render_template

from flaskext.gravatar import Gravatar
from flaskext.flatpages import FlatPages


app = Flask(__name__)
app.config.from_envvar('BEERBLOGGING_SETTINGS')

# export BEERBLOGGING_SETTINGS='/Users/victor/code/public/beerblogging/beerblogger/settings_dev.py'
# echo 'export BEERBLOGGING_SETTINGS=/deploy/beerblogging/beerblogger/settings_prod.py' >> /etc/apache2/envvars

gravatar = Gravatar(app, size=75, rating='x', default='retro', force_default=False, force_lower=False)

pages = FlatPages(app)


from models import *

from views import *

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

import feedparser
from time import mktime
from datetime import datetime    

