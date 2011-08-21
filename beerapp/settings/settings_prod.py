#coding: utf-8
from beerapp.helpers import AlchemyURI

DEBUG = True

MEMBERS_FILE = 'members.yaml'

DB_NAME = 'beerblogging'
DB_HOST = '173.230.129.203'
DB_USER = 'root'
DB_PWD = 'winspector$$'

SQLALCHEMY_DATABASE_URI = AlchemyURI(database=DB_NAME,user=DB_USER,pwd=DB_PWD,host=DB_HOST).mysql()