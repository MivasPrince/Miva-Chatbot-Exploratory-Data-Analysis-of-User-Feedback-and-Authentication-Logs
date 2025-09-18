<p align="center">
    <img src="https://i.imgur.com/azwWWQN.jpeg" alt="Miva Logo" width="120"/>
    <h1>Miva AI Database Analytics Dashboard</h1>
</p>



A comprehensive Streamlit dashboard for analyzing Miva AI database content with interactive visualizations and real-time data exploration.

## 🚀 Features

### 📋 Database Overview
- Real-time connection testing
- Table statistics and row counts
- Database schema information

### 💬 Chat Feedback Analysis
- Rating distributions and trends
- User agent and IP address analysis
- Time-based trend analysis
- Missing data visualization
- Text length analysis

### 🔐 OTP Analysis
- OTP usage statistics
- Code length distributions
- Status and usage patterns
- User engagement metrics

### 📊 Custom Analysis
- Custom SQL query execution
- Interactive data exploration
- Export functionality
- Real-time results

## 🛠️ Technologies Used

- **Streamlit** - Interactive web app framework
- **PostgreSQL** - Database backend
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **psycopg2** - PostgreSQL adapter

## 📦 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/miva-ai-dashboard.git
   cd miva-ai-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database connection**
   
   Update the database configuration in `app.py`:
   ```python
   db_config = {
       "host": "your_host",
       "port": 5432,
       "user": "your_username", 
       "password": "your_password",
       "database": "your_database"
   }
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### 🌐 Deployment Options

#### Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Add secrets in the Streamlit Cloud dashboard:
     ```toml
     [database]
     host = "your_host"
     port = 5432
     user = "your_username"
     password = "your_password" 
     database = "your_database"
     ```

#### Heroku Deployment

1. **Create Procfile**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

#### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   docker build -t miva-dashboard .
   docker run -p 8501:8501 miva-dashboard
   ```

## 🔧 Configuration

### Environment Variables

For production deployment, use environment variables:

```python
import os

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "miva_ai_db")
}
```

### Streamlit Secrets

For Streamlit Cloud, add to `.streamlit/secrets.toml`:

```toml
[database]
host = "your_host"
port = 5432
user = "your_username"
password = "your_password"
database = "your_database"
```

Then update the app to use secrets:

```python
import streamlit as st

db_config = {
    "host": st.secrets["database"]["host"],
    "port": st.secrets["database"]["port"], 
    "user": st.secrets["database"]["user"],
    "password": st.secrets["database"]["password"],
    "database": st.secrets["database"]["database"]
}
```

## 📊 Usage

### Dashboard Navigation

1. **Overview Tab**: Database connection status and table statistics
2. **Chat Feedback Tab**: Detailed analysis of chat feedback data
3. **OTPs Tab**: OTP usage patterns and statistics  
4. **Custom Analysis Tab**: Execute custom SQL queries

### Key Features

- **Interactive Charts**: Hover, zoom, and filter data
- **Real-time Updates**: Refresh data with the sidebar button
- **Data Export**: Download results as CSV files
- **Responsive Design**: Works on desktop and mobile

### Sample Queries

```sql
-- Top rated feedback
SELECT * FROM chat_feedback WHERE rating = 5 ORDER BY created_at DESC;

-- OTP usage by email domain
SELECT SPLIT_PART(email, '@', 2) as domain, COUNT(*) 
FROM otps 
GROUP BY domain 
ORDER BY count DESC;

-- Daily feedback trends
SELECT DATE(created_at) as date, COUNT(*) as feedback_count
FROM chat_feedback 
GROUP BY DATE(created_at) 
ORDER BY date;
```

## 🔒 Security

- Database credentials should be stored securely
- Use environment variables or secrets management
- Enable SSL for database connections in production
- Implement proper access controls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Connection Error**: 
- Verify database credentials
- Check network connectivity
- Ensure PostgreSQL is running

**Module Not Found**:
- Run `pip install -r requirements.txt`
- Check Python version compatibility

**Performance Issues**:
- Enable caching with `@st.cache_data`
- Limit query result sizes
- Use database indexes

### Debug Mode

Run with debug logging:
```bash
streamlit run app.py --logger.level=debug
```

## 📞 Support

- 📧 Email: support@miva.ai
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/miva-ai-dashboard/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/miva-ai-dashboard/wiki)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- PostgreSQL community
- Plotly for interactive visualizations
- All contributors and users

---

**⭐ If you find this project helpful, please give it a star!**
