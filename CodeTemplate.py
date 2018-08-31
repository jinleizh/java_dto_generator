#!/usr/bin/env python
# coding=utf-8
import Constant

tpl_copy_right = """
/**
 *
 * This program is free software; you can redistribute it and/or modify it under the terms of the
 * GNU General Public License version 2 as published by the Free Software Foundation.
 *
 */"""

tpl_default_file_path = dict(
        input="./resource/",
        output_normal="./output/%s/normal/",  # 通用
        output_openapi="./output/%s/openapi/",  # 给openapi使用
        output_pmbank="./output/%s/pmbank/",  # 给pmbank使用
)

tpl_package_name = "package packageName;"

tpl_protocol_file = tpl_default_file_path.get("input") + "default.xls"

# 模版均可以修改, 但%s不能删除
tpl_class_definition = "public class %s extends BaseDTO {"
tpl_class_definition_end = "}"

tpl_property_definition = "    private %s %s;"

tpl_property_comment = """    /**
    * %s
    */"""

tpl_function_definition_set = """    public void set%s(%s %s) {
        this.%s = %s;
    }"""

tpl_function_definition_get = """    public %s get%s() {
        return %s;
    }"""

tpl_function_comment = """    /**
    *
    * @param %s %s
    */"""

tpl_json_property = "    @JsonProperty(\"%s\")"
tpl_json_serialize = "    @JsonSerialize(\"%s\")"

