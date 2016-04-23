#!/usr/bin/env python
# coding=utf-8

from LogTool import logger


class FileWriter(object):
    """
    写文件
    """
    @staticmethod
    def writeline_with_endl(fp, content, num=2):
        """
        带换行写内容
        :param num: 换行个数
        :param fp: 文件对象
        :param content: 要写入的内容
        """
        if content is not None:
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