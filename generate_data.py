"""生成10000条模拟KYC事件数据"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

N = 10000

# 国家分布（模拟真实加密用户分布）
countries = {
    '美国': 0.20, '印度': 0.12, '尼日利亚': 0.08, '越南': 0.07,
    '巴西': 0.06, '土耳其': 0.05, '印度尼西亚': 0.05, '英国': 0.04,
    '德国': 0.03, '日本': 0.03, '韩国': 0.03, '加拿大': 0.03,
    '澳大利亚': 0.02, '泰国': 0.02, '菲律宾': 0.02, '阿根廷': 0.02,
    '墨西哥': 0.02, '俄罗斯': 0.02, '南非': 0.02, '阿联酋': 0.02,
    '新加坡': 0.01, '马来西亚': 0.01, '法国': 0.01, '哥伦比亚': 0.01,
}
country_list = list(countries.keys())
country_weights = np.array(list(countries.values()))
country_weights = country_weights / country_weights.sum()

# 设备类型分布
device_types = ['iOS', 'Android', 'Web']
device_weights = [0.35, 0.45, 0.20]

# 证件类型分布
doc_types = ['passport', 'id_card', 'drivers_license']
doc_weights = [0.40, 0.35, 0.25]

# 步骤定义
steps = ['register', 'doc_capture', 'ocr', 'liveness', 'review', 'approved', 'first_deposit']
step_names_cn = {
    'register': '注册', 'doc_capture': '证件拍摄', 'ocr': 'OCR识别',
    'liveness': '人脸检测', 'review': '审核提交', 'approved': '审核通过', 'first_deposit': '首充'
}

# 失败原因分布
fail_reasons = ['blur', 'occlusion', 'glare', 'mismatch', 'deepfake',
                'timeout', 'network_error', 'expired', 'nil']
fail_weights = [0.30, 0.20, 0.05, 0.15, 0.02, 0.15, 0.10, 0.02, 0.01]

# 实验组
experiment_groups = ['control', 'group_a', 'group_b']
exp_weights = [0.50, 0.25, 0.25]

# 生成日期
start_date = datetime(2025, 4, 1)
end_date = datetime(2025, 4, 30)
date_range = [start_date + timedelta(days=i) for i in range(30)]

# 日期权重（工作日多，周末少）
date_weights = []
for d in date_range:
    if d.weekday() < 5:
        date_weights.append(1.0)
    else:
        date_weights.append(0.6)

records = []
event_counter = 0
user_counter = 0

for _ in range(N):
    event_counter += 1
    user_counter += 1
    event_id = f"EVT-{event_counter:06d}"
    user_id = f"USR-{user_counter:06d}"

    # 选择日期
    event_date = np.random.choice(date_range, p=np.array(date_weights) / sum(date_weights))

    # 选择国家
    country = np.random.choice(country_list, p=country_weights)

    # 选择设备
    device_type = np.random.choice(device_types, p=device_weights)

    # 选择证件类型
    doc_type = np.random.choice(doc_types, p=doc_weights)

    # 选择实验组
    experiment_group = np.random.choice(experiment_groups, p=exp_weights)

    # 为每个用户生成漏斗步骤
    # 基础转化率
    conversion_rates = {
        'register': 1.0,
        'doc_capture': 0.85,
        'ocr': 0.80,
        'liveness': 0.75,
        'review': 0.72,
        'approved': 0.65,
        'first_deposit': 0.40,
    }

    # 设备调整
    device_adj = {'iOS': 1.03, 'Android': 1.0, 'Web': 0.95}
    # 证件调整
    doc_adj = {'passport': 1.05, 'id_card': 1.0, 'drivers_license': 0.93}

    adj = device_adj[device_type] * doc_adj[doc_type]

    # 生成每个步骤的事件
    completed_steps = []
    for step in steps:
        base_rate = conversion_rates[step]
        adjusted_rate = min(base_rate * adj, 0.99) if step != 'register' else 1.0

        if step == 'register':
            completed_steps.append(step)
            continue

        # 如果上一步没完成，这步也不会到达
        if completed_steps[-1] != steps[steps.index(step) - 1]:
            break

        if np.random.random() < adjusted_rate:
            completed_steps.append(step)
        else:
            # 记录失败步骤
            completed_steps.append(step + '_fail')
            break

    # 为每个完成的步骤生成事件记录
    for i, step_status in enumerate(completed_steps):
        if step_status.endswith('_fail'):
            step = step_status.replace('_fail', '')
            status = np.random.choice(['fail', 'timeout'], p=[0.8, 0.2])
        else:
            step = step_status
            status = 'success'

        # 耗时（毫秒）
        duration_map = {
            'register': (100, 3000),
            'doc_capture': (2000, 30000),
            'ocr': (1000, 15000),
            'liveness': (3000, 45000),
            'review': (5000, 120000),
            'approved': (100, 5000),
            'first_deposit': (1000, 60000),
        }
        low, high = duration_map[step]
        if device_type == 'Web':
            low = int(low * 0.8)
            high = int(high * 0.9)
        elif device_type == 'Android':
            low = int(low * 0.9)
            high = int(high * 1.1)
        duration_ms = int(np.random.lognormal(np.log((low + high) / 2), 0.5))
        duration_ms = max(low, min(high, duration_ms))

        if status == 'timeout':
            duration_ms = high

        # 失败原因
        if status == 'fail':
            # 按步骤调整失败原因
            if step == 'doc_capture':
                step_fail_reasons = ['blur', 'occlusion', 'glare', 'nil']
                step_fail_weights = [0.35, 0.25, 0.20, 0.20]
            elif step == 'ocr':
                step_fail_reasons = ['blur', 'occlusion', 'glare', 'mismatch', 'nil']
                step_fail_weights = [0.30, 0.20, 0.15, 0.25, 0.10]
            elif step == 'liveness':
                step_fail_reasons = ['mismatch', 'deepfake', 'timeout', 'network_error', 'nil']
                step_fail_weights = [0.30, 0.10, 0.25, 0.25, 0.10]
            elif step == 'review':
                step_fail_reasons = ['mismatch', 'expired', 'nil']
                step_fail_weights = [0.50, 0.30, 0.20]
            else:
                step_fail_reasons = fail_reasons
                step_fail_weights = fail_weights
            fail_reason = np.random.choice(step_fail_reasons, p=step_fail_weights)
        else:
            fail_reason = 'nil'

        # 审核类型
        if step in ('review', 'approved'):
            review_type = np.random.choice(['auto', 'manual'], p=[0.70, 0.30])
        else:
            review_type = 'auto'

        # 是否重拍
        is_retry = np.random.choice([True, False], p=[0.15, 0.85]) if step == 'doc_capture' and status == 'success' else False

        # 风险等级
        risk_level = np.random.choice(['low', 'medium', 'high'], p=[0.85, 0.12, 0.03])

        # 制裁命中
        sanctions_hit = np.random.random() < 0.005

        # PEP命中
        pep_hit = np.random.random() < 0.01

        # 告警等级
        if sanctions_hit or pep_hit:
            alert_level = np.random.choice(['P0', 'P1', 'P2'], p=[0.1, 0.3, 0.6])
        else:
            alert_level = None

        records.append({
            'event_id': event_id,
            'user_id': user_id,
            'event_date': event_date.strftime('%Y-%m-%d'),
            'country': country,
            'device_type': device_type,
            'doc_type': doc_type,
            'step': step,
            'status': status,
            'duration_ms': duration_ms,
            'fail_reason': fail_reason,
            'review_type': review_type,
            'is_retry': is_retry,
            'risk_level': risk_level,
            'sanctions_hit': sanctions_hit,
            'pep_hit': pep_hit,
            'alert_level': alert_level,
            'experiment_group': experiment_group,
        })

df = pd.DataFrame(records)
df.to_csv('/data/user/work/kyc_analysis/data/sample_data.csv', index=False, encoding='utf-8-sig')
print(f"生成 {len(df)} 条记录，覆盖 {df['user_id'].nunique()} 个用户")
print(f"日期范围: {df['event_date'].min()} ~ {df['event_date'].max()}")
print(f"步骤分布:\n{df['step'].value_counts()}")
print(f"\n状态分布:\n{df['status'].value_counts()}")
print(f"\n国家分布:\n{df['country'].value_counts()}")
