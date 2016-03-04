#!/bin/env/python
# coding=utf-8
"""
程序运行入口
"""
from LogTool import logger
from CodeGenerator import CodeGenerator
import time
import Target

logger.debug("gen start")
# package_name = raw_input("Please input java package name(like com.xxx.xxx):")
package_name = "com.test"
CodeGenerator.set_package_name(package_name)

CodeGenerator.set_option_comment(True)
CodeGenerator.set_option_json_serialize(False)

module_list = [
]
CodeGenerator.extend_import_module(module_list)

CodeGenerator.set_protocol_file("D:\docs\wepower\wms_protocol_v0.xlsx")

start_time = time.clock()
CodeGenerator.run(Target.Target_pmbank)
CodeGenerator.run(Target.Target_openapi)
CodeGenerator.run(Target.Target_normal)
stop_time = time.clock()
use_time = stop_time - start_time

logger.debug("gen success. Time spend:%.4f(s)" % use_time)
print "gen success. Time spend:%.4f(s)" % use_time