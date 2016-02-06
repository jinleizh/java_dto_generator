#!/usr/bin/env python
# coding=utf-8
import logging
import logging.handlers

logger = logging.getLogger("logger")
log_level = logging.DEBUG
logger.setLevel(log_level)
log_file = "./CodeGenereator.log"
log_handle = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1, 30)
log_handle.suffix = "%Y%m%d.log"
log_format = logging.Formatter('%(asctime)s|%(filename)s:%(lineno)d|%(funcName)s|%(levelname)s|%(message)s')
log_handle.setFormatter(log_format)
logger.addHandler(log_handle)