#!/usr/bin/env python
# coding=utf-8

# 将excel中标识的类型 映射成 java标准类型
# List类型 映射为 List<?>，业务需自行修改
type_dict = dict(
        integer="int",
        int="int",
        long="long",
        float="float",
        double="double",
        bool="boolean",
        char="char",
        string="String",
        h="String",
        list="List<?>",
        array="List<?>",
        n="int",
        c="String",
        b="BigDecimal",
        decimal="BigDecimal",
        bigdecimal="BigDecimal",
        t="Date",
        d="Date",
        date="Date",
)
