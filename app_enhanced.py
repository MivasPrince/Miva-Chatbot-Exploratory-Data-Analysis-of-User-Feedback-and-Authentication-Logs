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
import os
from typing import Dict, Optional, Tuple, List

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
    
    .stAlert > div {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseConfig:
    """Database configuration management"""
    
    @staticmethod
    def get_config() -> Dict[str, str]:
        """Get database configuration from environment or Streamlit secrets"""
        try:
            # Try Streamlit secrets first (for Streamlit Cloud)
            if hasattr(st, 'secrets') and 'database' in st.secrets:
                return {
                    "host": st.secrets["database"]["host"],
                    "port": st.secrets["database"]["port"],
                    "user": st.secrets["database"]["user"],
                    "password": st.secrets["database"]["password"],
                    "database": st.secrets["database"]["database"]
                }
        except:
            pass
        
        # Fall back to environment variables
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
        """Test database connection"""
        try:
            conn = psycopg2.connect(**_self.config)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            conn.close()
            return True, version[0] if version else "Unknown"
        except Exception as e:
            return False, str(e)
    
    @st.cache_data(ttl=300)
    def run_query(_self, query: str) -> List:
        """Execute a query and return results"""
        try:
            conn = psycopg2.connect(**_self.config)
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
    def query_df(_self, query: str) -> pd.DataFrame:
        """Run a SQL query and return result as Pandas DataFrame"""
        try:
            conn = psycopg2.connect(**_self.config)
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"DataFrame query error: {e}")
            return pd.DataFrame()

class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def try_parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
        """Auto-parse likely datetime columns"""
        for col in df.columns:
            if df[col].dtype == "object" and any(k in col.lower() for k in ["time","date","at","created","updated"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="ignore", utc=True)
                except Exception:
                    pass
        return df
    
    @staticmethod
    def get_table_info(db_manager: DatabaseManager) -> pd.DataFrame:
        """Get table information with row counts"""
        try:
            query = """
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_rows,
                n_dead_tup as dead_rows
            FROM pg_stat_user_tables 
            ORDER BY n_live_tup DESC;
            """
            return db_manager.query_df(query)
        except:
            # Fallback query
            tables = db_manager.run_query("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            return pd.DataFrame(tables, columns=['table_name'])

class Visualizer:
    """Visualization utilities using Plotly"""
    
    @staticmethod
    def plot_missing_values(df: pd.DataFrame, title: str):
        """Create interactive missing values plot"""
        na_counts = df.isna().sum()
        na_counts = na_counts[na_counts > 0].sort_values(ascending=False)
        
        if na_counts.empty:
            st.success(f"✅ No missing values in {title}")
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
    
    @staticmethod
    def plot_rating_distribution(df: pd.DataFrame, col: str, title: str):
        """Create interactive rating histogram"""
        data = df[col].dropna()
        if data.empty:
            st.warning(f"No data in {col}")
            return
        
        # Create histogram with statistics
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=[f"{col} Distribution", "Rating Statistics"],
            specs=[[{"type": "xy"}, {"type": "indicator"}]]
        )
        
        # Histogram
        fig.add_trace(
            go.Histogram(x=data, nbinsx=5, name="Ratings"),
            row=1, col=1
        )
        
        # Statistics
        avg_rating = data.mean()
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=avg_rating,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Average Rating"},
                gauge={
                    'axis': {'range': [None, 5]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 2], 'color': "lightgray"},
                        {'range': [2, 4], 'color': "gray"},
                        {'range': [4, 5], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 4.5
                    }
                }
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f"{title}: {col} Analysis",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_top_categories(df: pd.DataFrame, col: str, title: str, top_n: int = 20):
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
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=max(400, 30*len(vc)))
        fig.update_yaxis(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_time_trends(df: pd.DataFrame, title: str, freq: str = "D"):
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
            
            # Create line plot with moving average
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=counts.index,
                y=counts.values,
                mode='lines+markers',
                name='Daily Count',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4)
            ))
            
            # Add 7-day moving average if enough data
            if len(counts) >= 7:
                ma_7 = counts.rolling(window=7, center=True).mean()
                fig.add_trace(go.Scatter(
                    x=ma_7.index,
                    y=ma_7.values,
                    mode='lines',
                    name='7-day Moving Average',
                    line=dict(color='red', width=2, dash='dash')
                ))
            
            fig.update_layout(
                title=f"{title}: Trends by {col} ({freq})",
                xaxis_title="Time",
                yaxis_title="Count",
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)

def create_dashboard():
    """Main dashboard application"""
    # Initialize components
    db_manager = DatabaseManager()
    processor = DataProcessor()
    viz = Visualizer()
    
    # Header
    st.markdown('<h1 class="main-header">📊 Miva AI Database Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Dashboard Controls")
        
        # Connection test
        st.markdown("#### Database Connection")
        if st.button("🔄 Test Connection", type="primary"):
            with st.spinner("Testing connection..."):
                success, info = db_manager.test_connection()
                if success:
                    st.success("✅ Connected successfully!")
                    with st.expander("Connection Details"):
                        st.code(f"Host: {db_manager.config['host']}\nPort: {db_manager.config['port']}\nDatabase: {db_manager.config['database']}")
                        st.info(f"PostgreSQL: {info[:100]}...")
                else:
                    st.error(f"❌ Connection failed")
                    st.error(f"Error: {info}")
        
        # Data management
        st.markdown("#### Data Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh"):
                st.cache_data.clear()
                st.success("Cache cleared!")
                st.experimental_rerun()
        
        with col2:
            auto_refresh = st.checkbox("Auto-refresh", help="Refresh data every 5 minutes")
        
        # Analysis options
        st.markdown("#### Analysis Options")
        show_missing = st.checkbox("Missing Values", True)
        show_distributions = st.checkbox("Distributions", True)
        show_trends = st.checkbox("Time Trends", True)
        show_advanced = st.checkbox("Advanced Analytics", False)
        
        # Filters
        st.markdown("#### Filters")
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            help="Filter data by date range"
        )
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.experimental_rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", 
        "💬 Chat Feedback", 
        "🔐 OTPs", 
        "📊 Custom Analysis",
        "🔍 Advanced Analytics"
    ])
    
    with tab1:
        st.markdown("### Database Overview")
        
        # Get table information
        with st.spinner("Loading database information..."):
            try:
                table_info = processor.get_table_info(db_manager)
                
                if not table_info.empty:
                    # Metrics row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    total_tables = len(table_info)
                    total_rows = table_info.get('live_rows', [0]).sum() if 'live_rows' in table_info.columns else 0
                    
                    with col1:
                        st.metric("📊 Total Tables", total_tables)
                    with col2:
                        st.metric("📈 Total Records", f"{total_rows:,}")
                    with col3:
                        last_update = datetime.now().strftime("%H:%M:%S")
                        st.metric("🕒 Last Updated", last_update)
                    with col4:
                        health_score = "🟢 Healthy" if total_rows > 0 else "🟡 Warning"
                        st.metric("💚 Status", health_score)
                    
                    # Table details
                    st.markdown("### 📋 Table Statistics")
                    
                    if 'live_rows' in table_info.columns:
                        fig = px.bar(
                            table_info,
                            x='tablename',
                            y='live_rows',
                            title="Records per Table",
                            labels={'live_rows': 'Live Records', 'tablename': 'Table Name'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display table info
                    st.dataframe(table_info, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error loading overview: {e}")
    
    with tab2:
        st.markdown("### 💬 Chat Feedback Analysis")
        
        with st.spinner("Loading chat feedback data..."):
            df_chat = db_manager.query_df("SELECT * FROM chat_feedback;")
            
            if not df_chat.empty:
                df_chat = processor.try_parse_datetimes(df_chat)
                
                # Apply date filter
                if len(date_range) == 2 and 'created_at' in df_chat.columns:
                    mask = (df_chat['created_at'].dt.date >= date_range[0]) & (df_chat['created_at'].dt.date <= date_range[1])
                    df_chat = df_chat.loc[mask]
                
                # Metrics dashboard
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
                    with st.expander("🔍 Missing Values Analysis", expanded=True):
                        viz.plot_missing_values(df_chat, "Chat Feedback")
                
                if show_distributions:
                    with st.expander("📊 Data Distributions", expanded=True):
                        if 'rating' in df_chat.columns:
                            viz.plot_rating_distribution(df_chat, 'rating', 'Chat Feedback')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'user_agent' in df_chat.columns:
                                viz.plot_top_categories(df_chat, 'user_agent', 'Chat Feedback', 10)
                        with col2:
                            if 'ip_address' in df_chat.columns:
                                viz.plot_top_categories(df_chat, 'ip_address', 'Chat Feedback', 10)
                
                if show_trends:
                    with st.expander("📈 Time Trends Analysis", expanded=True):
                        viz.plot_time_trends(df_chat, "Chat Feedback")
                
                if show_advanced:
                    with st.expander("🔬 Advanced Analytics", expanded=False):
                        # Rating correlation analysis
                        if 'rating' in df_chat.columns:
                            st.markdown("#### Rating Analysis")
                            
                            # Rating distribution by time of day
                            if 'created_at' in df_chat.columns:
                                df_chat['hour'] = df_chat['created_at'].dt.hour
                                hourly_ratings = df_chat.groupby('hour')['rating'].agg(['mean', 'count']).reset_index()
                                
                                fig = make_subplots(
                                    rows=1, cols=2,
                                    subplot_titles=['Average Rating by Hour', 'Feedback Count by Hour']
                                )
                                
                                fig.add_trace(
                                    go.Bar(x=hourly_ratings['hour'], y=hourly_ratings['mean'], name='Avg Rating'),
                                    row=1, col=1
                                )
                                
                                fig.add_trace(
                                    go.Scatter(x=hourly_ratings['hour'], y=hourly_ratings['count'], 
                                             mode='lines+markers', name='Count'),
                                    row=1, col=2
                                )
                                
                                fig.update_layout(title="Rating Patterns by Hour of Day")
                                st.plotly_chart(fig, use_container_width=True)
                
                # Data export and preview
                with st.expander("📋 Data Preview & Export", expanded=False):
                    st.dataframe(df_chat.head(100), use_container_width=True)
                    
                    # Export options
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        csv = df_chat.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"chat_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_data = df_chat.to_json(orient='records', date_format='iso')
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"chat_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col3:
                        # Quick stats
                        st.metric("Rows in Export", len(df_chat))
            else:
                st.warning("No chat feedback data found.")
    
    with tab3:
        st.markdown("### 🔐 OTP Analysis")
        
        with st.spinner("Loading OTP data..."):
            df_otps = db_manager.query_df("SELECT * FROM otps;")
            
            if not df_otps.empty:
                df_otps = processor.try_parse_datetimes(df_otps)
                
                # Apply date filter
                if len(date_range) == 2 and 'created_at' in df_otps.columns:
                    mask = (df_otps['created_at'].dt.date >= date_range[0]) & (df_otps['created_at'].dt.date <= date_range[1])
                    df_otps = df_otps.loc[mask]
                
                # Metrics dashboard
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Total OTPs", f"{len(df_otps):,}")
                with col2:
                    if 'otp_code' in df_otps.columns:
                        avg_length = df_otps['otp_code'].astype(str).str.len().mean()
                        st.metric("📏 Avg Length", f"{avg_length:.1f}")
                with col3:
                    if 'used' in df_otps.columns:
                        used_rate = df_otps['used'].mean() * 100
                        st.metric("✅ Usage Rate", f"{used_rate:.1f}%")
                with col4:
                    unique_emails = df_otps['email'].nunique() if 'email' in df_otps.columns else 0
                    st.metric("👥 Unique Users", f"{unique_emails:,}")
                
                # Analysis sections
                if show_missing:
                    with st.expander("🔍 Missing Values Analysis", expanded=True):
                        viz.plot_missing_values(df_otps, "OTPs")
                
                if show_distributions:
                    with st.expander("📊 Data Distributions", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # OTP length distribution
                            if 'otp_code' in df_otps.columns:
                                lengths = df_otps['otp_code'].dropna().astype(str).str.len()
                                if not lengths.empty:
                                    fig = px.histogram(
                                        x=lengths,
                                        title="OTP Code Length Distribution",
                                        labels={'x': 'Length', 'y': 'Frequency'},
                                        nbins=10
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Usage status distribution
                            if 'used' in df_otps.columns:
                                status_counts = df_otps['used'].value_counts()
                                fig = px.pie(
                                    values=status_counts.values,
                                    names=['Used' if x else 'Unused' for x in status_counts.index],
                                    title="OTP Usage Status",
                                    color_discrete_sequence=['#ff7f0e', '#1f77b4']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Email domain analysis
                        if 'email' in df_otps.columns:
                            df_otps['email_domain'] = df_otps['email'].str.split('@').str[1]
                            viz.plot_top_categories(df_otps, 'email_domain', 'OTPs', 15)
                
                if show_trends:
                    with st.expander("📈 Time Trends Analysis", expanded=True):
                        viz.plot_time_trends(df_otps, "OTPs")
                
                if show_advanced:
                    with st.expander("🔬 Advanced Analytics", expanded=False):
                        # Usage patterns
                        if 'used' in df_otps.columns and 'created_at' in df_otps.columns:
                            st.markdown("#### Usage Patterns")
                            
                            # Usage rate over time
                            df_otps['date'] = df_otps['created_at'].dt.date
                            daily_usage = df_otps.groupby('date').agg({
                                'used': ['sum', 'count', 'mean']
                            }).reset_index()
                            daily_usage.columns = ['date', 'used_count', 'total_count', 'usage_rate']
                            
                            fig = make_subplots(
                                rows=2, cols=1,
                                subplot_titles=['Daily OTP Generation vs Usage', 'Daily Usage Rate'],
                                shared_xaxes=True
                            )
                            
                            fig.add_trace(
                                go.Bar(x=daily_usage['date'], y=daily_usage['total_count'], 
                                      name='Generated', marker_color='lightblue'),
                                row=1, col=1
                            )
                            
                            fig.add_trace(
                                go.Bar(x=daily_usage['date'], y=daily_usage['used_count'], 
                                      name='Used', marker_color='darkblue'),
                                row=1, col=1
                            )
                            
                            fig.add_trace(
                                go.Scatter(x=daily_usage['date'], y=daily_usage['usage_rate'] * 100, 
                                          mode='lines+markers', name='Usage Rate (%)',
                                          line=dict(color='red', width=2)),
                                row=2, col=1
                            )
                            
                            fig.update_layout(
                                title="OTP Usage Analysis Over Time",
                                height=600,
                                showlegend=True
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                # Data export and preview
                with st.expander("📋 Data Preview & Export", expanded=False):
                    st.dataframe(df_otps.head(100), use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        csv = df_otps.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"otps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_data = df_otps.to_json(orient='records', date_format='iso')
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"otps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col3:
                        st.metric("Rows in Export", len(df_otps))
            else:
                st.warning("No OTP data found.")
    
    with tab4:
        st.markdown("### 📊 Custom SQL Analysis")
        
        # Query templates
        st.markdown("#### 📝 Query Templates")
        template_options = {
            "Select All Chat Feedback": "SELECT * FROM chat_feedback LIMIT 100;",
            "Top Rated Feedback": "SELECT * FROM chat_feedback WHERE rating = 5 ORDER BY created_at DESC LIMIT 20;",
            "OTP Usage by Email Domain": """
                SELECT 
                    SPLIT_PART(email, '@', 2) as domain,
                    COUNT(*) as total_otps,
                    SUM(CASE WHEN used = true THEN 1 ELSE 0 END) as used_otps,
                    ROUND(AVG(CASE WHEN used = true THEN 1.0 ELSE 0.0 END) * 100, 2) as usage_rate
                FROM otps 
                GROUP BY domain 
                ORDER BY total_otps DESC
                LIMIT 10;
            """,
            "Daily Feedback Trends": """
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as feedback_count,
                    AVG(rating) as avg_rating
                FROM chat_feedback 
                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(created_at) 
                ORDER BY date DESC;
            """,
            "User Engagement Analysis": """
                SELECT 
                    cf.email,
                    COUNT(cf.id) as feedback_count,
                    AVG(cf.rating) as avg_rating,
                    COUNT(o.id) as otp_count,
                    MAX(cf.created_at) as last_feedback
                FROM chat_feedback cf
                LEFT JOIN otps o ON cf.email = o.email
                GROUP BY cf.email
                HAVING COUNT(cf.id) > 1
                ORDER BY feedback_count DESC
                LIMIT 20;
            """
        }
        
        selected_template = st.selectbox(
            "Choose a template:",
            options=list(template_options.keys()),
            index=0
        )
        
        # Query input
        query = st.text_area(
            "SQL Query:",
            value=template_options[selected_template],
            height=200,
            help="Write your SQL query here. Be careful with large result sets!"
        )
        
        # Query execution
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Execute Query", type="primary"):
                if query.strip():
                    with st.spinner("Executing query..."):
                        try:
                            start_time = time.time()
                            result_df = db_manager.query_df(query)
                            execution_time = time.time() - start_time
                            
                            if not result_df.empty:
                                st.success(f"✅ Query executed successfully! {len(result_df)} rows returned in {execution_time:.2f}s")
                                
                                # Display results with pagination
                                if len(result_df) > 1000:
                                    st.warning("⚠️ Large result set detected. Showing first 1000 rows.")
                                    display_df = result_df.head(1000)
                                else:
                                    display_df = result_df
                                
                                st.dataframe(display_df, use_container_width=True)
                                
                                # Quick statistics
                                if len(result_df.select_dtypes(include=[np.number]).columns) > 0:
                                    st.markdown("#### 📊 Quick Statistics")
                                    st.dataframe(result_df.describe(), use_container_width=True)
                                
                                # Download results
                                col1, col2 = st.columns(2)
                                with col1:
                                    csv = result_df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Results (CSV)",
                                        data=csv,
                                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                        mime="text/csv"
                                    )
                                
                                with col2:
                                    json_data = result_df.to_json(orient='records', date_format='iso')
                                    st.download_button(
                                        label="📥 Download Results (JSON)",
                                        data=json_data,
                                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                        mime="application/json"
                                    )
                            else:
                                st.info("Query executed successfully but returned no results.")
                                
                        except Exception as e:
                            st.error(f"❌ Query execution failed: {e}")
                else:
                    st.warning("Please enter a SQL query.")
        
        with col2:
            if st.button("🔄 Clear Query"):
                st.experimental_rerun()
        
        with col3:
            if st.button("💾 Save Query"):
                st.info("Query saving feature coming soon!")
    
    with tab5:
        if show_advanced:
            st.markdown("### 🔍 Advanced Analytics")
            
            # Cross-table analysis
            st.markdown("#### 🔗 Cross-Table Analysis")
            
            with st.spinner("Loading cross-table analysis..."):
                try:
                    # User engagement correlation
                    correlation_query = """
                    SELECT 
                        COALESCE(cf.email, o.email) as email,
                        COUNT(DISTINCT cf.id) as feedback_count,
                        AVG(cf.rating) as avg_rating,
                        COUNT(DISTINCT o.id) as otp_count,
                        AVG(CASE WHEN o.used = true THEN 1.0 ELSE 0.0 END) as otp_usage_rate
                    FROM chat_feedback cf
                    FULL OUTER JOIN otps o ON cf.email = o.email
                    WHERE COALESCE(cf.email, o.email) IS NOT NULL
                    GROUP BY COALESCE(cf.email, o.email)
                    HAVING COUNT(DISTINCT cf.id) > 0 OR COUNT(DISTINCT o.id) > 0;
                    """
                    
                    correlation_df = db_manager.query_df(correlation_query)
                    
                    if not correlation_df.empty:
                        # Scatter plot: feedback vs OTP usage
                        fig = px.scatter(
                            correlation_df,
                            x='feedback_count',
                            y='otp_count',
                            color='avg_rating',
                            size='otp_usage_rate',
                            hover_data=['email'],
                            title="User Engagement: Feedback vs OTP Usage",
                            labels={
                                'feedback_count': 'Number of Feedback',
                                'otp_count': 'Number of OTPs',
                                'avg_rating': 'Average Rating'
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Correlation matrix
                        numeric_cols = ['feedback_count', 'avg_rating', 'otp_count', 'otp_usage_rate']
                        corr_matrix = correlation_df[numeric_cols].corr()
                        
                        fig_corr = px.imshow(
                            corr_matrix,
                            title="Correlation Matrix: User Engagement Metrics",
                            aspect="auto",
                            color_continuous_scale="RdBu"
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)
                        
                        # Top users
                        st.markdown("#### 🏆 Top Engaged Users")
                        top_users = correlation_df.nlargest(10, 'feedback_count')
                        st.dataframe(top_users, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error in cross-table analysis: {e}")
        else:
            st.info("Enable 'Advanced Analytics' in the sidebar to see this section.")
    
    # Footer with system info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**🕒 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        st.markdown(f"**🗄️ Database:** {db_manager.config['host']}")
    
    with col3:
        if st.button("ℹ️ System Info"):
            st.info(f"""
            **System Information:**
            - Python: {pd.__version__}
            - Pandas: {pd.__version__}
            - Streamlit: {st.__version__}
            - Database: PostgreSQL
            """)

# Application entry point
def main():
    """Main application entry point"""
    try:
        create_dashboard()
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.info("Please check your database connection and try refreshing the page.")

if __name__ == "__main__":
    main()
