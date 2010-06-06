#!/usr/bin/python

import os
import logging
from logging.handlers import TimedRotateFileHandler
import silpautils

conf_values = silpautils.loadConfiguration()
LOG_FOLDER = os.path.join(silpautils.getRootFolder(),conf_values.get("SILPA_LOG_FOLDER","logs"))
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
    logger = logging.getLogger("SILPA")
    logger.setLevel(LOG_LEVELS.get(conf_vaules.get("SILPA_LOG_LEVEL","debug"),logging.DEBUG))

    log_handler = TimedRotateFileHandler(LOG_FILE,"midnight",BACKUPS)

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    return logger
