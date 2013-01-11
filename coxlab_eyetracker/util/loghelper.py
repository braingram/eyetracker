#
#  EyetrackerUtilities.py
#  EyeTracker
#
#  Created by David Cox on 3/11/09.
#  Copyright (c) 2009 Harvard University. All rights reserved.
#

import logging


def make_logger(name):
    l = logging.getLogger(name)
    if len(l) == 0:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(\
            '%(name)s:%(levelname)8s:%(asctime)s:%(filename)s:' \
            '%(lineno)d:%(funcName)s:%(message)s'))
        l.addHandler(h)
    return l

log = make_logger('util')
