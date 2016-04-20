#!/usr/bin/env python
# coding=utf-8
import logging
import logging.handlers

# 程序执行日志
logger = logging.getLogger("logger")
log_level = logging.DEBUG
logger.setLevel(log_level)
log_file = "./CodeGenereator.log"
log_handle = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1, 30)
log_handle.suffix = "%Y%m%d.log"
log_format = logging.Formatter('%(asctime)s|%(filename)s:%(lineno)d|%(funcName)s|%(levelname)s|%(message)s')
log_handle.setFormatter(log_format)
logger.addHandler(log_handle)

"""
# 统计用的日志
report_logger = logging.getLogger("report_logger")
report_log_level = logging.DEBUG
report_logger.setLevel(report_log_level)
report_log_file = "./report.log"
report_log_handle = logging.handlers.TimedRotatingFileHandler(report_log_file, 'midnight', 1, 30)
report_log_handle.suffix = "%Y%m%d.log"
report_log_handle.setFormatter(log_format)
report_logger.addHandler(report_log_handle)
"""