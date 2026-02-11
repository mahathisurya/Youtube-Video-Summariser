#!/bin/bash

# YouTube Video Summarizer - Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "================================================"
echo "YouTube Video Summarizer - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
echo "🔨 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
echo "⏳ This may take a few minutes (downloading BERT model ~400MB)..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your AssemblyAI API key!"
    echo "   Get a free API key at: https://www.assemblyai.com/"
else
    echo "✓ .env file already exists"
fi
echo ""

# Create necessary directories
echo "📁 Creating temporary directories..."
mkdir -p temp_videos temp_audio
echo "✓ Directories created"
echo ""

echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ASSEMBLYAI_API_KEY"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo "4. Test: python test_api.py"
echo ""
echo "API will be available at http://localhost:5000"
echo ""
