#!/usr/bin/env python3
"""
CodeRoot Bot - Run Script
Simple script to start the bot with error handling and logging
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Check if environment is properly configured"""
    required_env_vars = [
        'BOT_TOKEN',
        'API_ID', 
        'API_HASH',
        'ADMIN_USER_ID'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📝 Please check your .env file and ensure all required variables are set.")
        return False
    
    return True

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / 'bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import pyrogram
        import motor
        import pymongo
        import jdatetime
        import qrcode
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please run: pip install -r requirements.txt")
        return False

async def main():
    """Main function to run the bot"""
    print("🤖 Starting CodeRoot Bot...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    try:
        # Import and start bot
        from bot import main as bot_main
        await bot_main()
        
    except KeyboardInterrupt:
        print("\n⏹ Bot stopped by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        logging.exception("Fatal error occurred")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"💥 Failed to start bot: {e}")
        sys.exit(1)