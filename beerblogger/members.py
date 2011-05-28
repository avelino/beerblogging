#coding: utf-8

import yaml
from util import Singleton

from . import app

from os import listdir

class Member(object):

    def __init__(self, name, email, blog, feed_url, group, post_meta,date_started, twitter=''):
        self.name = name
        self.email = email
        self.blog = blog
        self.feed_url = feed_url
        self.group = group
        self.post_meta = post_meta
        self.date_started = date_started
        self.twitter = twitter
        self.eemail = str(email)

class Members(Singleton):

    def __init__(self):
        if not hasattr(self, 'objects'):            
            self.objects = []
            self.dump_folder = app.config['DUMP_FOLDER']
            
            for group_file in listdir(self.dump_folder):
                print "Lendo arquivo: %s" % group_file                  
                stream = file(self.dump_folder+group_file, 'r')

                for m in yaml.load(stream):
                    mo = Member(m['name'], m['email'], m['blog'], m['feed_url'], m['group'], m['post_meta'], m['date_started'], m['twitter'])
                    self.objects.append(mo)
                    print mo.name +" " + mo.group
                
    def by_email(self, email):
        for m in self.objects:
            if m.email == email:
                return m
        return None
