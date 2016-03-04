#!/usr/bin/env python
# coding=utf-8

from LogTool import logger
import json

class ErrorUtil:
    """
    错误处理类
    """
    error_dict = {}

    def __init__(self):
        pass

    @staticmethod
    def addInvalidFieldId(target, sheet_name, field_name="unknown"):
        """
        统计字段id错误数
        :param target:
        :param field_name: 字段名
        :param sheet_name: excel sheet名
        """

        if ErrorUtil.error_dict.get(target) is None:
            ErrorUtil.error_dict[target] = {}

        if ErrorUtil.error_dict.get(target).get(sheet_name) is None:
            ErrorUtil.error_dict[target][sheet_name] = {}
            ErrorUtil.error_dict[target][sheet_name]["invalid_field_id_num"] = 0
            ErrorUtil.error_dict[target][sheet_name]["fields_with_invalid_id"] = []

        ErrorUtil.error_dict[target][sheet_name]["invalid_field_id_num"] += 1
        ErrorUtil.error_dict[target][sheet_name]["fields_with_invalid_id"].append(field_name)

    @staticmethod
    def addEmptyFieldName(target, sheet_name):
        """
        统计字段名错误数
        :param target:
        :param sheet_name:
        """
        if ErrorUtil.error_dict.get(target) is None:
            ErrorUtil.error_dict[target] = {}

        if ErrorUtil.error_dict.get(target).get(sheet_name) is None:
            ErrorUtil.error_dict[target][sheet_name] = {}
            ErrorUtil.error_dict[target][sheet_name]["empty_field_name_num"] = 0

        ErrorUtil.error_dict[target][sheet_name]["empty_field_name_num"] += 1

    @staticmethod
    def addInvalidFieldType(target, sheet_name, field_name):
        """
        统计缺少类型的字段
        :param field_name:
        :param target:
        :param sheet_name:
        """
        if ErrorUtil.error_dict.get(target) is None:
            ErrorUtil.error_dict[target] = {}

        if ErrorUtil.error_dict.get(target).get(sheet_name) is None:
            ErrorUtil.error_dict[target][sheet_name] = {}
            ErrorUtil.error_dict[target][sheet_name]["invalid_field_type_num"] = []

        ErrorUtil.error_dict[target][sheet_name]["invalid_field_type_num"].append(field_name)

    @staticmethod
    def display(num=1):
        """
        展示错误统计结果
        :param num: 对齐
        """
        result = json.dumps(ErrorUtil.error_dict, indent=num)
        logger.error(result)
        return result
