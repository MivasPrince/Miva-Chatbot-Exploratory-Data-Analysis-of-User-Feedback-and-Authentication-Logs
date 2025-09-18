import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine, text

# =========================
# Page / App Configuration
# =========================
st.set_page_config(page_title="MIVA EDA Enhanced", page_icon="📊", layout="wide")

st.markdown("""
# 📊 MIVA Enhanced EDA App
Explore **chat feedback** and **OTP authentication logs** directly from PostgreSQL.
""")

# =========================
# Secrets / Config Helpers
# =========================
def _load_secrets():
    # Prefer Streamlit secrets; fallback to env vars
    if "postgres" in st.secrets:
        p = st.secrets["postgres"]
        return {
            "host": p.get("host"),
            "port": p.get("port", 5432),
            "database": p.get("database"),
            "user": p.get("user"),
            "password": p.get("password"),
            "sslmode": p.get("sslmode", "prefer"),
            "schema": p.get("schema", "public"),
        }
    return {
        "host": os.getenv("PGHOST"),
        "port": int(os.getenv("PGPORT", "5432")),
        "database": os.getenv("PGDATABASE"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
        "sslmode": os.getenv("PGSSLMODE", "prefer"),
        "schema": os.getenv("PGSCHEMA", "public"),
    }

CFG = _load_secrets()

# =========================
# DB Connection (psycopg v3)
# =========================
@st.cache_resource(show_spinner=False)
def get_engine():
    assert CFG["host"] and CFG["database"] and CFG["user"], "Database secrets missing."
    # Use psycopg v3 driver ("postgresql+psycopg://")
    url = (
        f"postgresql+psycopg://{CFG['user']}:{CFG['password']}"
        f"@{CFG['host']}:{CFG['port']}/{CFG['database']}?sslmode={CFG['sslmode']}"
    )
    engine = create_engine(url, pool_pre_ping=True)
    return engine

@st.cache_data(ttl=300, show_spinner=False)
def list_tables(schema: str):
    q = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = :schema
        ORDER BY table_name;
    """)
    with get_engine().connect() as conn:
        return [r[0] for r in conn.execute(q, {"schema": schema}).fetchall()]

@st.cache_data(ttl=300, show_spinner=False)
def get_columns(table: str, schema: str):
    q = text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
        ORDER BY ordinal_position;
    """)
    with get_engine().connect() as conn:
        rows = conn.execute(q, {"schema": schema, "table": table}).fetchall()
    return pd.DataFrame(rows, columns=["column_name", "data_type"])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_df(table: str, schema: str, limit: int | None = 5000):
    if limit and limit > 0:
        sql = text(f'SELECT * FROM "{schema}"."{table}" LIMIT :lim')
        params = {"lim": int(limit)}
    else:
        sql = text(f'SELECT * FROM "{schema}"."{table}"')
        params = {}
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn, params=params)

# =========================
# EDA Utilities
# =========================
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
        s = pd.to_datetime(df[col], errors="coerce").dropna()
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

def otp_special_cols(df: pd.DataFrame):
    code_col = next((c for c in df.columns if c.lower() in ("otp", "code", "otp_code")), None)
    status_col = next((c for c in df.columns if c.lower() in ("status", "state", "used", "is_used")), None)
    created_col = next((c for c in df.columns if "creat" in c.lower() or "time" in c.lower() or "date" in c.lower()), None)
    return code_col, status_col, created_col

def otp_special(df: pd.DataFrame):
    code_col, status_col, created_col = otp_special_cols(df)
    if code_col:
        lengths = df[code_col].dropna().astype(str).str.len()
        if not lengths.empty:
            fig = plt.figure(figsize=(6, 3.2))
            lo, hi = int(lengths.min()), int(lengths.max())
            plt.hist(lengths.values, bins=range(lo, hi + 2))
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

def feedback_special_cols(df: pd.DataFrame):
    rating_col = next((c for c in df.columns if any(k in c.lower() for k in ("rating", "score", "stars"))), None)
    sentiment_col = next((c for c in df.columns if "sentiment" in c.lower()), None)
    text_col = next((c for c in df.columns if any(k in c.lower() for k in ("comment", "feedback", "text", "message"))), None)
    time_col = next((c for c in df.columns if any(k in c.lower() for k in ("time", "date", "created", "updated"))), None)
    return rating_col, sentiment_col, text_col, time_col

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
    if text_col is not None and df[text_col].dtype == "object":
        L = df[text_col].dropna().astype(str).str.len()
        if not L.empty:
            fig = plt.figure(figsize=(6, 3.2))
            plt.hist(L.values, bins=30)
            plt.title(f"Feedback text length ({text_col})")
            plt.xlabel("Length (chars)")
            plt.ylabel("Frequency")
            st.pyplot(fig)
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

# =========================
# Sidebar / Controls
# =========================
with st.sidebar:
    st.header("🔌 Data Source")
    st.write(f"**Host**: `{CFG.get('host')}`")
    st.write(f"**DB**: `{CFG.get('database')}`")
    st.write(f"**Schema**: `{CFG.get('schema', 'public')}`")

    st.divider()
    st.subheader("📂 Table")
    tables = list_tables(CFG.get("schema", "public"))
    if not tables:
        st.error("No tables found. Check DB credentials / schema / privileges.")
        st.stop()

    default_index = tables.index("chat_feedback") if "chat_feedback" in tables else 0
    table = st.selectbox("Select a table", options=tables, index=default_index)
    limit = st.slider("Max rows to load", min_value=100, max_value=20000, value=5000, step=100)

    st.divider()
    st.subheader("⚙️ Display")
    show_raw = st.checkbox("Show raw data preview", value=True)
    top_n_cats = st.number_input("Top categories (bar charts)", min_value=5, max_value=50, value=20, step=1)
    bins_num = st.number_input("Histogram bins (numeric)", min_value=10, max_value=100, value=30, step=5)

# =========================
# Data Load
# =========================
with st.spinner("Loading data..."):
    df = fetch_df(table, schema=CFG.get("schema", "public"), limit=limit)
    df = try_parse_datetimes(df)

st.subheader(f"📦 `{CFG.get('schema', 'public')}.{table}` — {df.shape[0]} rows × {df.shape[1]} columns")
st.dataframe(get_columns(table, CFG.get("schema", "public")), use_container_width=True)

if show_raw:
    st.write("### 🔎 Sample (first 1,000 rows)")
    st.dataframe(df.head(1000), use_container_width=True)

# =========================
# Tabs
# =========================
tab_overview, tab_missing, tab_num, tab_cat, tab_corr, tab_box, tab_time, tab_special, tab_sql = st.tabs(
    ["Overview", "Missingness", "Numeric", "Categorical", "Correlations", "Boxplots", "Time Trends", "Domain Specials", "SQL Runner"]
)

with tab_overview:
    st.markdown("**Column dtypes**")
    dtypes_df = pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)}).reset_index(drop=True)
    st.dataframe(dtypes_df, use_container_width=True)

    st.markdown("**Descriptive statistics (numeric)**")
    try:
        st.dataframe(df.describe(include="number").T, use_container_width=True)
    except Exception:
        st.info("No numeric columns.")

    st.markdown("**Descriptive statistics (categorical)**")
    try:
        st.dataframe(df.describe(include="object").T, use_container_width=True)
    except Exception:
        st.info("No categorical columns.")

with tab_missing:
    plot_missingness(df, title=f"{table}")

with tab_num:
    plot_numeric_histograms(df, title=f"{table}", bins=bins_num)

with tab_cat:
    plot_categorical_bars(df, title=f"{table}", top_n=top_n_cats)

with tab_corr:
    plot_corr_heatmap(df, title=f"{table}")

with tab_box:
    plot_boxplots(df, title=f"{table}")

with tab_time:
    plot_time_trends(df, title=f"{table}")

with tab_special:
    st.markdown("**Context-aware visuals**")
    if table.lower() == "otps":
        otp_special(df)
    elif table.lower() == "chat_feedback":
        feedback_special(df)
    else:
        st.info("Switch to `otps` or `chat_feedback` to see domain-specific charts.")

with tab_sql:
    st.markdown("Run ad-hoc SQL (**read-only recommended**). Use `LIMIT` to keep results light.")
    user_sql = st.text_area(
        "SQL",
        value=f'SELECT * FROM "{CFG.get("schema","public")}"."{table}" LIMIT 50;',
        height=150
    )
    run = st.button("Run query")
    if run and user_sql.strip():
        try:
            lowered = user_sql.strip().lower()
            if any(kw in lowered for kw in ["update ", "insert ", "delete ", "drop ", "alter ", "create "]):
                st.error("Mutation queries are disabled for safety.")
            else:
                with get_engine().connect() as conn:
                    dfq = pd.read_sql(text(user_sql), conn)
                st.success(f"Returned {len(dfq)} rows.")
                st.dataframe(dfq, use_container_width=True)
        except Exception as e:
            st.exception(e)

st.caption("© MIVA — EDA utility. Never commit real secrets; use Streamlit Secrets or environment variables.")
