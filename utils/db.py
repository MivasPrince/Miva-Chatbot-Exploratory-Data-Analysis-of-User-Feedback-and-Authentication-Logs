import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

def _secrets():
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

@st.cache_resource(show_spinner=False)
def get_engine():
    cfg = _secrets()
    assert cfg["host"] and cfg["database"] and cfg["user"], "Database secrets missing."
    url = (
        f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['database']}?sslmode={cfg['sslmode']}"
    )
    engine = create_engine(url, pool_pre_ping=True)
    return engine

@st.cache_data(ttl=300, show_spinner=False)
def list_tables(schema: str):
    engine = get_engine()
    q = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = :schema
        ORDER BY table_name;
    """)
    with engine.connect() as conn:
        return [r[0] for r in conn.execute(q, {"schema": schema}).fetchall()]

@st.cache_data(ttl=300, show_spinner=False)
def get_columns(table: str, schema: str):
    engine = get_engine()
    q = text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
        ORDER BY ordinal_position;
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"schema": schema, "table": table}).fetchall()
    return pd.DataFrame(rows, columns=["column_name", "data_type"])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_df(table: str, schema: str, limit: int | None = 5000):
    engine = get_engine()
    if limit and limit > 0:
        sql = text(f'SELECT * FROM "{schema}"."{table}" LIMIT :lim')
        params = {"lim": int(limit)}
    else:
        sql = text(f'SELECT * FROM "{schema}"."{table}"')
        params = {}
    return pd.read_sql(sql, get_engine().connect(), params=params)
