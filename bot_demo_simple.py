#!/usr/bin/env python3
"""
Simplified CodeRoot Demo Bot - Works without real API
نسخه ساده ربات دمو که بدون API واقعی کار می‌کند
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
def load_config():
    """Load configuration with defaults"""
    config = {
        'BOT_TOKEN': os.getenv('BOT_TOKEN', '7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM'),
        'ADMIN_USER_ID': int(os.getenv('ADMIN_USER_ID', '7707164235')),
        'API_ID': int(os.getenv('API_ID', '12345678')),
        'API_HASH': os.getenv('API_HASH', 'abcdef1234567890abcdef1234567890'),
        'DEMO_MODE': os.getenv('DEMO_MODE', 'true').lower() == 'true'
    }
    return config

class SimpleCodeRootBot:
    def __init__(self):
        """Initialize simple bot"""
        self.config = load_config()
        self.running = False
        
        logger.info("🎭 Initializing Simple CodeRoot Demo Bot")
        logger.info(f"📊 Bot Token: {self.config['BOT_TOKEN'][:15]}...")
        logger.info(f"👤 Admin ID: {self.config['ADMIN_USER_ID']}")
        logger.info(f"🎭 Demo Mode: {self.config['DEMO_MODE']}")
        
        # Check if we have real API credentials
        if (self.config['API_ID'] == 12345678 or 
            self.config['API_HASH'] == 'abcdef1234567890abcdef1234567890'):
            logger.warning("⚠️ Using demo API credentials")
            logger.info("🎭 Will run in standalone demo mode")
            self.telegram_available = False
        else:
            logger.info("🚀 Real API credentials detected")
            self.telegram_available = True
            
        # Try to import Pyrogram
        try:
            from pyrogram import Client
            self.pyrogram_available = True
            logger.info("✅ Pyrogram available")
        except ImportError:
            self.pyrogram_available = False
            logger.warning("⚠️ Pyrogram not available")
    
    async def create_telegram_bot(self):
        """Create Telegram bot if possible"""
        if not self.pyrogram_available:
            logger.error("❌ Pyrogram not installed")
            return None
            
        try:
            from pyrogram import Client, filters
            from pyrogram.types import Message
            
            # Create bot client
            bot = Client(
                "simple_demo_bot",
                api_id=self.config['API_ID'],
                api_hash=self.config['API_HASH'],
                bot_token=self.config['BOT_TOKEN']
            )
            
            # Register simple handlers
            @bot.on_message(filters.command("start"))
            async def start_handler(client, message: Message):
                user_id = message.from_user.id
                user_name = message.from_user.first_name or "کاربر"
                
                welcome_text = f"""
🎭 سلام {user_name}!

به ربات دمو CodeRoot خوش آمدید!

✨ این نسخه دمو شامل:
• 🏪 ساخت فروشگاه شبیه‌سازی شده
• 💰 مدیریت مالی نمونه
• 📊 گزارش‌گیری کامل
• ⚙️ پنل مدیریت

🆔 شناسه شما: {user_id}
🎯 حالت: دمو کامل

💡 تمام قابلیت‌ها شبیه‌سازی شده‌اند
                """
                
                await message.reply_text(welcome_text)
                logger.info(f"👤 Start command from user {user_id} ({user_name})")
            
            @bot.on_message(filters.command("demo"))
            async def demo_handler(client, message: Message):
                demo_text = """
🎭 اطلاعات نسخه دمو:

📊 وضعیت سیستم:
• ✅ ربات فعال
• ✅ دیتابیس شبیه‌سازی
• ✅ پنل مدیریت
• ✅ گزارش‌گیری

🏪 فروشگاه‌های نمونه: 12
👥 کاربران نمونه: 156
💰 درآمد نمونه: 2,500,000 تومان

⚠️ تمام داده‌ها شبیه‌سازی شده‌اند
                """
                await message.reply_text(demo_text)
            
            @bot.on_message(filters.command("status"))
            async def status_handler(client, message: Message):
                status_text = f"""
📊 وضعیت ربات:

🕐 زمان فعلی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎭 حالت: دمو
👤 ادمین: {self.config['ADMIN_USER_ID']}
🔗 اتصال: تلگرام API

✅ سیستم سالم است
                """
                await message.reply_text(status_text)
            
            @bot.on_message(filters.text & filters.private)
            async def echo_handler(client, message: Message):
                if not message.text.startswith('/'):
                    await message.reply_text(f"🎭 دمو: شما نوشتید: {message.text}")
            
            return bot
            
        except Exception as e:
            logger.error(f"❌ Error creating Telegram bot: {e}")
            return None
    
    async def run_telegram_bot(self):
        """Run Telegram bot"""
        logger.info("🚀 Starting Telegram bot...")
        
        bot = await self.create_telegram_bot()
        if not bot:
            logger.error("❌ Failed to create Telegram bot")
            return False
        
        try:
            await bot.start()
            me = await bot.get_me()
            logger.info(f"✅ Bot started successfully: @{me.username}")
            logger.info(f"🆔 Bot ID: {me.id}")
            
            # Send test message to admin
            try:
                await bot.send_message(
                    self.config['ADMIN_USER_ID'],
                    f"🎭 ربات دمو CodeRoot آماده!\n\n"
                    f"🤖 نام: @{me.username}\n"
                    f"🆔 شناسه: {me.id}\n"
                    f"🕐 زمان: {datetime.now()}\n\n"
                    f"✅ برای تست /start بزنید"
                )
                logger.info("✅ Notification sent to admin")
            except Exception as e:
                logger.warning(f"⚠️ Could not send notification to admin: {e}")
            
            # Keep running
            self.running = True
            logger.info("🎭 Bot is running. Waiting for messages...")
            
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Error running bot: {e}")
            return False
        finally:
            if bot:
                await bot.stop()
                logger.info("🛑 Bot stopped")
        
        return True
    
    async def run_standalone_demo(self):
        """Run standalone demo without Telegram"""
        logger.info("🎭 Starting standalone demo service...")
        
        while True:
            logger.info(f"🎭 Demo service running - {datetime.now()}")
            logger.info(f"📊 Simulated stats:")
            logger.info(f"   👥 Users: 156")
            logger.info(f"   🏪 Shops: 12") 
            logger.info(f"   💰 Revenue: 2,500,000 T")
            logger.info(f"   ⚙️ Admin: {self.config['ADMIN_USER_ID']}")
            
            await asyncio.sleep(60)  # Log every minute
    
    async def start(self):
        """Start the bot"""
        try:
            logger.info("🎭 Starting CodeRoot Demo Bot...")
            
            # Try Telegram bot first
            if self.telegram_available and self.pyrogram_available:
                logger.info("🚀 Attempting Telegram connection...")
                success = await self.run_telegram_bot()
                if success:
                    return
                else:
                    logger.warning("⚠️ Telegram connection failed, falling back to standalone mode")
            
            # Fallback to standalone mode
            logger.info("🎭 Running in standalone demo mode")
            await self.run_standalone_demo()
            
        except KeyboardInterrupt:
            logger.info("⏹️ Bot stopped by user")
            self.running = False
        except Exception as e:
            logger.error(f"💥 Fatal error: {e}")
            sys.exit(1)

def main():
    """Main function"""
    print("🎭 CodeRoot Demo Bot - Simple Version")
    print("=" * 50)
    
    bot = SimpleCodeRootBot()
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()