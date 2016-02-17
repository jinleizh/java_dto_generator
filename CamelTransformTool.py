#!/usr/bin/env python
# coding=utf-8
import re


class CamelTransformTool(object):
    """
    驼峰格式转换工具类

    """
    def __init__(self):
        pass

    @staticmethod
    def is_camel(field):
        """
        判断是否为驼峰写法
        :param field:
        """
        pass

    @staticmethod
    def trans_underline_field_to_camel_field(field):
        """
        将下划线写法转换为驼峰写法,步骤如下
        0.转换为标准的以单个下划线分割的字符串,
        1.单词转换为全小写
        2.第一个单词首字母不变, 从第二个单词开始，首字母需大写

        example:输入" OPEN ID "
        0.转换为"OPEN_ID"
        1.转换为"open_id"
        2.转换为"openId"

        :param field:
        """
        for symbol in ' _\t\n':
            field = field.strip(symbol)

        word_list = re.sub(r'\s+|_+', '_', field).lower().split('_')
        word_len = len(word_list)
        camel_field = ""
        for i in xrange(word_len):
            if 0 == i:
                camel_field += word_list[i]
                continue

            camel_field += word_list[i].capitalize()

        return camel_field

    @staticmethod
    def trans_underline_field_to_camel_classname(field):
        """
        类名输出为驼峰格式, 首字母需要大写
        :param field: 类名
        """
        field = CamelTransformTool.trans_underline_field_to_camel_field(field)
        field = field[0].upper() + field[1:]
        return field


"""
仅用于自测
"""
if __name__ == "__main__":
    print CamelTransformTool.trans_underline_field_to_camel_field("OPEN_ID_HELLO_WORLD")
    print CamelTransformTool.trans_underline_field_to_camel_classname("open_id_sheet")
