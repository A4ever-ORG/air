#!/usr/bin/env python3
"""
Test script for CodeRoot Demo Bot
تست عملکرد نسخه دمو ربات CodeRoot
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_environment_variables():
    """Test environment variables"""
    print("🔍 بررسی متغیرهای محیطی...")
    
    required_vars = ['BOT_TOKEN', 'API_ID', 'API_HASH', 'ADMIN_USER_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ متغیرهای محیطی ناقص: {', '.join(missing_vars)}")
        print("💡 فایل .env را بررسی کنید")
        return False
    
    print("✅ متغیرهای محیطی در نظم است")
    return True

def test_imports():
    """Test all imports"""
    print("📦 بررسی import ها...")
    
    try:
        # Test config
        from config import Config, PLANS
        print("✅ Config imported successfully")
        
        # Test database mock
        from database_mock import UserManager, ShopManager, init_database
        print("✅ Mock Database imported successfully")
        
        # Test handlers
        from handlers.user_handlers import UserHandlers
        from handlers.admin_handlers import AdminHandlers
        print("✅ Handlers imported successfully")
        
        # Test utils
        from utils import BotUtils, MessageTemplates, KeyboardMarkups
        print("✅ Utils imported successfully")
        
        # Test pyrogram
        from pyrogram import Client
        print("✅ Pyrogram imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطای import: {e}")
        return False

async def test_mock_database():
    """Test mock database functionality"""
    print("🗄️ تست دیتابیس مخصوص دمو...")
    
    try:
        from database_mock import init_database, UserManager, ShopManager
        
        # Initialize database
        await init_database()
        print("✅ دیتابیس مخصوص دمو راه‌اندازی شد")
        
        # Test user creation
        test_user = {
            "user_id": 999999999,
            "username": "test_user",
            "first_name": "کاربر",
            "last_name": "تست"
        }
        
        user = await UserManager.create_user(test_user)
        print("✅ ایجاد کاربر تست موفق")
        
        # Test user retrieval
        retrieved_user = await UserManager.get_user(999999999)
        if retrieved_user:
            print("✅ بازیابی کاربر موفق")
        else:
            print("❌ خطا در بازیابی کاربر")
            return False
        
        # Test shop creation
        test_shop = {
            "owner_id": 999999999,
            "name": "فروشگاه تست",
            "bot_token": "test_token",
            "plan": "free"
        }
        
        shop = await ShopManager.create_shop(test_shop)
        print("✅ ایجاد فروشگاه تست موفق")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست دیتابیس مخصوص دمو: {e}")
        return False

def test_bot_configuration():
    """Test bot configuration"""
    print("⚙️ بررسی تنظیمات ربات...")
    
    try:
        from config import Config, PLANS
        
        # Check required config
        if not Config.BOT_TOKEN:
            print("❌ BOT_TOKEN تنظیم نشده")
            return False
        
        if not Config.API_ID or Config.API_ID == 0:
            print("❌ API_ID تنظیم نشده")
            return False
        
        if not Config.API_HASH:
            print("❌ API_HASH تنظیم نشده")
            return False
        
        if not Config.ADMIN_USER_ID:
            print("❌ ADMIN_USER_ID تنظیم نشده")
            return False
        
        # Check plans configuration
        if not PLANS or len(PLANS) != 3:
            print("❌ پلن‌ها به درستی تنظیم نشده‌اند")
            return False
        
        print("✅ تنظیمات ربات صحیح است")
        return True
        
    except Exception as e:
        print(f"❌ خطا در بررسی تنظیمات: {e}")
        return False

async def test_bot_initialization():
    """Test bot initialization without starting"""
    print("🤖 تست راه‌اندازی ربات...")
    
    try:
        from bot_demo import CodeRootDemoBot
        
        # Create bot instance
        bot = CodeRootDemoBot()
        print("✅ نمونه ربات ایجاد شد")
        
        # Check if handlers are registered
        if hasattr(bot.app, 'handlers'):
            print("✅ Handlers ثبت شده‌اند")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی ربات: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("🛠️ تست ابزارهای کمکی...")
    
    try:
        from utils import BotUtils, MessageTemplates, KeyboardMarkups, ValidationUtils
        
        # Test price formatting
        formatted_price = BotUtils.format_price(1000000)
        if "1,000,000" in formatted_price:
            print("✅ فرمت قیمت صحیح است")
        else:
            print("❌ مشکل در فرمت قیمت")
            return False
        
        # Test keyboard creation
        main_keyboard = KeyboardMarkups.main_menu()
        if main_keyboard and hasattr(main_keyboard, 'inline_keyboard'):
            print("✅ کیبورد اصلی ایجاد شد")
        else:
            print("❌ مشکل در ایجاد کیبورد")
            return False
        
        # Test validation
        if ValidationUtils.validate_shop_name("فروشگاه تست"):
            print("✅ اعتبارسنجی نام فروشگاه")
        else:
            print("❌ مشکل در اعتبارسنجی")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست ابزارها: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    print("📁 بررسی ساختار فایل‌ها...")
    
    required_files = [
        'bot_demo.py',
        'database_mock.py',
        'config.py',
        'utils.py',
        'handlers/user_handlers.py',
        'handlers/admin_handlers.py',
        'requirements.txt',
        'Dockerfile.liara',
        'liara.json'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ فایل‌های ناقص: {', '.join(missing_files)}")
        return False
    
    print("✅ تمام فایل‌های مورد نیاز موجود است")
    return True

async def run_all_tests():
    """Run all tests"""
    print("🎭 شروع تست‌های نسخه دمو CodeRoot")
    print("=" * 50)
    
    tests = [
        ("بررسی ساختار فایل‌ها", test_file_structure),
        ("بررسی متغیرهای محیطی", test_environment_variables),
        ("بررسی import ها", test_imports),
        ("بررسی تنظیمات ربات", test_bot_configuration),
        ("تست دیتابیس مخصوص دمو", test_mock_database),
        ("تست ابزارهای کمکی", test_utils),
        ("تست راه‌اندازی ربات", test_bot_initialization),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
                print(f"✅ {test_name}: موفق")
            else:
                failed += 1
                print(f"❌ {test_name}: ناموفق")
                
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: خطا - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتایج تست:")
    print(f"✅ موفق: {passed}")
    print(f"❌ ناموفق: {failed}")
    print(f"📊 کل: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 تمام تست‌ها موفق! نسخه دمو آماده استفاده است.")
        print("🚀 برای شروع: python bot_demo.py")
        return True
    else:
        print(f"\n⚠️ {failed} تست ناموفق. لطفاً مشکلات را برطرف کنید.")
        return False

def main():
    """Main function"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Run tests
        result = asyncio.run(run_all_tests())
        
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ تست متوقف شد.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 خطای کلی: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()