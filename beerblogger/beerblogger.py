#coding: utf-8

from flask import Flask, g, render_template

import feedparser
import urllib2
from models import *
app = Flask(__name__)

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

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
    


@app.route('/')
def index():
    #url = urllib2.urlopen(BEERBLOGGERS[u'Victor Fontes']).geturl()

    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(0, 20)

    return render_template('index.html', sorted_entries=entries)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d/%m/%Y   [%H:%M]'):
    return value.strftime(format)