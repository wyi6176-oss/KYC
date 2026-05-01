# -*- coding: utf-8 -*-
"""
KYC数据分析平台 - 主应用入口
Streamlit Web应用，包含10个分析Tab页
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.graph_objects as go

from scipy import stats

# 确保可以导入utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.metrics import (
    calc_completion_rate, calc_avg_duration, calc_auto_review_rate,
    calc_retry_rate, calc_fail_rate, calc_percentiles,
    get_daily_trend, get_country_top_n, get_fail_trend,
    get_compliance_metrics, get_step_durations, STEPS, STEP_NAMES,
)
from utils.funnel import build_funnel, build_funnel_by_dimension
from utils.charts import (
    create_trend_chart, create_bar_chart, create_funnel_chart,
    create_pie_chart, create_box_chart, create_heatmap_chart,
    create_scatter_chart, create_multi_bar_chart,
    create_stacked_funnel_comparison, COLOR_THEME,
)

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="KYC数据分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自定义CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #0891B2 0%, #06B6D4 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        font-size: 14px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 数据加载
# ============================================================
@st.cache_data
def load_sample_data():
    """加载示例数据"""
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'sample_data.csv')
    df = pd.read_csv(csv_path)
    df['event_date'] = pd.to_datetime(df['event_date'])
    return df


def apply_filters(df, date_range, countries, devices):
    """应用侧边栏筛选条件"""
    filtered = df.copy()
    if date_range:
        filtered = filtered[(filtered['event_date'] >= pd.Timestamp(date_range[0])) &
                            (filtered['event_date'] <= pd.Timestamp(date_range[1]))]
    if countries:
        filtered = filtered[filtered['country'].isin(countries)]
    if devices:
        filtered = filtered[filtered['device_type'].isin(devices)]
    return filtered


# ============================================================
# 侧边栏
# ============================================================
def render_sidebar(df):
    """渲染侧边栏筛选器"""
    st.sidebar.markdown("## 🔍 数据筛选")

    # 日期范围
    min_date = df['event_date'].min().date()
    max_date = df['event_date'].max().date()
    date_range = st.sidebar.date_input(
        "日期范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # 国家筛选
    all_countries = sorted(df['country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "国家",
        options=all_countries,
        default=[],
        placeholder="全部国家",
    )

    # 设备筛选
    all_devices = sorted(df['device_type'].unique().tolist())
    selected_devices = st.sidebar.multiselect(
        "设备类型",
        options=all_devices,
        default=[],
        placeholder="全部设备",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 数据信息")
    st.sidebar.info(f"原始数据: {len(df):,} 条记录")

    return date_range, selected_countries, selected_devices


# ============================================================
# Tab 1: 数据导入
# ============================================================
def tab_data_import():
    """数据导入页"""
    st.header("📁 数据导入")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 上传CSV文件")
        uploaded_file = st.file_uploader(
            "拖拽或点击上传CSV文件",
            type=['csv'],
            help="支持包含KYC事件数据的CSV文件",
        )

    with col2:
        st.markdown("#### 使用示例数据")
        if st.button("加载内置示例数据（10,000条）", type="primary", use_container_width=True):
            st.session_state['df'] = load_sample_data()
            st.success("示例数据加载成功！")
            st.rerun()

    # 如果有上传文件
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'event_date' in df.columns:
                df['event_date'] = pd.to_datetime(df['event_date'])
            st.session_state['df'] = df
            st.success(f"文件上传成功！共 {len(df):,} 条记录")
        except Exception as e:
            st.error(f"文件解析失败: {e}")

    # 显示已加载的数据信息
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.markdown("---")
        st.markdown("#### 数据基本信息")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("总行数", f"{len(df):,}")
        with col_b:
            if 'event_date' in df.columns:
                st.metric("时间范围", f"{df['event_date'].min().strftime('%Y-%m-%d')} ~ {df['event_date'].max().strftime('%Y-%m-%d')}")
            else:
                st.metric("时间范围", "无日期字段")
        with col_c:
            st.metric("字段数量", f"{len(df.columns)}")

        st.markdown("#### 字段列表")
        st.write(list(df.columns))

        st.markdown("#### 数据预览（前10行）")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("请上传CSV文件或加载示例数据以开始分析。")


# ============================================================
# Tab 2: 实时概览
# ============================================================
def tab_overview(df):
    """实时概览页"""
    st.header("📈 实时概览")

    # 核心指标卡片
    today_kyc = df[df['step'] == 'register']['user_id'].nunique()
    completion_rate = calc_completion_rate(df)
    avg_duration = calc_avg_duration(df)
    auto_rate = calc_auto_review_rate(df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("KYC发起量", f"{today_kyc:,}", help="筛选范围内的注册用户数")
    with col2:
        st.metric("完成率", f"{completion_rate:.1%}", help="注册→审核通过转化率")
    with col3:
        st.metric("平均耗时", f"{avg_duration:.1f}s", help="所有成功步骤的平均耗时")
    with col4:
        st.metric("自动审核率", f"{auto_rate:.1%}", help="自动审核占总审核的比例")

    st.markdown("---")

    # 7天趋势
    trend = get_daily_trend(df)
    # 取最近7天
    last_7 = trend.tail(7)
    fig_trend = create_trend_chart(
        last_7, y_col='kyc_count', y2_col='completion_rate',
        title='近7天KYC趋势',
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # 国家Top10
    st.markdown("---")
    col_left, col_right = st.columns(2)
    with col_left:
        country_top = get_country_top_n(df, 10)
        fig_bar = create_bar_chart(
            country_top, x_col='country', y_col='count',
            title='KYC量 Top10 国家',
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_right:
        # 设备分布
        device_dist = df[df['step'] == 'register'].groupby('device_type').agg(
            count=('user_id', 'nunique')
        ).reset_index()
        fig_device = create_pie_chart(
            device_dist, names_col='device_type', values_col='count',
            title='设备类型分布',
        )
        st.plotly_chart(fig_device, use_container_width=True)


# ============================================================
# Tab 3: 转化漏斗
# ============================================================
def tab_funnel(df):
    """转化漏斗页"""
    st.header("🔄 转化漏斗")

    # 维度选择
    col1, col2 = st.columns([1, 3])
    with col1:
        dimension = st.selectbox(
            "下钻维度",
            options=['无', 'country', 'device_type', 'doc_type'],
            format_func=lambda x: {'无': '整体漏斗', 'country': '按国家', 'device_type': '按设备类型', 'doc_type': '按证件类型'}[x],
        )

    if dimension == '无':
        # 整体漏斗
        funnel = build_funnel(df)
        fig = create_funnel_chart(funnel)
        st.plotly_chart(fig, use_container_width=True)

        # 漏斗数据表
        st.markdown("#### 漏斗数据明细")
        display_funnel = funnel.copy()
        display_funnel['conversion_rate'] = display_funnel['conversion_rate'].apply(lambda x: f"{x:.1%}")
        display_funnel['dropoff_rate'] = display_funnel['dropoff_rate'].apply(lambda x: f"{x:.1%}")
        display_funnel.columns = ['步骤', '步骤名称', '用户数', '转化率', '流失率']
        st.dataframe(display_funnel, use_container_width=True, hide_index=True)
    else:
        # 按维度下钻
        dim_label = {'country': '国家', 'device_type': '设备类型', 'doc_type': '证件类型'}[dimension]
        funnel_by_dim = build_funnel_by_dimension(df, dimension)

        # 如果维度值太多，限制显示
        dim_values = df[dimension].unique()
        if len(dim_values) > 8:
            # 按注册量取Top N
            top_vals = df[df['step'] == 'register'].groupby(dimension)['user_id'].nunique().nlargest(8).index.tolist()
            selected_vals = st.multiselect(
                f"选择{dim_label}（最多8个）",
                options=dim_values,
                default=top_vals,
            )
        else:
            selected_vals = dim_values

        filtered_funnel = funnel_by_dim[funnel_by_dim[dimension].isin(selected_vals)]
        fig = create_stacked_funnel_comparison(filtered_funnel, dimension)
        st.plotly_chart(fig, use_container_width=True)

        # 数据表
        st.markdown("#### 漏斗数据明细")
        display_df = filtered_funnel.copy()
        display_df['conversion_rate'] = display_df['conversion_rate'].apply(lambda x: f"{x:.1%}")
        display_df['dropoff_rate'] = display_df['dropoff_rate'].apply(lambda x: f"{x:.1%}")
        dim_name_map = {'country': '国家', 'device_type': '设备类型', 'doc_type': '证件类型'}
        display_df.columns = ['步骤', '步骤名称', '用户数', '转化率', '流失率', dim_name_map[dimension]]
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ============================================================
# Tab 4: 失败分析
# ============================================================
def tab_failure(df):
    """失败分析页"""
    st.header("⚠️ 失败分析")

    fail_df = df[df['status'] == 'fail'].copy()

    if fail_df.empty:
        st.info("没有失败记录。")
        return

    col1, col2 = st.columns(2)

    with col1:
        # 失败原因分布饼图
        fail_reasons = fail_df[fail_df['fail_reason'] != 'nil']['fail_reason'].value_counts().reset_index()
        fail_reasons.columns = ['fail_reason', 'count']
        if not fail_reasons.empty:
            fig_pie = create_pie_chart(
                fail_reasons, names_col='fail_reason', values_col='count',
                title='失败原因分布',
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # 失败原因Top10柱状图
        fig_bar = create_bar_chart(
            fail_reasons.head(10), x_col='fail_reason', y_col='count',
            title='失败原因 Top10',
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        # 按步骤拆分的失败分布
        fail_by_step = fail_df.groupby(['step', 'fail_reason']).size().reset_index(name='count')
        fail_by_step = fail_by_step[fail_by_step['fail_reason'] != 'nil']
        fail_by_step['step_name'] = fail_by_step['step'].map(STEP_NAMES)
        fig_step = create_multi_bar_chart(
            fail_by_step, x_col='step_name', y_col='count',
            group_col='fail_reason', title='按步骤拆分的失败分布',
        )
        st.plotly_chart(fig_step, use_container_width=True)

    with col4:
        # 失败率趋势（7天）
        fail_trend = get_fail_trend(df)
        fail_trend['event_date'] = pd.to_datetime(fail_trend['event_date'])
        last_7_fail = fail_trend.tail(7)
        fig_trend = create_trend_chart(
            last_7_fail, y_col='fail_rate',
            title='近7天失败率趋势',
        )
        # 修改Y轴为百分比
        fig_trend.update_layout(yaxis_tickformat='.1%')
        st.plotly_chart(fig_trend, use_container_width=True)


# ============================================================
# Tab 5: 耗时分析
# ============================================================
def tab_duration(df):
    """耗时分析页"""
    st.header("⏱️ 耗时分析")

    col1, col2 = st.columns(2)

    with col1:
        # 各步骤耗时箱线图
        step_durations = get_step_durations(df)
        if not step_durations.empty:
            fig_box = create_box_chart(
                step_durations, x_col='step_name', y_col='duration_s',
                title='各步骤耗时分布（箱线图）',
            )
            st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        # P50/P75/P90/P95/P99耗时表
        st.markdown("#### 各步骤耗时百分位")
        percentile_data = []
        for step in STEPS:
            p_df = calc_percentiles(df, step)
            if not p_df.empty:
                p_df['step'] = STEP_NAMES[step]
                percentile_data.append(p_df)

        if percentile_data:
            all_percentiles = pd.concat(percentile_data, ignore_index=True)
            # 转为宽表
            pivot_p = all_percentiles.pivot_table(
                index='step', columns='百分位', values='耗时(秒)'
            ).reset_index()
            pivot_p.columns = ['步骤'] + [f'P{p}' for p in [50, 75, 90, 95, 99]]
            numeric_cols = pivot_p.select_dtypes(include='number').columns
            st.dataframe(pivot_p.style.format({col: "{:.2f}" for col in numeric_cols}), use_container_width=True, hide_index=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        # 按设备类型的耗时对比
        device_duration = df[df['status'] == 'success'].copy()
        device_duration['duration_s'] = device_duration['duration_ms'] / 1000
        device_duration['step_name'] = device_duration['step'].map(STEP_NAMES)

        # 按设备和步骤计算平均耗时
        device_avg = device_duration.groupby(['device_type', 'step_name'])['duration_s'].mean().reset_index()
        fig_device = create_multi_bar_chart(
            device_avg, x_col='step_name', y_col='duration_s',
            group_col='device_type', title='按设备类型的平均耗时对比',
        )
        st.plotly_chart(fig_device, use_container_width=True)

    with col4:
        # 耗时趋势（7天）
        daily_duration = df[df['status'] == 'success'].groupby('event_date').agg(
            avg_duration=('duration_ms', 'mean')
        ).reset_index()
        daily_duration['avg_duration_s'] = daily_duration['avg_duration'] / 1000
        last_7_dur = daily_duration.tail(7)
        fig_dur_trend = create_trend_chart(
            last_7_dur, y_col='avg_duration_s',
            title='近7天平均耗时趋势',
        )
        fig_dur_trend.update_layout(yaxis_title='平均耗时(秒)')
        st.plotly_chart(fig_dur_trend, use_container_width=True)


# ============================================================
# Tab 6: 国家分析
# ============================================================
def tab_country(df):
    """国家分析页"""
    st.header("🌍 国家分析")

    all_countries = sorted(df['country'].unique().tolist())
    selected_country = st.selectbox("选择国家", options=all_countries)

    country_df = df[df['country'] == selected_country]

    # 核心指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kyc_count = country_df[country_df['step'] == 'register']['user_id'].nunique()
        st.metric("KYC发起量", f"{kyc_count:,}")
    with col2:
        cr = calc_completion_rate(country_df)
        st.metric("完成率", f"{cr:.1%}")
    with col3:
        avg_dur = calc_avg_duration(country_df)
        st.metric("平均耗时", f"{avg_dur:.1f}s")
    with col4:
        fr = calc_fail_rate(country_df)
        st.metric("失败率", f"{fr:.1%}")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        # 选中国家的漏斗分析
        funnel = build_funnel(country_df)
        fig_funnel = create_funnel_chart(funnel)
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_right:
        # 选中国家的失败原因分布
        fail_df = country_df[country_df['status'] == 'fail']
        fail_reasons = fail_df[fail_df['fail_reason'] != 'nil']['fail_reason'].value_counts().reset_index()
        fail_reasons.columns = ['fail_reason', 'count']
        if not fail_reasons.empty:
            fig_pie = create_pie_chart(
                fail_reasons, names_col='fail_reason', values_col='count',
                title=f'{selected_country} - 失败原因分布',
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info(f"{selected_country} 没有失败记录。")

    st.markdown("---")

    # 全球热力图（Top20国家KYC量）
    st.markdown("#### 全球KYC量分布（Top20国家）")
    country_top20 = get_country_top_n(df, 20)

    fig_heatmap = go.Figure()
    fig_heatmap.add_trace(go.Bar(
        x=country_top20['country'],
        y=country_top20['count'],
        marker=dict(
            color=country_top20['count'],
            colorscale='Blues',
            colorbar=dict(title='KYC量'),
        ),
        text=country_top20['count'],
        textposition='auto',
    ))
    fig_heatmap.update_layout(
        title='Top20国家KYC量',
        title_font_size=16,
        height=400,
        margin=dict(l=50, r=30, t=50, b=80),
        template='plotly_white',
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


# ============================================================
# Tab 7: 设备分析
# ============================================================
def tab_device(df):
    """设备分析页"""
    st.header("📱 设备分析")

    devices = sorted(df['device_type'].unique().tolist())

    # 各设备核心指标
    st.markdown("#### 核心指标对比")
    metrics_data = []
    for device in devices:
        device_df = df[df['device_type'] == device]
        metrics_data.append({
            '设备': device,
            'KYC量': device_df[device_df['step'] == 'register']['user_id'].nunique(),
            '完成率': f"{calc_completion_rate(device_df):.1%}",
            '平均耗时(s)': f"{calc_avg_duration(device_df):.1f}",
            '重拍率': f"{calc_retry_rate(device_df):.1%}",
            '失败率': f"{calc_fail_rate(device_df):.1%}",
            '自动审核率': f"{calc_auto_review_rate(device_df):.1%}",
        })

    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        # 各设备漏斗对比
        funnel_by_device = build_funnel_by_dimension(df, 'device_type')
        fig_funnel = create_stacked_funnel_comparison(funnel_by_device, 'device_type')
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col2:
        # 各设备失败原因对比
        fail_df = df[df['status'] == 'fail'].copy()
        fail_df = fail_df[fail_df['fail_reason'] != 'nil']
        fail_by_device = fail_df.groupby(['device_type', 'fail_reason']).size().reset_index(name='count')
        fig_fail = create_multi_bar_chart(
            fail_by_device, x_col='fail_reason', y_col='count',
            group_col='device_type', title='各设备失败原因对比',
        )
        st.plotly_chart(fig_fail, use_container_width=True)


# ============================================================
# Tab 8: 合规监控
# ============================================================
def tab_compliance(df):
    """合规监控页"""
    st.header("🛡️ 合规监控")

    compliance = get_compliance_metrics(df)

    # 核心指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("制裁命中率", f"{compliance['sanctions_hit_rate']:.2%}")
    with col2:
        st.metric("PEP命中率", f"{compliance['pep_hit_rate']:.2%}")
    with col3:
        st.metric("SAR报告数", compliance['sar_count'])
    with col4:
        st.metric("CTR报告数", compliance['ctr_count'])

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        # 制裁/PEP命中趋势
        daily_hits = df.groupby('event_date').agg(
            sanctions=('sanctions_hit', 'sum'),
            pep=('pep_hit', 'sum'),
        ).reset_index()
        daily_hits['event_date'] = pd.to_datetime(daily_hits['event_date'])

        fig_hits = go.Figure()
        fig_hits.add_trace(go.Scatter(
            x=daily_hits['event_date'], y=daily_hits['sanctions'],
            mode='lines+markers', name='制裁命中',
            line=dict(color=COLOR_THEME['danger'], width=2),
        ))
        fig_hits.add_trace(go.Scatter(
            x=daily_hits['event_date'], y=daily_hits['pep'],
            mode='lines+markers', name='PEP命中',
            line=dict(color=COLOR_THEME['warning'], width=2),
        ))
        fig_hits.update_layout(
            title='制裁/PEP命中趋势',
            title_font_size=16,
            height=400,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        )
        st.plotly_chart(fig_hits, use_container_width=True)

    with col_right:
        # 告警分布
        alert_df = df[df['alert_level'].notna()]
        if not alert_df.empty:
            alert_counts = alert_df['alert_level'].value_counts().reset_index()
            alert_counts.columns = ['alert_level', 'count']
            fig_alert = create_bar_chart(
                alert_counts, x_col='alert_level', y_col='count',
                title='告警分布（按等级）',
            )
            st.plotly_chart(fig_alert, use_container_width=True)
        else:
            st.info("没有告警记录。")

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        # 筛查通过率趋势
        daily_total = df.groupby('event_date').size().reset_index(name='total')
        daily_pass = df[~df['sanctions_hit'] & ~df['pep_hit']].groupby('event_date').size().reset_index(name='pass')
        daily_screen = daily_total.merge(daily_pass, on='event_date', how='left')
        daily_screen['pass'] = daily_screen['pass'].fillna(0)
        daily_screen['pass_rate'] = daily_screen['pass'] / daily_screen['total']
        daily_screen['event_date'] = pd.to_datetime(daily_screen['event_date'])

        fig_screen = create_trend_chart(
            daily_screen, y_col='pass_rate',
            title='筛查通过率趋势',
        )
        fig_screen.update_layout(yaxis_tickformat='.1%')
        st.plotly_chart(fig_screen, use_container_width=True)

    with col4:
        # SAR/CTR报告统计
        sar_ctr_data = {
            '报告类型': ['SAR（可疑交易报告）', 'CTR（大额交易报告）'],
            '数量': [compliance['sar_count'], compliance['ctr_count']],
        }
        sar_ctr_df = pd.DataFrame(sar_ctr_data)
        fig_sar = create_bar_chart(
            sar_ctr_df, x_col='报告类型', y_col='数量',
            title='SAR/CTR报告统计',
        )
        st.plotly_chart(fig_sar, use_container_width=True)


# ============================================================
# Tab 9: AB实验
# ============================================================
def tab_ab_test(df):
    """AB实验分析页"""
    st.header("🧪 AB实验分析")

    groups = sorted(df['experiment_group'].unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        group_a = st.selectbox("实验组A", options=groups, index=0)
    with col2:
        group_b = st.selectbox("实验组B", options=groups, index=min(1, len(groups) - 1))

    df_a = df[df['experiment_group'] == group_a]
    df_b = df[df['experiment_group'] == group_b]

    # 核心指标对比
    st.markdown("#### 核心指标对比")
    metrics_comparison = []
    for label, func in [
        ('完成率', calc_completion_rate),
        ('平均耗时(s)', calc_avg_duration),
        ('重拍率', calc_retry_rate),
        ('失败率', calc_fail_rate),
        ('自动审核率', calc_auto_review_rate),
    ]:
        val_a = func(df_a)
        val_b = func(df_b)
        diff = val_b - val_a
        metrics_comparison.append({
            '指标': label,
            f'{group_a}': f"{val_a:.2%}" if '率' in label else f"{val_a:.2f}",
            f'{group_b}': f"{val_b:.2%}" if '率' in label else f"{val_b:.2f}",
            '差异': f"{diff:+.2%}" if '率' in label else f"{diff:+.2f}",
        })

    st.dataframe(pd.DataFrame(metrics_comparison), use_container_width=True, hide_index=True)

    st.markdown("---")

    # 统计显著性检验
    st.markdown("#### 统计显著性检验")

    # 完成率卡方检验
    n_a = df_a[df_a['step'] == 'register']['user_id'].nunique()
    n_b = df_b[df_b['step'] == 'register']['user_id'].nunique()
    approved_a = df_a[df_a['step'] == 'approved']['user_id'].nunique()
    approved_b = df_b[df_b['step'] == 'approved']['user_id'].nunique()

    not_approved_a = n_a - approved_a
    not_approved_b = n_b - approved_b

    chi2, p_value_chi2, _, _ = stats.chi2_contingency(
        [[approved_a, not_approved_a], [approved_b, not_approved_b]]
    )

    # 耗时t检验
    duration_a = df_a[df_a['status'] == 'success']['duration_ms'].dropna()
    duration_b = df_b[df_b['status'] == 'success']['duration_ms'].dropna()

    if len(duration_a) > 1 and len(duration_b) > 1:
        t_stat, p_value_t = stats.ttest_ind(duration_a, duration_b, equal_var=False)
    else:
        t_stat, p_value_t = 0, 1.0

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**完成率卡方检验**")
        st.write(f"- 卡方统计量: {chi2:.4f}")
        st.write(f"- P值: {p_value_chi2:.4f}")
        if p_value_chi2 < 0.05:
            st.success("✅ 差异显著（p < 0.05）")
        else:
            st.warning("❌ 差异不显著（p >= 0.05）")

    with col_right:
        st.markdown("**耗时t检验（Welch's）**")
        st.write(f"- t统计量: {t_stat:.4f}")
        st.write(f"- P值: {p_value_t:.4f}")
        if p_value_t < 0.05:
            st.success("✅ 差异显著（p < 0.05）")
        else:
            st.warning("❌ 差异不显著（p >= 0.05）")

    st.markdown("---")

    # 按维度的细分对比
    st.markdown("#### 按维度的细分对比")
    dim_select = st.selectbox("选择细分维度", options=['device_type', 'doc_type', 'country'])

    dim_values = sorted(df[dim_select].unique().tolist())
    sub_metrics = []
    for dim_val in dim_values:
        sub_a = df_a[df_a[dim_select] == dim_val]
        sub_b = df_b[df_b[dim_select] == dim_val]
        sub_metrics.append({
            dim_select: dim_val,
            f'{group_a}_完成率': f"{calc_completion_rate(sub_a):.1%}",
            f'{group_b}_完成率': f"{calc_completion_rate(sub_b):.1%}",
            f'{group_a}_耗时': f"{calc_avg_duration(sub_a):.1f}s",
            f'{group_b}_耗时': f"{calc_avg_duration(sub_b):.1f}s",
        })

    st.dataframe(pd.DataFrame(sub_metrics), use_container_width=True, hide_index=True)


# ============================================================
# Tab 10: 自定义分析
# ============================================================
def tab_custom_analysis(df):
    """自定义分析页"""
    st.header("🎯 自定义分析")

    col1, col2, col3 = st.columns(3)

    with col1:
        dimension = st.selectbox(
            "选择维度",
            options=['country', 'device_type', 'doc_type', 'event_date'],
            format_func=lambda x: {
                'country': '国家', 'device_type': '设备类型',
                'doc_type': '证件类型', 'event_date': '时间段',
            }[x],
        )

    with col2:
        metric = st.selectbox(
            "选择指标",
            options=['completion_rate', 'avg_duration', 'retry_rate', 'fail_rate'],
            format_func=lambda x: {
                'completion_rate': '完成率', 'avg_duration': '平均耗时',
                'retry_rate': '重拍率', 'fail_rate': '失败率',
            }[x],
        )

    with col3:
        chart_type = st.selectbox(
            "选择图表类型",
            options=['line', 'bar', 'scatter', 'heatmap'],
            format_func=lambda x: {
                'line': '折线图', 'bar': '柱状图',
                'scatter': '散点图', 'heatmap': '热力图',
            }[x],
        )

    # 计算数据
    metric_func = {
        'completion_rate': calc_completion_rate,
        'avg_duration': calc_avg_duration,
        'retry_rate': calc_retry_rate,
        'fail_rate': calc_fail_rate,
    }
    metric_label = {
        'completion_rate': '完成率', 'avg_duration': '平均耗时',
        'retry_rate': '重拍率', 'fail_rate': '失败率',
    }

    dim_label_map = {
        'country': '国家', 'device_type': '设备类型',
        'doc_type': '证件类型', 'event_date': '时间段',
    }

    analysis_data = []
    for dim_val in sorted(df[dimension].unique().tolist()):
        subset = df[df[dimension] == dim_val]
        val = metric_func[metric](subset)
        analysis_data.append({
            'dimension': str(dim_val),
            'metric_value': val,
        })

    analysis_df = pd.DataFrame(analysis_data)

    if dimension == 'event_date':
        analysis_df['dimension'] = pd.to_datetime(analysis_df['dimension'])
        analysis_df = analysis_df.sort_values('dimension')

    # 生成图表
    if chart_type == 'line':
        fig = create_trend_chart(
            analysis_df, x_col='dimension', y_col='metric_value',
            title=f'{metric_label[metric]} - 按{dim_label_map[dimension]}',
        )
    elif chart_type == 'bar':
        fig = create_bar_chart(
            analysis_df, x_col='dimension', y_col='metric_value',
            title=f'{metric_label[metric]} - 按{dim_label_map[dimension]}',
        )
    elif chart_type == 'scatter':
        fig = create_scatter_chart(
            analysis_df, x_col='dimension', y_col='metric_value',
            title=f'{metric_label[metric]} - 按{dim_label_map[dimension]}',
        )
    elif chart_type == 'heatmap':
        # 热力图需要两个维度，这里使用维度x指标值的热力展示
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=analysis_df['dimension'],
            y=analysis_df['metric_value'],
            marker=dict(
                color=analysis_df['metric_value'],
                colorscale='Blues',
                colorbar=dict(title=metric_label[metric]),
            ),
            text=[f"{v:.2%}" if metric in ('completion_rate', 'retry_rate', 'fail_rate') else f"{v:.1f}" for v in analysis_df['metric_value']],
            textposition='auto',
        ))
        fig.update_layout(
            title=f'{metric_label[metric]} - 按{dim_label_map[dimension]}（热力色阶）',
            title_font_size=16,
            height=400,
            template='plotly_white',
            xaxis_tickangle=-45,
        )

    st.plotly_chart(fig, use_container_width=True)

    # 数据表
    st.markdown("#### 数据明细")
    display_df = analysis_df.copy()
    display_df.columns = [dim_label_map[dimension], metric_label[metric]]
    if metric in ('completion_rate', 'retry_rate', 'fail_rate'):
        display_df[metric_label[metric]] = display_df[metric_label[metric]].apply(lambda x: f"{x:.2%}")
    else:
        display_df[metric_label[metric]] = display_df[metric_label[metric]].apply(lambda x: f"{x:.2f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# ============================================================
# 主入口
# ============================================================
def main():
    st.title("📊 KYC数据分析平台")

    # 初始化数据
    if 'df' not in st.session_state:
        st.session_state['df'] = load_sample_data()

    df = st.session_state['df']

    # 侧边栏
    date_range, selected_countries, selected_devices = render_sidebar(df)

    # 应用筛选
    filtered_df = apply_filters(df, date_range, selected_countries, selected_devices)

    if filtered_df.empty:
        st.warning("筛选后没有数据，请调整筛选条件。")
        return

    # Tab页
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "📁 数据导入", "📈 实时概览", "🔄 转化漏斗", "⚠️ 失败分析",
        "⏱️ 耗时分析", "🌍 国家分析", "📱 设备分析", "🛡️ 合规监控",
        "🧪 AB实验", "🎯 自定义分析",
    ])

    with tab1:
        tab_data_import()
    with tab2:
        tab_overview(filtered_df)
    with tab3:
        tab_funnel(filtered_df)
    with tab4:
        tab_failure(filtered_df)
    with tab5:
        tab_duration(filtered_df)
    with tab6:
        tab_country(filtered_df)
    with tab7:
        tab_device(filtered_df)
    with tab8:
        tab_compliance(filtered_df)
    with tab9:
        tab_ab_test(filtered_df)
    with tab10:
        tab_custom_analysis(filtered_df)


if __name__ == '__main__':
    main()
