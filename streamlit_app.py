import streamlit as st
import pandas as pd
from utils.db import list_tables, get_columns, fetch_df, _secrets
from utils.eda import (
    try_parse_datetimes, plot_missingness, plot_numeric_histograms,
    plot_categorical_bars, plot_corr_heatmap, plot_boxplots, plot_time_trends,
    otp_special, feedback_special, detect_text_like
)

st.set_page_config(page_title="MIVA EDA", page_icon="📊", layout="wide")

st.title("📊 MIVA Interaction & OTP EDA")
st.caption("Explore **chat_feedback** and **otps** tables (and more) directly from PostgreSQL.")

cfg = _secrets()
schema = cfg.get("schema", "public")

with st.sidebar:
    st.header("🔌 Data Source")
    st.write(f"**Host**: `{cfg.get('host')}`")
    st.write(f"**DB**: `{cfg.get('database')}`")
    st.write(f"**Schema**: `{schema}`")

    st.divider()
    st.subheader("📂 Table")
    tables = list_tables(schema)
    if not tables:
        st.error("No tables found. Check your DB permissions / schema.")
        st.stop()

    table = st.selectbox("Select a table", options=tables, index=max(tables.index("chat_feedback") if "chat_feedback" in tables else 0, 0))
    limit = st.slider("Max rows to load", min_value=100, max_value=20000, value=5000, step=100)

    st.divider()
    st.subheader("⚙️ Display")
    show_raw = st.checkbox("Show raw data preview", value=True)
    top_n_cats = st.number_input("Top categories (bar charts)", min_value=5, max_value=50, value=20, step=1)
    bins_num = st.number_input("Histogram bins (numeric)", min_value=10, max_value=100, value=30, step=5)

# Load data
with st.spinner("Loading data..."):
    df = fetch_df(table, schema=schema, limit=limit)
    df = try_parse_datetimes(df)

st.subheader(f"📦 `{schema}.{table}` — shape: {df.shape[0]} rows × {df.shape[1]} columns")
st.dataframe(get_columns(table, schema), use_container_width=True)

if show_raw:
    st.write("### 🔎 Sample (first 1,000 rows max)")
    st.dataframe(df.head(1000), use_container_width=True)

# Tabs
tab_overview, tab_missing, tab_num, tab_cat, tab_corr, tab_box, tab_time, tab_special, tab_sql = st.tabs(
    ["Overview", "Missingness", "Numeric", "Categorical", "Correlations", "Boxplots", "Time Trends", "Domain Specials", "SQL Runner"]
)

with tab_overview:
    st.markdown("**Column dtypes**")
    dtypes_df = pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)}).reset_index(drop=True)
    st.dataframe(dtypes_df, use_container_width=True)

    st.markdown("**Descriptive statistics (numeric)**")
    st.dataframe(df.describe(include="number").T, use_container_width=True)

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
        value=f'SELECT * FROM "{schema}"."{table}" LIMIT 50;',
        height=150
    )
    run = st.button("Run query")
    if run and user_sql.strip():
        try:
            # simple guard: discourage mutation
            lowered = user_sql.strip().lower()
            if any(kw in lowered for kw in ["update ", "insert ", "delete ", "drop ", "alter ", "create "]):
                st.error("Mutation queries are disabled for safety.")
            else:
                from sqlalchemy import text
                from utils.db import get_engine
                with get_engine().connect() as conn:
                    dfq = pd.read_sql(text(user_sql), conn)
                st.success(f"Returned {len(dfq)} rows.")
                st.dataframe(dfq, use_container_width=True)
        except Exception as e:
            st.exception(e)

st.caption("© MIVA — EDA utility. Avoid committing secrets; use Streamlit Secrets or env variables.")
