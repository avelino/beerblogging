#coding: utf-8

from flask import Flask, g, render_template

from flaskext.gravatar import Gravatar

app = Flask(__name__)
app.config.from_envvar('BEERBLOGGING_SETTINGS')
# export BEERBLOGGING_SETTINGS='/Users/victor/code/public/beerblogging/beerblogger/settings_dev.py'
# echo 'export BEERBLOGGING_SETTINGS=/deploy/beerblogging/beerblogger/settings_prod.py' >> /etc/apache2/envvars

gravatar = Gravatar(app, size=100, rating='x', default='retro', force_default=False, force_lower=False)

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

def refresh_entries():
    database.connect()
    for member in Members().objects:
        feed = feedparser.parse(member.feed_url)
        member_entries_ids = [i.eid for i in BlogEntry.select().where(author_email=member.email)]

        for entry in feed['items']:
            if entry['id'] not in member_entries_ids:
                new_entry = BlogEntry()
                new_entry.title = entry['title']
                new_entry.author_email = member.email
                new_entry.summary = entry['summary']
                #new_entry.content = entry['content']
                new_entry.link = entry['link']
                new_entry.eid = entry['id']
                new_entry.updated = datetime.fromtimestamp(mktime(entry['updated_parsed']))
                new_entry.date = datetime.fromtimestamp(mktime(entry['date_parsed']))
                new_entry.save()
    
    database.close()