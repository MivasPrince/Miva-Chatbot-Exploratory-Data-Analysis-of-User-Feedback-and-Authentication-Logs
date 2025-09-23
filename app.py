# -*- coding: utf-8 -*-
"""app.py

Fully updated Streamlit dashboard for Miva AI database analytics.
"""

import streamlit as st
import pandas as pd
import psycopg2
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas.api.types import is_datetime64_any_dtype
import warnings
from datetime import datetime, timedelta
import time
import os
from typing import Dict, Tuple, List
import json

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Miva AI Database Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with Miva brand theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
        font-family: 'Manrope', sans-serif;
    }

    /* Miva color scheme: Blue (#1e40af), Red (#dc2626), Ash (#64748b) */
    .metric-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.15);
        margin: 0.5rem 0;
        font-family: 'Manrope', sans-serif;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Manrope', sans-serif;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# --- CORE CLASSES (Database, Processing, Visualization) ---

class DatabaseConfig:
    """Database configuration management"""
    @staticmethod
    def get_config() -> Dict[str, str]:
        try:
            if hasattr(st, 'secrets') and 'database' in st.secrets:
                return st.secrets["database"]
        except: pass
        return {
            "host": os.getenv("DB_HOST", "16.170.143.253"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "user": os.getenv("DB_USER", "admin"),
            "password": os.getenv("DB_PASSWORD", "password123"),
            "database": os.getenv("DB_NAME", "miva_ai_db")
        }

class DatabaseManager:
    """Database connection and query management"""
    def __init__(self):
        self.config = DatabaseConfig.get_config()

    @st.cache_data(ttl=300)
    def test_connection(_self) -> Tuple[bool, str]:
        try:
            with psycopg2.connect(**_self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()
            return True, version[0] if version else "Unknown"
        except Exception as e:
            return False, str(e)

    @st.cache_data(ttl=300)
    def query_df(_self, query: str) -> pd.DataFrame:
        try:
            with psycopg2.connect(**_self.config) as conn:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            st.error(f"DataFrame query error: {e}")
            return pd.DataFrame()

class DataProcessor:
    """Data processing utilities"""
    @staticmethod
    def try_parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if df[col].dtype == "object" and any(k in col.lower() for k in ["time", "date", "at", "created", "updated"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
                except Exception: pass
        return df

    @staticmethod
    @st.cache_data(ttl=300)
    def get_table_info(db_manager: DatabaseManager) -> pd.DataFrame:
        query = """
        SELECT relname as tablename, n_live_tup as live_rows
        FROM pg_stat_user_tables ORDER BY n_live_tup DESC;
        """
        return db_manager.query_df(query)

class Visualizer:
    """Visualization utilities using Plotly"""
    MIVA_BLUE = "#1e40af"
    MIVA_RED = "#dc2626"

    @staticmethod
    def plot_metric(label, value, delta=None):
        st.metric(label, value, delta)

    @staticmethod
    def plot_missing_values(df: pd.DataFrame, title: str):
        na_counts = df.isna().sum()
        na_counts = na_counts[na_counts > 0].sort_values(ascending=False)
        if na_counts.empty:
            st.success(f"✅ No missing values in **{title}**")
            return
        fig = px.bar(x=na_counts.values, y=na_counts.index, orientation='h',
                     title=f"Missing Values: {title}", labels={'x': 'Missing Count', 'y': 'Columns'},
                     color=na_counts.values, color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_top_categories(df: pd.DataFrame, col: str, title: str, top_n: int = 10):
        if col not in df.columns: return
        vc = df[col].astype("str").fillna("(Missing)").value_counts().nlargest(top_n)
        if vc.empty: return
        fig = px.bar(vc, y=vc.index, x=vc.values, orientation='h',
                     title=f"Top {top_n} in {col}", labels={'x': 'Count', 'y': col},
                     color=vc.values, color_continuous_scale='Blues')
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_time_trends(df: pd.DataFrame, time_col: str, title: str, freq: str = "D"):
        if time_col not in df.columns or not is_datetime64_any_dtype(df[time_col]):
            st.warning(f"Datetime column '{time_col}' not found for '{title}' trend plot.")
            return
        s = pd.to_datetime(df[time_col], errors="coerce", utc=True).dropna()
        if s.empty: return
        counts = s.dt.floor(freq).value_counts().sort_index()
        fig = px.line(counts, x=counts.index, y=counts.values, title=title,
                      labels={'x': 'Date', 'y': 'Count'}, markers=True)
        fig.update_traces(line_color=Visualizer.MIVA_BLUE)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_interactive_rating_distribution(df: pd.DataFrame, col: str, title: str, comment_col: str):
        # This function is retained from the original script for detailed feedback analysis
        # (For brevity, its original code is assumed to be here)
        st.markdown(f"#### 📊 Interactive Rating Distribution for {title}")
        if col not in df.columns:
            st.warning("Rating column not found.")
            return
        rating_counts = df[col].dropna().value_counts().sort_index()
        fig = px.bar(rating_counts, x=rating_counts.index, y=rating_counts.values,
                     title=f"Distribution of Ratings: {title}", labels={'x': 'Rating', 'y': 'Count'})
        fig.update_layout(xaxis=dict(type='category'))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"#### 💬 Comments for {title}")
        if comment_col in df.columns:
            comments_df = df[df[comment_col].notna() & (df[comment_col] != '')][[col, comment_col]]
            st.dataframe(comments_df, use_container_width=True)
        else:
            st.warning("Comment column not found.")


# --- UI RENDERING FUNCTIONS FOR TABS ---

def render_feedback_tab(db_manager, viz, date_range):
    """Renders the EDA for all feedback-related tables."""
    st.markdown("### 🗣️ User & Chat Feedback Analysis")

    st.info("This tab analyzes user feedback from `chat_feedback` and `user_feedback` tables.")

    # Load data
    df_chat_feedback = db_manager.query_df("SELECT * FROM chat_feedback;")
    df_user_feedback = db_manager.query_df("SELECT * FROM user_feedback;")

    # Process data
    df_chat_feedback = DataProcessor.try_parse_datetimes(df_chat_feedback)
    df_user_feedback = DataProcessor.try_parse_datetimes(df_user_feedback)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💬 Chat Feedback (`chat_feedback`)")
        if not df_chat_feedback.empty:
            viz.plot_metric("Total Chat Feedback", f"{len(df_chat_feedback):,}")
            viz.plot_interactive_rating_distribution(df_chat_feedback, 'rating', "Chat Feedback", 'comment')
            viz.plot_time_trends(df_chat_feedback, 'created_at', "Chat Feedback Over Time")
            with st.expander("Raw Chat Feedback Data"):
                st.dataframe(df_chat_feedback, use_container_width=True)
        else:
            st.warning("No data found in `chat_feedback`.")

    with col2:
        st.markdown("#### ⭐ General User Feedback (`user_feedback`)")
        if not df_user_feedback.empty:
            viz.plot_metric("Total General Feedback", f"{len(df_user_feedback):,}")
            viz.plot_interactive_rating_distribution(df_user_feedback, 'rating', "General User Feedback", 'feedback_text')
            viz.plot_time_trends(df_user_feedback, 'created_at', "General Feedback Over Time")
            with st.expander("Raw User Feedback Data"):
                st.dataframe(df_user_feedback, use_container_width=True)
        else:
            st.warning("No data found in `user_feedback`.")

def render_chat_analysis_tab(db_manager, viz):
    """Renders the EDA for chat and session tables, including the chat viewer."""
    st.markdown("### 🗨️ Chat & Session Analysis")
    st.info("Analyze individual conversations and session metadata from `chat_messages` and `chat_sessions`.")

    # Load data
    df_sessions = db_manager.query_df("SELECT * FROM chat_sessions ORDER BY created_at DESC;")
    df_messages = db_manager.query_df("SELECT * FROM chat_messages;")

    if df_sessions.empty or df_messages.empty:
        st.warning("No session or message data available for analysis.")
        return

    # --- Interactive Chat Viewer ---
    st.markdown("#### 📜 View Individual Chat Conversations")
    session_list = df_sessions['session_id'].unique().tolist()
    selected_session = st.selectbox("Select a Session ID to view its messages:", session_list)

    if selected_session:
        session_messages = df_messages[df_messages['session_id'] == selected_session].sort_values(by="timestamp")
        if not session_messages.empty:
            for _, row in session_messages.iterrows():
                role = "user" if row['message_type'] == 'human' else "assistant"
                with st.chat_message(role):
                    st.write(row['content'])
                    if row['timestamp']:
                        st.caption(f"_{pd.to_datetime(row['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}_")
        else:
            st.info("No messages found for the selected session.")

    st.markdown("---")
    # --- Overall Session Analysis ---
    st.markdown("#### 📈 Overall Session Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        viz.plot_metric("Total Sessions", f"{df_sessions['session_id'].nunique():,}")
    with col2:
        viz.plot_metric("Total Messages", f"{len(df_messages):,}")
    with col3:
        avg_msgs_per_session = len(df_messages) / df_sessions['session_id'].nunique() if df_sessions['session_id'].nunique() > 0 else 0
        viz.plot_metric("Avg Msgs/Session", f"{avg_msgs_per_session:.2f}")

    # Visualizations and Data Previews
    df_sessions = DataProcessor.try_parse_datetimes(df_sessions)
    viz.plot_time_trends(df_sessions, 'created_at', "Chat Sessions Over Time")

    with st.expander("Raw Chat Sessions Data (`chat_sessions`)"):
        st.dataframe(df_sessions, use_container_width=True)
    with st.expander("Raw Chat Messages Data (`chat_messages`)"):
        st.dataframe(df_messages, use_container_width=True)

def render_otp_tab(db_manager, viz):
    """Renders the EDA for OTP tables."""
    st.markdown("### 🔐 One-Time Password (OTP) Analysis")
    st.info("This section provides insights into OTP generation and verification from `otps` and `otp_verifications`.")

    # Load data
    df_otps = db_manager.query_df("SELECT * FROM otps;")
    df_verifications = db_manager.query_df("SELECT * FROM otp_verifications;")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### OTP Generation (`otps`)")
        if not df_otps.empty:
            df_otps = DataProcessor.try_parse_datetimes(df_otps)
            used_count = df_otps['is_used'].sum()
            total_count = len(df_otps)
            usage_rate = (used_count / total_count * 100) if total_count > 0 else 0

            c1, c2, c3 = st.columns(3)
            with c1: viz.plot_metric("Total OTPs Generated", f"{total_count:,}")
            with c2: viz.plot_metric("OTPs Used", f"{used_count:,}")
            with c3: viz.plot_metric("Usage Rate", f"{usage_rate:.2f}%")

            viz.plot_top_categories(df_otps, 'purpose', 'OTP Purpose')
            viz.plot_time_trends(df_otps, 'created_at', 'OTP Generation Over Time')
            with st.expander("Raw OTP Generation Data"):
                st.dataframe(df_otps, use_container_width=True)
        else:
            st.warning("No data found in `otps` table.")

    with col2:
        st.markdown("#### OTP Verifications (`otp_verifications`)")
        if not df_verifications.empty:
            df_verifications = DataProcessor.try_parse_datetimes(df_verifications)
            verified_count = df_verifications['is_verified'].sum()
            total_verifications = len(df_verifications)
            verification_rate = (verified_count / total_verifications * 100) if total_verifications > 0 else 0

            c1, c2, c3 = st.columns(3)
            with c1: viz.plot_metric("Total Verifications", f"{total_verifications:,}")
            with c2: viz.plot_metric("Successful Verifications", f"{verified_count:,}")
            with c3: viz.plot_metric("Success Rate", f"{verification_rate:.2f}%")

            viz.plot_time_trends(df_verifications, 'created_at', 'OTP Verifications Over Time')
            with st.expander("Raw OTP Verification Data"):
                st.dataframe(df_verifications, use_container_width=True)
        else:
            st.warning("No data found in `otp_verifications` table.")


# --- MAIN APPLICATION STRUCTURE ---

def login_page():
    """Displays the login page and handles authentication."""
    st.markdown('<h1 class="main-header">Miva AI Dashboard Login</h1>', unsafe_allow_html=True)
    CORRECT_USERNAME = "miva_admin"
    CORRECT_PASSWORD = "password123"

    with st.form("login_form"):
        st.image("https://i.imgur.com/azwWWQN.jpeg", width=200)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Log In"):
            if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect username or password")

def create_dashboard():
    """Main dashboard application layout and logic"""
    db_manager = DatabaseManager()
    viz = Visualizer()

    st.markdown('<h1 class="main-header">Miva AI Database Analytics Dashboard</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://i.imgur.com/azwWWQN.jpeg", use_container_width=True)
        st.markdown("### 🔧 Dashboard Controls")
        if st.button("🔄 Test Connection"):
            success, info = db_manager.test_connection()
            st.success(f"Connection OK! Version: {info.split(',')[0]}") if success else st.error(f"Connection Failed: {info}")
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
        date_range = st.date_input("Date Range", value=(datetime.now() - timedelta(days=30), datetime.now()))
        st.markdown("---")
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()

    tab_list = [
        "📋 Overview",
        "🗣️ Feedback Analysis",
        "🗨️ Chat & Session Analysis",
        "🔐 OTP Analysis",
        "📊 Custom Analysis"
    ]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_list)

    with tab1:
        st.markdown("### 📈 Database Overview")
        col1, col2 = st.columns(2)
        with col1:
            table_info = DataProcessor.get_table_info(db_manager)
            if not table_info.empty:
                st.metric("📊 Total Tables", len(table_info))
                st.metric("Records (Live Rows)", f"{table_info['live_rows'].sum():,}")
                fig = px.bar(table_info, x='tablename', y='live_rows', title="Records per Table",
                             labels={'live_rows': 'Live Records', 'tablename': 'Table Name'}, color_discrete_sequence=[viz.MIVA_BLUE])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Could not retrieve table statistics.")
        with col2:
            st.dataframe(table_info, use_container_width=True)

    with tab2:
        render_feedback_tab(db_manager, viz, date_range)

    with tab3:
        render_chat_analysis_tab(db_manager, viz)

    with tab4:
        render_otp_tab(db_manager, viz)

    with tab5:
        st.markdown("### 📊 Custom Analysis")
        st.info("💡 Write your own SQL query to explore the database.")
        query = st.text_area("SQL Query", "SELECT * FROM chat_feedback LIMIT 100;", height=200)
        if st.button("🚀 Run Query"):
            with st.spinner("Executing your query..."):
                df_custom = db_manager.query_df(query)
                if not df_custom.empty:
                    st.success(f"Query returned {len(df_custom)} rows.")
                    st.dataframe(df_custom, use_container_width=True)
                else:
                    st.warning("Query returned no results.")

def main():
    """Main function to run the app with authentication."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if st.session_state["authenticated"]:
        create_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()
