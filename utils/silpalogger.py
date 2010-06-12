# -*- coding: utf-8 -*-
# Copyright 2009-2010 
#   Vasudev Kamath <kamathvasudev@gmail.com>
#   Santhosh Thottingal <santhosh.thottingal@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

'''WSGI logging and event reporting middleware.'''

import os
import logging
from logging.handlers import TimedRotatingFileHandler
import silpautils

__all__ = ['silpalogger']

conf_values = silpautils.load_configuration()
LOG_FOLDER = os.path.join(silpautils.get_root_folder(),conf_values.get("SILPA_LOG_FOLDER","logs"))
LOG_FILE = os.path.join(LOG_FOLDER,"silpa.log")
silpautils.ensure_dir(LOG_FOLDER)
BACKUPS = 10

LOG_LEVELS = {
    "info":logging.INFO,
    "debug":logging.DEBUG,
    "warning":logging.WARNING,
    "error":logging.ERROR,
    "critical":logging.CRITICAL,
    }

def get_logger():
    '''
       Funcion creates and configures new instance of logger
       for the SILPA and returns it
    '''
    global conf_values
    logger = logging.getLogger("SILPA")
    logger.setLevel(LOG_LEVELS.get(conf_values.get("SILPA_LOG_LEVEL","debug"),logging.DEBUG))

    log_handler = TimedRotatingFileHandler(LOG_FILE,"midnight",BACKUPS)

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    return logger

silpalogger = get_logger()