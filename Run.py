#!/bin/env/python
# coding=utf-8
"""
程序运行入口
"""
from LogTool import logger
from CodeGenerator import CodeGenerator
from ErrorUtil import ErrorUtil
import time
import Target
from ExcelConf import excel_conf

logger.debug("gen start")

# package_name = raw_input("Please input java package name(like com.xxx.xxx):")
CodeGenerator.set_package_name(excel_conf.get("package_name"))
CodeGenerator.set_protocol_file(excel_conf.get("protocol_file"))
CodeGenerator.set_service_name(excel_conf.get("service_name"))
CodeGenerator.set_option_comment(True)
CodeGenerator.set_option_json_serialize(False)
module_list = [
]
CodeGenerator.extend_import_module(module_list)

start_time = time.clock()
CodeGenerator.run(Target.Target_pmbank)
CodeGenerator.run(Target.Target_openapi)
CodeGenerator.run(Target.Target_normal)
stop_time = time.clock()
use_time = stop_time - start_time

print "gen success, statics="
logger.debug("#" * 60)
print ErrorUtil.display(4)
logger.debug("gen success. Time spend:%.4f(s)" % use_time)
logger.debug("#" * 60)
print "Time spend:%.4f(s)" % use_time
