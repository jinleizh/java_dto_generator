#!/usr/bin/env python
# coding=utf-8

"""
工具仅解析sheets_name_dict中所列出的sheet，生成对应的dto文件, 所以此处需要业务自己配置
未来可以开放成web服务提供给业务
"""
service_didi = {
    # 维护sheet名与所对应的dto类名之间的映射
    "sheets_name_dict": {
        "开户申请": "OpenAccount",
        "开户信息补充": "CompleteOpenAccountInfo",
        "密码设置": "SetPasswd",
        "修改密码": "ModifyPasswd",
        "重置密码": "ResetPasswd",
        "个人中心": "AccountCenter",
        "借款借据（试算）": "TrialBalance",
        "放款申请": "LoanApply",
        "客户向下还款计划": "UserRefundPlan",
        "客户向下所有借款记录": "UserLoanRecord",
        "客户向下所有还款记录": "UserRefundRecord",
        "单笔借据对应的还款计划": "ReceiptRefundPlan",
        "单笔借款详情": "ReceiptLoanDetail",
        "提前结清查询（含详情）": "EarlySettlementQuery",
        "提前结清申请": "EarlySettlementApply",
        "逾期查询": "QueryOverdue",
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

# 滴滴项目
service = service_didi

# excel描述信息，代码生成工具会解析此处的配置信息，用于生成Dto代码
excel_desc = dict(
        sheets_name_dict=service.get("sheets_name_dict"),
        sheets_row_format=service.get("sheets_row_format"),
        sheets_field_position=service.get("sheets_field_position"),
)
