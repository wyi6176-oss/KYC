# 🔐 KYC Product Suite — Crypto Exchange Compliance Platform

<p align="center">
  <strong>Full-stack KYC/AML compliance product suite for crypto exchanges</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.30%2B-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-5.15%2B-orange" alt="Plotly">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

---

## 🎯 Project Overview

A comprehensive KYC (Know Your Customer) product suite designed for mid-to-large crypto exchanges, covering the complete 7-layer compliance framework:

> **Identity Verification → CDD → EDD → Sanctions/Risk Screening → Ongoing Monitoring → Travel Rule → Reporting**

This repository includes **product documentation**, a **runnable data analytics application**, and **market research reports** — everything needed to understand, build, and operate an industry-leading KYC system.

## 📁 Repository Structure

```
kyc-project/
├── app.py                    # Streamlit analytics app (main entry)
├── generate_data.py          # Sample data generator
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore
│
├── .streamlit/
│   └── config.toml           # Streamlit server config
│
├── data/
│   └── sample_data.csv       # 46K+ simulated KYC events
│
├── utils/                    # Analytics utility modules
│   ├── __init__.py
│   ├── charts.py             # Plotly chart factory
│   ├── funnel.py             # Funnel analysis logic
│   └── metrics.py            # KPI calculation functions
│
└── docs/                     # 📋 Product Documentation
    ├── KYC产品PRD_v2.md              # Product Requirements Document
    ├── KYC产品PRD_v2.docx
    ├── KYC技术供应商选型报告_v2.md     # Vendor Selection Report
    ├── KYC技术供应商选型报告_v2.docx
    ├── KYC产品战略规划书_v2.md        # Product Strategy & Roadmap
    ├── KYC产品战略规划书_v2.docx
    ├── KYC埋点数据分析产品文档.md      # Analytics Data Product Spec
    ├── KYC埋点数据分析产品文档.docx
    ├── ZK-KYC市场调研与竞品分析报告.md  # ZK-KYC Market Research
    ├── ZK-KYC市场调研与竞品分析报告.docx
    ├── KYC竞品分析报告_0x视野.html     # Competitor Analysis (Web Article)
    ├── SOLO挑战赛参赛帖.md             # Competition Entry Post
    └── KYC_产品战略规划.pptx           # Strategy Presentation
```

## 📋 Documentation Index

| Document | Format | Description |
|----------|--------|-------------|
| **KYC产品PRD v2** | MD / DOCX | 10-chapter PRD covering modules A-J, configurable rule engine (4-layer architecture), modular ZK-proof service (30 function points) |
| **技术供应商选型报告 v2** | MD / DOCX | 12 vendors evaluated (5 KYC + 7 AML), 8 jurisdiction compliance mapping, 3 recommended deployment plans |
| **产品战略规划书 v2** | MD / DOCX | 18-month 5-phase roadmap, ZK-proof strategic vision, $91.6M-$111.6M business value analysis |
| **埋点数据分析产品文档** | MD / DOCX | 39 tracking events, 8 AI/ML models, 6 dashboards, annual cost $1.49M |
| **ZK-KYC市场调研与竞品分析** | MD / DOCX | 10 competitors analyzed, zkPass deep dive (zkTLS/VOLEitH/MPC), 6 critical weaknesses identified |
| **竞品分析报告 (0x视野)** | HTML | WeChat-style article with embedded charts |
| **产品战略规划 PPT** | PPTX | Strategy presentation with visual roadmap |
| **SOLO挑战赛参赛帖** | MD | Competition entry with full project description |

## 📊 Data Analytics Application

A production-ready Streamlit web app for KYC data analysis — **zero frontend code, PM-maintainable**.

### 10 Analysis Modules

| Module | Description |
|--------|-------------|
| 📥 **Data Import** | Upload CSV or use built-in 46K+ sample dataset |
| 📈 **Real-time Dashboard** | KPI cards, 7-day trends, Top 10 countries |
| 🔻 **Conversion Funnel** | 7-step funnel with drill-down by country/device/doc type |
| ❌ **Failure Analysis** | Failure reason distribution, step breakdown, trend tracking |
| ⏱️ **Duration Analysis** | Box plots, percentile tables, device comparison |
| 🌍 **Country Analysis** | Per-country deep dive, global distribution heatmap |
| 📱 **Device Analysis** | iOS / Android / Web cross-comparison |
| 🛡️ **Compliance Monitor** | Sanctions/PEP hit rates, alerts, SAR/CTR tracking |
| 🧪 **A/B Testing** | Metric comparison with statistical significance testing |
| 🔧 **Custom Analysis** | Flexible dimension/metric/chart selector |

### Quick Start

```bash
# Clone the repository
git clone https://github.com/<your-username>/kyc-project.git
cd kyc-project

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the analytics app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → Select your repo → Click **"Deploy"**

Your app will be live at `https://<your-app>.streamlit.app`

### Data Format

Upload a CSV with these columns:

| Column | Type | Description |
|--------|------|-------------|
| `event_id` | string | Unique event identifier |
| `user_id` | string | User identifier |
| `country` | string | User's country |
| `device_type` | string | iOS / Android / Web |
| `doc_type` | string | passport / id_card / drivers_license |
| `step` | string | KYC step name |
| `status` | string | success / fail / timeout |
| `duration` | float | Step duration in seconds |
| `timestamp` | datetime | Event timestamp (ISO 8601) |
| `fail_reason` | string | Failure reason (if applicable) |
| `is_sanction_hit` | bool | Sanctions list match |
| `is_pep_hit` | bool | PEP match |
| `risk_level` | string | low / medium / high |

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [Streamlit](https://streamlit.io/) | Web application framework |
| [Plotly](https://plotly.com/python/) | Interactive visualizations |
| [Pandas](https://pandas.pydata.org/) | Data processing |
| [NumPy](https://numpy.org/) | Numerical computation |
| [SciPy](https://scipy.org/) | Statistical testing |

## 📝 License

MIT License — feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
