# -*- coding: utf-8 -*-
from os import environ

DEBUG = False

MEMBERS_FILE = 'members.yaml'

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
