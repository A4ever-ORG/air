#!/usr/bin/env python3
"""
Script to help get real Telegram API credentials
اسکریپت کمکی برای دریافت API واقعی تلگرام
"""

import sys

def print_instructions():
    """Print instructions for getting API credentials"""
    print("🔑 راهنمای دریافت API واقعی تلگرام")
    print("=" * 50)
    print()
    print("📱 مراحل دریافت API_ID و API_HASH:")
    print()
    print("1️⃣ به سایت my.telegram.org مراجعه کنید")
    print("   🔗 https://my.telegram.org")
    print()
    print("2️⃣ وارد حساب تلگرام خود شوید")
    print("   📱 شماره تلفن + کد تأیید")
    print()
    print("3️⃣ روی 'API development tools' کلیک کنید")
    print()
    print("4️⃣ فرم 'Create new application' را پر کنید:")
    print("   📝 App title: CodeRoot Demo")
    print("   📝 Short name: coderoot")
    print("   📝 URL: (خالی بگذارید)")
    print("   📝 Platform: Desktop")
    print("   📝 Description: Demo bot for CodeRoot")
    print()
    print("5️⃣ روی 'Create application' کلیک کنید")
    print()
    print("6️⃣ API_ID و API_HASH را کپی کنید")
    print()
    print("✅ سپس فایل .env را به‌روزرسانی کنید:")
    print("   API_ID=your_real_api_id")
    print("   API_HASH=your_real_api_hash")
    print()
    print("⚠️ نکات مهم:")
    print("• API_ID یک عدد است (مثل: 1234567)")
    print("• API_HASH یک رشته 32 کاراکتری است")
    print("• این اطلاعات محرمانه هستند")
    print("• هر حساب تلگرام فقط یک API دارد")
    print()
    print("🎭 بدون API واقعی، ربات فقط در حالت دمو کار می‌کند")

def check_current_config():
    """Check current configuration"""
    try:
        from config import Config
        
        print("🔍 بررسی تنظیمات فعلی:")
        print("=" * 30)
        
        if Config.BOT_TOKEN:
            print(f"✅ BOT_TOKEN: {Config.BOT_TOKEN[:10]}...")
        else:
            print("❌ BOT_TOKEN: تنظیم نشده")
        
        if Config.API_ID == 12345678:
            print("⚠️ API_ID: مقدار دمو (نیاز به API واقعی)")
        else:
            print(f"✅ API_ID: {Config.API_ID}")
        
        if Config.API_HASH == "abcdef1234567890abcdef1234567890":
            print("⚠️ API_HASH: مقدار دمو (نیاز به API واقعی)")
        else:
            print(f"✅ API_HASH: {Config.API_HASH[:10]}...")
        
        print(f"✅ ADMIN_USER_ID: {Config.ADMIN_USER_ID}")
        
        print()
        if Config.API_ID == 12345678 or Config.API_HASH == "abcdef1234567890abcdef1234567890":
            print("🎭 وضعیت: حالت دمو (بدون اتصال تلگرام)")
            print("💡 برای اتصال کامل، API واقعی دریافت کنید")
        else:
            print("🚀 وضعیت: آماده اتصال به تلگرام")
        
    except ImportError:
        print("❌ خطا در بارگذاری تنظیمات")

def main():
    """Main function"""
    print("🎭 CodeRoot Demo - مدیریت API")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_current_config()
    else:
        print_instructions()
        print()
        check_current_config()

if __name__ == "__main__":
    main()