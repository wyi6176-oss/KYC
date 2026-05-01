# -*- coding: utf-8 -*-
"""KYC图表生成函数（基于Plotly）"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 颜色主题
COLOR_THEME = {
    'primary': '#0891B2',
    'primary_light': '#22D3EE',
    'primary_dark': '#0E7490',
    'secondary': '#6366F1',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#3B82F6',
    'gray': '#6B7280',
    'bg': '#F8FAFC',
    'gradient': ['#0891B2', '#06B6D4', '#22D3EE', '#67E8F9', '#A5F3FC'],
}

STEP_NAMES = {
    'register': '注册', 'doc_capture': '证件拍摄', 'ocr': 'OCR识别',
    'liveness': '人脸检测', 'review': '审核提交', 'approved': '审核通过',
    'first_deposit': '首充',
}


def create_metric_card(label: str, value, delta: str = None, color: str = 'primary') -> go.Figure:
    """创建指标卡片（使用indicator）"""
    fig = go.Figure()

    color_map = {
        'primary': COLOR_THEME['primary'],
        'success': COLOR_THEME['success'],
        'warning': COLOR_THEME['warning'],
        'danger': COLOR_THEME['danger'],
    }
    c = color_map.get(color, COLOR_THEME['primary'])

    fig.add_trace(go.Indicator(
        mode='number+delta' if delta else 'number',
        value=value,
        title={'text': label, 'font': {'size': 14, 'color': '#374151'}},
        delta={'reference': 0, 'value': delta, 'relative': False} if delta else None,
        number={'font': {'size': 28, 'color': c}, 'valueformat': '.2f' if isinstance(value, float) else ',.0f'},
    ))

    fig.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_trend_chart(df: pd.DataFrame, date_col: str = 'event_date',
                       y_col: str = 'kyc_count', y2_col: str = None,
                       title: str = '') -> go.Figure:
    """创建双Y轴趋势折线图"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[y_col],
        mode='lines+markers',
        name='KYC发起量',
        line=dict(color=COLOR_THEME['primary'], width=2),
        marker=dict(size=6),
        yaxis='y',
    ))

    if y2_col and y2_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[date_col], y=df[y2_col] * 100,
            mode='lines+markers',
            name='完成率(%)',
            line=dict(color=COLOR_THEME['warning'], width=2, dash='dash'),
            marker=dict(size=6),
            yaxis='y2',
        ))
        fig.update_layout(
            yaxis2=dict(
                title=dict(text='完成率(%)', font=dict(color=COLOR_THEME['warning'])),
                overlaying='y',
                side='right',
                range=[0, 100],
                tickfont=dict(color=COLOR_THEME['warning']),
            )
        )

    fig.update_layout(
        title=title,
        title_font_size=16,
        height=400,
        margin=dict(l=50, r=50, t=50, b=30),
        xaxis_title='日期',
        yaxis_title=y_col,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    )
    return fig


def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str,
                     title: str = '', orientation: str = 'v',
                     color_col: str = None) -> go.Figure:
    """创建柱状图"""
    if orientation == 'h':
        fig = px.bar(
            df, x=y_col, y=x_col, orientation='h',
            color=color_col if color_col else None,
            color_discrete_sequence=[COLOR_THEME['primary']],
        )
    else:
        fig = px.bar(
            df, x=x_col, y=y_col,
            color=color_col if color_col else None,
            color_discrete_sequence=[COLOR_THEME['primary']],
        )

    fig.update_layout(
        title=title,
        title_font_size=16,
        height=400,
        margin=dict(l=50, r=30, t=50, b=30),
        template='plotly_white',
    )
    return fig


def create_funnel_chart(funnel_df: pd.DataFrame) -> go.Figure:
    """创建漏斗图"""
    fig = go.Figure()

    colors = ['#0891B2', '#06B6D4', '#22D3EE', '#67E8F9', '#A5F3FC', '#CFFAFE', '#ECFEFF']

    fig.add_trace(go.Funnel(
        y=funnel_df['step_name'].tolist(),
        x=funnel_df['user_count'].tolist(),
        textinfo='value+percent initial+percent previous',
        textposition='inside',
        marker=dict(color=colors[:len(funnel_df)]),
        opacity=0.9,
    ))

    fig.update_layout(
        title='KYC转化漏斗',
        title_font_size=16,
        height=500,
        margin=dict(l=50, r=50, t=50, b=30),
        template='plotly_white',
    )
    return fig


def create_pie_chart(df: pd.DataFrame, names_col: str, values_col: str,
                     title: str = '') -> go.Figure:
    """创建饼图"""
    fig = px.pie(
        df, names=names_col, values=values_col,
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        title=title,
        title_font_size=16,
        height=400,
        margin=dict(l=30, r=30, t=50, b=30),
        template='plotly_white',
    )
    return fig


def create_box_chart(df: pd.DataFrame, x_col: str, y_col: str,
                     title: str = '', color_col: str = None) -> go.Figure:
    """创建箱线图"""
    fig = px.box(
        df, x=x_col, y=y_col,
        color=color_col if color_col else None,
        color_discrete_sequence=[COLOR_THEME['primary'], COLOR_THEME['secondary'], COLOR_THEME['warning']],
    )
    fig.update_layout(
        title=title,
        title_font_size=16,
        height=450,
        margin=dict(l=50, r=30, t=50, b=80),
        xaxis_title='',
        yaxis_title='耗时(秒)',
        template='plotly_white',
        xaxis_tickangle=-15,
    )
    return fig


def create_heatmap_chart(df: pd.DataFrame, x_col: str, y_col: str,
                         z_col: str, title: str = '') -> go.Figure:
    """创建热力图"""
    fig = px.imshow(
        df.pivot_table(index=y_col, columns=x_col, values=z_col, fill_value=0),
        color_continuous_scale='Blues',
        aspect='auto',
    )
    fig.update_layout(
        title=title,
        title_font_size=16,
        height=400,
        margin=dict(l=80, r=30, t=50, b=80),
        template='plotly_white',
    )
    return fig


def create_scatter_chart(df: pd.DataFrame, x_col: str, y_col: str,
                         title: str = '', color_col: str = None,
                         size_col: str = None) -> go.Figure:
    """创建散点图"""
    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=color_col if color_col else None,
        size=size_col if size_col else None,
        color_discrete_sequence=[COLOR_THEME['primary'], COLOR_THEME['secondary'], COLOR_THEME['warning']],
    )
    fig.update_layout(
        title=title,
        title_font_size=16,
        height=400,
        margin=dict(l=50, r=30, t=50, b=30),
        template='plotly_white',
    )
    return fig


def create_multi_bar_chart(df: pd.DataFrame, x_col: str, y_col: str,
                           group_col: str, title: str = '',
                           barmode: str = 'group') -> go.Figure:
    """创建分组柱状图"""
    fig = px.bar(
        df, x=x_col, y=y_col, color=group_col,
        barmode=barmode,
        color_discrete_sequence=[COLOR_THEME['primary'], COLOR_THEME['secondary'], COLOR_THEME['warning']],
    )
    fig.update_layout(
        title=title,
        title_font_size=16,
        height=400,
        margin=dict(l=50, r=30, t=50, b=80),
        template='plotly_white',
        xaxis_tickangle=-15,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    )
    return fig


def create_stacked_funnel_comparison(funnel_df: pd.DataFrame, dimension_col: str) -> go.Figure:
    """创建多维度漏斗对比图"""
    fig = go.Figure()
    colors = [COLOR_THEME['primary'], COLOR_THEME['secondary'], COLOR_THEME['warning'],
              COLOR_THEME['success'], COLOR_THEME['danger'], COLOR_THEME['info']]

    for i, dim_val in enumerate(funnel_df[dimension_col].unique()):
        subset = funnel_df[funnel_df[dimension_col] == dim_val]
        fig.add_trace(go.Funnel(
            name=str(dim_val),
            y=subset['step_name'].tolist(),
            x=subset['user_count'].tolist(),
            textinfo='value+percent previous',
            marker=dict(color=colors[i % len(colors)]),
        ))

    fig.update_layout(
        title=f'漏斗对比（按{dimension_col}）',
        title_font_size=16,
        height=500,
        margin=dict(l=50, r=50, t=50, b=30),
        template='plotly_white',
    )
    return fig
