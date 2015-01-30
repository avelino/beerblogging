# -*- coding: utf-8 -*-
"""
    beerblogging
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from functools import wraps
from flask import render_template

from datetime import datetime
from time import mktime


class SADialects(object):
    DIALECTS = {
        'SQLITE': 'sqlite://',
        'MYSQL': 'mysql://',
        'POSTGRE': 'postgresql://',
        'ORACLE': 'oracle://', }

    DRIVERS = {
        'SQLITE': ['__skip_driver_check__', ],
        'MYSQL': ['__skip_driver_check__', ],
        'ORACLE': ['__skip_driver_check__', ],
        'POSTGRE': ['psycopg2', ], }

    class __metaclass__(type):
        def __getattr__(cls, attr):
            dialects = object.__getattribute__(cls, 'DIALECTS')

            if attr.lower() in map(lambda x: x.lower(), dialects.keys()):
                dialect = dialects[attr.upper()] + "%s%s"
                return lambda *args: dialect % ('+', args[0]) if len(args) > 1 else dialect % ('', '')

            return object.__getattribute__(cls, attr)


class AlchemyURI(object):

    def __init__(self, database=None, user=None, pwd=None, host='localhost', port=''):
        self.db = database
        self.user = user
        self.pwd = pwd
        self._host = host
        self._port = port

    @property
    def host(self):
        port = ':' + self._port if bool(self._port) else ''
        return self._host + port

    def _conn_string(self):
        return '%s:%s@%s/%s' % (self.user, self.pwd, self.host, self.db)

    def sqlite_temp(self, driver=''):
        return SADialects.sqlite(driver) + '/tmp/test.db'

    def sqlite(self, path='', driver=''):
        return SADialects.sqlite(driver) + path + self.db

    def mysql(self, driver=''):
        return SADialects.mysql(driver) + self._conn_string()

    def postgre(self, driver=''):
        return SADialects.postgre(driver) + self._conn_string()

    def oracle(self, driver=''):
        return SADialects.oracle(driver) + self._conn_string()


def to_datetime(dt_str):
    "converts a timestamp string to datetime.datetime"
    entry_time = mktime(dt_str)
    return datetime.fromtimestamp(entry_time)


def br_month_filter(value):
    br_months = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro',
    }
    return br_months[value.month][:3]


def to_html(template):
    " render_template shortcut, views just need to return locals() "
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator
