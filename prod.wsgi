#!/deploy/envs/env_beerblogging/bin/python

import sys
sys.path.append('/deploy/beerblogging/')
from beerblogger import app as application

