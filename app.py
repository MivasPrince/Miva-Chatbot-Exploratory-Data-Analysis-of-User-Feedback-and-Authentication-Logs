import streamlit as st
import pandas as pd
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas.api.types import is_datetime64_any_dtype
import warnings
from datetime import datetime, timedelta
import time

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Miva AI Database Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 50%, #f0f2f6 100%);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .status-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .status-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Database configuration
@st.cache_data
def get_db_config():
    return {
        "host": "16.170.143.253",
        "port": 5432,
        "user": "admin",
        "password": "password123",
        "database": "miva_ai_db"
    }

# Database connection functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def test_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(**get_db_config())
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        return True, version[0] if version else "Unknown"
    except Exception as e:
        return False, str(e)

@st.cache_data(ttl=300)
def run_query(query):
    """Execute a query and return results"""
    try:
        conn = psycopg2.connect(**get_db_config())
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Query error: {e}")
        return []

@st.cache_data(ttl=300)
def query_df(query):
    """Run a SQL query and return result as Pandas DataFrame"""
    try:
        conn = psycopg2.connect(**get_db_config())
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"DataFrame query error: {e}")
        return pd.DataFrame()

def try_parse_datetimes(df):
    """Auto-parse likely datetime columns"""
    for col in df.columns:
        if df[col].dtype == "object" and any(k in col.lower() for k in ["time","date","at","created","updated"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore", utc=True)
            except Exception:
                pass
    return df

# Plotting functions
def plot_missingness_plotly(df, title):
    """Create interactive missing values plot"""
    na_counts = df.isna().sum()
    na_counts = na_counts[na_counts > 0].sort_values(ascending=False)
    
    if na_counts.empty:
        st.info(f"✅ No missing values in {title}")
        return
    
    fig = px.bar(
        x=na_counts.values,
        y=na_counts.index,
        orientation='h',
        title=f"{title}: Missing Values per Column",
        labels={'x': 'Missing Count', 'y': 'Columns'},
        color=na_counts.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(height=max(300, 40*len(na_counts)))
    st.plotly_chart(fig, use_container_width=True)

def plot_rating_histogram_plotly(df, col, title):
    """Create interactive rating histogram"""
    data = df[col].dropna()
    if data.empty:
        st.warning(f"No data in {col}")
        return
    
    fig = px.histogram(
        x=data,
        nbins=5,
        title=f"{title}: Distribution of {col}",
        labels={'x': col, 'y': 'Frequency'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_xaxis(dtick=1)
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

def plot_top_categories_plotly(df, col, title, top_n=20):
    """Create interactive top categories plot"""
    if col not in df.columns:
        st.warning(f"Column '{col}' not found in {title}")
        return
    
    vc = df[col].astype("object").fillna("(Missing)").value_counts().head(top_n)
    if vc.empty:
        st.warning(f"No data in '{col}' for {title}")
        return
    
    fig = px.bar(
        x=vc.values,
        y=vc.index,
        orientation='h',
        title=f"{title}: Top {top_n} {col} Values",
        labels={'x': 'Count', 'y': col},
        color=vc.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=max(400, 30*len(vc)))
    fig.update_yaxis(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

def plot_time_trends_plotly(df, title, freq="D"):
    """Create interactive time trends plot"""
    time_cols = [c for c in df.columns if is_datetime64_any_dtype(df[c])]
    if not time_cols:
        st.warning(f"No datetime columns detected in {title}")
        return
    
    for col in time_cols:
        s = pd.to_datetime(df[col], errors="coerce", utc=True).dropna()
        if s.empty:
            continue
        
        s = s.dt.tz_convert(None)
        stamped = s.dt.floor(freq)
        counts = stamped.value_counts().sort_index()
        
        if counts.empty:
            continue
        
        fig = px.line(
            x=counts.index,
            y=counts.values,
            title=f"{title}: Trends by {col} ({freq})",
            labels={'x': 'Time', 'y': 'Count'}
        )
        fig.update_traces(line_color='#1f77b4', line_width=2)
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

def plot_text_length_plotly(df, col, title, min_len=3):
    """Plot text length distribution"""
    if col not in df.columns or df[col].dtype != "object":
        return
    
    lengths = df[col].dropna().astype(str).str.len()
    if lengths.empty or lengths.median() < min_len:
        return
    
    fig = px.histogram(
        x=lengths,
        nbins=30,
        title=f"{title}: Text Length Distribution of {col}",
        labels={'x': 'Length (characters)', 'y': 'Frequency'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Miva AI Database Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Dashboard Controls")
        
        # Connection test
        st.markdown("#### Database Connection")
        if st.button("🔄 Test Connection", type="primary"):
            with st.spinner("Testing connection..."):
                success, info = test_connection()
                if success:
                    st.success("✅ Connected successfully!")
                    st.info(f"PostgreSQL: {info[:50]}...")
                else:
                    st.error(f"❌ Connection failed: {info}")
        
        # Refresh data
        st.markdown("#### Data Management")
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("Cache cleared! Data will be refreshed.")
            st.experimental_rerun()
        
        # Analysis options
        st.markdown("#### Analysis Options")
        show_missing = st.checkbox("Show Missing Values Analysis", True)
        show_distributions = st.checkbox("Show Data Distributions", True)
        show_trends = st.checkbox("Show Time Trends", True)
        show_text_analysis = st.checkbox("Show Text Analysis", False)
        
        # Table selection
        st.markdown("#### Table Selection")
        selected_tables = st.multiselect(
            "Select tables to analyze:",
            ["chat_feedback", "otps"],
            default=["chat_feedback", "otps"]
        )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "💬 Chat Feedback", "🔐 OTPs", "📊 Custom Analysis"])
    
    with tab1:
        st.markdown("### Database Overview")
        
        # Load basic info
        with st.spinner("Loading database information..."):
            try:
                # Get table list
                tables = run_query("""
                    SELECT table_name, 
                           (xpath('/row/cnt/text()', xml_count))[1]::text::int as row_count
                    FROM (
                        SELECT table_name,
                               query_to_xml(format('SELECT count(*) as cnt FROM %I', table_name), false, true, '') as xml_count
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                    ) t;
                """)
                
                if tables:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="metric-container status-success">', unsafe_allow_html=True)
                        st.metric("📊 Total Tables", len(tables))
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show table details
                    st.markdown("### 📋 Tables Information")
                    table_df = pd.DataFrame(tables, columns=['Table Name', 'Row Count'])
                    
                    # Create metrics for each table
                    cols = st.columns(len(table_df))
                    for i, (idx, row) in enumerate(table_df.iterrows()):
                        with cols[i]:
                            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                            st.metric(f"📊 {row['Table Name']}", f"{row['Row Count']:,} rows")
                            st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error loading overview: {e}")
    
    with tab2:
        if "chat_feedback" in selected_tables:
            st.markdown("### 💬 Chat Feedback Analysis")
            
            with st.spinner("Loading chat feedback data..."):
                df_chat = query_df("SELECT * FROM chat_feedback;")
                
                if not df_chat.empty:
                    df_chat = try_parse_datetimes(df_chat)
                    
                    # Basic stats
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Total Records", f"{len(df_chat):,}")
                    with col2:
                        if 'rating' in df_chat.columns:
                            avg_rating = df_chat['rating'].mean()
                            st.metric("⭐ Average Rating", f"{avg_rating:.2f}")
                    with col3:
                        if 'created_at' in df_chat.columns:
                            latest = df_chat['created_at'].max()
                            st.metric("📅 Latest Entry", latest.strftime("%Y-%m-%d") if pd.notna(latest) else "N/A")
                    with col4:
                        unique_users = df_chat['email'].nunique() if 'email' in df_chat.columns else 0
                        st.metric("👥 Unique Users", f"{unique_users:,}")
                    
                    # Analysis sections
                    if show_missing:
                        st.markdown("#### Missing Values Analysis")
                        plot_missingness_plotly(df_chat, "Chat Feedback")
                    
                    if show_distributions:
                        st.markdown("#### Data Distributions")
                        
                        # Rating distribution
                        if 'rating' in df_chat.columns:
                            plot_rating_histogram_plotly(df_chat, 'rating', 'Chat Feedback')
                        
                        # Top categories
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'user_agent' in df_chat.columns:
                                plot_top_categories_plotly(df_chat, 'user_agent', 'Chat Feedback', 10)
                        
                        with col2:
                            if 'ip_address' in df_chat.columns:
                                plot_top_categories_plotly(df_chat, 'ip_address', 'Chat Feedback', 10)
                    
                    if show_trends:
                        st.markdown("#### Time Trends")
                        plot_time_trends_plotly(df_chat, "Chat Feedback")
                    
                    if show_text_analysis:
                        st.markdown("#### Text Analysis")
                        if 'email' in df_chat.columns:
                            plot_text_length_plotly(df_chat, 'email', 'Chat Feedback')
                    
                    # Data preview
                    with st.expander("📋 Data Preview", expanded=False):
                        st.dataframe(df_chat.head(100), use_container_width=True)
                        
                        # Download button
                        csv = df_chat.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Chat Feedback Data",
                            data=csv,
                            file_name=f"chat_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                else:
                    st.warning("No chat feedback data found.")
    
    with tab3:
        if "otps" in selected_tables:
            st.markdown("### 🔐 OTP Analysis")
            
            with st.spinner("Loading OTP data..."):
                df_otps = query_df("SELECT * FROM otps;")
                
                if not df_otps.empty:
                    df_otps = try_parse_datetimes(df_otps)
                    
                    # Basic stats
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Total OTPs", f"{len(df_otps):,}")
                    with col2:
                        if 'otp_code' in df_otps.columns:
                            avg_length = df_otps['otp_code'].astype(str).str.len().mean()
                            st.metric("📏 Avg OTP Length", f"{avg_length:.1f}")
                    with col3:
                        if 'used' in df_otps.columns:
                            used_rate = df_otps['used'].mean() * 100
                            st.metric("✅ Usage Rate", f"{used_rate:.1f}%")
                    with col4:
                        unique_emails = df_otps['email'].nunique() if 'email' in df_otps.columns else 0
                        st.metric("👥 Unique Users", f"{unique_emails:,}")
                    
                    # Analysis sections
                    if show_missing:
                        st.markdown("#### Missing Values Analysis")
                        plot_missingness_plotly(df_otps, "OTPs")
                    
                    if show_distributions:
                        st.markdown("#### Data Distributions")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # OTP length distribution
                            if 'otp_code' in df_otps.columns:
                                lengths = df_otps['otp_code'].dropna().astype(str).str.len()
                                if not lengths.empty:
                                    fig = px.histogram(
                                        x=lengths,
                                        title="OTP Code Length Distribution",
                                        labels={'x': 'Length', 'y': 'Frequency'}
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Status distribution
                            if 'used' in df_otps.columns:
                                status_counts = df_otps['used'].value_counts()
                                fig = px.pie(
                                    values=status_counts.values,
                                    names=['Used' if x else 'Unused' for x in status_counts.index],
                                    title="OTP Usage Status"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                    
                    if show_trends:
                        st.markdown("#### Time Trends")
                        plot_time_trends_plotly(df_otps, "OTPs")
                    
                    # Data preview
                    with st.expander("📋 Data Preview", expanded=False):
                        st.dataframe(df_otps.head(100), use_container_width=True)
                        
                        # Download button
                        csv = df_otps.to_csv(index=False)
                        st.download_button(
                            label="📥 Download OTP Data",
                            data=csv,
                            file_name=f"otps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                else:
                    st.warning("No OTP data found.")
    
    with tab4:
        st.markdown("### 📊 Custom SQL Analysis")
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **💡 Pro Tip:** Write custom SQL queries to explore your data in depth. 
        Some example queries you can try:
        - `SELECT COUNT(*) FROM chat_feedback WHERE rating >= 4;`
        - `SELECT email, COUNT(*) as otp_count FROM otps GROUP BY email ORDER BY otp_count DESC LIMIT 10;`
        - `SELECT DATE(created_at), COUNT(*) FROM chat_feedback GROUP BY DATE(created_at) ORDER BY DATE(created_at);`
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Custom query input
        query = st.text_area(
            "Enter your SQL query:",
            height=150,
            placeholder="SELECT * FROM chat_feedback WHERE rating = 5 LIMIT 10;"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 Execute Query", type="primary"):
                if query.strip():
                    with st.spinner("Executing query..."):
                        try:
                            result_df = query_df(query)
                            if not result_df.empty:
                                st.success(f"✅ Query executed successfully! {len(result_df)} rows returned.")
                                st.dataframe(result_df, use_container_width=True)
                                
                                # Download results
                                csv = result_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Results",
                                    data=csv,
                                    file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.info("Query executed successfully but returned no results.")
                        except Exception as e:
                            st.error(f"❌ Query execution failed: {e}")
                else:
                    st.warning("Please enter a SQL query.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>📊 Miva AI Database Analytics Dashboard | Built with Streamlit</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
