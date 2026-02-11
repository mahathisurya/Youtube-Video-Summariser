#!/bin/bash

# YouTube Video Summarizer - Quick Deployment Script

set -e

echo "================================================"
echo "YouTube Video Summarizer - Deployment Helper"
echo "================================================"
echo ""

# Function to display menu
show_menu() {
    echo "Select deployment option:"
    echo ""
    echo "1) 🏠 Local Development (Run on localhost)"
    echo "2) 🐳 Docker (Build and run with Docker)"
    echo "3) ☁️  Prepare for Cloud (Railway/Render/Heroku)"
    echo "4) 🚀 Production Setup (Gunicorn)"
    echo "5) ❌ Exit"
    echo ""
}

# Local development
deploy_local() {
    echo "Starting local development server..."
    echo ""
    
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo ""
    echo "✅ Starting server on http://localhost:5000"
    echo "Press Ctrl+C to stop"
    echo ""
    
    python app.py
}

# Docker deployment
deploy_docker() {
    echo "Deploying with Docker..."
    echo ""
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    echo "Building Docker image..."
    docker build -t youtube-summarizer .
    
    echo "Starting container..."
    docker run -d -p 5000:5000 --name youtube-summarizer youtube-summarizer
    
    echo ""
    echo "✅ Deployed! Access at http://localhost:5000"
    echo ""
    echo "Useful commands:"
    echo "  View logs: docker logs -f youtube-summarizer"
    echo "  Stop: docker stop youtube-summarizer"
    echo "  Remove: docker rm youtube-summarizer"
}

# Prepare for cloud
prepare_cloud() {
    echo "Preparing for cloud deployment..."
    echo ""
    
    # Check if git repo exists
    if [ ! -d ".git" ]; then
        echo "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit for deployment"
        echo ""
        echo "✅ Git repository initialized"
    else
        echo "Git repository already exists"
    fi
    
    # Add production files
    echo "Adding production configuration..."
    
    # Procfile for Heroku
    echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT --timeout 300 app:app" > Procfile
    
    # runtime.txt
    echo "python-3.11.0" > runtime.txt
    
    # Add gunicorn to requirements if not present
    if ! grep -q "gunicorn" requirements.txt; then
        echo "gunicorn==21.2.0" >> requirements.txt
    fi
    
    echo ""
    echo "✅ Files prepared for cloud deployment!"
    echo ""
    echo "Next steps:"
    echo ""
    echo "📌 For Railway (Recommended):"
    echo "   1. Push to GitHub:"
    echo "      git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "      git push -u origin main"
    echo "   2. Go to railway.app"
    echo "   3. Deploy from GitHub repo"
    echo ""
    echo "📌 For Render:"
    echo "   1. Push to GitHub (same as above)"
    echo "   2. Go to render.com"
    echo "   3. New Web Service → Connect GitHub"
    echo ""
    echo "📌 For Heroku:"
    echo "   heroku create your-app-name"
    echo "   git push heroku main"
}

# Production setup with Gunicorn
deploy_production() {
    echo "Setting up production server with Gunicorn..."
    echo ""
    
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install gunicorn
    
    echo ""
    echo "✅ Starting production server..."
    echo ""
    
    gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 --access-logfile - --error-logfile - app:app
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter your choice [1-5]: " choice
    echo ""
    
    case $choice in
        1)
            deploy_local
            break
            ;;
        2)
            deploy_docker
            break
            ;;
        3)
            prepare_cloud
            break
            ;;
        4)
            deploy_production
            break
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please choose 1-5."
            echo ""
            ;;
    esac
done
