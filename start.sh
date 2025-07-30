#!/bin/bash

# Start script for CodeRoot Bot on Render
echo "🤖 Starting CodeRoot Bot..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Set environment
export PYTHONPATH="${PYTHONPATH}:."
export PYTHONUNBUFFERED=1

# Start the bot
echo "🚀 Launching bot..."
python3 bot.py