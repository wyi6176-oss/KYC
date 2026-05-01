# KYC 埋点数据分析产品文档

> **版本**：v1.0
> **文档类型**：产品设计文档（PRD）
> **编写日期**：2026-04-29
> **文档负责人**：数据产品经理
> **保密级别**：内部 - 机密

---

## 目录

- [1. 产品概述](#1-产品概述)
- [2. 数据采集体系](#2-数据采集体系)
- [3. 大数据技术架构](#3-大数据技术架构)
- [4. AI 与机器学习应用](#4-ai-与机器学习应用)
  - [4.6 制裁命中风险评估模型](#46-制裁命中风险评估模型)
  - [4.7 交易行为异常检测模型增强](#47-交易行为异常检测模型增强)
  - [4.8 ZK 服务使用预测模型](#48-zk-服务使用预测模型)
- [5. 数据看板与可视化](#5-数据看板与可视化)
  - [5.6 合规监控看板](#56-合规监控看板)
  - [5.7 ZK 服务运营看板](#57-zk-服务运营看板)
- [6. 自动化运营闭环](#6-自动化运营闭环)
- [7. 数据安全与隐私](#7-数据安全与隐私)
- [8. 实施路线图](#8-实施路线图)
- [9. 成本估算](#9-成本估算)
- [附录 A：术语表](#附录-a术语表)
- [附录 B：埋点事件完整清单](#附录-b埋点事件完整清单)

---

## 1. 产品概述

### 1.1 产品定位

**KYC 全链路数据分析平台（KYC Analytics Platform，简称 KAP）** 是一个面向 Web3 企业的数据驱动型分析产品，专注于对 Know Your Customer（KYC）认证全流程进行深度数据采集、智能分析与闭环优化。平台通过先进的埋点体系、实时大数据管道和 AI/ML 模型，实现对 KYC 转化漏斗的精细化运营，帮助企业将 KYC 完成率从行业平均 60-70% 提升至 85% 以上，平均完成时间从 8-15 分钟缩短至 3 分钟以内。

### 1.2 目标用户

| 用户角色 | 核心诉求 | 使用场景 |
|---------|---------|---------|
| **产品经理** | 了解 KYC 各步骤转化率，定位流失瓶颈，优化产品体验 | 查看转化漏斗、流失归因分析、A/B 测试结果 |
| **运营人员** | 监控实时认证量，处理异常情况，执行运营策略 | 实时监控看板、告警处理、分群运营 |
| **风控团队** | 识别欺诈行为，监控审核质量，降低合规风险 | 欺诈检测看板、异常事件流、审核质量报告 |
| **技术负责人** | 监控系统稳定性，定位技术故障，评估性能瓶颈 | 系统健康看板、API 性能监控、错误追踪 |

### 1.3 核心价值

1. **数据驱动决策**：将 KYC 优化从经验驱动升级为数据驱动，用量化指标指导每一次产品迭代
2. **实时感知异常**：毫秒级异常检测能力，确保 KYC 服务可用性和用户体验
3. **AI 智能洞察**：通过机器学习模型预测流失、检测欺诈、自动归因，释放人力
4. **闭环优化能力**：从数据采集 → 分析洞察 → 自动化 Action 形成完整闭环
5. **合规与安全**：内置 GDPR/CCPA 合规能力，确保数据处理合法合规

### 1.4 业务背景与目标

#### 1.4.1 KYC 流程步骤

```
选择证件类型 → 拍摄证件正面 → 拍摄证件反面 → 人脸活体检测 → 提交审核 → 等待结果
     Step 1         Step 2          Step 3          Step 4         Step 5       Step 6
```

#### 1.4.2 关键业务指标（KPI）

| 指标 | 当前行业基准 | 目标值 | 提升幅度 |
|-----|------------|-------|---------|
| KYC 完成率 | 60-70% | 85%+ | +15-25pp |
| 平均完成时间 | 8-15 分钟 | < 3 分钟 | -60%+ |
| 重拍率 | 2.5 次/人 | 1.2 次/人 | -52% |
| 自动审核通过率 | 50-60% | 90%+ | +30pp |
| 月均新增注册用户 | 50 万 | 50 万（基准） | — |
| 人工审核占比 | 40-50% | < 10% | -75% |

---

## 2. 数据采集体系

### 2.1 埋点架构设计

#### 2.1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        数据采集层                                │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  前端 SDK     │  │  后端 Agent  │  │  第三方数据源          │  │
│  │  (Web/iOS/   │  │  (服务端埋点) │  │  (审核系统/客服/      │  │
│  │   Android)   │  │              │  │   App Store)          │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │              │
│         ▼                 ▼                      ▼              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              数据采集网关 (API Gateway)                    │  │
│  │  - 协议转换  - 数据校验  - 限流熔断  - 设备指纹采集        │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Kafka 消息队列 (实时管道)                     │  │
│  │  - 事件缓冲  - 分区有序  - 多副本  - Retention 策略        │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        数据处理层                                │
│                                                                 │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  实时处理 (Flink)     │    │  离线处理 (Spark + Hive)      │  │
│  │  - 实时聚合           │    │  - T+1 批处理                 │  │
│  │  - 异常检测           │    │  - 历史趋势分析               │  │
│  │  - 实时看板数据       │    │  - 模型训练数据准备            │  │
│  └──────────┬───────────┘    └──────────────┬───────────────┘  │
│             │                               │                  │
│             ▼                               ▼                  │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  ClickHouse (OLAP)   │    │  Delta Lake (数据湖)          │  │
│  │  - 实时查询           │    │  - 原始数据存储               │  │
│  │  - 低延迟聚合         │    │  - 数据血缘管理               │  │
│  └──────────────────────┘    └──────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.1.2 前端 SDK 设计

前端 SDK 是埋点数据采集的核心组件，需要覆盖 Web、iOS、Android 三端。

**SDK 核心能力**：

| 能力 | 说明 |
|-----|------|
| 自动采集 | 页面浏览（PV/UV）、页面停留时长、异常错误自动捕获 |
| 手动埋点 | 业务自定义事件（拍照、提交、重拍等） |
| 设备指纹 | 采集设备唯一标识（Device ID），支持跨会话追踪 |
| 离线缓存 | 网络不可用时本地缓存，恢复后自动上报 |
| 数据压缩 | 事件批量压缩上报，减少网络开销 |
| 采样控制 | 支持按百分比采样，控制数据量 |
| 生命周期管理 | App 前后台切换事件、会话管理 |

**SDK 集成规范**：

```javascript
// Web 端 SDK 初始化示例
import { KYCAnalytics } from '@company/kyc-analytics-sdk';

const analytics = new KYCAnalytics({
  appId: 'kyc_web_app',
  serverUrl: 'https://collect.company.com/v2/event',
  maxBatchSize: 20,           // 批量上报大小
  flushInterval: 5000,        // 上报间隔（ms）
  enableAutoTrack: true,      // 开启自动采集
  enableDeviceFingerprint: true, // 开启设备指纹
  sampleRate: 1.0,            // 采样率 100%
  persistence: 'localStorage', // 本地存储方式
});

// 手动埋点示例
analytics.track('kyc_photo_capture', {
  step: 'id_front',
  attempt_count: 2,
  camera_permission_granted: true,
  image_quality_score: 0.85,
  session_id: 'sess_abc123',
});
```

#### 2.1.3 后端采集设计

后端采集主要覆盖前端无法触达的数据维度：

| 采集点 | 采集内容 | 技术方案 |
|-------|---------|---------|
| API Gateway | 请求响应时间、状态码、错误信息 | Access Log + 自定义中间件 |
| 业务服务层 | KYC 状态变更、审核结果、业务规则命中 | Event Bus + Domain Event |
| 基础设施层 | 服务健康状态、资源使用率、依赖服务状态 | Prometheus + Grafana Agent |
| 第三方服务 | OCR 结果、活体检测结果、第三方 API 调用 | 回调 + Webhook |

### 2.2 埋点事件分类体系

#### 2.2.1 事件分类总览

```
埋点事件体系
├── 页面级事件（Page Events）
│   ├── 页面进入（page_enter）
│   ├── 页面退出（page_exit）
│   └── 页面停留时长（page_duration）
│
├── 交互级事件（Interaction Events）
│   ├── 拍照操作（photo_capture / photo_retake）
│   ├── 提交操作（form_submit）
│   ├── 错误操作（error_action）
│   ├── 按钮点击（button_click）
│   └── 引导交互（guide_interaction）
│
├── 系统级事件（System Events）
│   ├── API 响应（api_response）
│   ├── 错误码上报（error_code）
│   └── 服务可用性（service_availability）
│
└── 业务结果级事件（Business Events）
    ├── KYC 通过（kyc_approved）
    ├── KYC 拒绝（kyc_rejected）
    ├── KYC 过期（kyc_expired）
    └── 审核队列状态（review_queue_status）
```

#### 2.2.2 页面级事件

##### 事件 1：页面进入（page_enter）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_page_enter` |
| **触发时机** | 用户进入 KYC 流程中的任一步骤页面时触发，包括首次进入和返回该页面 |
| **采集频率** | 每次页面进入触发 1 次 |
| **业务目的** | 构建 KYC 转化漏斗的入口数据，计算各步骤的进入率和跳出率 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `page_name` | String | 是 | 页面标识 | `kyc_step_select_id_type` |
| `page_title` | String | 是 | 页面标题 | "选择证件类型" |
| `step_number` | Integer | 是 | 步骤序号（1-6） | `1` |
| `step_name` | String | 是 | 步骤名称 | `select_id_type` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `user_id` | String | 否 | 用户 ID（已登录时） | `uid_10001` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `referrer` | String | 否 | 来源页面 | `kyc_step_photo_front` |
| `entry_source` | String | 是 | 进入来源 | `registration` / `profile` / `deep_link` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353600000` |
| `timezone` | String | 是 | 用户时区 | `Asia/Shanghai` |
| `app_version` | String | 是 | App 版本号 | `3.2.1` |
| `platform` | String | 是 | 平台 | `ios` / `android` / `web` |
| `os_version` | String | 是 | 操作系统版本 | `iOS 17.4` |
| `network_type` | String | 是 | 网络类型 | `wifi` / `4g` / `5g` |
| `country` | String | 是 | 国家/地区 | `SG` |
| `locale` | String | 是 | 语言偏好 | `zh-CN` |

**数据口径**：
- `page_name` 采用统一命名规范：`kyc_step_{step_name}`
- `step_number` 从 1 开始编号，对应 KYC 六个步骤
- `session_id` 定义：用户从进入 KYC 流程到完成或放弃的完整过程为一个 Session，超时 30 分钟自动断开

##### 事件 2：页面退出（page_exit）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_page_exit` |
| **触发时机** | 用户离开 KYC 流程中的任一步骤页面时触发，包括正常跳转、关闭页面、App 切后台 |
| **采集频率** | 每次页面退出触发 1 次 |
| **业务目的** | 计算页面停留时长，识别用户在哪个步骤最容易放弃 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `page_name` | String | 是 | 页面标识 | `kyc_step_photo_front` |
| `step_number` | Integer | 是 | 步骤序号 | `2` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `user_id` | String | 否 | 用户 ID | `uid_10001` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `exit_type` | String | 是 | 退出类型 | `forward` / `back` / `close` / `background` / `timeout` |
| `next_page` | String | 否 | 下一页面（forward 时） | `kyc_step_photo_back` |
| `duration_ms` | Long | 是 | 页面停留时长（ms） | `15000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353615000` |

**数据口径**：
- `duration_ms` 由 SDK 内部计时器计算，从 `page_enter` 到 `page_exit` 的时间差
- `exit_type` 枚举值：`forward`（前进到下一步）、`back`（返回上一步）、`close`（关闭页面/App）、`background`（切后台超过 30 秒）、`timeout`（页面超时无操作）
- 当 `exit_type` 为 `close` 时，`next_page` 为空，标记为流失点

##### 事件 3：页面停留时长（page_duration）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_page_duration` |
| **触发时机** | 页面退出时由 SDK 自动计算并上报，或在页面停留超过阈值（如 60 秒）时上报心跳 |
| **采集频率** | 页面退出时 1 次 + 心跳上报（每 60 秒 1 次） |
| **业务目的** | 分析用户在各步骤的耗时分布，识别耗时过长的步骤 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `page_name` | String | 是 | 页面标识 | `kyc_step_liveness` |
| `step_number` | Integer | 是 | 步骤序号 | `4` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `duration_ms` | Long | 是 | 累计停留时长（ms） | `45000` |
| `is_heartbeat` | Boolean | 是 | 是否心跳上报 | `false` |
| `interaction_count` | Integer | 是 | 页面内交互次数 | `5` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353650000` |

**数据口径**：
- `duration_ms` 为累计值，心跳上报时为从页面进入到当前时刻的累计时长
- `interaction_count` 统计页面内所有按钮点击、输入、滑动等交互次数
- 心跳数据用于处理用户长时间停留在某页面但最终未退出（如关闭浏览器）的场景

#### 2.2.3 交互级事件

##### 事件 4：拍照操作（photo_capture）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_photo_capture` |
| **触发时机** | 用户完成证件/人脸拍照后触发 |
| **采集频率** | 每次拍照完成触发 1 次 |
| **业务目的** | 分析拍照成功率、重拍率、拍照耗时，优化拍照引导体验 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `capture_type` | String | 是 | 拍照类型 | `id_front` / `id_back` / `selfie` / `liveness` |
| `step_number` | Integer | 是 | 步骤序号 | `2` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `attempt_number` | Integer | 是 | 第几次尝试（含重拍） | `2` |
| `camera_type` | String | 是 | 摄像头类型 | `front` / `back` |
| `camera_permission_granted` | Boolean | 是 | 相机权限是否已授予 | `true` |
| `time_to_capture_ms` | Long | 是 | 从打开相机到拍照完成的时间（ms） | `3200` |
| `image_size_kb` | Integer | 是 | 图片大小（KB） | `850` |
| `image_resolution` | String | 是 | 图片分辨率 | `1920x1080` |
| `image_format` | String | 是 | 图片格式 | `jpeg` / `png` |
| `is_flash_used` | Boolean | 否 | 是否使用闪光灯 | `false` |
| `lighting_condition` | String | 否 | 光线条件（客户端评估） | `good` / `medium` / `poor` |
| `blur_score` | Float | 否 | 模糊度评分（0-1，1 为最清晰） | `0.82` |
| `glare_detected` | Boolean | 否 | 是否检测到反光 | `false` |
| `ocr_confidence` | Float | 否 | OCR 识别置信度（0-1） | `0.95` |
| `capture_result` | String | 是 | 拍照结果 | `success` / `timeout` / `permission_denied` / `camera_error` |
| `error_message` | String | 否 | 错误信息 | `Camera initialization failed` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353620000` |

**数据口径**：
- `attempt_number` 从 1 开始计数，同一 `capture_type` 每次拍照递增
- `time_to_capture_ms` 从相机界面完全加载到用户按下拍摄按钮的时间
- `blur_score` 和 `glare_detected` 由客户端 SDK 实时计算
- `ocr_confidence` 由后端 OCR 服务返回，拍照成功后异步填充

##### 事件 5：重拍操作（photo_retake）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_photo_retake` |
| **触发时机** | 用户主动点击重拍或系统建议重拍时触发 |
| **采集频率** | 每次重拍触发 1 次 |
| **业务目的** | 分析重拍原因，优化拍照引导和质量检测算法 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `capture_type` | String | 是 | 拍照类型 | `id_front` / `id_back` / `selfie` / `liveness` |
| `step_number` | Integer | 是 | 步骤序号 | `2` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `retake_reason` | String | 是 | 重拍原因 | `user_initiated` / `blur_detected` / `glare_detected` / `incomplete` / `wrong_id_type` / `quality_too_low` |
| `previous_attempt_number` | Integer | 是 | 上一次尝试的编号 | `1` |
| `total_attempts` | Integer | 是 | 累计尝试次数（含本次） | `2` |
| `previous_quality_score` | Float | 否 | 上一次图片质量评分 | `0.45` |
| `time_since_last_capture_ms` | Long | 是 | 距上次拍照的时间间隔（ms） | `5000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353625000` |

**数据口径**：
- `retake_reason` 区分用户主动重拍和系统检测不合格导致的重拍
- `previous_quality_score` 综合模糊度、反光、完整性等多维度的加权评分

##### 事件 6：提交操作（form_submit）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_form_submit` |
| **触发时机** | 用户点击提交按钮时触发 |
| **采集频率** | 每次提交触发 1 次 |
| **业务目的** | 监控提交成功率、提交耗时，定位提交失败原因 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `submit_type` | String | 是 | 提交类型 | `kyc_full_submit` / `step_submit` / `retry_submit` |
| `step_number` | Integer | 是 | 当前步骤序号 | `5` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `id_type` | String | 是 | 证件类型 | `passport` / `id_card` / `driver_license` |
| `id_country` | String | 是 | 证件签发国 | `SG` / `CN` / `US` |
| `form_completion_rate` | Float | 是 | 表单完成度（0-1） | `1.0` |
| `validation_errors` | Array | 否 | 表单校验错误列表 | `["name_mismatch", "id_number_invalid"]` |
| `has_validation_error` | Boolean | 是 | 是否有校验错误 | `false` |
| `time_on_form_ms` | Long | 是 | 在表单页面的累计时间（ms） | `120000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353700000` |

##### 事件 7：错误操作（error_action）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_error_action` |
| **触发时机** | KYC 流程中发生用户侧或系统侧错误时触发 |
| **采集频率** | 每次错误触发 1 次 |
| **业务目的** | 统计各类错误的发生频率和影响范围，指导错误处理优化 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `error_type` | String | 是 | 错误类型 | `network_error` / `permission_denied` / `camera_error` / `ocr_failed` / `liveness_failed` / `server_error` / `timeout` |
| `error_code` | String | 是 | 错误码 | `ERR_CAMERA_INIT_001` |
| `error_message` | String | 是 | 错误描述 | "Camera initialization failed" |
| `error_level` | String | 是 | 错误级别 | `fatal` / `recoverable` / `warning` |
| `step_number` | Integer | 是 | 发生错误的步骤 | `2` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `is_recovered` | Boolean | 否 | 用户是否恢复操作 | `true` |
| `recovery_action` | String | 否 | 恢复操作类型 | `retry` / `skip` / `switch_camera` / `contact_support` |
| `time_to_recovery_ms` | Long | 否 | 恢复耗时（ms） | `8000` |
| `stack_trace` | String | 否 | 错误堆栈（脱敏后） | `com.kyc.camera.CameraManager...` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353630000` |

##### 事件 8：引导交互（guide_interaction）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_guide_interaction` |
| **触发时机** | 用户与 KYC 引导提示（如拍照框、动画提示、帮助文档）发生交互时触发 |
| **采集频率** | 每次交互触发 1 次 |
| **业务目的** | 评估引导内容的有效性，优化引导策略 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `guide_type` | String | 是 | 引导类型 | `overlay_tutorial` / `tooltip` / `help_article` / `video_guide` / `animation_hint` |
| `step_number` | Integer | 是 | 步骤序号 | `2` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `interaction_type` | String | 是 | 交互类型 | `view` / `dismiss` / `click_cta` / `expand` / `video_play` / `video_complete` |
| `guide_id` | String | 是 | 引导内容 ID | `guide_photo_front_001` |
| `time_spent_ms` | Long | 否 | 查看引导的时长（ms） | `5000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353640000` |

#### 2.2.4 系统级事件

##### 事件 9：API 响应（api_response）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_api_response` |
| **触发时机** | KYC 相关 API 请求完成后触发（由后端 Agent 采集） |
| **采集频率** | 每次 API 调用触发 1 次 |
| **业务目的** | 监控 API 性能，定位慢接口和故障接口 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `api_name` | String | 是 | API 名称 | `/api/v2/kyc/verify-id` |
| `api_method` | String | 是 | HTTP 方法 | `POST` |
| `http_status_code` | Integer | 是 | HTTP 状态码 | `200` |
| `response_time_ms` | Long | 是 | 响应时间（ms） | `350` |
| `is_success` | Boolean | 是 | 是否成功 | `true` |
| `error_code` | String | 否 | 业务错误码 | `ERR_OCR_QUALITY_LOW` |
| `error_message` | String | 否 | 错误信息 | "Image quality below threshold" |
| `request_size_bytes` | Long | 否 | 请求体大小（bytes） | `2048000` |
| `response_size_bytes` | Long | 否 | 响应体大小（bytes） | `1024` |
| `server_instance` | String | 是 | 服务实例标识 | `kyc-service-pod-abc123` |
| `upstream_service` | String | 否 | 上游服务 | `ocr-service` / `liveness-service` / `review-service` |
| `upstream_response_time_ms` | Long | 否 | 上游服务响应时间（ms） | `280` |
| `retry_count` | Integer | 是 | 重试次数 | `0` |
| `rate_limit_hit` | Boolean | 是 | 是否触发限流 | `false` |
| `trace_id` | String | 是 | 分布式追踪 ID | `trace_xyz789` |
| `session_id` | String | 是 | 关联会话 ID | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353650000` |

**数据口径**：
- `response_time_ms` 包含完整的请求-响应周期（含网络传输时间）
- `upstream_response_time_ms` 仅包含上游服务的处理时间
- 所有时间精度为毫秒级

##### 事件 10：错误码上报（error_code）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_error_code` |
| **触发时机** | KYC 流程中产生业务错误码时触发 |
| **采集频率** | 每次错误产生触发 1 次 |
| **业务目的** | 统计各类业务错误码的分布和趋势，指导产品和技术优化 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `error_domain` | String | 是 | 错误域 | `ocr` / `liveness` / `document` / `face_match` / `system` / `compliance` |
| `error_code` | String | 是 | 错误码 | `OCR_001` |
| `error_message` | String | 是 | 错误描述 | "Document type not supported" |
| `error_category` | String | 是 | 错误分类 | `user_error` / `system_error` / `third_party_error` / `compliance_error` |
| `step_number` | Integer | 是 | 步骤序号 | `3` |
| `session_id` | String | 是 | 会话唯一标识 | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `is_user_visible` | Boolean | 是 | 是否向用户展示错误 | `true` |
| `user_action_after_error` | String | 否 | 用户看到错误后的操作 | `retry` / `go_back` / `close` / `contact_support` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353660000` |

##### 事件 11：服务可用性（service_availability）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_service_availability` |
| **触发时机** | 定期心跳上报（每 30 秒）或服务状态变更时触发 |
| **采集频率** | 每 30 秒 1 次（心跳） + 状态变更时实时触发 |
| **业务目的** | 监控 KYC 依赖服务的可用性，确保 SLA |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `service_name` | String | 是 | 服务名称 | `ocr-service` / `liveness-service` / `review-service` / `kyc-api-gateway` |
| `status` | String | 是 | 服务状态 | `healthy` / `degraded` / `down` |
| `uptime_seconds` | Long | 是 | 连续运行时间（秒） | `86400` |
| `error_rate_5m` | Float | 是 | 近 5 分钟错误率 | `0.002` |
| `avg_response_time_ms_5m` | Long | 是 | 近 5 分钟平均响应时间（ms） | `350` |
| `p99_response_time_ms_5m` | Long | 是 | 近 5 分钟 P99 响应时间（ms） | `1200` |
| `active_connections` | Integer | 是 | 当前活跃连接数 | `1500` |
| `cpu_usage` | Float | 否 | CPU 使用率 | `0.65` |
| `memory_usage` | Float | 否 | 内存使用率 | `0.72` |
| `region` | String | 是 | 服务部署区域 | `ap-southeast-1` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353670000` |

#### 2.2.5 业务结果级事件

##### 事件 12：KYC 通过（kyc_approved）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_approved` |
| **触发时机** | KYC 审核通过时触发 |
| **采集频率** | 每次审核通过触发 1 次 |
| **业务目的** | 计算 KYC 通过率，分析通过路径特征 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `session_id` | String | 是 | 完成认证的会话 ID | `sess_abc123` |
| `device_id` | String | 是 | 设备唯一标识 | `did_xxxxx` |
| `review_type` | String | 是 | 审核类型 | `auto` / `manual` |
| `review_result` | String | 是 | 审核结果 | `approved` |
| `review_duration_ms` | Long | 是 | 审核耗时（ms） | `5000` |
| `total_kyc_duration_ms` | Long | 是 | KYC 全流程耗时（ms） | `180000` |
| `id_type` | String | 是 | 证件类型 | `passport` |
| `id_country` | String | 是 | 证件签发国 | `SG` |
| `risk_level` | String | 是 | 风险等级 | `low` / `medium` / `high` |
| `total_photo_attempts` | Integer | 是 | 总拍照尝试次数 | `3` |
| `total_errors` | Integer | 是 | 总错误次数 | `1` |
| `total_steps_completed` | Integer | 是 | 完成的步骤数 | `6` |
| `reviewer_id` | String | 否 | 审核员 ID（人工审核时） | `reviewer_001` |
| `compliance_checks_passed` | Array | 是 | 通过的合规检查项 | `["sanction_check", "pep_check", "aml_check"]` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353800000` |

##### 事件 13：KYC 拒绝（kyc_rejected）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_rejected` |
| **触发时机** | KYC 审核拒绝时触发 |
| **采集频率** | 每次审核拒绝触发 1 次 |
| **业务目的** | 分析拒绝原因分布，降低误拒率 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10002` |
| `session_id` | String | 是 | 会话 ID | `sess_def456` |
| `device_id` | String | 是 | 设备唯一标识 | `did_yyyyy` |
| `review_type` | String | 是 | 审核类型 | `auto` / `manual` |
| `rejection_reason` | String | 是 | 拒绝原因 | `document_expired` / `photo_blur` / `face_mismatch` / `name_mismatch` / `fraud_suspected` / `sanction_hit` |
| `rejection_category` | String | 是 | 拒绝分类 | `quality_issue` / `authenticity_issue` / `compliance_issue` / `user_error` |
| `is_appealable` | Boolean | 是 | 是否可申诉 | `true` |
| `step_failed` | Integer | 否 | 失败步骤 | `3` |
| `total_kyc_duration_ms` | Long | 是 | KYC 全流程耗时（ms） | `300000` |
| `reviewer_id` | String | 否 | 审核员 ID | `reviewer_002` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353900000` |

##### 事件 14：KYC 过期（kyc_expired）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_expired` |
| **触发时机** | 用户 KYC 状态过期时触发 |
| **采集频率** | 每次过期触发 1 次 |
| **业务目的** | 监控 KYC 过期率，触发重新认证提醒 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10003` |
| `original_approval_date` | Long | 是 | 原始通过日期 | `1711766400000` |
| `expiry_date` | Long | 是 | 过期日期 | `1724371200000` |
| `days_since_approval` | Integer | 是 | 距通过天数 | `180` |
| `kyc_version` | Integer | 是 | KYC 版本号 | `2` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1724371200000` |

##### 事件 15：审核队列状态（review_queue_status）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_review_queue_status` |
| **触发时机** | 审核队列状态变更时触发（定期 + 事件驱动） |
| **采集频率** | 每 60 秒 1 次（定期） + 队列状态变更时实时触发 |
| **业务目的** | 监控审核队列积压情况，优化审核资源配置 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `queue_name` | String | 是 | 队列名称 | `manual_review_queue` / `appeal_queue` / `high_risk_queue` |
| `queue_depth` | Integer | 是 | 队列深度（待处理数量） | `150` |
| `avg_wait_time_ms` | Long | 是 | 平均等待时间（ms） | `600000` |
| `max_wait_time_ms` | Long | 是 | 最大等待时间（ms） | `1800000` |
| `active_reviewers` | Integer | 是 | 在线审核员数量 | `12` |
| `processing_rate_per_min` | Float | 是 | 每分钟处理速率 | `25.5` |
| `sla_breach_count` | Integer | 是 | SLA 违规数量 | `5` |
| `sla_target_ms` | Long | 是 | SLA 目标时间（ms） | `900000` |
| `region` | String | 是 | 区域 | `ap-southeast-1` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353700000` |

#### 2.2.6 制裁与风险筛查模块埋点（模块G）

##### 事件 16：筛查流程启动（screening_initiated）

| 属性 | 定义 |
|-----|------|
| **事件名** | `screening_initiated` |
| **触发时机** | 用户进入制裁与风险筛查流程时触发 |
| **采集频率** | 每次进入筛查流程触发 1 次 |
| **业务目的** | 分析筛查触发率，了解各筛查类型的发起量 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `screening_type` | String | 是 | 筛查类型 | `sanctions` / `pep` / `adverse_media` / `full` |
| `country` | String | 是 | 用户所在国家 | `SG` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353700000` |

##### 事件 17：筛查流程完成（screening_completed）

| 属性 | 定义 |
|-----|------|
| **事件名** | `screening_completed` |
| **触发时机** | 筛查流程完成时触发（无论结果） |
| **采集频率** | 每次筛查完成触发 1 次 |
| **业务目的** | 分析筛查通过率、筛查耗时分布 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `screening_type` | String | 是 | 筛查类型 | `sanctions` / `pep` / `adverse_media` / `full` |
| `result` | String | 是 | 筛查结果 | `hit` / `clear` |
| `hit_details` | String | 否 | 命中详情（JSON） | `{"list": "OFAC SDN", "entity": "John Doe"}` |
| `duration_ms` | Long | 是 | 筛查耗时（ms） | `2500` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353702000` |

##### 事件 18：制裁名单命中（sanctions_hit）

| 属性 | 定义 |
|-----|------|
| **事件名** | `sanctions_hit` |
| **触发时机** | 制裁名单筛查命中时触发 |
| **采集频率** | 每次命中触发 1 次 |
| **业务目的** | 监控制裁命中情况，辅助合规决策 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `list_type` | String | 是 | 制裁名单类型 | `OFAC` / `EU` / `UN` / `UK_HMT` / `AU_DFAT` |
| `matched_entity` | String | 是 | 匹配到的实体名称 | `John Doe` |
| `match_score` | Float | 是 | 匹配分数（0-1） | `0.92` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353703000` |

##### 事件 19：PEP 名单命中（pep_hit）

| 属性 | 定义 |
|-----|------|
| **事件名** | `pep_hit` |
| **触发时机** | PEP（政治公众人物）名单筛查命中时触发 |
| **采集频率** | 每次命中触发 1 次 |
| **业务目的** | 监控 PEP 命中情况，评估关联风险 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `pep_name` | String | 是 | 匹配到的 PEP 姓名 | `Jane Smith` |
| `pep_role` | String | 是 | PEP 职务 | `Minister of Finance` |
| `pep_country` | String | 是 | PEP 所在国家 | `CN` |
| `relationship_type` | String | 是 | 关联关系类型 | `direct` / `family` / `associate` / `close_associate` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353704000` |

##### 事件 20：不良媒体命中（adverse_media_hit）

| 属性 | 定义 |
|-----|------|
| **事件名** | `adverse_media_hit` |
| **触发时机** | 不良媒体筛查命中时触发 |
| **采集频率** | 每次命中触发 1 次 |
| **业务目的** | 监控负面媒体报道，辅助风险评估 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `media_source` | String | 是 | 媒体来源 | `BBC` / `Reuters` / `Local News` |
| `media_summary` | String | 是 | 媒体报道摘要 | `Suspected involvement in money laundering case` |
| `severity` | String | 是 | 严重程度 | `high` / `medium` / `low` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353705000` |

##### 事件 21：人工复核筛查结果（screening_review）

| 属性 | 定义 |
|-----|------|
| **事件名** | `screening_review` |
| **触发时机** | 人工复核筛查结果时触发 |
| **采集频率** | 每次复核触发 1 次 |
| **业务目的** | 分析人工复核效率，优化复核流程 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `original_result` | String | 是 | 原始筛查结果 | `hit` / `clear` |
| `review_result` | String | 是 | 复核结果 | `confirmed_hit` / `false_positive` / `escalated` |
| `reviewer_id` | String | 是 | 复核员 ID | `reviewer_003` |
| `review_duration` | Long | 是 | 复核耗时（ms） | `300000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354005000` |

#### 2.2.7 持续监控模块埋点（模块H）

##### 事件 22：风控告警触发（monitoring_alert_triggered）

| 属性 | 定义 |
|-----|------|
| **事件名** | `monitoring_alert_triggered` |
| **触发时机** | 风控告警触发时触发 |
| **采集频率** | 每次告警触发 1 次 |
| **业务目的** | 监控告警分布，了解告警触发频率和类型 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `alert_type` | String | 是 | 告警类型 | `transaction_anomaly` / `risk_score_change` / `kyc_expiry` / `behavioral_anomaly` |
| `alert_level` | String | 是 | 告警等级 | `P0` / `P1` / `P2` |
| `rule_id` | String | 是 | 触发的规则 ID | `RULE_TX_STRUCTURING_001` |
| `trigger_details` | String | 否 | 触发详情（JSON） | `{"pattern": "structuring", "amount": 9500}` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353800000` |

##### 事件 23：告警处理完成（monitoring_alert_resolved）

| 属性 | 定义 |
|-----|------|
| **事件名** | `monitoring_alert_resolved` |
| **触发时机** | 告警处理完成时触发 |
| **采集频率** | 每次告警处理完成触发 1 次 |
| **业务目的** | 分析告警处理效率，监控积压情况 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `alert_id` | String | 是 | 告警唯一标识 | `alert_abc123` |
| `resolution` | String | 是 | 处理结果 | `action_taken` / `false_positive` / `escalated` |
| `resolver_id` | String | 是 | 处理人 ID | `resolver_001` |
| `duration` | Long | 是 | 处理耗时（ms） | `600000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354400000` |

##### 事件 24：钱包风险评分变化（wallet_risk_score_changed）

| 属性 | 定义 |
|-----|------|
| **事件名** | `wallet_risk_score_changed` |
| **触发时机** | 钱包风险评分发生变化时触发 |
| **采集频率** | 每次评分变化触发 1 次 |
| **业务目的** | 监控钱包风险变化趋势，识别风险恶化用户 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `wallet_address` | String | 是 | 钱包地址 | `0x1234...abcd` |
| `old_score` | Float | 是 | 变化前评分 | `0.3` |
| `new_score` | Float | 是 | 变化后评分 | `0.75` |
| `reason` | String | 是 | 变化原因 | `large_transaction` / `mixer_interaction` / `sanction_association` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353900000` |

##### 事件 25：异常交易模式检测（transaction_pattern_detected）

| 属性 | 定义 |
|-----|------|
| **事件名** | `transaction_pattern_detected` |
| **触发时机** | 检测到异常交易模式时触发 |
| **采集频率** | 每次检测到异常模式触发 1 次 |
| **业务目的** | 监控异常交易模式，辅助 AML 调查 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `pattern_type` | String | 是 | 异常模式类型 | `structuring` / `rapid` / `large` / `round_trip` / `unusual_counterparty` |
| `details` | String | 否 | 模式详情（JSON） | `{"count": 5, "total_amount": 47500, "time_window": "24h"}` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353950000` |

##### 事件 26：用户 KYC 信息变更（kyc_info_changed）

| 属性 | 定义 |
|-----|------|
| **事件名** | `kyc_info_changed` |
| **触发时机** | 用户 KYC 信息发生变更时触发 |
| **采集频率** | 每次信息变更触发 1 次 |
| **业务目的** | 监控 KYC 信息变更频率，识别异常变更行为 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `changed_fields` | Array | 是 | 变更字段列表 | `["name", "address"]` |
| `old_values` | String | 否 | 变更前值（脱敏，JSON） | `{"name": "J*** D**", "address": "S*** Rd"}` |
| `new_values` | String | 否 | 变更后值（脱敏，JSON） | `{"name": "J*** S***", "address": "O*** St"}` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353960000` |

##### 事件 27：不活跃账户重新激活（account_reactivation）

| 属性 | 定义 |
|-----|------|
| **事件名** | `account_reactivation` |
| **触发时机** | 不活跃账户重新激活时触发 |
| **采集频率** | 每次账户激活触发 1 次 |
| **业务目的** | 监控账户重新激活风险，识别潜在的洗钱行为 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `inactive_days` | Integer | 是 | 不活跃天数 | `180` |
| `risk_score` | Float | 是 | 激活时风险评分 | `0.65` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353970000` |

#### 2.2.8 Travel Rule 模块埋点（模块I）

##### 事件 28：Travel Rule 信息收集完成（travel_rule_info_collected）

| 属性 | 定义 |
|-----|------|
| **事件名** | `travel_rule_info_collected` |
| **触发时机** | Travel Rule 信息收集完成时触发 |
| **采集频率** | 每次信息收集完成触发 1 次 |
| **业务目的** | 监控 TR 合规率，评估信息收集完整性 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `transfer_type` | String | 是 | 转账类型 | `send` / `receive` |
| `counterparty_vasp` | String | 是 | 对手方 VASP 名称 | `Binance` / `Coinbase` / `Unknown` |
| `info_completeness` | Float | 是 | 信息完整度（0-1） | `0.85` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353980000` |

##### 事件 29：Travel Rule 信息传输（travel_rule_info_transmitted）

| 属性 | 定义 |
|-----|------|
| **事件名** | `travel_rule_info_transmitted` |
| **触发时机** | 信息成功传输给对手方 VASP 时触发 |
| **采集频率** | 每次传输触发 1 次 |
| **业务目的** | 监控 TR 传输成功率，评估协议兼容性 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `counterparty_vasp` | String | 是 | 对手方 VASP 名称 | `Binance` |
| `protocol` | String | 是 | 传输协议 | `NOTABENE` / `SYGNA` / `OPENVASP` / `MANUAL` |
| `transmission_status` | String | 是 | 传输状态 | `success` / `failed` / `pending` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353985000` |

##### 事件 30：Travel Rule 信息接收（travel_rule_info_received）

| 属性 | 定义 |
|-----|------|
| **事件名** | `travel_rule_info_received` |
| **触发时机** | 收到对手方 VASP 的 Travel Rule 信息时触发 |
| **采集频率** | 每次接收触发 1 次 |
| **业务目的** | 监控 TR 信息接收情况，评估对手方合规水平 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `originator_vasp` | String | 是 | 发起方 VASP 名称 | `Coinbase` |
| `info_completeness` | Float | 是 | 接收信息完整度（0-1） | `0.90` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714353990000` |

#### 2.2.9 合规报告模块埋点（模块J）

##### 事件 31：SAR 报告生成（sar_generated）

| 属性 | 定义 |
|-----|------|
| **事件名** | `sar_generated` |
| **触发时机** | SAR（可疑活动报告）生成时触发 |
| **采集频率** | 每次生成触发 1 次 |
| **业务目的** | 监控 SAR 报告生成量，评估自动生成效率 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `sar_type` | String | 是 | SAR 类型 | `transaction_suspicion` / `identity_fraud` / `sanction_evasion` |
| `trigger_reason` | String | 是 | 触发原因 | `structuring_pattern_detected` |
| `auto_generated` | Boolean | 是 | 是否自动生成 | `true` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354000000` |

##### 事件 32：SAR 报告提交（sar_submitted）

| 属性 | 定义 |
|-----|------|
| **事件名** | `sar_submitted` |
| **触发时机** | SAR 报告提交给监管机构时触发 |
| **采集频率** | 每次提交触发 1 次 |
| **业务目的** | 监控 SAR 提交合规率，确保监管合规 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `sar_id` | String | 是 | SAR 报告唯一标识 | `SAR-2026-001234` |
| `submitted_to` | String | 是 | 提交目标监管机构 | `MAS` / `FCA` / `FINCEN` |
| `submission_status` | String | 是 | 提交状态 | `success` / `failed` / `pending_review` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354100000` |

##### 事件 33：CTR 大额交易报告触发（ctr_triggered）

| 属性 | 定义 |
|-----|------|
| **事件名** | `ctr_triggered` |
| **触发时机** | 交易金额达到 CTR（大额交易报告）阈值时触发 |
| **采集频率** | 每次触发 1 次 |
| **业务目的** | 监控大额交易频率，确保 CTR 合规 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `amount` | Float | 是 | 交易金额 | `15000.00` |
| `currency` | String | 是 | 交易币种 | `USD` / `SGD` / `BTC` |
| `threshold` | Float | 是 | 触发的阈值 | `10000.00` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354150000` |

##### 事件 34：审计日志导出（audit_log_exported）

| 属性 | 定义 |
|-----|------|
| **事件名** | `audit_log_exported` |
| **触发时机** | 审计日志导出时触发 |
| **采集频率** | 每次导出触发 1 次 |
| **业务目的** | 监控审计日志访问情况，确保审计合规 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `exporter_id` | String | 是 | 导出人 ID | `auditor_001` |
| `export_scope` | String | 是 | 导出范围 | `full` / `date_range` / `user_specific` / `event_specific` |
| `export_format` | String | 是 | 导出格式 | `csv` / `json` / `pdf` |
| `record_count` | Integer | 是 | 导出记录数 | `50000` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354200000` |

#### 2.2.10 模块化 ZK 服务埋点（模块F）

##### 事件 35：ZK 证明请求发起（zk_proof_requested）

| 属性 | 定义 |
|-----|------|
| **事件名** | `zk_proof_requested` |
| **触发时机** | ZK 证明请求发起时触发 |
| **采集频率** | 每次请求触发 1 次 |
| **业务目的** | 分析 ZK 服务使用量，了解属性需求分布 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `requested_attributes` | Array | 是 | 请求的属性列表 | `["age_above_18", "country_of_residence"]` |
| `client_id` | String | 否 | 外部客户 ID（B2B 场景） | `client_exchange_001` |
| `proof_type` | String | 是 | 证明类型 | `single` / `composite` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354300000` |

##### 事件 36：ZK 证明生成完成（zk_proof_generated）

| 属性 | 定义 |
|-----|------|
| **事件名** | `zk_proof_generated` |
| **触发时机** | ZK 证明生成完成时触发 |
| **采集频率** | 每次生成完成触发 1 次 |
| **业务目的** | 分析 ZK 证明生成性能，优化电路设计 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `attributes_proved` | Array | 是 | 已证明的属性列表 | `["age_above_18", "kyc_verified"]` |
| `generation_time_ms` | Long | 是 | 生成耗时（ms） | `3500` |
| `proof_size_bytes` | Integer | 是 | 证明大小（bytes） | `2048` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354303500` |

##### 事件 37：ZK 证明验证完成（zk_proof_verified）

| 属性 | 定义 |
|-----|------|
| **事件名** | `zk_proof_verified` |
| **触发时机** | ZK 证明验证完成时触发 |
| **采集频率** | 每次验证完成触发 1 次 |
| **业务目的** | 分析 ZK 证明验证成功率，监控验证性能 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `verification_result` | String | 是 | 验证结果 | `valid` / `invalid` |
| `verification_time_ms` | Long | 是 | 验证耗时（ms） | `150` |
| `verifier_type` | String | 是 | 验证方类型 | `onchain` / `offchain` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354303650` |

##### 事件 38：ZK 证明过期（zk_proof_expired）

| 属性 | 定义 |
|-----|------|
| **事件名** | `zk_proof_expired` |
| **触发时机** | ZK 证明过期时触发 |
| **采集频率** | 每次过期触发 1 次 |
| **业务目的** | 分析 ZK 证明生命周期，优化 TTL 策略 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `user_id` | String | 是 | 用户 ID | `uid_10001` |
| `attributes` | Array | 是 | 过期证明的属性列表 | `["age_above_18"]` |
| `ttl` | Long | 是 | 证明有效期（ms） | `86400000` |
| `expiry_reason` | String | 是 | 过期原因 | `ttl_reached` / `revoked` / `schema_updated` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714440700000` |

##### 事件 39：外部客户接入 ZK 服务（zk_client_onboarded）

| 属性 | 定义 |
|-----|------|
| **事件名** | `zk_client_onboarded` |
| **触发时机** | 外部客户完成 ZK 服务接入时触发 |
| **采集频率** | 每次客户接入触发 1 次 |
| **业务目的** | 分析 ZK 服务客户增长，了解客户类型分布 |

**参数列表**：

| 参数名 | 类型 | 是否必填 | 说明 | 示例值 |
|-------|------|---------|------|-------|
| `client_id` | String | 是 | 客户 ID | `client_defi_001` |
| `client_type` | String | 是 | 客户类型 | `exchange` / `defi` / `platform` / `institution` |
| `selected_attributes` | Array | 是 | 客户选择的属性列表 | `["kyc_verified", "age_above_18", "country_not_sanctioned"]` |
| `plan_type` | String | 是 | 订阅计划类型 | `free` / `basic` / `enterprise` |
| `timestamp` | Long | 是 | 事件时间戳（ms） | `1714354400000` |

### 2.3 数据质量保障机制

#### 2.3.1 数据去重

| 策略 | 说明 |
|-----|------|
| **客户端去重** | SDK 内部维护事件 ID 缓存（基于 `event_id = hash(event_name + timestamp + key_params)`），相同事件 5 秒内不重复发送 |
| **网关去重** | 采集网关基于 `event_id` 进行幂等校验，重复事件直接丢弃 |
| **管道去重** | Flink 任务使用 `event_id` + `device_id` 作为去重 Key，窗口大小 10 分钟，Exactly-Once 语义保证 |

#### 2.3.2 数据校验

```
校验层级：
┌─────────────────────────────────────────────┐
│ Level 1: SDK 端校验（客户端）                 │
│  - 必填字段非空校验                           │
│  - 字段类型校验                               │
│  - 枚举值合法性校验                           │
│  - 时间戳合理性校验（不能是未来时间）           │
├─────────────────────────────────────────────┤
│ Level 2: 网关校验（服务端）                    │
│  - Schema 校验（JSON Schema / Protobuf）      │
│  - 数据大小限制（单事件 < 64KB）              │
│  - 频率限制（单设备 < 100 事件/秒）           │
│  - 签名校验（防伪造）                         │
├─────────────────────────────────────────────┤
│ Level 3: 管道校验（Flink）                    │
│  - 业务规则校验（如 step_number 在 1-6 范围） │
│  - 时序校验（事件顺序合理性）                  │
│  - 关联校验（session_id 是否存在）            │
└─────────────────────────────────────────────┘
```

#### 2.3.3 异常检测

| 异常类型 | 检测方法 | 处理策略 |
|---------|---------|---------|
| 数据量突增/突降 | 3-Sigma 规则 + 移动平均 | 告警 + 自动排查 |
| 字段值异常 | 枚举值白名单 + 范围校验 | 隔离到异常 Topic + 告警 |
| 时序异常 | 事件时间与服务器时间偏差 > 5 分钟 | 时间校正 + 标记 |
| 重复事件 | 事件 ID 去重 | 丢弃重复 + 记录日志 |
| 数据缺失 | 字段空值率监控 | 告警 + 补采策略 |

---

## 3. 大数据技术架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                           数据源层                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Web SDK  │  │ iOS SDK  │  │Android SDK│  │ 后端 Agent       │   │
│  └────┬─────┘  └────┬─────┘  └────┬──────┘  └────────┬─────────┘   │
│       │              │              │                   │             │
│       └──────────────┴──────┬───────┴───────────────────┘             │
│                             │                                       │
│                             ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Nginx / API Gateway (负载均衡 + 限流)            │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                       │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        数据接入层                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Kafka Cluster                              │   │
│  │  Topic: kyc.events.raw (原始事件)                              │   │
│  │  Topic: kyc.events.validated (校验后事件)                      │   │
│  │  Topic: kyc.events.anomaly (异常事件)                          │   │
│  │  Topic: kyc.events.dead_letter (死信队列)                      │   │
│  │  Partitions: 32 | Replication Factor: 3                       │   │
│  │  Retention: 7 days (raw) / 30 days (validated)                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  实时处理层       │ │  离线处理层   │ │  ML 训练层        │
│                  │ │              │ │                  │
│  Apache Flink    │ │  Apache Spark│ │  Spark MLlib     │
│  - 实时聚合      │ │  + Hive      │ │  + Python        │
│  - 实时异常检测  │ │  + Delta Lake│ │  (Jupyter/       │
│  - 实时看板数据  │ │              │ │   Airflow)       │
│  - 流式特征计算  │ │  - T+1 报表  │ │                  │
│                  │ │  - 历史分析  │ │  - 模型训练      │
│                  │ │  - 数据仓库  │ │  - 特征工程      │
│                  │ │              │ │  - 模型评估      │
└────────┬─────────┘ └──────┬───────┘ └────────┬─────────┘
         │                 │                   │
         ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         数据存储层                                   │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  ClickHouse     │  │  PostgreSQL  │  │  S3 / Delta Lake      │  │
│  │  (实时 OLAP)    │  │  (元数据)    │  │  (原始数据湖)          │  │
│  │                 │  │              │  │                       │  │
│  │  - 实时聚合表   │  │  - 用户画像  │  │  - 原始事件存储       │  │
│  │  - 漏斗数据     │  │  - 埋点元数据│  │  - 模型训练数据       │  │
│  │  - 异常事件     │  │  - 配置信息  │  │  - 数据归档           │  │
│  │  - 实时指标     │  │  - 权限管理  │  │  - 数据血缘           │  │
│  │                 │  │              │  │                       │  │
│  │  Retention:     │  │              │  │  Retention:           │  │
│  │  热数据 90 天   │  │              │  │  原始数据 2 年        │  │
│  │  温数据 1 年    │  │              │  │  聚合数据 3 年        │  │
│  └─────────────────┘  └──────────────┘  └───────────────────────┘  │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────────────────────────────┐  │
│  │  Redis          │  │  Elasticsearch                          │  │
│  │  (缓存层)       │  │  (日志检索)                              │  │
│  │                 │  │                                          │  │
│  │  - 实时指标缓存 │  │  - 原始事件全文检索                      │  │
│  │  - 会话状态     │  │  - 错误日志分析                          │  │
│  │  - 限流计数     │  │  - 调试排障                              │  │
│  └─────────────────┘  └──────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        数据服务层                                    │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  GraphQL API    │  │  REST API    │  │  WebSocket            │  │
│  │  (看板查询)     │  │  (通用查询)  │  │  (实时推送)           │  │
│  └─────────────────┘  └──────────────┘  └───────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        应用层                                        │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  数据看板       │  │  告警系统    │  │  AI 分析引擎          │  │
│  │  (Grafana /     │  │  (PagerDuty  │  │  (ML Pipeline)        │  │
│  │   自研前端)     │  │   / Slack)   │  │                       │  │
│  └─────────────────┘  └──────────────┘  └───────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 实时数据处理

#### 3.2.1 Kafka 集群配置

| 配置项 | 值 | 说明 |
|-------|---|------|
| 集群规模 | 6 Brokers | 3 ZooKeeper 节点 |
| Topic 数量 | 4 个核心 Topic | raw / validated / anomaly / dead_letter |
| 分区数 | 32 | 按 `device_id` 哈希分区 |
| 副本因子 | 3 | 高可用保证 |
| 消息格式 | Avro + Schema Registry | 强类型 + 向后兼容 |
| 保留策略 | raw: 7 天 / validated: 30 天 | 按时间和大小双策略 |
| 压缩 | LZ4 | 平衡压缩比和速度 |
| 最大消息大小 | 1 MB | 单事件上限 |

#### 3.2.2 Flink 实时处理作业

| 作业名称 | 功能 | 输入 | 输出 | 延迟 |
|---------|------|-----|------|------|
| `kyc-event-validator` | 事件校验 + 清洗 | `kyc.events.raw` | `kyc.events.validated` / `kyc.events.anomaly` | < 1s |
| `kyc-realtime-aggregator` | 实时指标聚合 | `kyc.events.validated` | ClickHouse 实时表 | < 5s |
| `kyc-funnel-calculator` | 实时漏斗计算 | `kyc.events.validated` | ClickHouse 漏斗表 | < 10s |
| `kyc-anomaly-detector` | 实时异常检测 | `kyc.events.validated` | 告警系统 | < 30s |
| `kyc-session-tracker` | 会话追踪 | `kyc.events.validated` | ClickHouse 会话表 | < 5s |
| `kyc-feature-computer` | 实时特征计算 | `kyc.events.validated` | Redis 特征存储 | < 10s |

#### 3.2.3 实时数据流示例

```
用户拍照 → SDK 采集 kyc_photo_capture 事件
  → 发送到 API Gateway
  → Schema 校验 + 去重
  → 写入 Kafka (kyc.events.raw)
  → Flink kyc-event-validator 消费
    → 校验通过 → kyc.events.validated
    → 校验失败 → kyc.events.anomaly
  → Flink kyc-realtime-aggregator 消费 kyc.events.validated
    → 更新 ClickHouse 实时聚合表
    → 更新 Redis 缓存
  → WebSocket 推送到前端看板（延迟 < 5s）
```

### 3.3 离线数据处理

#### 3.3.1 Spark + Hive 数据仓库

**数据仓库分层**：

```
┌─────────────────────────────────────────┐
│  ODS (Operational Data Store)           │
│  - 原始事件数据（1:1 从 Kafka 落盘）     │
│  - 分区：dt (日期) / hour (小时)         │
│  - 格式：Parquet + Snappy 压缩           │
│  - 存储：S3                              │
├─────────────────────────────────────────┤
│  DWD (Data Warehouse Detail)            │
│  - 清洗后的明细数据                      │
│  - 会话聚合明细                          │
│  - 用户行为序列                          │
│  - 分区：dt (日期)                       │
│  - 格式：Delta Lake                      │
├─────────────────────────────────────────┤
│  DWS (Data Warehouse Summary)           │
│  - 按维度聚合的汇总数据                  │
│  - 日/周/月聚合表                        │
│  - 漏斗汇总表                            │
│  - 分区：dt (日期) / granularity         │
│  - 格式：Delta Lake                      │
├─────────────────────────────────────────┤
│  ADS (Application Data Store)           │
│  - 面向应用的数据集                      │
│  - 看板数据集                            │
│  - ML 特征数据集                         │
│  - 报表数据集                            │
│  - 格式：Delta Lake + ClickHouse         │
└─────────────────────────────────────────┘
```

#### 3.3.2 核心 ETL 任务

| 任务名称 | 调度频率 | 输入 | 输出 | 说明 |
|---------|---------|-----|------|------|
| `ods_to_dwd_event_clean` | 每小时 | ODS 原始事件 | DWD 清洗事件 | 数据清洗 + 类型转换 |
| `dwd_to_dws_session_agg` | 每日 01:00 | DWD 事件明细 | DWS 会话聚合 | 会话级指标聚合 |
| `dwd_to_dws_funnel_daily` | 每日 02:00 | DWD 事件明细 | DWS 日漏斗表 | 每日漏斗数据 |
| `dws_to_ads_dashboard` | 每日 03:00 | DWS 汇总表 | ADS 看板数据集 | 看板数据准备 |
| `dwd_to_ads_ml_features` | 每日 04:00 | DWD 事件明细 | ADS ML 特征集 | ML 模型训练数据 |
| `data_quality_check` | 每日 05:00 | 全层 | 数据质量报告 | 数据质量巡检 |
| `data_lifecycle_manage` | 每日 06:00 | 全层 | 归档/删除 | 生命周期管理 |

#### 3.3.3 Delta Lake 优势

- **ACID 事务**：确保数据写入的原子性和一致性
- **Schema Evolution**：支持埋点事件的字段新增和修改
- **Time Travel**：支持数据回溯和审计
- **Upsert/Merge**：高效支持聚合数据的更新
- **Z-Ordering**：按查询维度优化数据布局，提升查询性能

### 3.4 数据存储选型

| 存储引擎 | 用途 | 数据量级 | 查询延迟 | 保留策略 |
|---------|------|---------|---------|---------|
| **ClickHouse** | 实时 OLAP 查询 | ~500GB 热数据 | < 100ms (P95) | 热数据 90 天，温数据 1 年 |
| **PostgreSQL** | 元数据、用户画像、配置 | ~50GB | < 10ms | 永久保留 |
| **S3 + Delta Lake** | 原始数据、训练数据、归档 | ~10TB/年 | 秒级（批量） | 原始 2 年，聚合 3 年 |
| **Redis** | 实时缓存、会话状态、限流 | ~5GB | < 1ms | 按需过期 |
| **Elasticsearch** | 日志检索、错误分析 | ~1TB | < 500ms | 90 天 |

### 3.5 数据治理

#### 3.5.1 数据血缘

```
埋点事件定义 (YAML)
       │
       ▼
SDK 代码生成 (事件 Schema → 代码)
       │
       ▼
Kafka Topic (Schema Registry 管理)
       │
       ├──→ Flink 实时作业 → ClickHouse 实时表
       │
       ├──→ Spark ETL → Delta Lake ODS → DWD → DWS → ADS
       │
       └──→ ML Pipeline → 特征存储 → 模型训练 → 模型服务
```

**血缘管理工具**：Apache Atlas / OpenLineage
- 自动采集 Flink 和 Spark 作业的输入输出关系
- 支持字段级血缘追踪
- 影响分析：当上游埋点变更时，自动评估下游影响范围

#### 3.5.2 数据质量监控

| 监控维度 | 指标 | 告警阈值 |
|---------|------|---------|
| 完整性 | 必填字段空值率 | > 1% 告警，> 5% 严重告警 |
| 一致性 | 跨表数据一致性（如事件数 vs 聚合数） | 偏差 > 0.1% 告警 |
| 及时性 | 数据延迟（事件时间 vs 入库时间） | > 5 分钟告警 |
| 准确性 | 枚举值分布异常 | 新增值占比 > 1% 告警 |
| 唯一性 | 事件重复率 | > 0.01% 告警 |
| 数据量 | 每日事件总量 | 日环比偏差 > 20% 告警 |

#### 3.5.3 数据生命周期管理

| 数据层级 | 热存储 | 温存储 | 冷存储 | 删除 |
|---------|-------|-------|-------|------|
| ODS 原始事件 | 7 天 (S3 Standard) | 90 天 (S3 IA) | 2 年 (S3 Glacier) | 2 年后删除 |
| DWD 明细数据 | 30 天 (ClickHouse) | 1 年 (S3 IA) | 3 年 (S3 Glacier) | 3 年后删除 |
| DWS 汇总数据 | 90 天 (ClickHouse) | 1 年 (S3 IA) | 永久 (S3 Glacier) | — |
| ML 特征数据 | 90 天 (Redis + S3) | 1 年 (S3 IA) | 2 年 (S3 Glacier) | 2 年后删除 |
| 审计日志 | 30 天 (ES) | 1 年 (S3 IA) | 7 年 (S3 Glacier) | 7 年后删除 |

---

## 4. AI 与机器学习应用

### 4.1 转化率预测模型

#### 4.1.1 问题定义

**目标**：预测用户在 KYC 流程中每个步骤的流失概率，提前识别高流失风险用户，触发干预策略。

**建模方式**：二分类模型（流失 vs 完成），在每个步骤入口进行预测。

#### 4.1.2 特征工程

| 特征类别 | 特征名称 | 类型 | 说明 | 示例 |
|---------|---------|------|------|------|
| **设备信息** | `device_os` | Categorical | 操作系统 | `iOS 17.4` |
| | `device_model` | Categorical | 设备型号 | `iPhone 15 Pro` |
| | `screen_resolution` | Categorical | 屏幕分辨率 | `1170x2532` |
| | `camera_quality_score` | Numerical | 摄像头质量评分 | `0.85` |
| | `available_storage_gb` | Numerical | 可用存储空间 | `45.2` |
| | `battery_level` | Numerical | 电量百分比 | `0.65` |
| **行为序列** | `step_enter_count` | Numerical | 各步骤进入次数 | `{1:1, 2:3, 3:1}` |
| | `total_interactions` | Numerical | 总交互次数 | `15` |
| | `error_count` | Numerical | 错误次数 | `2` |
| | `retake_count` | Numerical | 重拍次数 | `1` |
| | `back_navigation_count` | Numerical | 返回上一步次数 | `1` |
| | `help_guide_viewed` | Boolean | 是否查看帮助 | `true` |
| | `avg_step_duration_ms` | Numerical | 平均步骤时长 | `25000` |
| | `time_since_last_action_ms` | Numerical | 距上次操作时间 | `30000` |
| | `action_sequence` | Sequence | 操作序列编码 | `[enter, click, error, retake, ...]` |
| **历史数据** | `previous_kyc_attempts` | Numerical | 历史 KYC 尝试次数 | `1` |
| | `previous_kyc_result` | Categorical | 历史 KYC 结果 | `rejected` / `null` |
| | `account_age_days` | Numerical | 账号注册天数 | `30` |
| | `previous_app_sessions` | Numerical | 历史 App 使用次数 | `15` |
| | `previous_transaction_count` | Numerical | 历史交易次数 | `5` |
| **环境因素** | `network_type` | Categorical | 网络类型 | `wifi` / `4g` |
| | `network_latency_ms` | Numerical | 网络延迟 | `50` |
| | `time_of_day` | Numerical | 当前时段（0-23） | `14` |
| | `day_of_week` | Numerical | 星期几（0-6） | `2` |
| | `country` | Categorical | 国家/地区 | `SG` |
| | `locale` | Categorical | 语言偏好 | `zh-CN` |
| | `is_holiday` | Boolean | 是否节假日 | `false` |
| **实时特征** | `current_step_duration_ms` | Numerical | 当前步骤已停留时间 | `45000` |
| | `current_step_interactions` | Numerical | 当前步骤交互次数 | `8` |
| | `realtime_api_error_rate` | Numerical | 实时 API 错误率 | `0.05` |
| | `realtime_service_health` | Categorical | 实时服务健康状态 | `degraded` |

#### 4.1.3 模型选择与训练

**主模型：XGBoost / LightGBM**

| 配置项 | XGBoost | LightGBM |
|-------|---------|----------|
| 适用场景 | 小样本、高精度要求 | 大样本、训练速度快 |
| 优势 | 鲁棒性强、可解释性好 | 训练速度快、内存效率高 |
| 超参数 | `max_depth=6, learning_rate=0.05, n_estimators=500, subsample=0.8` | `num_leaves=63, learning_rate=0.05, n_estimators=500, feature_fraction=0.8` |
| 特征重要性 | SHAP 值 | Gain / Split |

**备选模型：深度学习（Transformer）**

- 使用 Transformer Encoder 编码用户行为序列
- 适用于行为序列较长、特征交互复杂的场景
- 模型结构：Embedding Layer → Transformer Encoder (4 layers, 8 heads) → FC → Sigmoid
- 训练数据量要求：> 100 万条标注样本

**模型训练流程**：

```
数据准备 (Spark ETL)
    │
    ▼
特征工程 (Feature Store)
    │
    ▼
训练集 / 验证集 / 测试集划分 (7:2:1, 时间切分)
    │
    ▼
模型训练 (XGBoost / LightGBM)
    │
    ▼
超参数调优 (Optuna / Hyperopt, Bayesian Optimization)
    │
    ▼
模型评估 (AUC, Precision, Recall, F1)
    │
    ▼
模型解释 (SHAP Analysis)
    │
    ▼
模型部署 (MLflow + ONNX Runtime)
    │
    ▼
在线推理 (Redis Feature Store + Model Serving)
    │
    ▼
A/B 测试验证
```

#### 4.1.4 模型输出与评估

**模型输出**：

```json
{
  "user_id": "uid_10001",
  "session_id": "sess_abc123",
  "current_step": 3,
  "churn_probability": 0.78,
  "churn_risk_level": "high",
  "top_churn_factors": [
    {"factor": "photo_retake_count", "contribution": 0.32, "value": 3},
    {"factor": "error_count", "contribution": 0.25, "value": 2},
    {"factor": "current_step_duration_ms", "contribution": 0.18, "value": 120000},
    {"factor": "network_type", "contribution": 0.10, "value": "4g"},
    {"factor": "device_model", "contribution": 0.08, "value": "iPhone 8"}
  ],
  "recommended_action": "show_simplified_guide",
  "prediction_timestamp": 1714353700000
}
```

**评估指标**：

| 指标 | 目标值 | 说明 |
|-----|-------|------|
| AUC-ROC | > 0.85 | 区分能力 |
| Precision@20% | > 0.70 | 高风险用户中实际流失的比例 |
| Recall@20% | > 0.60 | 流失用户中被识别为高风险的比例 |
| F1-Score | > 0.65 | 综合指标 |
| 特征稳定性 (PSI) | < 0.1 | 特征分布稳定性 |

### 4.2 异常检测

#### 4.2.1 实时异常检测

**检测场景**：

| 异常类型 | 检测指标 | 检测方法 | 告警阈值 |
|---------|---------|---------|---------|
| API 延迟突增 | P99 响应时间 | 3-Sigma + EWMA | 超过均值 3 倍标准差 |
| 错误率飙升 | 5xx 错误率 | CUSUM 变点检测 | 错误率 > 5% 或环比增长 > 300% |
| 转化率异常下降 | 步骤转化率 | STL 分解 + 残差检测 | 低于历史同期 2 个标准差 |
| 认证量异常 | 每分钟认证量 | 移动平均 + 季节性分解 | 偏差 > 30% |
| 队列积压 | 审核队列深度 | 趋势外推 | 预计 30 分钟内 SLA 违规 |

**技术实现**：

```
Flink 实时流 → 滑动窗口聚合（1 分钟窗口，30 秒滑动）
    │
    ▼
特征提取（均值、标准差、变化率、趋势）
    │
    ▼
异常检测引擎
    ├── 统计方法：3-Sigma, CUSUM, Grubbs Test
    ├── 机器学习：Isolation Forest（在线更新）
    └── 规则引擎：业务规则 + 阈值
    │
    ▼
异常评分（0-100）
    │
    ▼
告警决策（三级告警）
    │
    ▼
通知推送（Slack / PagerDuty / 邮件）
```

#### 4.2.2 欺诈行为检测

**检测维度**：

| 欺诈类型 | 检测特征 | 检测方法 |
|---------|---------|---------|
| 批量注册 | 同一设备/IP 短时间大量注册 | 频率统计 + 聚类分析 |
| 设备指纹异常 | 虚拟机、模拟器、Root/越狱设备 | 设备指纹库 + 规则引擎 |
| 地理位置异常 | GPS 欺骗、VPN、短时间内多地登录 | IP-Geo 库 + 行为分析 |
| 身份欺诈 | 同一证件多次使用、证件图片伪造 | OCR 交叉验证 + 图片指纹 |
| 活体检测绕过 | 照片/视频攻击、3D 面具 | 活体检测服务 + 行为分析 |
| 合谋欺诈 | 多账号关联、资金归集 | 图算法（社区发现） |

**技术方案**：

```
┌─────────────────────────────────────────────────┐
│              欺诈检测引擎                         │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  规则引擎 (Drools)                        │   │
│  │  - 硬编码业务规则（100+ 条）               │   │
│  │  - 实时执行，低延迟                        │   │
│  │  - 覆盖已知欺诈模式                        │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Isolation Forest（离线 + 在线）           │   │
│  │  - 无监督异常检测                          │   │
│  │  - 特征：设备行为、网络行为、操作模式       │   │
│  │  - 在线增量更新（每月全量重训练）           │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Autoencoder（深度学习）                    │   │
│  │  - 编码用户正常行为模式                     │   │
│  │  - 重建误差 > 阈值 → 异常                  │   │
│  │  - 适用于复杂欺诈模式发现                   │   │
│  │  - 模型结构：Encoder(128-64-32) →          │   │
│  │    Decoder(32-64-128)                      │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  图算法（Neo4j）                           │   │
│  │  - 设备-用户-证件关系图                     │   │
│  │  - 社区发现（Louvain）                     │   │
│  │  - 关联分析（PageRank）                    │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  融合决策层                                │   │
│  │  - 加权投票 / Stacking                     │   │
│  │  - 输出：欺诈概率 + 风险等级               │   │
│  │  - 输出：欺诈类型 + 置信度                 │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 4.3 智能归因分析

#### 4.3.1 转化漏斗流失归因

**归因方法**：

| 方法 | 说明 | 适用场景 |
|-----|------|---------|
| **步骤级归因** | 计算每个步骤的流失率和流失绝对量 | 快速定位最大流失环节 |
| **Shapley Value 归因** | 基于博弈论的贡献度分配 | 多因素交互场景 |
| **决策树归因** | 构建决策树，按分裂节点归因 | 可解释性要求高 |
| **反事实归因** | "如果该因素不存在，转化率会怎样" | 因果推断场景 |

**流失归因维度**：

```
总流失率 = 35%（假设）
│
├── 证件类型选择页流失：5%（占比 14.3%）
│   ├── 原因：证件类型不支持（40%）
│   ├── 原因：页面加载慢（25%）
│   └── 原因：用户主动退出（35%）
│
├── 拍摄证件正面流失：10%（占比 28.6%）
│   ├── 原因：拍照失败/质量差（45%）
│   ├── 原因：相机权限被拒（20%）
│   ├── 原因：重拍次数过多放弃（25%）
│   └── 原因：页面超时（10%）
│
├── 拍摄证件反面流失：5%（占比 14.3%）
│   ├── 原因：拍照失败/质量差（50%）
│   └── 原因：用户主动退出（50%）
│
├── 人脸活体检测流失：8%（占比 22.9%）
│   ├── 原因：活体检测失败（40%）
│   ├── 原因：光线不足（25%）
│   ├── 原因：用户不理解指引（20%）
│   └── 原因：技术故障（15%）
│
├── 提交审核流失：4%（占比 11.4%）
│   └── 原因：提交失败/网络错误（60%）
│
└── 等待结果流失：3%（占比 8.6%）
    ├── 原因：等待时间过长（50%）
    └── 原因：审核被拒后放弃（50%）
```

#### 4.3.2 多维度下钻分析

**下钻维度**：

| 维度 | 下钻层级 | 分析场景 |
|-----|---------|---------|
| **国家/地区** | 大区 → 国家 → 城市 | 不同地区的 KYC 体验差异 |
| **设备** | 平台 → OS 版本 → 设备型号 | 特定设备的兼容性问题 |
| **证件类型** | 证件大类 → 具体证件 → 签发国 | 不同证件的通过率差异 |
| **时间段** | 月 → 周 → 日 → 小时 | 时间维度的流量和转化规律 |
| **网络环境** | 网络类型 → 运营商 → 延迟区间 | 网络质量对 KYC 体验的影响 |
| **用户属性** | 新老用户 → 注册渠道 → 用户等级 | 不同用户群体的行为差异 |
| **App 版本** | 大版本 → 小版本 → 构建号 | 版本更新对转化率的影响 |

**下钻分析示例**：

```
转化率：65%（整体）
│
├── 按国家下钻
│   ├── 新加坡：78%
│   ├── 印度尼西亚：52%  ← 异常低，需重点分析
│   │   ├── 按设备下钻
│   │   │   ├── Android 低端机：38%  ← 核心问题
│   │   │   └── Android 高端机：65%
│   │   └── 按证件类型下钻
│   │       ├── KTP（印尼身份证）：45%  ← OCR 识别率低
│   │       └── Passport：68%
│   └── 尼日利亚：61%
│
├── 按设备下钻
│   ├── iOS：75%
│   └── Android：58%  ← 需优化
│
└── 按时间段下钻
    ├── 工作日 9:00-18:00：72%
    ├── 工作日 18:00-24:00：65%
    └── 周末：58%  ← 可能与客服支持相关
```

#### 4.3.3 因果推断

**A/B 测试框架**：

| 组件 | 说明 |
|-----|------|
| **实验平台** | 自研 A/B 测试平台，支持流量分层、灰度发布 |
| **实验设计** | 最小样本量计算、随机化策略、分层因子 |
| **指标体系** | 核心指标（转化率）、护栏指标（错误率）、辅助指标（耗时） |
| **统计方法** | t 检验 / Mann-Whitney U 检验 / Bootstrap 置信区间 |
| **效果评估** | 绝对提升、相对提升、统计显著性（p < 0.05）、效应量（Cohen's d） |

**差分法（Difference-in-Differences）**：

适用于无法进行 A/B 测试的场景（如政策变更、外部环境影响）：

```
转化率变化 = (实验组后期 - 实验组前期) - (对照组后期 - 对照组前期)

示例：
- 新加坡上线新版拍照引导（实验组），马来西亚保持旧版（对照组）
- 实验前：SG 72%, MY 70%（基线差异 2pp）
- 实验后：SG 80%, MY 71%
- 净效果 = (80-72) - (71-70) = 8pp - 1pp = 7pp
- 结论：新版拍照引导带来 7pp 的转化率提升
```

### 4.4 用户分群与个性化

#### 4.4.1 基于行为特征的用户分群

**分群方法**：

| 方法 | 说明 | 适用场景 |
|-----|------|---------|
| **K-Means** | 基于距离的聚类，需要预设 K 值 | 大规模用户分群，快速迭代 |
| **DBSCAN** | 基于密度的聚类，自动发现簇数 | 发现异常用户群体 |
| **Gaussian Mixture Model** | 概率模型，软聚类 | 不确定性分析 |

**分群特征空间**：

| 特征维度 | 具体特征 | 权重 |
|---------|---------|------|
| 效率维度 | 平均步骤耗时、总完成时间、操作次数 | 0.3 |
| 质量维度 | 重拍次数、错误次数、图片质量评分 | 0.25 |
| 意愿维度 | 是否查看帮助、返回次数、暂停次数 | 0.2 |
| 技术维度 | 设备型号、网络类型、App 版本 | 0.15 |
| 环境维度 | 国家、时段、证件类型 | 0.1 |

**典型用户分群**：

| 分群名称 | 特征描述 | 占比 | 平均转化率 | 优化策略 |
|---------|---------|------|-----------|---------|
| **顺畅型** | 设备好、网络好、一次通过 | 35% | 95% | 保持体验，引导下一步操作 |
| **耐心型** | 耗时长但最终完成 | 20% | 88% | 优化耗时，提供进度提示 |
| **受挫型** | 多次重拍、多次错误但仍在尝试 | 15% | 65% | 加强引导、简化操作、提供人工帮助入口 |
| **技术困难型** | 低端设备、网络差、权限问题 | 15% | 45% | 降级方案、离线模式、网络优化 |
| **犹豫型** | 多次返回、长时间停留、查看帮助 | 10% | 55% | 增强信任感、简化流程、提供客服 |
| **快速流失型** | 进入后很快退出 | 5% | 12% | 优化首屏体验、降低认知负荷 |

#### 4.4.2 个性化引导策略

**策略引擎**：

```
用户进入 KYC 流程
    │
    ▼
实时特征获取（设备、网络、历史行为、分群标签）
    │
    ▼
策略匹配引擎
    │
    ├── 受挫型用户 → 显示简化引导 + 进度条 + 鼓励文案
    │
    ├── 技术困难型用户 → 自动检测设备能力
    │   ├── 低端设备 → 降低图片分辨率要求
    │   ├── 网络差 → 启用图片压缩 + 断点续传
    │   └── 权限问题 → 提供详细的权限开启引导
    │
    ├── 犹豫型用户 → 显示社交证明（"已有 XX 人完成认证"）
    │   ├── 提供客服入口
    │   └── 显示预计完成时间
    │
    ├── 快速流失型用户 → 显示最简流程
    │   ├── 预填已知信息
    │   └── 提供激励（如完成认证获得奖励）
    │
    └── 顺畅型用户 → 标准流程，不增加额外干扰
```

### 4.5 NLP 分析

#### 4.5.1 用户反馈文本分析

**数据来源**：

| 来源 | 数据量 | 采集方式 |
|-----|-------|---------|
| 客服工单 | ~500 条/天 | CRM 系统导出 |
| App Store / Google Play 评论 | ~200 条/天 | API 定期拉取 |
| App 内反馈 | ~100 条/天 | SDK 采集 |
| 社交媒体提及 | ~1000 条/天 | 社交媒体监听 API |
| KYC 流程中的用户留言 | ~50 条/天 | 表单采集 |

#### 4.5.2 情感分析 + 主题提取

**技术方案**：

```
用户反馈文本
    │
    ▼
文本预处理
    ├── 多语言分词（中文 jieba / 英文 spaCy）
    ├── 去除停用词、标点、特殊字符
    ├── 拼写纠正
    └── 统一大小写
    │
    ▼
情感分析（Fine-tuned BERT / RoBERTa）
    ├── 情感极性：正面 / 负面 / 中性
    ├── 情感强度：1-5 分
    └── 情感维度：满意度、挫败感、困惑度、信任感
    │
    ▼
主题提取（BERTopic / LDA）
    ├── 主题 1：拍照质量差（占比 25%）
    ├── 主题 2：活体检测失败（占比 20%）
    ├── 主题 3：等待时间过长（占比 18%）
    ├── 主题 4：界面不直观（占比 15%）
    ├── 主题 5：证件不被接受（占比 12%）
    └── 主题 6：其他（占比 10%）
    │
    ▼
关键词提取（TF-IDF + TextRank）
    │
    ▼
情感趋势分析（按天/周聚合）
    │
    ▼
异常情感检测（负面情感突增告警）
```

#### 4.5.3 自动生成优化建议

**建议生成逻辑**：

```python
# 伪代码示例
def generate_optimization_suggestions(analysis_result):
    suggestions = []

    # 基于情感分析
    if analysis_result.negative_sentiment_spike:
        suggestions.append({
            "priority": "high",
            "category": "user_experience",
            "description": f"近期负面情感评分上升 {analysis_result.sentiment_change}%，"
                          f"主要与'{analysis_result.top_negative_topic}'相关",
            "action_items": [
                f"排查{analysis_result.top_negative_topic}相关流程",
                "安排用户访谈深入了解问题",
                "考虑临时增加客服支持"
            ]
        })

    # 基于主题分析
    if analysis_result.top_topic == "photo_quality":
        suggestions.append({
            "priority": "medium",
            "category": "product",
            "description": "拍照质量相关反馈占比最高（25%），建议优化拍照引导",
            "action_items": [
                "增加实时拍照质量反馈",
                "优化拍照框和光线提示",
                "降低对低端设备的图片质量要求"
            ]
        })

    # 基于流失归因
    if analysis_result.top_churn_step == "liveness":
        suggestions.append({
            "priority": "high",
            "category": "product",
            "description": "活体检测步骤流失率最高（22.9%），需重点优化",
            "action_items": [
                "A/B 测试不同的活体检测方案",
                "优化活体检测引导动画",
                "增加活体检测失败后的重试引导"
            ]
        })

    return suggestions
```

### 4.6 制裁命中风险评估模型

#### 4.6.1 问题定义

**目标**：预测制裁名单命中的误报率（False Positive Rate），优化匹配算法阈值，减少不必要的人工复核工作量。

**建模方式**：二分类模型（真命中 vs 误报），对每次制裁命中进行误报概率预测。

#### 4.6.2 特征工程

| 特征类别 | 特征名称 | 类型 | 说明 | 示例 |
|---------|---------|------|------|------|
| **匹配特征** | `match_score` | Numerical | 模糊匹配分数 | `0.92` |
| | `list_type` | Categorical | 制裁名单类型 | `OFAC` / `EU` / `UN` |
| | `match_algorithm` | Categorical | 匹配算法 | `fuzzy` / `phonetic` / `exact` |
| | `matched_field_count` | Integer | 匹配字段数量 | `3`（姓名+国家+出生日期） |
| **用户特征** | `user_country` | Categorical | 用户所在国家 | `SG` |
| | `user_nationality` | Categorical | 用户国籍 | `CN` |
| | `kyc_risk_level` | Categorical | KYC 风险等级 | `low` / `medium` / `high` |
| | `account_age_days` | Numerical | 账号注册天数 | `365` |
| **历史行为** | `previous_sanction_hits` | Integer | 历史制裁命中次数 | `0` |
| | `previous_false_positive_rate` | Float | 历史误报率 | `0.85` |
| | `transaction_volume_30d` | Numerical | 近 30 天交易量 | `50000` |
| **实体特征** | `entity_type` | Categorical | 匹配到的实体类型 | `individual` / `entity` / `vessel` |
| | `sanction_program` | Categorical | 制裁计划 | `SDGT` / `SDN` / `EU_Consolidated` |
| | `name_similarity_score` | Float | 姓名相似度 | `0.88` |

#### 4.6.3 模型训练与评估

**主模型**：LightGBM（适合结构化表格数据，训练速度快）

| 指标 | 目标值 | 说明 |
|-----|-------|------|
| AUC-ROC | > 0.90 | 区分真命中与误报的能力 |
| Precision@10% | > 0.85 | 高风险中真命中的比例 |
| False Negative Rate | < 5% | 漏掉真命中的比例（严格控制） |
| 特征稳定性 (PSI) | < 0.1 | 特征分布稳定性 |

**模型输出**：

```json
{
  "hit_id": "hit_xyz789",
  "user_id": "uid_10001",
  "false_positive_probability": 0.92,
  "risk_level": "low",
  "top_factors": [
    {"factor": "name_similarity_score", "contribution": 0.35, "value": 0.72},
    {"factor": "previous_false_positive_rate", "contribution": 0.28, "value": 0.90},
    {"factor": "user_country_mismatch", "contribution": 0.20, "value": true}
  ],
  "recommendation": "auto_close",
  "prediction_timestamp": 1714353700000
}
```

### 4.7 交易行为异常检测模型增强

#### 4.7.1 新增链上行为特征

在原有欺诈检测模型基础上，新增以下链上行为特征维度：

| 特征类别 | 特征名称 | 类型 | 说明 | 示例 |
|---------|---------|------|------|------|
| **跨链行为** | `cross_chain_hop_count` | Integer | 30 天内跨链跳转次数 | `5` |
| | `cross_chain_volume_ratio` | Float | 跨链交易金额占总交易比例 | `0.65` |
| | `cross_chain_chain_types` | Array | 涉及的链类型 | `["ETH", "BSC", "TRON"]` |
| **混币器交互** | `mixer_interaction_count` | Integer | 30 天内与混币器交互次数 | `2` |
| | `mixer_volume` | Numerical | 混币器交互金额 | `10000` |
| | `mixer_type` | Categorical | 混币器类型 | `tornado_cash` / `bitcoin_fog` |
| **暗网关联** | `darknet_exposure_score` | Float | 暗网关联评分（0-1） | `0.15` |
| | `darknet_interaction_flag` | Boolean | 是否有暗网地址交互 | `false` |
| **链上行为模式** | `tx_time_distribution_entropy` | Float | 交易时间分布熵值 | `0.85` |
| | `counterparty_diversity_score` | Float | 交易对手多样性评分 | `0.45` |
| | `gas_price_anomaly_score` | Float | Gas 价格异常评分 | `0.20` |

#### 4.7.2 与 Chainalysis/Elliptic 风险评分融合

**融合策略**：

```
用户风险评分 = w1 * 内部模型评分 + w2 * Chainalysis 评分 + w3 * Elliptic 评分

默认权重：w1 = 0.4, w2 = 0.35, w3 = 0.25

动态权重调整规则：
- 当 Chainalysis/Elliptic 评分不可用时，自动将权重分配给内部模型
- 当内部模型与外部评分差异 > 0.3 时，触发人工复核
- 按月评估各评分源的预测能力，动态调整权重
```

| 融合方案 | 说明 | 适用场景 |
|---------|------|---------|
| **加权平均** | 各评分源加权求和 | 日常风险评分 |
| **取最大值** | 取各评分源最大值 | 高安全要求场景 |
| **Stacking 融合** | 用元模型学习最优融合方式 | 精细化风控 |

### 4.8 ZK 服务使用预测模型

#### 4.8.1 问题定义

**目标**：预测外部客户对 ZK 属性的选择偏好，优化定价策略和资源规划。

**建模方式**：多标签分类模型（预测客户可能选择的属性组合）+ 回归模型（预测请求量）。

#### 4.8.2 特征工程

| 特征类别 | 特征名称 | 类型 | 说明 | 示例 |
|---------|---------|------|------|------|
| **客户特征** | `client_type` | Categorical | 客户类型 | `exchange` / `defi` / `platform` |
| | `client_size` | Categorical | 客户规模 | `small` / `medium` / `large` / `enterprise` |
| | `client_region` | Categorical | 客户所在区域 | `APAC` / `EMEA` / `Americas` |
| | `plan_type` | Categorical | 订阅计划 | `free` / `basic` / `enterprise` |
| **历史行为** | `historical_request_volume` | Numerical | 历史请求量 | `5000` |
| | `historical_attribute_set` | Array | 历史使用的属性集合 | `["kyc_verified", "age_above_18"]` |
| | `request_growth_rate` | Float | 请求量月增长率 | `0.15` |
| **行业特征** | `industry_sector` | Categorical | 行业领域 | `centralized_exchange` / `defi_protocol` / `nft_platform` |
| | `regulatory_jurisdiction` | Categorical | 监管辖区 | `SG` / `EU` / `US` |
| **时间特征** | `month` | Integer | 月份 | `4` |
| | `quarter` | Integer | 季度 | `2` |
| | `is_pre_regulation_deadline` | Boolean | 是否临近监管截止日 | `true` |

#### 4.8.3 模型训练与评估

**主模型**：XGBoost Multi-output + LightGBM 回归

| 指标 | 目标值 | 说明 |
|-----|-------|------|
| 属性预测准确率 (Top-3) | > 0.80 | 预测的前 3 个属性中包含实际选择的概率 |
| 请求量预测 MAPE | < 15% | 月度请求量预测的平均绝对百分比误差 |
| 特征稳定性 (PSI) | < 0.1 | 特征分布稳定性 |

**业务应用**：

| 应用场景 | 说明 | 预期收益 |
|---------|------|---------|
| **定价优化** | 基于预测的属性偏好，制定差异化定价策略 | 收入提升 10-15% |
| **资源规划** | 基于预测的请求量，提前规划 ZK 证明生成资源 | 成本优化 5-10% |
| **客户推荐** | 向客户推荐可能需要的属性组合 | 客户留存率提升 |
| **库存管理** | 预热高频属性组合的电路，降低生成延迟 | P95 延迟降低 20% |

---

## 5. 数据看板与可视化

### 5.1 看板体系总览

```
KYC 数据看板体系
├── 实时监控看板（Real-time Dashboard）
│   ├── 实时认证量 & 认证速率
│   ├── 实时转化漏斗
│   ├── 审核队列状态
│   ├── 系统健康指标
│   └── 异常告警面板
│
├── 趋势分析看板（Trend Dashboard）
│   ├── 日/周/月趋势
│   ├── 分维度趋势对比
│   ├── 同期对比（YoY / WoW）
│   └── 移动平均趋势线
│
├── 运营分析看板（Operations Dashboard）
│   ├── 流失分析
│   ├── 失败原因分布
│   ├── 审核员效率
│   ├── 地域热力图
│   └── 用户分群分布
│
├── AI 洞察看板（AI Insights Dashboard）
│   ├── 流失预测热力图
│   ├── 异常事件流
│   ├── 优化建议列表
│   ├── NLP 情感趋势
│   └── 欺诈风险地图
│
├── 合规监控看板（Compliance Dashboard）
│   ├── 制裁/PEP/不良媒体命中趋势图
│   ├── 告警分布热力图（按类型/等级/国家）
│   ├── 人工复核效率指标（平均处理时长、积压量）
│   └── SAR/STR 报告统计
│
└── ZK 服务运营看板（ZK Service Dashboard）
    ├── ZK 证明请求量趋势（按客户/属性/类型）
    ├── ZK 证明生成性能监控（P50/P95/P99 延迟）
    ├── ZK 证明验证成功率
    ├── 外部客户使用量排行
    └── 属性组合分布（哪些属性组合最受欢迎）
```

### 5.2 实时监控看板

#### 5.2.1 核心指标卡片

| 指标 | 展示形式 | 刷新频率 | 说明 |
|-----|---------|---------|------|
| 实时认证量（今日） | 大数字 + 迷你趋势图 | 10 秒 | 今日已完成 KYC 的用户数 |
| 实时认证速率 | 大数字 + 迷你趋势图 | 10 秒 | 每分钟正在进行的 KYC 会话数 |
| 整体转化率 | 环形图 + 数字 | 30 秒 | 今日 KYC 完成率 |
| 平均完成时间 | 大数字 + 分布图 | 30 秒 | 今日平均 KYC 完成时间 |
| 实时错误率 | 大数字 + 颜色编码 | 10 秒 | 近 5 分钟错误率 |
| 审核队列深度 | 大数字 + 趋势 | 30 秒 | 当前待审核数量 |

#### 5.2.2 实时转化漏斗

```
┌─────────────────────────────────────────────────────────────┐
│                    实时转化漏斗（今日）                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  选择证件类型          50,000  ████████████████████ 100%│   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  拍摄证件正面          45,000  ██████████████████   90% │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  拍摄证件反面          40,500  ████████████████     81% │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  人脸活体检测          35,000  ██████████████       70% │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  提交审核              33,000  █████████████        66% │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  审核通过              30,000  ████████████         60% │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  最大流失环节：人脸活体检测（流失 5,500 人，流失率 13.6%）     │
│  [下钻分析] [查看详情] [导出数据]                              │
└─────────────────────────────────────────────────────────────┘
```

#### 5.2.3 异常告警面板

```
┌─────────────────────────────────────────────────────────────┐
│  异常告警                                                     │
│                                                              │
│  🔴 [严重] API 响应时间突增                                    │
│     OCR 服务 P99 延迟从 350ms 上升至 2800ms                   │
│     影响范围：所有使用护照的用户                                │
│     持续时间：5 分钟                                          │
│     [查看详情] [触发预案]                                     │
│                                                              │
│  🟡 [警告] 拍摄证件正面转化率下降                              │
│     近 30 分钟转化率从 90% 下降至 82%                          │
│     主要影响：Android 8.x 设备                                │
│     [查看详情] [开始调查]                                     │
│                                                              │
│  🟢 [信息] 审核队列深度增加                                    │
│     当前队列深度 200（正常范围 < 150）                         │
│     预计 45 分钟后恢复正常                                     │
│     [查看详情]                                                │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 趋势分析看板

#### 5.3.1 核心图表

| 图表类型 | 展示内容 | 交互能力 |
|---------|---------|---------|
| **折线图** | 日/周/月转化率趋势 | 时间范围选择、多维度叠加、同期对比 |
| **堆叠面积图** | 各步骤流失量趋势 | 维度切换、下钻 |
| **热力图** | 小时 x 星期 转化率矩阵 | 点击单元格查看明细 |
| **箱线图** | 完成时间分布趋势 | 异常值标注、分位数展示 |
| **瀑布图** | 转化率变化归因 | 展示各因素对转化率变化的贡献 |

#### 5.3.2 同期对比分析

```
转化率同期对比（本周 vs 上周）

  95% ┤
      │          ╭──╮
  90% ┤      ╭──╯  ╰──╮
      │  ╭──╯          ╰──╮
  85% ┤──╯                ╰──────── 本周
      │  ╭──╮    ╭──╮
  80% ┤──╯  ╰────╯  ╰────────── 上周
      │
  75% ┤
      │
  Mon   Tue   Wed   Thu   Fri   Sat   Sun

  本周平均：87.2%  |  上周平均：82.5%  |  环比提升：+4.7pp
```

### 5.4 运营分析看板

#### 5.4.1 流失分析

**流失漏斗桑基图**：

```
                    ┌──→ 证件类型不支持 ──→ 退出 (2%)
                    │
                    ├──→ 页面加载慢 ──→ 退出 (1.3%)
                    │
选择证件类型 ──→ 5% ──┤
  (100%)             └──→ 主动退出 ──→ 退出 (1.7%)
                    │
                    ├──→ 拍照失败 ──→ 重拍 ──→ 放弃 (4.5%)
                    │
拍摄证件正面 ──→ 10% ──┤
  (90%)              ├──→ 权限被拒 ──→ 退出 (2%)
                    │
                    └──→ 重拍过多 ──→ 放弃 (3.5%)
```

#### 5.4.2 失败原因分布

| 图表类型 | 展示内容 |
|---------|---------|
| **饼图** | 各类失败原因占比 |
| **帕累托图** | 失败原因累计分布（80/20 分析） |
| **矩阵图** | 失败原因 x 证件类型 热力图 |
| **趋势图** | 各失败原因的时间趋势 |

#### 5.4.3 审核员效率

| 指标 | 展示形式 | 说明 |
|-----|---------|------|
| 审核吞吐量 | 柱状图（按审核员） | 每人每小时处理量 |
| 审核准确率 | 散点图（吞吐量 vs 准确率） | 识别高效且准确的审核员 |
| 审核耗时分布 | 直方图 | 单次审核耗时分布 |
| 审核一致性 | 热力图 | 不同审核员对同类案件的判定一致性 |

#### 5.4.4 地域热力图

- 基于 Mapbox / Leaflet 的交互式地图
- 按国家/地区着色，颜色深浅表示转化率高低
- 支持点击下钻到城市级别
- 叠加认证量气泡图

### 5.5 AI 洞察看板

#### 5.5.1 流失预测热力图

```
流失风险热力图（实时）

步骤 \ 时段    00-06   06-12   12-18   18-24
选择证件类型    🟢      🟢      🟢      🟢
拍摄正面       🟡      🟢      🟡      🔴
拍摄反面       🟢      🟢      🟡      🟡
活体检测       🔴      🟡      🟡      🔴
提交审核       🟢      🟢      🟢      🟡
等待结果       🟡      🟢      🟢      🟡

图例：🟢 低风险(<20%)  🟡 中风险(20-50%)  🔴 高风险(>50%)

[查看详情] [导出报告] [设置告警]
```

#### 5.5.2 异常事件流

```
异常事件时间线（近 24 小时）

14:30  🔴 OCR 服务延迟突增（P99: 2800ms）  → 已恢复
14:15  🟡 Android 8.x 拍照成功率下降       → 调查中
13:45  🟢 审核队列深度增加（200）            → 已自动扩容
12:00  🟢 午间流量高峰（认证速率 +40%）      → 正常
10:30  🟡 印尼地区转化率下降（-8pp）         → 调查中
09:00  🟢 系统巡检完成，无异常               → 正常
```

#### 5.5.3 优化建议列表

```
AI 优化建议（按优先级排序）

1. [高优先级] 活体检测步骤优化
   - 当前流失率：22.9%（目标 < 10%）
   - 建议操作：
     a) A/B 测试新的活体检测算法（预计提升 5pp）
     b) 优化光线不足场景的引导文案
     c) 增加活体检测失败后的降级方案
   - 预期收益：转化率提升 3-5pp
   - [创建实验] [查看分析] [标记处理]

2. [高优先级] Android 低端设备拍照优化
   - 影响用户：约 15% 的 Android 用户
   - 建议操作：
     a) 降低低端设备的图片分辨率要求
     b) 优化相机初始化速度
     c) 增加拍照前的设备兼容性检测
   - 预期收益：Android 转化率提升 5-8pp
   - [创建实验] [查看分析] [标记处理]

3. [中优先级] 印尼 KTP 证件 OCR 优化
   - KTP 识别失败率：15%（其他证件 5%）
   - 建议操作：
     a) 收集更多 KTP 训练数据
     b) 优化 KTP 版本识别逻辑
   - 预期收益：印尼地区转化率提升 8-10pp
   - [创建实验] [查看分析] [标记处理]
```

### 5.6 合规监控看板

#### 5.6.1 制裁/PEP/不良媒体命中趋势图

| 图表类型 | 展示内容 | 交互能力 |
|---------|---------|---------|
| **多系列折线图** | 制裁/PEP/不良媒体命中量按日/周/月趋势 | 时间范围选择、名单类型筛选、同期对比 |
| **堆叠柱状图** | 各制裁名单（OFAC/EU/UN/UK_HMT/AU_DFAT）命中量分布 | 按名单类型下钻、按国家筛选 |
| **桑基图** | 命中 → 人工复核 → 最终处置结果的全流程 | 查看各环节转化率、误报率 |

#### 5.6.2 告警分布热力图

```
告警分布热力图（按类型 x 等级 x 国家）

告警类型 \ 等级    P0（严重）  P1（警告）  P2（信息）
交易异常            ██ 12      ████ 45     ██████ 120
风险评分变化        █ 5        ██ 18       ████ 85
KYC 过期            ░ 0        █ 3         ██ 15
行为异常            █ 8        ██ 22       ██████ 98
账户激活            ░ 0        █ 2         ███ 30

图例：█ = 告警数量  ░ = 0

[按国家下钻] [按时间段筛选] [导出报告]
```

#### 5.6.3 人工复核效率指标

| 指标 | 展示形式 | 刷新频率 | 说明 |
|-----|---------|---------|------|
| 平均复核处理时长 | 大数字 + 趋势图 | 30 分钟 | 筛查结果人工复核的平均耗时 |
| 复核积压量 | 大数字 + 颜色编码 | 10 分钟 | 当前待复核的筛查命中数量 |
| 误报率 | 环形图 + 数字 | 1 小时 | 复核后判定为误报的比例 |
| 复核员效率排行 | 水平柱状图 | 1 天 | 按复核员展示处理量和准确率 |
| 复核结果分布 | 饼图 | 1 天 | confirmed_hit / false_positive / escalated 占比 |

#### 5.6.4 SAR/STR 报告统计

| 图表类型 | 展示内容 | 交互能力 |
|---------|---------|---------|
| **折线图** | SAR/STR 报告生成量月度趋势 | 时间范围选择、按类型筛选 |
| **柱状图** | SAR 报告按触发原因分布 | 下钻到具体案例 |
| **表格** | SAR 报告提交状态跟踪（待提交/已提交/被退回） | 筛选、排序、导出 |
| **饼图** | 自动生成 vs 手动生成占比 | 按时间段对比 |

### 5.7 ZK 服务运营看板

#### 5.7.1 ZK 证明请求量趋势

| 图表类型 | 展示内容 | 交互能力 |
|---------|---------|---------|
| **多系列折线图** | ZK 证明请求量按日/周/月趋势（按客户/属性/类型分组） | 维度切换、时间范围选择 |
| **堆叠面积图** | 各属性类型的请求量占比趋势 | 属性类型筛选 |
| **柱状图** | 按客户维度的请求量排行 | 客户下钻到具体请求明细 |

#### 5.7.2 ZK 证明生成性能监控

| 指标 | 展示形式 | 刷新频率 | 说明 |
|-----|---------|---------|------|
| P50 生成延迟 | 大数字 + 趋势图 | 5 分钟 | 50% 请求的生成耗时 |
| P95 生成延迟 | 大数字 + 趋势图 | 5 分钟 | 95% 请求的生成耗时 |
| P99 生成延迟 | 大数字 + 趋势图 | 5 分钟 | 99% 请求的生成耗时 |
| 平均证明大小 | 大数字 + 分布图 | 1 小时 | 生成证明的平均字节大小 |
| 生成失败率 | 大数字 + 颜色编码 | 10 分钟 | 证明生成失败的比例 |

```
ZK 证明生成延迟分布（近 24 小时）

延迟区间        请求量    占比
0-1s           ████████████████████  45%
1-3s           ████████████████      30%
3-5s           ████████              15%
5-10s          ████                   7%
>10s           ██                     3%

P50: 850ms | P95: 3,200ms | P99: 8,500ms
[查看慢请求详情] [按属性类型筛选]
```

#### 5.7.3 ZK 证明验证成功率

| 指标 | 展示形式 | 刷新频率 | 说明 |
|-----|---------|---------|------|
| 整体验证成功率 | 环形图 + 数字 | 10 分钟 | valid / (valid + invalid) |
| 链上验证成功率 | 环形图 + 数字 | 10 分钟 | onchain 验证的成功率 |
| 链下验证成功率 | 环形图 + 数字 | 10 分钟 | offchain 验证的成功率 |
| 验证失败原因分布 | 饼图 | 1 小时 | 按失败原因分类统计 |

#### 5.7.4 外部客户使用量排行

| 图表类型 | 展示内容 | 交互能力 |
|---------|---------|---------|
| **水平柱状图** | 按请求量排序的外部客户 Top 10 | 客户下钻、时间段选择 |
| **表格** | 客户详细指标（请求量、成功率、订阅计划、接入时间） | 排序、筛选、导出 |
| **折线图** | 各客户请求量趋势对比 | 多客户叠加对比 |

#### 5.7.5 属性组合分布

| 图表类型 | 展示内容 | 交互能力 |
|---------|---------|---------|
| **树状图（Treemap）** | 各属性组合的请求量占比 | 点击下钻到具体组合详情 |
| **桑基图** | 属性选择 → 证明生成 → 验证的全流程 | 查看各属性组合的转化率 |
| **表格** | 属性组合排行（Top 20） | 排序、筛选 |

```
属性组合热度排行（近 30 天）

排名  属性组合                                    请求量    占比
1     kyc_verified + age_above_18                 12,500   28%
2     kyc_verified + country_not_sanctioned        8,200   18%
3     age_above_18 + country_of_residence          6,800   15%
4     kyc_verified + age_above_18 + aml_cleared    5,100   11%
5     country_not_sanctioned + aml_cleared         4,300    10%
6     其他组合                                      7,600    18%

[查看完整列表] [导出数据]
```

### 5.8 看板交互能力

| 交互能力 | 说明 | 技术实现 |
|---------|------|---------|
| **下钻** | 点击图表元素下钻到更细粒度 | ClickHouse 物化视图 + 前端联动 |
| **筛选** | 多维度组合筛选（国家、设备、时间等） | GraphQL 动态查询构建 |
| **对比** | 两个时间段/维度的数据对比 | 并行查询 + 差异高亮 |
| **导出** | 导出为 CSV / Excel / PDF | 后端异步导出 + 文件下载 |
| **分享** | 生成看板快照链接 | 看板状态序列化 + URL 编码 |
| **订阅** | 定时邮件推送看板报告 | 定时任务 + PDF 生成 |
| **标注** | 在图表上添加事件标注（如版本发布） | 自定义事件标记 API |

---

## 6. 自动化运营闭环

### 6.1 告警机制

#### 6.1.1 三级告警体系

| 告警级别 | 颜色 | 触发条件 | 响应时间 | 通知渠道 | 处理流程 |
|---------|------|---------|---------|---------|---------|
| **P0 - 严重** | 红色 | KYC 服务不可用、转化率下降 > 50%、数据安全事件 | 5 分钟内响应 | PagerDuty + 电话 + Slack + 邮件 | 自动触发应急预案 + 值班人员立即介入 |
| **P1 - 警告** | 黄色 | 转化率下降 10-50%、API 延迟 > 3x 基线、错误率 > 5%、队列积压 > 2x SLA | 30 分钟内响应 | Slack + 邮件 | 相关负责人调查 + 1 小时内给出初步结论 |
| **P2 - 信息** | 绿色 | 转化率下降 < 10%、轻微性能波动、数据质量轻微异常 | 4 小时内响应 | 邮件 + 看板标记 | 下个工作日处理 + 记录到问题跟踪系统 |

#### 6.1.2 告警规则配置

```yaml
# 告警规则示例
alerts:
  - name: kyc_conversion_rate_drop_severe
    level: P0
    metric: kyc_funnel_conversion_rate
    condition: "current_30m < baseline_30m * 0.5"
    baseline: rolling_average_7d
    cooldown: 30m
    notifications:
      - channel: pagerduty
        escalation_policy: kyc_oncall
      - channel: slack
        webhook: https://hooks.slack.com/xxx
      - channel: email
        recipients: ["kyc-team@company.com", "oncall@company.com"]

  - name: kyc_api_latency_high
    level: P1
    metric: kyc_api_p99_latency_ms
    condition: "current_5m > baseline_5m * 3 AND current_5m > 3000"
    baseline: rolling_average_1h
    cooldown: 15m
    notifications:
      - channel: slack
        webhook: https://hooks.slack.com/xxx
      - channel: email
        recipients: ["kyc-eng@company.com"]

  - name: kyc_review_queue_backlog
    level: P1
    metric: kyc_review_queue_depth
    condition: "current > sla_target * 2"
    sla_target: 150
    cooldown: 30m
    notifications:
      - channel: slack
        webhook: https://hooks.slack.com/xxx
      - channel: email
        recipients: ["kyc-ops@company.com"]
```

### 6.2 自动化 Action

#### 6.2.1 自动化预案

| 触发条件 | 自动化 Action | 预期效果 |
|---------|--------------|---------|
| OCR 服务延迟 > 3x 基线 | 自动扩容 OCR 服务实例 | 5 分钟内恢复服务能力 |
| 审核队列深度 > 2x SLA | 自动通知审核团队 + 临时增加审核员 | 15 分钟内缓解积压 |
| 转化率异常下降 > 20% | 自动创建调查工单 + 通知产品和技术负责人 | 30 分钟内启动调查 |
| 拍照失败率 > 30% | 自动切换到备用 OCR 模型 | 降低失败率 |
| 欺诈检测命中 | 自动标记高风险用户 + 人工审核队列 | 防止欺诈通过 |
| 数据管道延迟 > 10 分钟 | 自动重启 Flink 作业 + 告警 | 恢复数据流 |

#### 6.2.2 自动化工作流引擎

```
异常检测引擎
    │
    ▼
告警评估（级别判定）
    │
    ├── P0 → 立即执行应急预案
    │         ├── 自动扩容/降级
    │         ├── 通知所有相关方
    │         └── 创建 P0 工单
    │
    ├── P1 → 触发调查工作流
    │         ├── 自动归因分析
    │         ├── 生成初步报告
    │         └── 通知负责人
    │
    └── P2 → 记录到跟踪系统
              ├── 自动记录到 Jira
              └── 纳入下次复盘
```

### 6.3 A/B 测试平台

#### 6.3.1 平台能力

| 能力 | 说明 |
|-----|------|
| **实验管理** | 创建、编辑、停止实验，支持多变量实验 |
| **流量分配** | 支持按百分比、用户标签、地理位置等维度分配流量 |
| **分层实验** | 支持流量分层，同一用户可同时参与多个正交实验 |
| **指标追踪** | 自动追踪核心指标和护栏指标 |
| **统计引擎** | 自动计算统计显著性、置信区间、效应量 |
| **实验报告** | 自动生成实验报告，包含结论和建议 |

#### 6.3.2 KYC 实验示例

```
实验名称：新版拍照引导 A/B 测试
实验假设：增加实时拍照质量反馈可以降低重拍率 30%
实验设计：
  - 对照组（50%）：当前拍照引导
  - 实验组（50%）：新版拍照引导（增加实时质量反馈 + 优化动画）
核心指标：
  - 重拍率（预期从 2.5 次降至 1.75 次）
  - 拍照步骤转化率（预期提升 5pp）
护栏指标：
  - 整体 KYC 完成时间（不增加）
  - 错误率（不增加）
最小样本量：每组 10,000 用户（基于 80% 功效、5% 显著性水平）
实验周期：14 天
```

### 6.4 优化建议引擎

#### 6.4.1 建议生成逻辑

```
数据输入
├── 实时指标（转化率、错误率、延迟）
├── AI 模型输出（流失预测、异常检测、归因分析）
├── NLP 分析结果（用户反馈主题、情感趋势）
└── 历史数据（A/B 测试结果、优化历史）
    │
    ▼
规则引擎 + ML 模型
├── 基于规则的启发式建议（已知模式匹配）
├── 基于 ML 的建议排序（预测建议效果）
└── 基于因果推断的建议验证
    │
    ▼
建议输出
├── 优先级排序（预期收益 x 实施难度）
├── 具体行动项
├── 预期效果估算
└── 关联的 A/B 测试建议
```

#### 6.4.2 建议类型

| 建议类型 | 触发条件 | 示例 |
|---------|---------|------|
| **产品优化** | 特定步骤流失率高于阈值 | "活体检测步骤增加降级方案" |
| **技术优化** | API 延迟/错误率异常 | "优化 OCR 服务图片预处理逻辑" |
| **运营优化** | 特定用户群体转化率低 | "针对印尼用户增加 KTP 拍照引导" |
| **内容优化** | NLP 分析发现用户困惑 | "简化证件类型选择页面的文案" |
| **实验建议** | 多个优化方向待验证 | "建议对 3 种活体检测方案进行 A/B 测试" |

---

## 7. 数据安全与隐私

### 7.1 数据脱敏规则

| 数据类别 | 脱敏规则 | 脱敏示例 | 存储方式 |
|---------|---------|---------|---------|
| 用户 ID | 不可逆哈希 | `uid_10001` → `h_a1b2c3d4` | 脱敏后存储 |
| 设备 ID | 不可逆哈希 | `did_xxxxx` → `h_e5f6g7h8` | 脱敏后存储 |
| 证件号码 | 全部遮盖 | `S1234567A` → `*******` | 不存储原始值 |
| 证件图片 | 不采集/不存储 | — | 仅存储元数据（质量评分等） |
| 人脸图片 | 不采集/不存储 | — | 仅存储元数据（活体检测结果等） |
| 姓名 | 部分遮盖 | `Zhang San` → `Z*** S**` | 脱敏后存储 |
| IP 地址 | 前 3 段保留 | `192.168.1.100` → `192.168.1.*` | 脱敏后存储 |
| GPS 坐标 | 降低精度到城市级别 | 精确坐标 → 城市中心点 | 仅存储城市 |
| 手机号 | 中间 4 位遮盖 | `+65 9123 4567` → `+65 9*** *567` | 脱敏后存储 |
| 邮箱 | 域名保留 | `user@example.com` → `u***@example.com` | 脱敏后存储 |

### 7.2 访问权限控制

#### 7.2.1 RBAC 权限模型

| 角色 | 实时看板 | 趋势分析 | 运营分析 | AI 洞察 | 原始数据 | 导出 | 管理 |
|-----|---------|---------|---------|---------|---------|------|------|
| **管理员** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **产品经理** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| **运营人员** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| **风控人员** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| **技术负责人** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **只读用户** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

#### 7.2.2 数据访问审计

- 所有数据访问记录到审计日志
- 审计日志包含：访问人、访问时间、访问内容、访问来源 IP
- 敏感数据访问触发二次审批
- 异常访问模式自动告警（如非工作时间大量导出）

### 7.3 数据保留策略

| 数据类型 | 保留期限 | 销毁方式 |
|---------|---------|---------|
| 埋点事件原始数据 | 2 年 | 安全删除（S3 Object Lock 到期自动删除） |
| 聚合统计数据 | 3 年 | 安全删除 |
| 审计日志 | 7 年 | 安全删除 |
| ML 模型训练数据 | 2 年 | 安全删除 |
| 用户画像数据 | 账号存续期 + 30 天 | 账号注销后 30 天内删除 |
| A/B 测试数据 | 1 年 | 安全删除 |

### 7.4 GDPR / CCPA 合规

| 合规要求 | 实现措施 |
|---------|---------|
| **数据最小化** | 仅采集分析所需的最少数据字段，不采集证件图片、人脸图片等敏感数据 |
| **目的限制** | 数据仅用于 KYC 体验优化，不用于其他商业目的 |
| **用户同意** | 在 KYC 流程开始前获取用户同意，明确说明数据用途 |
| **访问权** | 用户可请求查看其相关数据（通过隐私设置页面） |
| **删除权** | 用户可请求删除其所有数据（通过账号注销流程） |
| **可携带权** | 用户可请求导出其数据（JSON 格式） |
| **数据保护影响评估（DPIA）** | 上线前完成 DPIA 评估 |
| **跨境数据传输** | 数据存储在用户所在区域的数据中心，跨境传输使用加密通道 |
| **数据加密** | 传输中加密（TLS 1.3）+ 静态加密（AES-256） |
| **第三方数据处理** | 与所有第三方数据处理方签订 DPA（数据处理协议） |

---

## 8. 实施路线图

### 8.1 Phase 1：基础建设（第 1-2 月）

#### 8.1.1 目标

搭建完整的数据采集和存储基础设施，上线基础数据看板，实现数据可见。

#### 8.1.2 里程碑与交付物

| 周 | 里程碑 | 交付物 |
|----|-------|-------|
| W1-W2 | 埋点 SDK 开发 | Web/iOS/Android SDK v1.0，支持自动采集和手动埋点 |
| W3 | 埋点事件定义完成 | 完整的埋点事件文档（本文档第 2 节），Schema Registry 配置 |
| W4 | 数据管道搭建 | Kafka 集群部署，Flink 校验和聚合作业上线 |
| W5-W6 | 数据仓库建设 | ClickHouse 集群部署，核心表结构设计，Spark ETL 作业开发 |
| W7 | 数据质量保障 | 数据校验规则上线，数据质量监控看板 |
| W8 | 基础看板上线 | 实时监控看板（认证量、转化漏斗、错误率），趋势分析看板 |

#### 8.1.3 关键指标

- 埋点覆盖率：100%（所有 KYC 页面和关键交互）
- 数据准确率：> 99%
- 看板数据延迟：< 30 秒
- 数据管道可用性：> 99.9%

### 8.2 Phase 2：AI 赋能（第 3-4 月）

#### 8.2.1 目标

训练和上线 AI 模型，实现智能分析和预测能力。

#### 8.2.2 里程碑与交付物

| 周 | 里程碑 | 交付物 |
|----|-------|-------|
| W9-W10 | ML 特征工程建设 | 离线特征计算管道，在线特征服务（Redis Feature Store） |
| W11-W12 | 流失预测模型训练 | XGBoost 模型 v1.0，AUC > 0.80 |
| W13 | 异常检测模型上线 | Isolation Forest + 规则引擎，覆盖 API 延迟和错误率检测 |
| W14 | 智能归因分析 | 流失归因分析模块，多维度下钻分析 |
| W15 | 用户分群 | K-Means 用户分群模型，分群标签服务 |
| W16 | AI 洞察看板上线 | 流失预测热力图、异常事件流、优化建议列表 |

#### 8.2.3 关键指标

- 流失预测 AUC：> 0.80
- 异常检测准确率：> 85%（误报率 < 15%）
- 用户分群覆盖率：> 90%
- 归因分析覆盖所有 KYC 步骤

### 8.3 Phase 3：闭环优化（第 5-6 月）

#### 8.3.1 目标

实现自动化运营闭环，持续优化 KYC 转化率。

#### 8.3.2 里程碑与交付物

| 周 | 里程碑 | 交付物 |
|----|-------|-------|
| W17-W18 | 告警系统上线 | 三级告警体系，多通道通知，告警规则配置平台 |
| W19 | 自动化 Action 上线 | 自动扩容、自动切换、自动工单创建 |
| W20-W21 | A/B 测试平台上线 | 实验管理、流量分配、统计引擎、实验报告 |
| W22 | NLP 分析上线 | 用户反馈情感分析、主题提取、自动建议生成 |
| W23 | 个性化策略引擎 | 基于用户分群的个性化引导策略 |
| W24 | 全面验收 | 全链路压测、安全审计、合规检查、用户验收测试 |

#### 8.3.3 关键指标

- 告警响应时间：P0 < 5 分钟，P1 < 30 分钟
- 自动化 Action 覆盖率：> 80% 的常见异常场景
- A/B 测试平台支持并发实验：> 10 个
- NLP 情感分析准确率：> 80%
- **KYC 完成率目标：> 80%**（向 85% 迈进）
- **平均完成时间目标：< 5 分钟**（向 3 分钟迈进）

### 8.4 持续优化（第 7 月及以后）

| 优化方向 | 具体措施 |
|---------|---------|
| 模型迭代 | 每月重新训练模型，持续优化特征和超参数 |
| 新场景覆盖 | 覆盖更多 KYC 场景（如企业 KYC、增强尽职调查） |
| 跨产品复用 | 将分析能力复用到其他产品流程（如支付认证、登录认证） |
| 自助分析 | 提供自助分析工具，让非技术用户也能进行数据探索 |
| 预测性运营 | 从被动响应升级为预测性运营，提前预防问题 |

---

## 9. 成本估算

### 9.1 基础设施成本（月度）

| 资源 | 规格 | 月费用（USD） | 说明 |
|-----|------|-------------|------|
| **Kafka 集群** | 6 Brokers (m5.xlarge) | $1,800 | 含 ZooKeeper |
| **Flink 集群** | 4 TaskManagers (m5.2xlarge) | $1,200 | 实时处理 |
| **ClickHouse 集群** | 3 节点 (i3.xlarge, 2TB SSD) | $2,100 | 热数据存储 + 查询 |
| **Spark 集群** | 4 Workers (m5.2xlarge, 按需) | $800 | 离线处理（按需计费） |
| **PostgreSQL** | db.r5.xlarge (Multi-AZ) | $600 | 元数据存储 |
| **Redis** | cache.r5.large (Cluster) | $400 | 缓存层 |
| **Elasticsearch** | 3 节点 (r5.xlarge, 1TB) | $1,500 | 日志检索 |
| **S3 存储** | ~10TB/年 + 请求费用 | $500 | 数据湖存储 |
| **网络流量** | 数据传输 + NAT 网关 | $300 | 跨区域流量 |
| **监控服务** | Prometheus + Grafana Cloud | $200 | 系统监控 |
| **Schema Registry** | Confluent Cloud (Basic) | $100 | Schema 管理 |
| **ML 模型服务** | 2 节点 (g4dn.xlarge, GPU) | $800 | 模型推理 |
| **AML 合规数据存储** | ClickHouse 扩展 2 节点 (i3.xlarge) | $1,400 | 制裁筛查/监控告警/合规报告数据 |
| **ZK 证明生成服务** | 2 节点 (c5.2xlarge) | $600 | ZK 电路计算与证明生成 |
| **ZK 证明存储** | S3 ~2TB/年 | $100 | ZK 证明归档存储 |
| **Neo4j 图数据库** | 3 节点 (r5.xlarge) | $1,500 | 链上关系图谱、合谋分析 |
| **小计** | | **$13,900** | |

### 9.2 人力成本（月度）

| 角色 | 人数 | 月费用（USD） | 职责 |
|-----|------|-------------|------|
| 数据工程师 | 2 | $30,000 | 数据管道、ETL、数据仓库 |
| ML 工程师 | 1 | $18,000 | 模型训练、部署、优化 |
| 后端工程师 | 1 | $16,000 | SDK 开发、API 开发 |
| 前端工程师 | 1 | $15,000 | 看板开发、可视化 |
| 数据产品经理 | 1 | $14,000 | 产品设计、需求管理 |
| DevOps 工程师 | 0.5 | $7,000 | 基础设施运维（兼职） |
| **小计** | **6.5** | **$100,000** | |

### 9.3 第三方服务成本（月度）

| 服务 | 月费用（USD） | 说明 |
|-----|-------------|------|
| PagerDuty | $300 | 告警通知 |
| Slack (Business+) | $200 | 团队协作 |
| Confluent Cloud | $100 | Schema Registry |
| Mapbox | $200 | 地图可视化 |
| 数据血缘工具 | $500 | Apache Atlas 托管 |
| A/B 测试平台（如有） | $1,000 | 或自建 |
| 制裁名单数据源（Refinitiv/Dow Jones） | $3,000 | 制裁/PEP/不良媒体名单订阅 |
| Chainalysis 风险评分 API | $2,500 | 链上风险评估 |
| Elliptic 风险评分 API | $2,000 | 链上风险评估（备选/补充） |
| Travel Rule 协议服务（Notabene/Sygna） | $1,500 | VASP 间信息传输 |
| ZK 电路审计服务 | $500 | 定期安全审计 |
| **小计** | **$10,300** | |

### 9.4 成本汇总

| 成本类别 | 月费用（USD） | 年费用（USD） |
|---------|-------------|-------------|
| 基础设施 | $13,900 | $166,800 |
| 人力 | $100,000 | $1,200,000 |
| 第三方服务 | $10,300 | $123,600 |
| **总计** | **$124,200** | **$1,490,400** |

### 9.5 ROI 估算

假设月均新增注册用户 50 万，KYC 完成率从 65% 提升至 85%：

| 指标 | 提升前 | 提升后 | 增量 |
|-----|-------|-------|------|
| 月均 KYC 完成用户 | 325,000 | 425,000 | +100,000 |
| 单用户 LTV（假设） | $50 | $50 | — |
| 月均增量收入 | — | — | +$5,000,000 |
| 年均增量收入 | — | — | +$60,000,000 |
| 年化投入产出比 | — | — | **44:1** |

> **注**：以上 ROI 估算基于理想情况，实际效果取决于产品优化执行质量、市场竞争环境等因素。建议在 Phase 1 完成后根据实际数据修正 ROI 模型。

---

## 附录 A：术语表

| 术语 | 全称 | 说明 |
|-----|------|------|
| KYC | Know Your Customer | 了解你的客户，金融合规要求 |
| KAP | KYC Analytics Platform | KYC 数据分析平台 |
| SDK | Software Development Kit | 软件开发工具包 |
| OLAP | Online Analytical Processing | 联机分析处理 |
| ODS | Operational Data Store | 操作数据存储层 |
| DWD | Data Warehouse Detail | 数据仓库明细层 |
| DWS | Data Warehouse Summary | 数据仓库汇总层 |
| ADS | Application Data Store | 应用数据存储层 |
| ETL | Extract, Transform, Load | 数据抽取、转换、加载 |
| SLA | Service Level Agreement | 服务等级协议 |
| AUC | Area Under Curve | ROC 曲线下面积 |
| SHAP | SHapley Additive exPlanations | 模型解释方法 |
| PSI | Population Stability Index | 群体稳定性指标 |
| RBAC | Role-Based Access Control | 基于角色的访问控制 |
| DPIA | Data Protection Impact Assessment | 数据保护影响评估 |
| DPA | Data Processing Agreement | 数据处理协议 |
| LTV | Life Time Value | 用户生命周期价值 |
| AML | Anti-Money Laundering | 反洗钱 |
| SAR | Suspicious Activity Report | 可疑活动报告 |
| STR | Suspicious Transaction Report | 可疑交易报告 |
| CTR | Currency Transaction Report | 大额交易报告 |
| PEP | Politically Exposed Person | 政治公众人物 |
| OFAC | Office of Foreign Assets Control | 美国海外资产控制办公室 |
| VASP | Virtual Asset Service Provider | 虚拟资产服务提供商 |
| Travel Rule | FATF Travel Rule | 金融行动特别工作组旅行规则 |
| ZK | Zero-Knowledge | 零知识证明 |
| ZKP | Zero-Knowledge Proof | 零知识证明协议 |

---

## 附录 B：埋点事件完整清单

| 序号 | 事件名 | 事件分类 | 触发时机 | 采集端 |
|-----|-------|---------|---------|-------|
| 1 | `kyc_page_enter` | 页面级 | 进入 KYC 步骤页面 | 前端 SDK |
| 2 | `kyc_page_exit` | 页面级 | 离开 KYC 步骤页面 | 前端 SDK |
| 3 | `kyc_page_duration` | 页面级 | 页面退出或心跳上报 | 前端 SDK |
| 4 | `kyc_photo_capture` | 交互级 | 完成拍照 | 前端 SDK |
| 5 | `kyc_photo_retake` | 交互级 | 主动或系统触发重拍 | 前端 SDK |
| 6 | `kyc_form_submit` | 交互级 | 点击提交按钮 | 前端 SDK |
| 7 | `kyc_error_action` | 交互级 | 发生用户侧/系统侧错误 | 前端 SDK |
| 8 | `kyc_guide_interaction` | 交互级 | 与引导提示交互 | 前端 SDK |
| 9 | `kyc_api_response` | 系统级 | API 请求完成 | 后端 Agent |
| 10 | `kyc_error_code` | 系统级 | 产生业务错误码 | 后端 Agent |
| 11 | `kyc_service_availability` | 系统级 | 心跳上报或状态变更 | 后端 Agent |
| 12 | `kyc_approved` | 业务结果级 | KYC 审核通过 | 后端 Agent |
| 13 | `kyc_rejected` | 业务结果级 | KYC 审核拒绝 | 后端 Agent |
| 14 | `kyc_expired` | 业务结果级 | KYC 状态过期 | 后端 Agent |
| 15 | `kyc_review_queue_status` | 业务结果级 | 审核队列状态变更 | 后端 Agent |
| 16 | `screening_initiated` | 合规模块（G） | 进入制裁与风险筛查流程 | 后端 Agent |
| 17 | `screening_completed` | 合规模块（G） | 筛查流程完成 | 后端 Agent |
| 18 | `sanctions_hit` | 合规模块（G） | 制裁名单命中 | 后端 Agent |
| 19 | `pep_hit` | 合规模块（G） | PEP 名单命中 | 后端 Agent |
| 20 | `adverse_media_hit` | 合规模块（G） | 不良媒体命中 | 后端 Agent |
| 21 | `screening_review` | 合规模块（G） | 人工复核筛查结果 | 后端 Agent |
| 22 | `monitoring_alert_triggered` | 合规模块（H） | 风控告警触发 | 后端 Agent |
| 23 | `monitoring_alert_resolved` | 合规模块（H） | 告警处理完成 | 后端 Agent |
| 24 | `wallet_risk_score_changed` | 合规模块（H） | 钱包风险评分变化 | 后端 Agent |
| 25 | `transaction_pattern_detected` | 合规模块（H） | 异常交易模式检测 | 后端 Agent |
| 26 | `kyc_info_changed` | 合规模块（H） | 用户 KYC 信息变更 | 后端 Agent |
| 27 | `account_reactivation` | 合规模块（H） | 不活跃账户重新激活 | 后端 Agent |
| 28 | `travel_rule_info_collected` | 合规模块（I） | Travel Rule 信息收集完成 | 后端 Agent |
| 29 | `travel_rule_info_transmitted` | 合规模块（I） | Travel Rule 信息传输 | 后端 Agent |
| 30 | `travel_rule_info_received` | 合规模块（I） | Travel Rule 信息接收 | 后端 Agent |
| 31 | `sar_generated` | 合规模块（J） | SAR 报告生成 | 后端 Agent |
| 32 | `sar_submitted` | 合规模块（J） | SAR 报告提交 | 后端 Agent |
| 33 | `ctr_triggered` | 合规模块（J） | CTR 大额交易报告触发 | 后端 Agent |
| 34 | `audit_log_exported` | 合规模块（J） | 审计日志导出 | 后端 Agent |
| 35 | `zk_proof_requested` | ZK 服务（F） | ZK 证明请求发起 | 后端 Agent |
| 36 | `zk_proof_generated` | ZK 服务（F） | ZK 证明生成完成 | 后端 Agent |
| 37 | `zk_proof_verified` | ZK 服务（F） | ZK 证明验证完成 | 后端 Agent |
| 38 | `zk_proof_expired` | ZK 服务（F） | ZK 证明过期 | 后端 Agent |
| 39 | `zk_client_onboarded` | ZK 服务（F） | 外部客户接入 ZK 服务 | 后端 Agent |

---

> **文档结束**
>
> 本文档由数据产品团队编写和维护，如有疑问请联系 kyc-analytics@company.com。
> 文档版本历史请查看 Git 仓库提交记录。
