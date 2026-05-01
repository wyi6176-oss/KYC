# -*- coding: utf-8 -*-
"""KYC数据分析工具包"""

from .metrics import (
    calc_completion_rate,
    calc_avg_duration,
    calc_auto_review_rate,
    calc_retry_rate,
    calc_fail_rate,
    calc_percentiles,
    get_daily_trend,
    get_country_top_n,
)
from .funnel import (
    build_funnel,
    build_funnel_by_dimension,
    get_funnel_conversion_rates,
)
from .charts import (
    create_metric_card,
    create_trend_chart,
    create_bar_chart,
    create_funnel_chart,
    create_pie_chart,
    create_box_chart,
    create_heatmap_chart,
    create_scatter_chart,
    create_multi_bar_chart,
    create_stacked_funnel_comparison,
    COLOR_THEME,
)

__all__ = [
    'calc_completion_rate', 'calc_avg_duration', 'calc_auto_review_rate',
    'calc_retry_rate', 'calc_fail_rate', 'calc_percentiles',
    'get_daily_trend', 'get_country_top_n',
    'build_funnel', 'build_funnel_by_dimension', 'get_funnel_conversion_rates',
    'create_metric_card', 'create_trend_chart', 'create_bar_chart',
    'create_funnel_chart', 'create_pie_chart', 'create_box_chart',
    'create_heatmap_chart', 'create_scatter_chart',
    'create_multi_bar_chart', 'create_stacked_funnel_comparison',
    'COLOR_THEME',
]
