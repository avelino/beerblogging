#!/usr/bin/env python
#coding: utf-8

import sys
from beerblogger import *


TASKS = ['localserver', 'externalserver', 'update_entries', 'create_db']
USAGE_TEXT = u'\nUsage: \n./manager.py command_name (arguments)\n'

DATE_BET_STARTED = datetime(year=2011,month=3,day=21)

def help(*args):
    print USAGE_TEXT
        
    for task_name in TASKS:
        task_func = globals()[task_name]
        print '- %s: \t %s' % (task_name, task_func.__doc__)


def localserver(*args):
    'runs dev server on "localhost:5000"'
    app.run()


def externalserver(*args):
    'runs dev server that answers to request from other hosts'
    app.run(host='0.0.0.0')


def create_db(*args):
    'creates the database'
    database.connect()
    BlogEntry.create_table()


def update_entries(*args):
    'Updates database with new posts'
    
    database.connect()
    
    for member in Members().objects:
        feed = feedparser.parse(member.feed_url)
        member_entries_ids = [i.eid for i in BlogEntry.select().where(author_email=member.email)]

        for entry in feed['items']:
            if entry['id'] not in member_entries_ids:
                #if datetime.fromtimestamp(mktime(entry['updated_parsed'])) > DATE_BET_STARTED:
                if datetime.fromtimestamp(mktime(entry['updated_parsed'])).date() >= member.date_started:
                    new_entry = BlogEntry()
                    new_entry.title = entry['title']
                    new_entry.author_email = member.email                    
                    new_entry.betting_group = member.group
                    new_entry.summary = entry['summary']
                    #new_entry.content = entry['content']
                    new_entry.link = entry['link']
                    new_entry.eid = entry['id']
                    new_entry.updated = datetime.fromtimestamp(mktime(entry['updated_parsed']))
                    new_entry.date = datetime.fromtimestamp(mktime(entry['date_parsed']))
                    new_entry.save()
    
    database.close()
 
    
if __name__ == '__main__':
    'Calls the method with the given name with the other args (if any)'

    task_func = sys.argv[1]
    task_args = sys.argv[2:]

    task = globals()[task_func]
    task(task_args)
