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

## Author
Developed by **The MIVA R & D Team** as part of MIVA AI analytics initiatives.  
