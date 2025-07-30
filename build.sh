#!/bin/bash

# Build script for Render deployment
echo "🚀 Starting CodeRoot Bot build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Set executable permissions
echo "🔧 Setting permissions..."
chmod +x main.py
chmod +x bot.py

# Verify installation
echo "✅ Verifying installation..."
python3 -c "import pyrogram, motor, redis; print('All core dependencies installed successfully')"

echo "🎉 Build completed successfully!"