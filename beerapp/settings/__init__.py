# -*- coding: utf-8 -*-
"""
    beerblogging.settings
    ~~~~~~~~~~~~~~

    imports settings for the current runing enviroment
    uses an enviroment var and defaults to development enviroment

from settings_dev import *
"""    

import os

ON_HEROKU = os.environ.has_key('DATABASE_URL')

from settings_common import *

if ON_HEROKU:
    from settings_prod import *
else:
    from settings_dev import *
