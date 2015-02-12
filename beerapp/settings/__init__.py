# -*- coding: utf-8 -*-
import os
from settings_common import *


ON_HEROKU = 'DATABASE_URL' in os.environ

if ON_HEROKU:
    from settings_prod import *
else:
    from settings_dev import *
