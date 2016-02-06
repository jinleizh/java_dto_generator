#!/usr/bin/env python
# coding=utf-8
import os
import traceback

import xlrd

import CodeTemplate

from LogTool import logger

from CamelTransformTool import CamelTransformTool

import TypeDict


class CodeGenerator(object):
    """
    代码生成工具
    """

    def __init__(self):
        pass

    @staticmethod
    def writeline_with_endl(fp, content, num=2):
        """
        带换行写内容
        :param num: 换行个数
        :param fp: 文件对象
        :param content: 要写入的内容
        """
        if content is not None and num >= 1:
            fp.write(content + '\n' * num)

        logger.info("empty content")

    @staticmethod
    def writelines_with_endl(fp, contents, num=1):
        """
        带换行写多行内容
        :param fp: 文件对象
        :param contents: 要写入的多行内容，列表
        """
        if contents is not None:
            for line in contents:
                fp.write(line + '\n' * num)

        logger.info("empty content")

    @staticmethod
    def gen():
        """
        生成代码
        :param fp:
        """

        protocol_data = CodeGenerator.init()
        for sheet in protocol_data:
            fp = open(CodeTemplate.java_template.get("default_file_path").get("output") + sheet.get("sheet_name"), "w+")
            CodeGenerator.gen_copyright(fp)
            CodeGenerator.gen_package_name(fp)
            CodeGenerator.gen_import(fp)
            CodeGenerator.gen_body(fp, sheet)
            fp.close()

    @staticmethod
    def init():
        """
        解析excel文件，收集要处理的数据
        """
        protocol_file = CodeTemplate.java_template.get("protocol_file")
        if os.path.isfile(protocol_file):
            excel_data = xlrd.open_workbook(protocol_file)
            sheets = excel_data.sheets()
            sheet_names = excel_data.sheet_names()
            sheet_num = len(sheets)

            if 0 >= sheet_num:
                logger.warn("data not found in excel")
                return

            index = 0
            protocol_data = []
            while index < sheet_num:
                content = {
                    "sheet_name": "",
                    "dto_elems": [],
                }
                table = sheets[index]
                content["sheet_name"] = sheet_names[index]
                nrows = table.nrows

                # 第一行是标题列, 故应该至少有2行才符合要求
                if nrows <= 1:
                    index += 1
                    continue

                for i in xrange(nrows):
                    if 0 == i:
                        continue

                    # your logic here
                    data = table.row_values(i)
                    if len(data) < 2:
                        logger.error("table data format is valid, you need at least 2 cols")
                        continue

                    dto_field = str(data[0]).strip()
                    dto_type = str(data[1]).strip()
                    if dto_field is None or dto_type is None:
                        logger.error("dto_field or dto_type miss, please check you protocol file")
                        continue

                    dto_elem = {
                        "field": dto_field,
                        "type": dto_type,
                    }
                    content["dto_elems"].append(dto_elem)

                protocol_data.append(content)
                index += 1

            return protocol_data

    @staticmethod
    def gen_copyright(fp):
        """
        生成版权信息
        :param fp:
        """
        CodeGenerator.writeline_with_endl(fp, CodeTemplate.java_template.get("copy_right"))

    @staticmethod
    def gen_import(fp):
        """
        import模块
        :param fp:
        """
        for import_elem in CodeTemplate.java_template.get("default_import_list"):
            text = "import " + import_elem + ";"
            CodeGenerator.writeline_with_endl(fp, text)

        if CodeTemplate.java_template.get("option_json_property"):
            for module in CodeTemplate.import_json_property:
                text = "import " + module + ";"
                CodeGenerator.writeline_with_endl(fp, text)

        if CodeTemplate.java_template.get("option_json_serialize"):
            for module in CodeTemplate.import_json_serialize:
                text = "import " + module + ";"
                CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def gen_package_name(fp):
        """
        生成包名
        :param fp:
        """
        CodeGenerator.writeline_with_endl(fp, CodeTemplate.java_template.get("package_name"))

    @staticmethod
    def class_define_begin(fp, classname):
        text = CodeTemplate.java_template.get("class_definition") % classname
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def class_define_end(fp):
        text = CodeTemplate.java_template.get("class_definition_end")
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def property_define(fp, type_name, field_name):
        text = CodeTemplate.java_template.get("property_definition") % (type_name, field_name)
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def property_comment(fp):
        if CodeTemplate.java_template.get("option_comment"):
            text = CodeTemplate.java_template.get("property_comment")
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def function_define_set(fp, type_name, field_name, field_name_cap):

        text = CodeTemplate.java_template.get("function_definition_set") % (field_name_cap, type_name, field_name,
                                                                            field_name, field_name)
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def function_define_get(fp, type_name, field_name, field_name_cap):
        text = CodeTemplate.java_template.get("function_definition_get") % (type_name, field_name_cap, field_name)
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def function_comment(fp, param, return_type):
        """
        函数注释
        :param fp:
        """
        if CodeTemplate.java_template.get("option_comment"):
            text = CodeTemplate.java_template.get("function_comment") % (param)
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def json_property(fp, func_type, field_name):
        if CodeTemplate.java_template.get("option_json_property"):
            text = CodeTemplate.java_template.get("json_property") % field_name
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def json_deserialize(fp):
        if CodeTemplate.java_template.get("option_json_serialize"):
            text = CodeTemplate.java_template.get("json_deserialize")
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def json_serialize(fp):
        if CodeTemplate.java_template.get("option_json_serialize"):
            text = CodeTemplate.java_template.get("json_serialize")
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def gen_body(fp, sheet):
        """
        生成代码主体
        :param sheet:
        :param fp:
        """
        sheet_name = sheet.get("sheet_name")
        dto_elems = sheet.get("dto_elems")

        if dto_elems is not None and sheet_name is not None:
            classname = CamelTransformTool.trans_underline_field_to_camel_classname(sheet_name)
            CodeGenerator.class_define_begin(fp, classname)

            for elem in dto_elems:
                elem_type = TypeDict.type_dict.get(elem.get("type").lower())
                elem_field_name = CamelTransformTool.trans_underline_field_to_camel_field(elem.get("field"))
                if elem_type is None or elem_field_name is None:
                    continue

                CodeGenerator.property_comment(fp)
                CodeGenerator.property_define(fp, elem_type, elem_field_name)

            for elem in dto_elems:
                elem_type = TypeDict.type_dict.get(elem.get("type").lower())
                elem_field_name = CamelTransformTool.trans_underline_field_to_camel_field(elem.get("field"))
                elem_field_name_cap = CamelTransformTool.trans_underline_field_to_camel_classname(elem.get("field"))
                if elem_type is None or elem_field_name is None:
                    continue

                CodeGenerator.function_comment(fp, elem_field_name, 'void')
                CodeGenerator.json_property(fp, 'set', elem_field_name)
                CodeGenerator.json_serialize(fp)
                CodeGenerator.function_define_set(fp, elem_type, elem_field_name, elem_field_name_cap)

                CodeGenerator.function_comment(fp, '', elem_type)
                # get需要使用原生的协议文件中的字段名
                CodeGenerator.json_property(fp, 'get', elem.get("field"))
                CodeGenerator.json_serialize(fp)
                CodeGenerator.function_define_get(fp, elem_type, elem_field_name, elem_field_name_cap)

            CodeGenerator.class_define_end(fp)

    # 以下接口提供给用户使用,
    # 通过代码覆盖配置文件, 而不是直接到配置文件中修改
    @staticmethod
    def set_package_name(package):
        """
        设置生成代码的完整包名，例如: com.webank.pmbank.ccs
        :param package:
        """
        CodeTemplate.java_template["package_name"] = "package " + package + ";"

    @staticmethod
    def set_protocol_file(file):
        """
        设置协议文件
        :param file:
        """
        CodeTemplate.java_template["protocol_file"] = file

    @staticmethod
    def set_option_json_property(option):
        """
        是否开启json property
        :param option: true or false
        """
        CodeTemplate.java_template["option_json_property"] = option

    @staticmethod
    def set_option_json_serialize(option):
        """
        是否开启序列化
        :param option:
        """
        CodeTemplate.java_template["option_json_serialize"] = option

    @staticmethod
    def set_option_comment(option):
        """
        是否开启注释
        :param option:
        """
        CodeTemplate.java_template["option_comment"] = option

    @staticmethod
    def add_import_module(module_list):
        """
        添加需要导入的模块, 会追加到默认导入的模块列表中
        :param module_list: 列表
        """
        CodeTemplate.java_template.get("default_import_list").extend(module_list)

    @staticmethod
    def set_import_module(module_list):
        """
        设置默认加载的模块列表
        例如:
        :param module_list:
        :return:
        """
        CodeTemplate.java_template["default_import_list"] = module_list


if __name__ == "__main__":
    logger.debug("gen start")
    CodeGenerator.set_protocol_file("./resource/1.xls")
    CodeGenerator.set_package_name("haha")
    CodeGenerator.set_option_comment(True)
    CodeGenerator.set_option_json_property(True)
    CodeGenerator.set_option_json_serialize(False)
    module_list = [
        "com.test.test",
    ]
    CodeGenerator.add_import_module(module_list)
    CodeGenerator.gen()
    logger.debug("gen stop")
