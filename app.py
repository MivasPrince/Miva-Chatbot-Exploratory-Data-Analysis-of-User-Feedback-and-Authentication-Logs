import os
import json
import math
import textwrap
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# =============================
# App Config
# =============================
st.set_page_config(
    page_title="Chatbot EDA & Explorer",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .small-note { font-size: 0.85rem; color: #6b7280; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================
# Helpers
# =============================
DEFAULT_SCHEMA = "public"
KNOWN_TABLES = [
    "chat_feedback",
    "chat_messages",
    "chat_sessions",
    "conversation_history",
    "conversation_sessions",
    "otp_verifications",
    "otps",
    "user_feedback",
]


def build_conn_url() -> str:
    host = st.session_state.get("DB_HOST") or os.getenv("DB_HOST", "localhost")
    port = st.session_state.get("DB_PORT") or os.getenv("DB_PORT", "5432")
    name = st.session_state.get("DB_NAME") or os.getenv("DB_NAME", "postgres")
    user = st.session_state.get("DB_USER") or os.getenv("DB_USER", "postgres")
    pwd = st.session_state.get("DB_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")
    sslmode = st.session_state.get("DB_SSLMODE") or os.getenv("DB_SSLMODE", "prefer")
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}?sslmode={sslmode}"


@st.cache_resource(show_spinner=False)
def get_engine(conn_url: str) -> Engine:
    return create_engine(conn_url, pool_pre_ping=True)


@st.cache_data(show_spinner=False)
def get_now(engine: Engine) -> datetime:
    with engine.begin() as conn:
        return conn.execute(text("SELECT NOW()")) .scalar_one()


@st.cache_data(show_spinner=False)
def fetch_dataframe(engine: Engine, sql: str, params: Optional[dict] = None, limit_preview: Optional[int] = None) -> pd.DataFrame:
    with engine.begin() as conn:
        df = pd.read_sql(text(sql), conn, params=params)
    if limit_preview is not None and len(df) > limit_preview:
        return df.head(limit_preview).copy()
    return df


@st.cache_data(show_spinner=False)
def get_columns(engine: Engine, table: str, schema: str = DEFAULT_SCHEMA) -> pd.DataFrame:
    sql = text(
        """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
        ORDER BY ordinal_position
        """
    )
    with engine.begin() as conn:
        return pd.read_sql(sql, conn, params={"schema": schema, "table": table})


@st.cache_data(show_spinner=False)
def get_rowcount(engine: Engine, table: str, schema: str = DEFAULT_SCHEMA) -> int:
    sql = text(f'SELECT COUNT(*) FROM "{schema}"."{table}"')
    with engine.begin() as conn:
        return int(conn.execute(sql).scalar_one())


def _maybe_json_normalize(series: pd.Series) -> pd.DataFrame:
    """Quick glance of JSON/JSONB column keys frequency (top-level only)."""
    keys_freq: Dict[str, int] = {}
    non_null = series.dropna()
    for v in non_null[:2000]:  # sample top 2000 to avoid heavy scans
        try:
            obj = v if isinstance(v, (dict, list)) else json.loads(v)
        except Exception:
            continue
        if isinstance(obj, dict):
            for k in obj.keys():
                keys_freq[k] = keys_freq.get(k, 0) + 1
        elif isinstance(obj, list):
            keys_freq["__list_items__"] = keys_freq.get("__list_items__", 0) + len(obj)
    if not keys_freq:
        return pd.DataFrame()
    df = pd.DataFrame(sorted(keys_freq.items(), key=lambda x: (-x[1], x[0])), columns=["key", "frequency_in_sample"])
    return df


def table_eda(engine: Engine, table: str, schema: str = DEFAULT_SCHEMA, sample_n: int = 5000):
    st.subheader(f"📊 {table}")
    cols_df = get_columns(engine, table, schema)
    rowcount = get_rowcount(engine, table, schema)

    c1, c2, c3 = st.columns([1, 1, 1])
    c1.metric("Rows", f"{rowcount:,}")
    c2.metric("Columns", f"{len(cols_df):,}")

    with st.expander("Schema (information_schema)", expanded=False):
        st.dataframe(cols_df, use_container_width=True, hide_index=True)

    # Sampling strategy for EDA
    limit = min(sample_n, max(1, rowcount))
    with st.spinner("Loading sample for EDA..."):
        df = fetch_dataframe(engine, f'SELECT * FROM "{schema}"."{table}" ORDER BY 1 DESC LIMIT {limit}')

    st.caption(f"Sampled {len(df):,} rows out of {rowcount:,} for quick EDA.")

    if len(df) == 0:
        st.info("No data in table.")
        return

    # Basic overviews
    with st.expander("Preview", expanded=True):
        st.dataframe(df, use_container_width=True)

    with st.expander("Data types & null counts", expanded=False):
        info_df = pd.DataFrame({
            "column": df.columns,
            "dtype": [str(t) for t in df.dtypes.values],
            "nulls": [int(df[c].isna().sum()) for c in df.columns],
            "null_rate": [float(df[c].isna().mean()) for c in df.columns],
            "unique": [int(df[c].nunique(dropna=True)) for c in df.columns],
        })
        st.dataframe(info_df.sort_values(["null_rate", "column"], ascending=[False, True]), use_container_width=True)

    # Numeric description
    numeric_cols = df.select_dtypes(include=["number", "datetime64[ns]"]).columns.tolist()
    if numeric_cols:
        with st.expander("Numeric/date summary", expanded=False):
            st.dataframe(df[numeric_cols].describe(include="all").T, use_container_width=True)

    # Categorical peek
    cat_cols = [c for c in df.columns if c not in numeric_cols]
    if cat_cols:
        with st.expander("Top categories (head 15)", expanded=False):
            top_k = st.slider("Top K", 5, 50, 15, key=f"topk_{table}")
            for c in cat_cols:
                vc = df[c].astype(str).value_counts(dropna=False).head(top_k).reset_index()
                vc.columns = [c, "count"]
                st.markdown(f"**{c}**")
                st.dataframe(vc, use_container_width=True, hide_index=True)

    # JSON columns summary
    json_like_cols = [c for c in df.columns if any(df[c].astype(str).str.startswith(pref, na=False) for pref in ["{", "["]) or str(df[c].dtype) in ("object",)]
    json_like_cols = [c for c in json_like_cols if any(df[c].astype(str).str.startswith("{") | df[c].astype(str).str.startswith("["))]
    if json_like_cols:
        with st.expander("JSON/JSONB keys frequency (sampled)", expanded=False):
            for c in json_like_cols:
                st.markdown(f"**{c}**")
                keys_df = _maybe_json_normalize(df[c])
                if keys_df.empty:
                    st.caption("No parsable JSON objects in sample.")
                else:
                    st.dataframe(keys_df, use_container_width=True, hide_index=True)

    # Simple time trend if timestamp-like columns exist
    ts_cols = [c for c in df.columns if any(k in c.lower() for k in ["time", "date"]) and pd.api.types.is_datetime64_any_dtype(df[c])]
    if ts_cols:
        with st.expander("Simple time trend (count by day)", expanded=False):
            ts_col = st.selectbox("Choose time column", ts_cols, key=f"ts_{table}")
            tmp = df.dropna(subset=[ts_col]).copy()
            tmp["_day"] = tmp[ts_col].dt.floor("D")
            series = tmp.groupby("_day").size().reset_index(name="count")
            st.bar_chart(series.set_index("_day"))


# =============================
# Sidebar – Connection & Navigation
# =============================
with st.sidebar:
    st.header("⚙️ Database Connection")
    st.text_input("Host", key="DB_HOST", value=os.getenv("DB_HOST", "localhost"))
    st.text_input("Port", key="DB_PORT", value=os.getenv("DB_PORT", "5432"))
    st.text_input("Database", key="DB_NAME", value=os.getenv("DB_NAME", "postgres"))
    st.text_input("User", key="DB_USER", value=os.getenv("DB_USER", "postgres"))
    st.text_input("Password", key="DB_PASSWORD", type="password", value=os.getenv("DB_PASSWORD", "postgres"))
    st.text_input("SSL Mode", key="DB_SSLMODE", value=os.getenv("DB_SSLMODE", "prefer"))

    schema = st.text_input("Schema", value=os.getenv("DB_SCHEMA", DEFAULT_SCHEMA))

    if st.button("Connect", type="primary"):
        st.session_state["_conn_url"] = build_conn_url()

# If no connection yet, try from env
conn_url = st.session_state.get("_conn_url") or build_conn_url()

# Header
st.title("🤖 Chatbot Data Explorer & EDA (No OTP)")
st.caption(
    "Explore and analyze your chatbot database with table‑wise EDA, message viewer with rich filters, and quick SQL runner."
)

# Attempt connect
engine: Optional[Engine] = None
try:
    engine = get_engine(conn_url)
    server_now = get_now(engine)
    st.success(f"Connected. Server time: {server_now}")
except Exception as e:
    st.error("Could not connect to the database. Check credentials in the sidebar.")
    st.exception(e)
    st.stop()


# =============================
# Main Tabs
# =============================
tab_overview, tab_tables, tab_messages, tab_sql, tab_exports = st.tabs([
    "Overview",
    "Table EDA",
    "Messages Viewer",
    "SQL Runner",
    "Exports",
])

# -----------------------------
# Overview
# -----------------------------
with tab_overview:
    st.subheader("Database Overview")
    cols = st.columns(4)
    for i, t in enumerate(KNOWN_TABLES):
        try:
            rc = get_rowcount(engine, t, schema)
            cols[i % 4].metric(t, f"{rc:,} rows")
        except Exception as e:
            cols[i % 4].metric(t, "—")

    st.markdown("---")
    st.markdown("### Quick Links")
    st.markdown("• Go to **Table EDA** to inspect schemas, distributions, JSON keys, and time trends.")
    st.markdown("• Go to **Messages Viewer** to browse all messages with filters, full‑text search, and pagination.")
    st.markdown("• Use **SQL Runner** for ad‑hoc queries.")


# -----------------------------
# Table EDA
# -----------------------------
with tab_tables:
    st.subheader("Table‑wise EDA")

    target_tables = st.multiselect(
        "Select tables to analyze",
        options=KNOWN_TABLES,
        default=KNOWN_TABLES,
    )
    sample_n = st.slider("Rows per table to sample for EDA", 500, 50000, 5000, step=500)

    for t in target_tables:
        with st.container(border=True):
            table_eda(engine, t, schema=schema, sample_n=sample_n)


# -----------------------------
# Messages Viewer
# -----------------------------
with tab_messages:
    st.subheader("Browse All Messages")

    # Filters
    with st.expander("Filters", expanded=True):
        c1, c2, c3 = st.columns([1, 1, 1])
        session_id = c1.text_input("Session ID contains")
        msg_type = c2.selectbox("Message type", ["(any)", "user", "assistant", "system", "other"], index=0)
        date_from = c3.date_input("From (date)", value=None)
        c4, c5, c6 = st.columns([1, 1, 2])
        date_to = c4.date_input("To (date)", value=None)
        search = c5.text_input("Full‑text search in content (ILIKE)")
        page_size = c6.select_slider("Page size", options=[25, 50, 100, 200, 500], value=100)

    where = ["1=1"]
    params: Dict[str, object] = {}

    if session_id:
        where.append("session_id ILIKE :sid")
        params["sid"] = f"%{session_id}%"
    if msg_type and msg_type != "(any)":
        where.append("message_type = :mtype")
        params["mtype"] = msg_type
    if search:
        where.append("content ILIKE :q")
        params["q"] = f"%{search}%"
    if date_from:
        where.append("timestamp >= :dfrom")
        params["dfrom"] = datetime.combine(date_from, datetime.min.time())
    if date_to:
        where.append("timestamp < :dto")
        params["dto"] = datetime.combine(date_to + timedelta(days=1), datetime.min.time())

    where_sql = " AND ".join(where)

    # Count query
    count_sql = f'SELECT COUNT(*) FROM "{schema}"."chat_messages" WHERE {where_sql}'
    try:
        total = fetch_dataframe(engine, count_sql, params).iloc[0, 0]
    except Exception as e:
        st.error("Failed to count messages. Check connection and permissions.")
        st.exception(e)
        total = 0

    # Pagination
    total_pages = max(1, math.ceil(total / page_size))
    page = st.number_input("Page", min_value=1, max_value=max(1, total_pages), value=1)
    offset = (page - 1) * page_size

    # Data query
    data_sql = text(
        f"""
        SELECT id, session_id, message_type, content, timestamp, message_metadata
        FROM "{schema}"."chat_messages"
        WHERE {where_sql}
        ORDER BY timestamp DESC
        LIMIT :limit OFFSET :offset
        """
    )
    params_page = dict(params)
    params_page.update({"limit": int(page_size), "offset": int(offset)})

    try:
        df_msg = fetch_dataframe(engine, str(data_sql), params_page)
        st.caption(f"Showing {len(df_msg):,} of {total:,} messages | page {page:,} / {total_pages:,}")
        st.dataframe(df_msg, use_container_width=True)
    except Exception as e:
        st.error("Failed to fetch messages.")
        st.exception(e)

    # Conversation preview by Session ID
    with st.expander("View conversation by Session ID", expanded=False):
        sid_exact = st.text_input("Exact Session ID")
        max_messages = st.slider("Max messages to pull", 50, 2000, 200)
        if sid_exact:
            try:
                convo_df = fetch_dataframe(
                    engine,
                    f"""
                    SELECT message_type, content, timestamp
                    FROM "{schema}"."chat_messages"
                    WHERE session_id = :s
                    ORDER BY timestamp ASC
                    LIMIT :lim
                    """,
                    params={"s": sid_exact, "lim": int(max_messages)},
                )
                for _, row in convo_df.iterrows():
                    role = row["message_type"].upper()
                    st.markdown(f"**{role}** · {row['timestamp']}")
                    st.markdown(
                        f"""
                        <div class='mono' style='white-space: pre-wrap; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px;'>
                        {st.session_state.get('','')}
                        {row['content']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error("Failed to fetch conversation by session.")
                st.exception(e)


# -----------------------------
# SQL Runner
# -----------------------------
with tab_sql:
    st.subheader("Run SQL")
    sql_input = st.text_area(
        "SQL",
        value=textwrap.dedent(
            f"""
            -- Example: row counts for key tables
            SELECT 'chat_messages' AS table, COUNT(*) AS rows FROM "{schema}"."chat_messages"
            UNION ALL SELECT 'chat_feedback', COUNT(*) FROM "{schema}"."chat_feedback"
            UNION ALL SELECT 'chat_sessions', COUNT(*) FROM "{schema}"."chat_sessions";
            """
        ).strip(),
        height=180,
        help="Only SELECT statements are recommended. Use at your own risk.",
    )
    if st.button("Execute", type="primary"):
        try:
            df_sql = fetch_dataframe(engine, sql_input)
            st.dataframe(df_sql, use_container_width=True)
        except Exception as e:
            st.error("Query failed.")
            st.exception(e)


# -----------------------------
# Exports
# -----------------------------
with tab_exports:
    st.subheader("Quick Exports (CSV)")
    pick_table = st.selectbox("Choose a table", KNOWN_TABLES, index=1)
    sample_for_export = st.number_input("Max rows to export", min_value=100, max_value=1_000_000, value=50_000, step=100)
    if st.button("Prepare Download"):
        try:
            df_exp = fetch_dataframe(engine, f'SELECT * FROM "{schema}"."{pick_table}" LIMIT :n', {"n": int(sample_for_export)})
            st.download_button(
                label=f"Download {pick_table}.csv",
                data=df_exp.to_csv(index=False).encode("utf-8"),
                file_name=f"{pick_table}.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error("Export failed.")
            st.exception(e)


# =============================
# Footer
# =============================
st.markdown("---")
st.caption(
    "Built for detailed EDA across all tables in the updated schema. This app retains core explorer components and adds rich filtering, schema introspection, JSON key summaries, and time‑trend views."
)
