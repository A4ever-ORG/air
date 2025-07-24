#!/usr/bin/env python3
"""
Diagnostic script for CodeRoot Demo Bot
تشخیص مشکلات ربات دمو
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check environment variables"""
    print("🔍 بررسی متغیرهای محیطی...")
    
    required_vars = {
        'BOT_TOKEN': '7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM',
        'ADMIN_USER_ID': '7707164235'
    }
    
    for var, default in required_vars.items():
        value = os.getenv(var, default)
        if value:
            print(f"✅ {var}: {value[:15]}...")
        else:
            print(f"❌ {var}: تنظیم نشده")
    
    print(f"🎭 DEMO_MODE: {os.getenv('DEMO_MODE', 'true')}")

def test_imports():
    """Test required imports"""
    print("\n📦 بررسی وابستگی‌ها...")
    
    imports = {
        'asyncio': 'Built-in',
        'logging': 'Built-in', 
        'os': 'Built-in',
        'sys': 'Built-in',
        'datetime': 'Built-in'
    }
    
    optional_imports = {
        'pyrogram': 'Telegram bot framework',
        'python-dotenv': 'Environment variables'
    }
    
    # Test required imports
    for module, desc in imports.items():
        try:
            __import__(module)
            print(f"✅ {module}: {desc}")
        except ImportError:
            print(f"❌ {module}: ناموجود - {desc}")
    
    # Test optional imports
    for module, desc in optional_imports.items():
        try:
            __import__(module.replace('-', '_'))
            print(f"✅ {module}: {desc}")
        except ImportError:
            print(f"⚠️ {module}: ناموجود - {desc} (اختیاری)")

async def test_bot_token():
    """Test bot token validity"""
    print("\n🤖 تست توکن ربات...")
    
    bot_token = os.getenv('BOT_TOKEN', '7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM')
    
    if not bot_token:
        print("❌ توکن ربات موجود نیست")
        return False
    
    if ':' not in bot_token:
        print("❌ فرمت توکن نامعتبر")
        return False
    
    print(f"✅ توکن فرمت صحیح: {bot_token[:15]}...")
    
    # Try to test with Pyrogram if available
    try:
        from pyrogram import Client
        print("✅ Pyrogram موجود است")
        
        # Test API credentials
        api_id = int(os.getenv('API_ID', '12345678'))
        api_hash = os.getenv('API_HASH', 'abcdef1234567890abcdef1234567890')
        
        if api_id == 12345678 or api_hash == 'abcdef1234567890abcdef1234567890':
            print("⚠️ API credentials دمو - اتصال ممکن نیست")
            return False
        
        print(f"🔑 API_ID: {api_id}")
        print(f"🔑 API_HASH: {api_hash[:10]}...")
        
        # Try to create client
        try:
            client = Client(
                "test_session",
                api_id=api_id,
                api_hash=api_hash,
                bot_token=bot_token
            )
            print("✅ کلاینت ایجاد شد")
            
            # Try to start and get bot info
            await client.start()
            me = await client.get_me()
            print(f"✅ ربات آماده: @{me.username}")
            print(f"🆔 Bot ID: {me.id}")
            await client.stop()
            
            return True
            
        except Exception as e:
            print(f"❌ خطا در اتصال: {e}")
            return False
        
    except ImportError:
        print("⚠️ Pyrogram ناموجود - تست اتصال ممکن نیست")
        return False

def test_network():
    """Test network connectivity"""
    print("\n🌐 تست اتصال شبکه...")
    
    import subprocess
    
    hosts = [
        'telegram.org',
        'api.telegram.org', 
        'google.com'
    ]
    
    for host in hosts:
        try:
            result = subprocess.run(
                ['ping', '-c', '1', host],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ {host}: قابل دسترس")
            else:
                print(f"❌ {host}: غیرقابل دسترس")
        except:
            print(f"⚠️ {host}: نمی‌توان تست کرد")

def test_ports():
    """Test port availability"""
    print("\n🔌 تست پورت‌ها...")
    
    import socket
    
    ports = [
        ('api.telegram.org', 443, 'Telegram HTTPS'),
        ('api.telegram.org', 80, 'Telegram HTTP'),
    ]
    
    for host, port, desc in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ {host}:{port} - {desc}")
            else:
                print(f"❌ {host}:{port} - {desc} (بسته)")
        except Exception as e:
            print(f"⚠️ {host}:{port} - خطا: {e}")

async def run_simple_test():
    """Run a simple bot test"""
    print("\n🧪 تست ساده ربات...")
    
    try:
        from bot_demo_simple import SimpleCodeRootBot
        
        bot = SimpleCodeRootBot()
        print("✅ نمونه ربات ایجاد شد")
        
        # Test config loading
        config = bot.config
        print(f"✅ تنظیمات بارگذاری شد")
        print(f"   Token: {config['BOT_TOKEN'][:15]}...")
        print(f"   Admin: {config['ADMIN_USER_ID']}")
        print(f"   Demo: {config['DEMO_MODE']}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست ربات: {e}")
        return False

async def main():
    """Main diagnostic function"""
    print("🏥 تشخیص مشکلات ربات CodeRoot")
    print("=" * 50)
    print(f"🕐 زمان: {datetime.now()}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Platform: {sys.platform}")
    
    # Run all tests
    check_environment()
    test_imports()
    await test_bot_token()
    test_network()
    test_ports()
    await run_simple_test()
    
    print("\n" + "=" * 50)
    print("📋 خلاصه تشخیص:")
    print("1. اگر Pyrogram موجود نیست، ربات در حالت standalone اجرا می‌شود")
    print("2. اگر API credentials دمو است، اتصال به تلگرام امکان‌پذیر نیست")
    print("3. برای اتصال واقعی، API_ID و API_HASH واقعی نیاز است")
    print("4. ربات حداقل در حالت لاگ باید کار کند")
    
    print("\n🚀 برای تست:")
    print("   python3 bot_demo_simple.py")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ تشخیص متوقف شد")
    except Exception as e:
        print(f"\n💥 خطا: {e}")