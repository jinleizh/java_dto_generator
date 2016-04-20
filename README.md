# java_dto_generator
###目标:
  * 根据excel描述的协议字段, 生成java dto文件
###背景:
  * 解决项目组手写dto比较费时的问题，有效缩短花费时间. 
  * 协议字段评审过后，通过该工具自动生成dto, 提高开发效率
  * 目前评审采用的是excel文件
###使用说明:
  * 在当前目录新建ExcelConf.py文件, 格式如下
```
#!/usr/bin/env python
# coding=utf-8

service_mybusiness = {
    "service_name": "mybusiness",
    "protocol_file": "D:\docs\mybusiness.xls",
    "package_name": "com.test.mybusiness",

    # 维护sheet名与所对应的dto类名之间的映射
    "sheets_name_dict": {
        "sheet1":"mybusiness1",
        "sheet1":"mybusiness2",
    },

    # 字段在excel文件中的列位置, 从0开始计数, 例如第一列，即为0
    # field_id : 序号,  生成工具读到序号为1的字段时，将开始生成新的dto
    # field_name : 字段名, 生成工具会将其转换为驼峰格式
    # field_comment : 注释, 若希望关闭注释，请在CodeTemplate.py中修改或者通过set_option_comment修改
    # field_len : 字段长度
    # field_state : 字段状态-require option condition
    # field_detail : 字段补充说明
    "sheets_field_position": {
        "field_id": 0,
        "field_name": 1,
        "field_comment": 2,
        "field_type": 3,
        "field_state": 4,
        "field_detail": 5,
    },

    # 行数据格式要求, 生成工具会依据以下条件，检查数据是否符合要求, 不满足则过滤
    "sheets_row_format": {
        "field_min_num": 6,
    }
}

service = service_mybusiness

# excel描述信息，代码生成工具会解析此处的配置信息，用于生成Dto代码
excel_conf = dict(
        service_name=service.get("service_name"),
        protocol_file=service.get("protocol_file"),
        package_name=service.get("package_name"),
        sheets_name_dict=service.get("sheets_name_dict"),
        sheets_row_format=service.get("sheets_row_format"),
        sheets_field_position=service.get("sheets_field_position"),
)
```

