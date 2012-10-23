# -*- coding: utf-8 -*-
"""
    epio_tools
    ~~~~~~~~~~~~~~

    http://ep.io

    :copyright: (c) 2011 by Victor Fontes.
    :license: BSD, see BSD for more details.
"""
try:
    from bundle_config import config
except:
    raise Exception('Cant bundle_config')

class PostGresConfig(object):
    def __init__(self):
        self.host = config['postgres']['host'],
        self.port = int(config['postgres']['port']),
        self.user = config['postgres']['username'],
        self.password = config['postgres']['password'],
        self.database = config['postgres']['database'],

    @property
    def sqlalchemy_uri(self):
        #return 'postgresql://%s:%s@%s:%s/%s' % (self.user, self.password, self.host, self.port, self.database)
        return 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (self.user, self.password, self.host, self.port, self.database)
        
        
    def get_connection(self):
        import psycopg2
        return psycopg2.connect( host = self.host, 
            port = self.port, database= self.database,
            user = self.user, password = self.password,
        )