#!/bin/env/python
# coding=utf-8
"""
程序运行入口
"""
from LogTool import logger
from CodeGenerator import CodeGenerator
import time
import Constant

logger.debug("gen start")
package_name = raw_input("Please input java package name(like com.xxx.xxx):")
CodeGenerator.set_package_name(package_name)

CodeGenerator.set_option_comment(True)
CodeGenerator.set_option_json_property(True)
CodeGenerator.set_option_json_serialize(False)
# CodeGenerator.set_json_property_style(Constant.json_property_style.get("above_property"))
# CodeGenerator.set_json_property_style(Constant.json_property_style.get("above_function_set_lower_case"))
CodeGenerator.set_json_property_style(Constant.json_property_style.get("above_function_set_upper_case"))

module_list = [
    #"com.webank.test",
]
CodeGenerator.extend_import_module(module_list)

CodeGenerator.set_protocol_file("D:\docs\protocol_v2_0217.xls")

start_time = time.clock()
CodeGenerator.run()
stop_time = time.clock()
use_time = stop_time - start_time

logger.debug("gen success. Time spend:%.4f(s)" % use_time)
print "gen success. Time spend:%.4f(s)" % use_time