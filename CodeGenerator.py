#!/usr/bin/env python
# coding=utf-8
import os

import time
import xlrd

import CodeTemplate

from LogTool import logger

from CamelTransformTool import CamelTransformTool

import TypeDict

from ExcelDesc import excel_desc

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class CodeGenerator(object):
    """
    代码生成工具
    """
    need_import_list = False

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
        else:
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
        else:
            logger.info("empty content")

    @staticmethod
    def gen_code(sheet):
        """
        实际处理逻辑, 抽取出来方便复用
        :param sheet: 包含sheet名称、sheet所拥有的数据
        """
        fp = open(CodeTemplate.java_template.get("default_file_path").get("output") + sheet.get("sheet_name"), "w+")
        CodeGenerator.gen_copyright(fp)
        CodeGenerator.gen_package_name(fp)
        CodeGenerator.gen_import(fp)
        CodeGenerator.gen_body(fp, sheet)
        fp.close()

    @staticmethod
    def run():
        """
        依次生成代码
        """
        protocol_data = CodeGenerator.init()
        for sheet in protocol_data:
            CodeGenerator.need_import_list = False
            CodeGenerator.gen_code(sheet)

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
                dto_num = 0
                sheet_origin_name = sheet_names[index].strip()
                # 从excel读到的sheet名称,为unicode格式, 需转换为utf-8编码
                sheet_origin_name = sheet_origin_name.encode('utf-8')
                sheet_name = excel_desc.get("sheets_name_dict").get(sheet_origin_name)
                if sheet_name is None:
                    index += 1
                    logger.warn("sheet_name=%s not in dict, no need to parse" % sheet_origin_name)
                    continue

                content = {
                    "sheet_name": sheet_name,
                    "dto_elems": [],
                }
                table = sheets[index]
                nrows = table.nrows

                # 加载excel描述规则
                row_format = excel_desc.get("sheets_row_format")
                if row_format is None:
                    logger.error("miss option sheets_row_format")
                    return

                min_field_num = row_format.get("field_min_num")
                if min_field_num is None:
                    logger.error("miss option field_min_num")
                    return

                field_pos = excel_desc.get("sheets_field_position")
                if field_pos is None:
                    logger.error("miss option sheets_field_position")
                    return

                pos_id = field_pos.get("field_id")
                pos_name = field_pos.get("field_name")
                pos_comment = field_pos.get("field_comment")
                pos_type = field_pos.get("field_type")

                if pos_id is None or pos_name is None or pos_type is None:
                    logger.error("miss field_id or field_name or field_type in sheets_field_position")
                    return

                # 公共的解析逻辑，基于excel描述规则
                for i in xrange(nrows):
                    data = table.row_values(i)
                    if len(data) < min_field_num:
                        logger.warn("sheet_name=%s row=%s miss some cols, you need at least %s cols" % (sheet_name, i, min_field_num))
                        continue

                    if data[pos_id] is None:
                        logger.warn("sheet_name=%s row=%s miss field_id" % (sheet_origin_name, i))
                        continue

                    # 兼容excel中序号为文本的情况, 将dto_field_id转为整型
                    if type(data[pos_id]) in (int, float) or str(data[pos_id]).strip().isdigit():
                        dto_field_id = int(data[pos_id])
                    else:
                        logger.warn("sheet_name=%s invalid field_id in row=%s" % (sheet_origin_name, i))
                        continue

                    dto_field_name = str("" if data[pos_name] is None else data[pos_name]).strip()
                    dto_field_type = str("" if data[pos_type] is None else data[pos_type]).strip()
                    pos = dto_field_type.find('(')
                    if pos > 0:
                        dto_field_type = dto_field_type[0:pos]
                    dto_field_comment = str("" if data[pos_comment] is None else data[pos_comment]).strip()

                    # 当读到字段id为1，且当前尚未生成过Dto时，需
                    # 1.更新sheet_name
                    # 2.dto计数加1
                    # 当读到字段id为1，且已生成过dto时，需
                    # 1.将已有的content内容加入protocol_data中
                    # 2.初始化content
                    if 1 == dto_field_id:
                        if 0 == dto_num:
                            content["sheet_name"] = sheet_name + "ReqDto"
                            dto_num += 1
                        else:
                            CodeGenerator.gen_code(content)
                            CodeGenerator.need_import_list = False
                            content["sheet_name"] = sheet_name + "RspDto"
                            content["dto_elems"] = []

                    # 是否包含list类型字段
                    if dto_field_type.lower() == "list":
                        CodeGenerator.need_import_list = True

                    if dto_field_name is None or dto_field_type is None:
                        logger.error("dto_field_name or dto_field_type miss, please check you protocol file")
                        continue

                    dto_elem = {
                        "name": dto_field_name,
                        "type": dto_field_type,
                        "comment": dto_field_comment,
                    }
                    content["dto_elems"].append(dto_elem)

                if dto_num > 0:
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
        if CodeGenerator.need_import_list:
            text = "import java.util.List;"
            CodeGenerator.writeline_with_endl(fp, text)

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
        """
        类开始
        :param fp:
        :param classname:
        """
        text = CodeTemplate.java_template.get("class_definition") % classname
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def class_define_end(fp):
        """
        类结束
        :param fp:
        """
        text = CodeTemplate.java_template.get("class_definition_end")
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def property_define(fp, type_name, field_name):
        """
        定义属性
        :param fp:
        :param type_name:
        :param field_name:
        """
        text = CodeTemplate.java_template.get("property_definition") % (type_name, field_name)
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def property_comment(fp, content=""):
        """
        定义注释
        :param content: 注释内容
        :param fp: 文件对象
        """
        if CodeTemplate.java_template.get("option_comment"):
            text = CodeTemplate.java_template.get("property_comment") % content
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def function_define_set(fp, type_name, field_name, field_name_cap):
        """
        定义set函数
        :param fp:
        :param type_name:
        :param field_name:
        :param field_name_cap:
        """
        text = CodeTemplate.java_template.get("function_definition_set") % (field_name_cap, type_name, field_name,
                                                                            field_name, field_name)
        CodeGenerator.writeline_with_endl(fp, text)

    @staticmethod
    def function_define_get(fp, type_name, field_name, field_name_cap):
        """
        定义get函数
        :param fp:
        :param type_name:
        :param field_name:
        :param field_name_cap:
        """
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
        """
        生成json property注解
        :param fp:
        :param func_type:
        :param field_name:
        """
        if CodeTemplate.java_template.get("option_json_property"):
            text = CodeTemplate.java_template.get("json_property") % field_name
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def json_deserialize(fp):
        """
        生成反序列化注解
        :param fp:
        """
        if CodeTemplate.java_template.get("option_json_serialize"):
            text = CodeTemplate.java_template.get("json_deserialize")
            CodeGenerator.writeline_with_endl(fp, text, 1)

    @staticmethod
    def json_serialize(fp):
        """
        生成序列化注解
        :param fp:
        """
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
            classname = sheet_name
            CodeGenerator.class_define_begin(fp, classname)

            for elem in dto_elems:
                elem_type = TypeDict.type_dict.get(elem.get("type").lower())
                elem_field_name = CamelTransformTool.trans_underline_field_to_camel_field(elem.get("name"))
                if elem_type is None or elem_field_name is None:
                    continue

                elem_property_comment = elem.get("comment")
                CodeGenerator.property_comment(fp, elem_property_comment)
                CodeGenerator.property_define(fp, elem_type, elem_field_name)

            for elem in dto_elems:
                elem_type = TypeDict.type_dict.get(elem.get("type").lower())
                elem_field_name = CamelTransformTool.trans_underline_field_to_camel_field(elem.get("name"))
                elem_field_name_cap = CamelTransformTool.trans_underline_field_to_camel_classname(elem.get("name"))
                if elem_type is None or elem_field_name is None:
                    continue

                CodeGenerator.function_comment(fp, elem_field_name, 'void')
                CodeGenerator.json_property(fp, 'set', elem_field_name)
                CodeGenerator.json_serialize(fp)
                CodeGenerator.function_define_set(fp, elem_type, elem_field_name, elem_field_name_cap)

                CodeGenerator.function_comment(fp, '', elem_type)
                # 反序列化需要使用原生的协议文件中的字段名
                CodeGenerator.json_property(fp, 'get', elem.get("name"))
                CodeGenerator.json_serialize(fp)
                CodeGenerator.function_define_get(fp, elem_type, elem_field_name, elem_field_name_cap)

            CodeGenerator.class_define_end(fp)

    # 以下接口提供给用户使用,
    # 通过代码覆盖配置文件, 而不是直接到配置文件中修改
    @staticmethod
    def set_package_name(package):
        """
        设置生成代码的完整包名
        :param package: 例如: com.webank.pmbank.ccs
        """
        CodeTemplate.java_template["package_name"] = "package " + package + ";"

    @staticmethod
    def set_protocol_file(pf):
        """
        设置协议文件
        :param file: 需包含完整路径名
        """
        CodeTemplate.java_template["protocol_file"] = pf

    @staticmethod
    def set_option_json_property(option):
        """
        是否生成json property注解
        :param option: true or false
        """
        CodeTemplate.java_template["option_json_property"] = option

    @staticmethod
    def set_option_json_serialize(option):
        """
        是否生成序列化注解
        :param option:
        """
        CodeTemplate.java_template["option_json_serialize"] = option

    @staticmethod
    def set_option_comment(option):
        """
        是否生成注释
        :param option:
        """
        CodeTemplate.java_template["option_comment"] = option

    @staticmethod
    def extend_import_module(modules):
        """
        添加需要导入的模块, 会追加到默认导入的模块列表中, 会去重
        :param modules: 列表
        """
        current_import_list = CodeTemplate.java_template.get("default_import_list")

        for module in modules:
            if module in current_import_list:
                modules.remove(module)

        current_import_list.extend(modules)

    @staticmethod
    def set_import_module(modules):
        """
        设置默认加载的模块列表
        例如:
        :param modules:
        :return:
        """
        CodeTemplate.java_template["default_import_list"] = modules

if __name__ == "__main__":
    logger.debug("gen start")
    package_name = raw_input("Please input java package name(like com.xxx.xxx):")
    CodeGenerator.set_package_name(package_name)

    CodeGenerator.set_option_comment(True)
    CodeGenerator.set_option_json_property(True)
    CodeGenerator.set_option_json_serialize(False)
    CodeGenerator.set_option_json_serialize(True)
    module_list = [
        #"com.webank.test",
    ]
    CodeGenerator.extend_import_module(module_list)
    CodeGenerator.set_protocol_file("D:\docs\protocol_v1.xls")

    start_time = time.clock()
    CodeGenerator.run()
    stop_time = time.clock()
    use_time = stop_time - start_time

    logger.debug("gen success. Time spend:%.4f(s)" % use_time)
    print "gen success. Time spend:%.4f(s)" % use_time