#coding: utf-8

import yaml
from util import Singleton

from . import app

class Member(object):

    def __init__(self, name, email, blog, feed_url, twitter=''):
        self.name = name
        self.email = email
        self.blog = blog
        self.feed_url = feed_url
        self.twitter = twitter
        self.eemail = str(email)

class Members(Singleton):

    def __init__(self):
        if not hasattr(self, 'objects'):            
            self.objects = []
            self.dump_file = app.config['DUMP_FILE']
            stream = file(self.dump_file, 'r')

            for m in yaml.load(stream):
                mo = Member(m['name'], m['email'], m['blog'], m['feed_url'], m['twitter'])
                self.objects.append(mo)
                
    def by_email(self, email):
        for m in self.objects:
            if m.email == email:
                return m
        return None