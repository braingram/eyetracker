#
#  EyetrackerUtilities.py
#  EyeTracker
#
#  Created by David Cox on 3/11/09.
#  Copyright (c) 2009 Harvard University. All rights reserved.
#

import os
import re

from ConfigParser import SafeConfigParser
from StringIO import StringIO

import loghelper

log = loghelper.make_logger('util')

default_config = '''
[simulation]

use_simulated=False
use_file_for_camera=False


[calibration]

calibration_path=~/.eyetracker/calibration


[mworks]

enable_mw_conduit=true
'''


def config_to_dict(cp, d={}):

    for section in cp.sections():
        log.debug('%s' % (cp.items(section), ))
        d.update(dict(cp.items(section)))

    # a bit hacky: covert from strings to values
    for (key, val) in d.items():
        if re.match(r'true', val, re.IGNORECASE):
            d[key] = True
        if re.match(r'false', val, re.IGNORECASE):
            d[key] = False
    #print('d: %s' % d)
    log.debug('d: %s' % d)
    return d


def load_default_config():
    cp = SafeConfigParser()
    sio = StringIO(default_config)
    cp.read(sio)
    return config_to_dict(cp)


def load_config_file(cfg_path):
    cp = SafeConfigParser()

    cp.read(os.path.expanduser(cfg_path))
    return config_to_dict(cp, load_default_config())
