# -*- coding: utf-8 -*-
"""
    beerblogging
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import datetime
import yaml
import feedparser
from helpers import to_datetime

DATE_BET_STARTED = datetime.datetime(year=2011,month=3,day=21)

class Member(object):
    def __init__(self, member_dic):
        self.id = member_dic['id']
        self.email = member_dic['email']
        self.name = member_dic['name']
        self.blog = member_dic['blog']
        self.feed = member_dic['feed']
        self.twitter = member_dic['twitter']
        self.date_joined = member_dic['date_joined']

    @property
    def posts(self):
        from posts import BlogPost
        return BlogPost.query.filter_by(author_email=self.email)

    @property
    def post_id_list(self):
        return [ post.id_post for post in self.posts ]
        
        
    def fetch_entries(self):
        from posts import BlogPost
        print "fetching entries for: %s" % self.name
        try:
            feed_posts = feedparser.parse(self.feed)['items']
            for p in feed_posts:
                if p['id'] not in self.post_id_list:
                    dt_published = to_datetime(p['updated_parsed'])
                    if dt_published > self.date_joined:
                        post = BlogPost(
                            email = self.email, title = p['title'],
                            link = p['link'], id_post = p['id'],
                            date_post = dt_published, date_updated = dt_published,
                            excerpt = p['summary'], content = p.get('summary', '') )
                        post.save()
        except:
            print 

class Members(object):
    def __init__(self, app):
        self.app = app
        members_str = open(app.config['MEMBERS_FILE']).read()
        self.all = map(Member, yaml.load_all(members_str) )
        
    def for_email(self, email):
        for m in self.all:
            if m.email.lower() == email.lower():
                return m
        return None
        
    def update_all_entries(self):
        for member in self.all:
            member.fetch_entries()            
