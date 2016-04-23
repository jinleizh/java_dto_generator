#!/usr/bin/python env
# coding=utf-8


class CommonUtil(object):
    """
    公共函数库
    """
    @staticmethod
    def is_empty(val):
        """
        val判空
        :param val:
        :return:
        """
        if val is None or "" == val:
            return True
        return False

    @staticmethod
    def isFloat(val):
        """
        判断字面值是否为浮点数
        :param val:
        :return:
        """
        if round(float(val)) == float(val):
            return False

        return True

    @staticmethod
    def belong(srcList, destList):
        """
        判断两者是否有交集
        :param destList:
        :param srcList:
        :return:
        """
        for item in srcList:
            if item in destList:
                return True

        return False

if __name__ == "__main__":

    print CommonUtil.isFloat("123")
    print round(float("1.0"))
    print float("1.0")