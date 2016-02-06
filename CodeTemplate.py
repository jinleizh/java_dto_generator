#!/usr/bin/env python
# coding=utf-8

tpl_copy_right = """/**
 * (C) 2016 WeBank Group Holding Limited.
 *
 * This program is free software; you can redistribute it and/or modify it under the terms of the
 * GNU General Public License version 2 as published by the Free Software Foundation.
 *
 */"""

tpl_default_file_path = dict(
    input="./resource/",
    output="./output/",
)

tpl_package_name = "package com.webank.pmbank.ccs.dto;"

tpl_protocol_file = tpl_default_file_path.get("input") + "1.xls"

# 模版均可以修改, 但%s不能删除
tpl_class_definition = "public class %s extends PmbankBaseDTO {"
tpl_class_definition_end = "}"

tpl_property_definition = "    private %s %s;"

tpl_property_comment = """    /**
    *
    */"""

tpl_function_definition_set = """    public void set%s(%s %s) {
        this.%s = %s;
    }"""

tpl_function_definition_get = """    public %s get%s() {
        return %s;
    }"""

tpl_function_comment = """    /**
    *
    * @param %s
    */"""

tpl_json_property = "    @JsonProperty(\"%s\")"
tpl_json_serialize = "    @JsonSerialize(\"%s\")"
tpl_json_deserialize = "    @JsonDeserialize(\"%s\")"
tpl_option_json_property = False
tpl_option_json_serialize = False
tpl_option_comment = True
tpl_default_import_list = [
    "cn.webank.pmbank.framework.common.dto.PmbankBaseDTO",
]

import_json_property = [
    "com.fasterxml.jackson.annotation.JsonProperty",
]

import_json_serialize = [
    "com.fasterxml.jackson.databind.annotation.JsonSerialize",
]


java_template = dict(
        copy_right=tpl_copy_right,
        package_name=tpl_package_name,
        protocol_file=tpl_protocol_file,
        class_definition=tpl_class_definition,
        class_definition_end=tpl_class_definition_end,
        property_definition=tpl_property_definition,
        function_definition_set=tpl_function_definition_set,
        function_definition_get=tpl_function_definition_get,
        json_property=tpl_json_property,
        json_deserialize=tpl_json_deserialize,
        json_serialize=tpl_json_serialize,
        function_comment=tpl_function_comment,
        property_comment=tpl_property_comment,
        option_json_property=tpl_option_json_property,
        option_json_serialize=tpl_option_json_serialize,
        option_comment=tpl_option_comment,
        default_import_list=tpl_default_import_list,
        default_file_path=tpl_default_file_path,
)
