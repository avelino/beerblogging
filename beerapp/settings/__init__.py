# -*- coding: utf-8 -*-
import os

ON_HEROKU = 'DATABASE_URL' in os.environ

from settings_common import *

if ON_HEROKU:
    from settings_prod import *
else:
    from settings_dev import *
