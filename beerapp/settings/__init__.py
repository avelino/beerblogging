# -*- coding: utf-8 -*-
"""
    beerblogging.settings
    ~~~~~~~~~~~~~~

    imports settings for the current runing enviroment
    uses an enviroment var and defaults to development enviroment

from settings_dev import *
"""    

import os

CURRENT_ENV = os.environ.get('ENV_BEERBLOGGING', 'DEV')

from settings_common import *

if CURRENT_ENV.upper() == 'PROD':
    from settings_prod import *
else:
    from settings_dev import *
