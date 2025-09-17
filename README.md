# MIVA AI Data EDA

## Project Overview
This repository contains a **comprehensive exploratory data analysis (EDA)** of two core tables from the **MIVA AI database**:

- **chat_feedback** — user-provided ratings, comments, and interaction logs  
- **otps** — one-time password (OTP) authentication records  

Together, these datasets provide a unique opportunity to analyze **user engagement**, **sentiment**, and **system verification reliability**.

---

## Objectives
- Understand the structure and quality of both datasets  
- Explore distributions of numeric and categorical features  
- Detect missing values, anomalies, and outliers  
- Identify correlations and trends  
- Derive domain-specific insights (feedback sentiment patterns, OTP usage frequency and validation success)

---

## Tech Stack
- **Python** (pandas, numpy)  
- **Matplotlib** (for plotting)  
- **PostgreSQL** (data source)  
- **Jupyter/Colab** (interactive analysis)  

---

## Key Analyses
1. **Data Quality Checks**  
   - Missing values per column  
   - Schema review and datatype consistency  

2. **Descriptive Statistics**  
   - Numerical summaries (mean, std, percentiles)  
   - Categorical frequency distributions  

3. **Visualizations**  
   - Histograms for numeric features  
   - Bar charts for categorical variables  
   - Correlation heatmaps  
   - Boxplots for outlier detection  
   - Time-series trends for datetime fields  

4. **Domain-Specific Insights**  
   - OTP length distributions & usage patterns  
   - Success/failure trends for OTP validation  
   - Chat feedback ratings & sentiment breakdowns  
   - Feedback trends over time  

---

## Results & Insights
- **User Experience**: Feedback distributions highlight strengths and weaknesses in chat interactions, providing actionable insight into user satisfaction.  
- **System Reliability**: OTP trends reveal authentication load, potential misuse, and system performance over time.  
- **Opportunities**: Combining user feedback and authentication logs can support predictive modeling for churn, fraud detection, and proactive system monitoring.  

---

## Repository Structure


├── Response_EDA.ipynb # Main notebook with analysis

├── README.md # Project documentation

└── requirements.txt # Dependencies

---

## Next Steps
- Build predictive models for user satisfaction and OTP failures  
- Develop anomaly detection for unusual OTP request patterns  
- Deploy interactive dashboards (e.g., Streamlit, Power BI, or Tableau)  
- Integrate with MIVA’s real-time monitoring system for proactive insights  

---




## MIVA Interaction & OTP EDA (Streamlit)

A Streamlit app that connects to a PostgreSQL database and explores **chat feedback** and **OTP authentication** tables with clean, actionable visuals.

## ✨ Features
- Connects to Postgres via Streamlit Secrets / env vars
- Table picker, schema preview, sample data
- Missingness bars, numeric histograms, category bars
- Correlation heatmaps, boxplots, daily time trends
- Domain-special views:
  - **OTPs**: code length, status mix, requests over time
  - **Chat Feedback**: rating/sentiment/text-length distributions, events over time
- Safe SQL runner (read-only enforced)

## 🧱 Tech
`streamlit`, `pandas`, `numpy`, `matplotlib`, `psycopg2-binary`, `SQLAlchemy`

## 🚀 Run locally

```bash
# 1) Clone
git clone https://github.com/<you>/miva-eda-app.git
cd miva-eda-app

# 2) (Optional) create venv
python -m venv .venv && source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Provide DB creds via env or .streamlit/secrets.toml
export PGHOST=16.170.143.253
export PGPORT=5432
export PGDATABASE=miva_ai_db
export PGUSER=admin
export PGPASSWORD=********
export PGSSLMODE=prefer
export PGSCHEMA=public

# or create .streamlit/secrets.toml (not committed)
# see .streamlit/secrets.toml template

# 5) Launch
streamlit run streamlit_app.py

##Deploy on Streamlit Community Cloud

Push this repo to GitHub.

Go to https://share.streamlit.io/
 → New app → Select your repo and streamlit_app.py.

In App → Settings → Secrets, add:

[postgres]
host = "16.170.143.253"
port = 5432
database = "miva_ai_db"
user = "admin"
password = "********"
sslmode = "prefer"
schema = "public"



## Author
Developed by **The MIVA R & D Team** as part of MIVA AI analytics initiatives.  
