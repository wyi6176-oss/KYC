# -*- coding: utf-8 -*-
"""KYC指标计算函数"""

import pandas as pd
import numpy as np

STEPS = ['register', 'doc_capture', 'ocr', 'liveness', 'review', 'approved', 'first_deposit']
STEP_NAMES = {
    'register': '注册', 'doc_capture': '证件拍摄', 'ocr': 'OCR识别',
    'liveness': '人脸检测', 'review': '审核提交', 'approved': '审核通过',
    'first_deposit': '首充',
}


def calc_completion_rate(df: pd.DataFrame) -> float:
    """计算整体完成率（从注册到审核通过）"""
    register_users = df[df['step'] == 'register']['user_id'].nunique()
    if register_users == 0:
        return 0.0
    approved_users = df[df['step'] == 'approved']['user_id'].nunique()
    return approved_users / register_users


def calc_avg_duration(df: pd.DataFrame, step: str = None) -> float:
    """计算平均耗时（秒）"""
    subset = df[df['status'] == 'success']
    if step:
        subset = subset[subset['step'] == step]
    if subset.empty:
        return 0.0
    return subset['duration_ms'].mean() / 1000


def calc_auto_review_rate(df: pd.DataFrame) -> float:
    """计算自动审核率"""
    review_df = df[df['step'].isin(['review', 'approved'])]
    if review_df.empty:
        return 0.0
    auto_count = review_df[review_df['review_type'] == 'auto'].shape[0]
    return auto_count / review_df.shape[0]


def calc_retry_rate(df: pd.DataFrame) -> float:
    """计算重拍率"""
    doc_df = df[df['step'] == 'doc_capture']
    if doc_df.empty:
        return 0.0
    retry_count = doc_df[doc_df['is_retry'] == True].shape[0]
    return retry_count / doc_df.shape[0]


def calc_fail_rate(df: pd.DataFrame, step: str = None) -> float:
    """计算失败率"""
    subset = df.copy()
    if step:
        subset = subset[subset['step'] == step]
    if subset.empty:
        return 0.0
    fail_count = subset[subset['status'] == 'fail'].shape[0]
    return fail_count / subset.shape[0]


def calc_percentiles(df: pd.DataFrame, step: str = None) -> pd.DataFrame:
    """计算P50/P75/P90/P95/P99耗时"""
    subset = df[df['status'] == 'success']
    if step:
        subset = subset[subset['step'] == step]
    if subset.empty:
        return pd.DataFrame()

    durations = subset['duration_ms'] / 1000  # 转换为秒
    percentiles = [50, 75, 90, 95, 99]
    values = [np.percentile(durations, p) for p in percentiles]
    return pd.DataFrame({
        '百分位': [f'P{p}' for p in percentiles],
        '耗时(秒)': [round(v, 2) for v in values],
    })


def get_daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    """获取每日趋势数据"""
    register_daily = df[df['step'] == 'register'].groupby('event_date').agg(
        kyc_count=('user_id', 'nunique')
    ).reset_index()

    approved_daily = df[df['step'] == 'approved'].groupby('event_date').agg(
        approved_count=('user_id', 'nunique')
    ).reset_index()

    trend = register_daily.merge(approved_daily, on='event_date', how='left')
    trend['approved_count'] = trend['approved_count'].fillna(0)
    trend['completion_rate'] = trend['approved_count'] / trend['kyc_count']
    trend['completion_rate'] = trend['completion_rate'].fillna(0)
    return trend


def get_country_top_n(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """获取KYC量Top N国家"""
    country_df = df[df['step'] == 'register'].groupby('country').agg(
        count=('user_id', 'nunique')
    ).reset_index()
    return country_df.sort_values('count', ascending=False).head(n)


def get_step_durations(df: pd.DataFrame) -> pd.DataFrame:
    """获取各步骤的耗时数据（用于箱线图）"""
    subset = df[df['status'] == 'success'].copy()
    subset['duration_s'] = subset['duration_ms'] / 1000
    subset['step_name'] = subset['step'].map(STEP_NAMES)
    return subset[['step', 'step_name', 'duration_s']]


def get_fail_trend(df: pd.DataFrame) -> pd.DataFrame:
    """获取失败率趋势"""
    daily = df.groupby(['event_date', 'status']).size().unstack(fill_value=0).reset_index()
    status_cols = [c for c in ['success', 'fail', 'timeout'] if c in daily.columns]
    total = daily[status_cols].sum(axis=1)
    daily['fail_rate'] = daily.get('fail', 0) / total
    return daily[['event_date', 'fail_rate']]


def get_compliance_metrics(df: pd.DataFrame) -> dict:
    """获取合规指标"""
    total = df.shape[0]
    return {
        'sanctions_hit_rate': df['sanctions_hit'].sum() / total if total > 0 else 0,
        'pep_hit_rate': df['pep_hit'].sum() / total if total > 0 else 0,
        'alert_counts': df[df['alert_level'].notna()]['alert_level'].value_counts().to_dict(),
        'sar_count': df[(df['alert_level'] == 'P0') & (df['sanctions_hit'] == True)].shape[0],
        'ctr_count': df[(df['alert_level'].isin(['P0', 'P1'])) & (df['pep_hit'] == True)].shape[0],
    }
