#!/bin/bash

# Miva AI Dashboard Deployment Script
# This script helps deploy the Streamlit app to various platforms

set -e

echo "🚀 Miva AI Dashboard Deployment Script"
echo "======================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_header "Checking requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check pip
    if ! command -v pip &> /dev/null; then
        print_error "pip is required but not installed."
        exit 1
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        print_error "git is required but not installed."
        exit 1
    fi
    
    print_status "All requirements satisfied ✅"
}

# Install dependencies
install_dependencies() {
    print_header "Installing dependencies..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    print_status "Dependencies installed ✅"
}

# Test the application locally
test_local() {
    print_header "Testing application locally..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Test import
    python3 -c "import app; print('✅ App structure is valid')" || {
        print_error "App structure test failed"
        exit 1
    }
    
    print_status "Local tests passed ✅"
}

# Deploy to Streamlit Cloud
deploy_streamlit_cloud() {
    print_header "Preparing for Streamlit Cloud deployment..."
    
    # Check if git repository is clean
    if [[ -n $(git status -s) ]]; then
        print_warning "You have uncommitted changes. Commit them before deployment."
        
        read -p "Do you want to commit changes now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            read -p "Enter commit message: " commit_msg
            git commit -m "$commit_msg"
        fi
    fi
    
    # Push to GitHub
    print_status "Pushing to GitHub..."
    git push origin main || {
        print_error "Failed to push to GitHub"
        exit 1
    }
    
    print_status "Code pushed to GitHub ✅"
    print_status "Now visit https://share.streamlit.io to deploy your app!"
    print_status "Repository URL: $(git remote get-url origin)"
}

# Deploy using Docker
deploy_docker() {
    print_header "Building Docker image..."
    
    # Build Docker image
    docker build -t miva-dashboard:latest . || {
        print_error "Docker build failed"
        exit 1
    }
    
    print_status "Docker image built successfully ✅"
    
    # Test Docker container
    print_status "Testing Docker container..."
    docker run -d --name miva-test -p 8501:8501 miva-dashboard:latest
    
    # Wait for container to start
    sleep 10
    
    # Health check
    if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        print_status "Docker container is healthy ✅"
        docker stop miva-test
        docker rm miva-test
    else
        print_error "Docker container health check failed"
        docker stop miva-test
        docker rm miva-test
        exit 1
    fi
    
    print_status "Docker deployment ready ✅"
    print_status "Run: docker run -p 8501:8501 miva-dashboard:latest"
}

# Deploy to Heroku
deploy_heroku() {
    print_header "Preparing Heroku deployment..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI is required but not installed."
        print_status "Install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Create Procfile if it doesn't exist
    if [ ! -f "Procfile" ]; then
        echo "web: sh setup.sh && streamlit run app.py" > Procfile
        print_status "Created Procfile"
    fi
    
    # Create setup.sh if it doesn't exist
    if [ ! -f "setup.sh" ]; then
        cat > setup.sh << EOF
mkdir -p ~/.streamlit/

echo "\\
[general]\\n\\
email = \\"your-email@domain.com\\"\\n\\
" > ~/.streamlit/credentials.toml

echo "\\
[server]\\n\\
headless = true\\n\\
enableCORS=false\\n\\
port = \$PORT\\n\\
" > ~/.streamlit/config.toml
EOF
        chmod +x setup.sh
        print_status "Created setup.sh"
    fi
    
    # Create or login to Heroku app
    read -p "Enter Heroku app name (or leave empty for random): " app_name
    
    if [ -z "$app_name" ]; then
        heroku create
    else
        heroku create $app_name
    fi
    
    # Set environment variables
    print_status "Setting environment variables..."
    heroku config:set DB_HOST=$DB_HOST
    heroku config:set DB_PORT=$DB_PORT
    heroku config:set DB_USER=$DB_USER
    heroku config:set DB_PASSWORD=$DB_PASSWORD
    heroku config:set DB_NAME=$DB_NAME
    
    # Deploy
    git add .
    git commit -m "Deploy to Heroku" --allow-empty
    git push heroku main
    
    print_status "Heroku deployment initiated ✅"
}

# Create secrets template for Streamlit Cloud
create_secrets_template() {
    print_header "Creating secrets template..."
    
    mkdir -p .streamlit
    
    cat > .streamlit/secrets.toml.template << EOF
# Streamlit Cloud Secrets Template
# Copy this to secrets.toml and fill in your values
# DO NOT commit secrets.toml to git!

[database]
host = "your-database-host"
port = 5432
user = "your-username"
password = "your-password"
database = "your-database-name"

# Optional: Email configuration
[email]
smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_user = "your-email@gmail.com"
smtp_password = "your-app-password"
admin_email = "admin@yourcompany.com"
EOF
    
    print_status "Secrets template created at .streamlit/secrets.toml.template ✅"
    print_warning "Remember to create .streamlit/secrets.toml with your actual values!"
}

# Main menu
show_menu() {
    echo
    print_header "Select deployment option:"
    echo "1. Install dependencies and test locally"
    echo "2. Deploy to Streamlit Cloud"
    echo "3. Deploy with Docker"
    echo "4. Deploy to Heroku"
    echo "5. Create secrets template"
    echo "6. Run all checks"
    echo "7. Exit"
    echo
}

# Main execution
main() {
    # Check requirements first
    check_requirements
    
    while true; do
        show_menu
        read -p "Choose an option (1-7): " -n 1 -r
        echo
        
        case $REPLY in
            1)
                install_dependencies
                test_local
                print_status "Ready for local development! Run: streamlit run app.py"
                ;;
            2)
                deploy_streamlit_cloud
                ;;
            3)
                deploy_docker
                ;;
            4)
                deploy_heroku
                ;;
            5)
                create_secrets_template
                ;;
            6)
                install_dependencies
                test_local
                print_status "All checks passed ✅"
                ;;
            7)
                print_status "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-7."
                ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Run main function
main
