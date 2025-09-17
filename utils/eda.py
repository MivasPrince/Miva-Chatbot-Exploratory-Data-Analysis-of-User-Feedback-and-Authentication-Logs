import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from dateutil import parser as dateparser

# ---------- helpers ----------
def try_parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == "object":
            name = col.lower()
            if any(k in name for k in ["time", "date", "at", "created", "updated", "timestamp"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
                except Exception:
                    pass
    return df

def detect_text_like(df: pd.DataFrame, min_median_len: int = 3):
    cols = []
    for c in df.columns:
        if df[c].dtype == "object":
            s = df[c].dropna().astype(str)
            if not s.empty and s.str.len().median() >= min_median_len:
                cols.append(c)
    return cols

def otp_special_cols(df: pd.DataFrame):
    code_col = next((c for c in df.columns if c.lower() in ("otp", "code", "otp_code")), None)
    status_col = next((c for c in df.columns if c.lower() in ("status", "state", "used", "is_used")), None)
    created_col = next((c for c in df.columns if "creat" in c.lower() or "time" in c.lower() or "date" in c.lower()), None)
    return code_col, status_col, created_col

def feedback_special_cols(df: pd.DataFrame):
    rating_col = next((c for c in df.columns if any(k in c.lower() for k in ("rating", "score", "stars"))), None)
    sentiment_col = next((c for c in df.columns if "sentiment" in c.lower()), None)
    text_col = next((c for c in df.columns if any(k in c.lower() for k in ("comment", "feedback", "text", "message"))), None)
    time_col = next((c for c in df.columns if any(k in c.lower() for k in ("time", "date", "created", "updated"))), None)
    return rating_col, sentiment_col, text_col, time_col

# ---------- plots ----------
def plot_missingness(df: pd.DataFrame, title: str):
    na_counts = df.isna().sum()
    na_counts = na_counts[na_counts > 0].sort_values(ascending=False)
    if na_counts.empty:
        st.info(f"No missing values in **{title}**.")
        return
    fig = plt.figure(figsize=(8, max(2.6, 0.3 * len(na_counts))))
    plt.barh(na_counts.index.astype(str), na_counts.values)
    plt.xlabel("Missing count")
    plt.ylabel("Columns")
    plt.title(f"{title}: Missing values per column")
    st.pyplot(fig)

def plot_numeric_histograms(df: pd.DataFrame, title: str, bins: int = 30):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        st.info(f"No numeric columns in **{title}**.")
        return
    for col in num_cols:
        data = df[col].dropna().values
        if data.size == 0:
            continue
        fig = plt.figure(figsize=(6, 3.8))
        plt.hist(data, bins=bins)
        plt.title(f"{title}: Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        st.pyplot(fig)

def plot_categorical_bars(df: pd.DataFrame, title: str, top_n: int = 20):
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if not cat_cols:
        st.info(f"No categorical columns in **{title}**.")
        return
    for col in cat_cols:
        vc = df[col].astype("object").fillna("⟂(NaN)").value_counts().head(top_n)
        if vc.empty:
            continue
        fig = plt.figure(figsize=(8, max(2.6, 0.3 * len(vc))))
        plt.barh(vc.index.astype(str), vc.values)
        plt.gca().invert_yaxis()
        plt.title(f"{title}: Top {top_n} of {col}")
        plt.xlabel("Count")
        plt.ylabel(col)
        st.pyplot(fig)

def plot_corr_heatmap(df: pd.DataFrame, title: str):
    corr = df.select_dtypes(include=[np.number]).corr(numeric_only=True)
    if corr.empty:
        st.info(f"No numeric correlation matrix for **{title}**.")
        return
    fig = plt.figure(figsize=(8, 6))
    im = plt.imshow(corr.values, aspect="auto", interpolation="nearest")
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.index)), corr.index)
    plt.title(f"{title}: Correlation Heatmap")
    st.pyplot(fig)

def plot_boxplots(df: pd.DataFrame, title: str):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        st.info(f"No numeric columns in **{title}** for boxplots.")
        return
    for col in num_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        fig = plt.figure(figsize=(6, 2.6))
        plt.boxplot(series.values, vert=False, whis=1.5)
        plt.title(f"{title}: Boxplot of {col}")
        plt.xlabel(col)
        st.pyplot(fig)

def plot_time_trends(df: pd.DataFrame, title: str):
    time_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.datetime64)]
    if not time_cols:
        st.info(f"No datetime columns detected in **{title}**.")
        return
    for col in time_cols:
        s = pd.to_datetime(df[col], errors="coerce")
        s = s.dropna()
        if s.empty:
            continue
        counts = s.dt.tz_localize(None).dt.date.value_counts().sort_index()
        if counts.empty:
            continue
        fig = plt.figure(figsize=(10, 3.5))
        plt.plot(list(counts.index), counts.values)
        plt.title(f"{title}: Daily count by {col}")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

def otp_special(df: pd.DataFrame):
    code_col, status_col, created_col = otp_special_cols(df)
    if code_col:
        lengths = df[code_col].dropna().astype(str).str.len()
        if not lengths.empty:
            fig = plt.figure(figsize=(6, 3.2))
            lo, hi = int(lengths.min()), int(lengths.max())
            bins = range(lo, hi + 2)
            plt.hist(lengths.values, bins=bins)
            plt.title(f"OTP length distribution ({code_col})")
            plt.xlabel("Length")
            plt.ylabel("Frequency")
            st.pyplot(fig)
    if status_col:
        vc = df[status_col].astype("object").fillna("⟂(NaN)").value_counts()
        if not vc.empty:
            fig = plt.figure(figsize=(7, max(2.6, 0.3 * len(vc))))
            plt.barh(vc.index.astype(str), vc.values)
            plt.gca().invert_yaxis()
            plt.title(f"OTP status distribution ({status_col})")
            plt.xlabel("Count")
            st.pyplot(fig)
    if created_col and np.issubdtype(df[created_col].dtype, np.datetime64):
        s = df[created_col].dropna()
        counts = s.dt.tz_localize(None).dt.date.value_counts().sort_index()
        if not counts.empty:
            fig = plt.figure(figsize=(10, 3.2))
            plt.plot(list(counts.index), counts.values)
            plt.title(f"OTP requests over time ({created_col})")
            plt.xlabel("Date")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)

def feedback_special(df: pd.DataFrame):
    rating_col, sentiment_col, text_col, time_col = feedback_special_cols(df)
    if rating_col is not None:
        if pd.api.types.is_numeric_dtype(df[rating_col]):
            vals = df[rating_col].dropna()
            if not vals.empty:
                fig = plt.figure(figsize=(6, 3.2))
                plt.hist(vals.values, bins=10)
                plt.title(f"Feedback rating distribution ({rating_col})")
                plt.xlabel(rating_col)
                plt.ylabel("Frequency")
                st.pyplot(fig)
        else:
            vc = df[rating_col].astype("object").fillna("⟂(NaN)").value_counts()
            if not vc.empty:
                fig = plt.figure(figsize=(7, max(2.6, 0.3 * len(vc))))
                plt.barh(vc.index.astype(str), vc.values)
                plt.gca().invert_yaxis()
                plt.title(f"Feedback rating distribution ({rating_col})")
                plt.xlabel("Count")
                st.pyplot(fig)
    if sentiment_col is not None:
        vc = df[sentiment_col].astype("object").fillna("⟂(NaN)").value_counts()
        if not vc.empty:
            fig = plt.figure(figsize=(7, max(2.6, 0.3 * len(vc))))
            plt.barh(vc.index.astype(str), vc.values)
            plt.gca().invert_yaxis()
            plt.title(f"Sentiment distribution ({sentiment_col})")
            plt.xlabel("Count")
            st.pyplot(fig)
    # optional: text length
    if text_col is not None and df[text_col].dtype == "object":
        L = df[text_col].dropna().astype(str).str.len()
        if not L.empty:
            fig = plt.figure(figsize=(6, 3.2))
            plt.hist(L.values, bins=30)
            plt.title(f"Feedback text length ({text_col})")
            plt.xlabel("Length (chars)")
            plt.ylabel("Frequency")
            st.pyplot(fig)
    # feedback over time
    if time_col and np.issubdtype(df[time_col].dtype, np.datetime64):
        s = df[time_col].dropna()
        counts = s.dt.tz_localize(None).dt.date.value_counts().sort_index()
        if not counts.empty:
            fig = plt.figure(figsize=(10, 3.2))
            plt.plot(list(counts.index), counts.values)
            plt.title(f"Feedback events over time ({time_col})")
            plt.xlabel("Date")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)
