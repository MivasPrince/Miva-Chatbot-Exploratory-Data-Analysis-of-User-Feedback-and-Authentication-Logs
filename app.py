import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine, text

# =========================
# Page / App Configuration
# =========================
st.set_page_config(page_title="MIVA DB EDA", page_icon="📊", layout="wide")

st.title("📊 MIVA – Database Explorer & EDA")
st.caption("Explore **chat_feedback**, **chat_messages**, **chat_sessions**, **conversation_history**, **conversation_sessions**, **otp_verifications**, **otps**, **user_feedback**.")

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
SCHEMA = CFG.get("schema", "public")

# =========================
# DB Connection (psycopg v3)
# =========================
@st.cache_resource(show_spinner=False)
def get_engine():
    assert CFG["host"] and CFG["database"] and CFG["user"], "Database secrets missing."
    url = (
        f"postgresql+psycopg://{CFG['user']}:{CFG['password']}"
        f"@{CFG['host']}:{CFG['port']}/{CFG['database']}?sslmode={CFG['sslmode']}"
    )
    engine = create_engine(url, pool_pre_ping=True)
    return engine

# =========================
# Data access helpers
# =========================
@st.cache_data(ttl=300, show_spinner=False)
def list_tables(schema: str) -> list[str]:
    q = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = :schema
        ORDER BY table_name;
    """)
    with get_engine().connect() as conn:
        return [r[0] for r in conn.execute(q, {"schema": schema}).fetchall()]

@st.cache_data(ttl=300, show_spinner=False)
def get_columns(schema: str, table: str) -> pd.DataFrame:
    q = text("""
        SELECT
          c.ordinal_position,
          c.column_name,
          c.data_type,
          c.is_nullable,
          c.column_default
        FROM information_schema.columns c
        WHERE c.table_schema = :schema AND c.table_name = :table
        ORDER BY c.ordinal_position;
    """)
    with get_engine().connect() as conn:
        rows = conn.execute(q, {"schema": schema, "table": table}).fetchall()
    return pd.DataFrame(rows, columns=["ordinal_position","column_name","data_type","is_nullable","column_default"])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_df(schema: str, table: str, limit: int | None = 5000) -> pd.DataFrame:
    if limit and limit > 0:
        sql = text(f'SELECT * FROM "{schema}"."{table}" LIMIT :lim')
        params = {"lim": int(limit)}
    else:
        sql = text(f'SELECT * FROM "{schema}"."{table}"')
        params = {}
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn, params=params)

@st.cache_data(ttl=300, show_spinner=False)
def count_rows(schema: str, table: str) -> int:
    sql = text(f'SELECT COUNT(*) FROM "{schema}"."{table}"')
    with get_engine().connect() as conn:
        return int(conn.execute(sql).scalar())

def try_parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == "object" and any(k in col.lower() for k in ["time","date","created","updated","timestamp","at"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
            except Exception:
                pass
    return df

# =========================
# Plot helpers (matplotlib)
# =========================
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

def plot_numeric_hists(df: pd.DataFrame, title: str, bins: int = 30):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        st.info(f"No numeric columns in **{title}**.")
        return
    for col in num_cols:
        data = df[col].dropna()
        if data.empty:
            continue
        fig = plt.figure(figsize=(6, 3.6))
        plt.hist(data.values, bins=bins)
        plt.title(f"{title}: Histogram of {col}")
        plt.xlabel(col); plt.ylabel("Frequency")
        st.pyplot(fig)

def plot_categorical_bars(df: pd.DataFrame, title: str, top_n: int = 20):
    cat_cols = df.select_dtypes(include=["object","category"]).columns.tolist()
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
        plt.xlabel("Count"); plt.ylabel(col)
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
        s = df[col].dropna()
        if s.empty:
            continue
        fig = plt.figure(figsize=(6, 2.6))
        plt.boxplot(s.values, vert=False, whis=1.5)
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
        series = s.dt.tz_localize(None).dt.date.value_counts().sort_index()
        if series.empty:
            continue
        fig = plt.figure(figsize=(10, 3.4))
        plt.plot(list(series.index), series.values)
        plt.title(f"{title}: Daily count by {col}")
        plt.xlabel("Date"); plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("🔌 Data Source")
    st.write(f"**Host**: `{CFG.get('host')}`")
    st.write(f"**DB**: `{CFG.get('database')}`")
    st.write(f"**Schema**: `{SCHEMA}`")

    st.divider()
    st.subheader("📂 Tables")
    tables = list_tables(SCHEMA)
    if not tables:
        st.error("No tables found. Check DB credentials / schema / privileges.")
        st.stop()

    table = st.selectbox("Default table for EDA", options=tables, index=tables.index("chat_messages") if "chat_messages" in tables else 0)
    limit = st.slider("Max rows to load", min_value=500, max_value=50000, value=5000, step=500)

    st.divider()
    st.subheader("⚙️ Display Options")
    show_raw = st.checkbox("Show raw data preview", value=True)
    top_n_cats = st.number_input("Top categories (bar charts)", min_value=5, max_value=50, value=20, step=1)
    bins_num = st.number_input("Histogram bins (numeric)", min_value=10, max_value=100, value=30, step=5)

# =========================
# Tabs
# =========================
tab_overview, tab_table_eda, tab_all_eda, tab_messages, tab_sql = st.tabs(
    ["Overview", "Table EDA", "Run EDA for ALL Tables", "Messages Explorer", "SQL Runner"]
)

# ---------- Overview ----------
with tab_overview:
    st.subheader("Tables in schema")
    st.write(", ".join(f"`{t}`" for t in tables))

    # quick sizes
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Row counts** (first 8 tables)")
        sizes = []
        for t in tables[:8]:
            try:
                sizes.append((t, count_rows(SCHEMA, t)))
            except Exception as e:
                sizes.append((t, f"error: {e}"))
        st.dataframe(pd.DataFrame(sizes, columns=["table","row_count"]), use_container_width=True)
    with col2:
        st.markdown("**Schema of selected table**")
        st.dataframe(get_columns(SCHEMA, table), use_container_width=True)

# ---------- Per-table EDA ----------
with tab_table_eda:
    st.subheader(f"EDA · `{SCHEMA}.{table}`")
    with st.spinner("Loading table…"):
        df = fetch_df(SCHEMA, table, limit=limit)
        df = try_parse_datetimes(df)

    st.markdown(f"**Shape:** `{df.shape[0]} rows × {df.shape[1]} cols`")
    if show_raw:
        st.write("**Sample (first 1,000 rows):**")
        st.dataframe(df.head(1000), use_container_width=True)

    st.markdown("**Column dtypes**")
    st.dataframe(pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)}), use_container_width=True)

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

    st.divider()
    plot_missingness(df, title=table)
    plot_numeric_hists(df, title=table, bins=bins_num)
    plot_categorical_bars(df, title=table, top_n=top_n_cats)
    plot_corr_heatmap(df, title=table)
    plot_boxplots(df, title=table)
    plot_time_trends(df, title=table)

# ---------- All-tables EDA ----------
with tab_all_eda:
    st.subheader("Run EDA for ALL tables")
    st.caption("This can be heavy. Uses the row limit in the sidebar for each table.")
    if st.button("Run EDA for all tables"):
        for t in tables:
            st.markdown(f"### `{SCHEMA}.{t}`")
            try:
                df_t = fetch_df(SCHEMA, t, limit=limit)
                df_t = try_parse_datetimes(df_t)
                st.write(f"**Shape:** `{df_t.shape[0]} × {df_t.shape[1]}`")
                st.dataframe(get_columns(SCHEMA, t), use_container_width=True)
                plot_missingness(df_t, title=t)
                plot_numeric_hists(df_t, title=t, bins=bins_num)
                plot_categorical_bars(df_t, title=t, top_n=top_n_cats)
                plot_corr_heatmap(df_t, title=t)
                plot_boxplots(df_t, title=t)
                plot_time_trends(df_t, title=t)
                st.divider()
            except Exception as e:
                st.warning(f"Failed EDA for `{t}`: {e}")

# ---------- Messages Explorer ----------
with tab_messages:
    st.subheader("💬 Messages Explorer (`chat_messages`)")
    if "chat_messages" not in tables:
        st.warning("`chat_messages` table not found.")
    else:
        # Filters
        colA, colB, colC, colD = st.columns([1,1,1,2])
        with colA:
            page_size = st.selectbox("Page size", [25, 50, 100, 200], index=1)
        with colB:
            page = st.number_input("Page", min_value=1, value=1, step=1)
        with colC:
            # message_type values
            try:
                q_types = text(f'SELECT DISTINCT message_type FROM "{SCHEMA}"."chat_messages" ORDER BY 1')
                with get_engine().connect() as conn:
                    types = [r[0] for r in conn.execute(q_types).fetchall() if r[0] is not None]
            except Exception:
                types = []
            msg_type = st.selectbox("Message type", options=["(all)"] + types)
        with colD:
            keyword = st.text_input("Search keyword in content (ILIKE)", value="")

        colE, colF = st.columns(2)
        with colE:
            # date range on timestamp
            default_end = datetime.utcnow().date()
            default_start = default_end - timedelta(days=30)
            start_date = st.date_input("Start date (timestamp)", value=default_start)
        with colF:
            end_date = st.date_input("End date (timestamp)", value=default_end)

        session_id = st.text_input("Filter by session_id (exact match)", value="")

        # Build WHERE
        where = ['1=1']
        params = {}
        if msg_type != "(all)":
            where.append("message_type = :mt")
            params["mt"] = msg_type
        if keyword.strip():
            where.append("content ILIKE :kw")
            params["kw"] = f"%{keyword.strip()}%"
        if session_id.strip():
            where.append("session_id = :sid")
            params["sid"] = session_id.strip()
        if start_date:
            where.append("timestamp >= :start_ts")
            params["start_ts"] = f"{start_date} 00:00:00+00"
        if end_date:
            where.append("timestamp <= :end_ts")
            params["end_ts"] = f"{end_date} 23:59:59.999+00"

        where_sql = " AND ".join(where)

        # Count
        q_count = text(f'SELECT COUNT(*) FROM "{SCHEMA}"."chat_messages" WHERE {where_sql}')
        with get_engine().connect() as conn:
            total = int(conn.execute(q_count, params).scalar())

        # Page fetch
        offset = (page - 1) * page_size
        q_page = text(
            f'''
            SELECT id, session_id, message_type, content, "timestamp", message_metadata
            FROM "{SCHEMA}"."chat_messages"
            WHERE {where_sql}
            ORDER BY "timestamp" DESC
            LIMIT :lim OFFSET :off
            '''
        )
        params_page = params | {"lim": int(page_size), "off": int(offset)}
        df_msgs = pd.read_sql(q_page, get_engine().connect(), params=params_page)

        st.write(f"**Results:** {len(df_msgs)} / {total} rows  ·  Page {page} of {max(1, (total + page_size - 1) // page_size)}")
        st.dataframe(df_msgs, use_container_width=True, height=500)

        # CSV export
        if not df_msgs.empty:
            csv = df_msgs.to_csv(index=False).encode("utf-8")
            st.download_button("Download current page as CSV", data=csv, file_name="chat_messages_page.csv", mime="text/csv")

        # Optional: session context (shows latest 20 messages in that session)
        if st.toggle("Show conversation context for a session_id"):
            sid_ctx = st.text_input("Enter session_id for context")
            if sid_ctx.strip():
                q_ctx = text(
                    f'''
                    SELECT id, session_id, message_type, content, "timestamp"
                    FROM "{SCHEMA}"."chat_messages"
                    WHERE session_id = :sid
                    ORDER BY "timestamp" DESC
                    LIMIT 200
                    '''
                )
                df_ctx = pd.read_sql(q_ctx, get_engine().connect(), params={"sid": sid_ctx.strip()})
                st.write(f"Showing {len(df_ctx)} messages (latest first) for session_id = `{sid_ctx}`")
                st.dataframe(df_ctx, use_container_width=True, height=600)

# ---------- SQL Runner ----------
with tab_sql:
    st.subheader("📝 SQL Runner (read-only)")
    st.markdown("Use `LIMIT` to keep results light. Mutation queries are blocked.")
    default_sql = f'SELECT * FROM "{SCHEMA}"."{table}" LIMIT 50;'
    user_sql = st.text_area("SQL", value=default_sql, height=160)
    run = st.button("Run query")
    if run and user_sql.strip():
        try:
            lowered = user_sql.strip().lower()
            if any(kw in lowered for kw in ["update ", "insert ", "delete ", "drop ", "alter ", "create ", "truncate "]):
                st.error("Mutation queries are disabled for safety.")
            else:
                dfq = pd.read_sql(text(user_sql), get_engine().connect())
                st.success(f"Returned {len(dfq)} rows.")
                st.dataframe(dfq, use_container_width=True)
                if not dfq.empty:
                    csv = dfq.to_csv(index=False).encode("utf-8")
                    st.download_button("Download results as CSV", data=csv, file_name="query_results.csv", mime="text/csv")
        except Exception as e:
            st.exception(e)

st.caption("© MIVA — DB EDA & Explorer. Keep credentials in Streamlit Secrets or env vars. Read-only recommended.")
