# -*- coding: utf-8 -*-
"""KYC漏斗分析函数"""

import pandas as pd
import numpy as np

STEPS = ['register', 'doc_capture', 'ocr', 'liveness', 'review', 'approved', 'first_deposit']
STEP_NAMES = {
    'register': '注册', 'doc_capture': '证件拍摄', 'ocr': 'OCR识别',
    'liveness': '人脸检测', 'review': '审核提交', 'approved': '审核通过',
    'first_deposit': '首充',
}


def build_funnel(df: pd.DataFrame) -> pd.DataFrame:
    """构建漏斗数据

    返回每一步的用户数、转化率、流失率
    """
    funnel_data = []
    prev_count = None

    for step in STEPS:
        step_df = df[df['step'] == step]
        # 统计到达该步骤的唯一用户数
        count = step_df['user_id'].nunique()

        if prev_count is None:
            conversion_rate = 1.0
        else:
            conversion_rate = count / prev_count if prev_count > 0 else 0

        if prev_count is None:
            dropoff_rate = 0.0
        else:
            dropoff_rate = 1 - conversion_rate

        funnel_data.append({
            'step': step,
            'step_name': STEP_NAMES[step],
            'user_count': count,
            'conversion_rate': round(conversion_rate, 4),
            'dropoff_rate': round(dropoff_rate, 4),
        })
        prev_count = count

    return pd.DataFrame(funnel_data)


def build_funnel_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """按维度构建漏斗数据

    Args:
        df: 原始数据
        dimension: 维度字段名（country/device_type/doc_type）
    """
    results = []
    for dim_val in df[dimension].unique():
        subset = df[df[dimension] == dim_val]
        funnel = build_funnel(subset)
        funnel[dimension] = dim_val
        results.append(funnel)

    return pd.concat(results, ignore_index=True)


def get_funnel_conversion_rates(funnel_df: pd.DataFrame) -> dict:
    """从漏斗数据中提取各步骤转化率"""
    return dict(zip(funnel_df['step'], funnel_df['conversion_rate']))


def get_step_user_counts(df: pd.DataFrame) -> pd.DataFrame:
    """获取各步骤的用户数"""
    counts = []
    for step in STEPS:
        count = df[df['step'] == step]['user_id'].nunique()
        counts.append({
            'step': step,
            'step_name': STEP_NAMES[step],
            'user_count': count,
        })
    return pd.DataFrame(counts)
