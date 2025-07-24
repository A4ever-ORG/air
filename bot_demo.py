import asyncio
import logging
import signal
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

# Import configuration
from config import Config

# Import mock database instead of real one
from database_mock import init_database, close_database

# Import handlers
from handlers.user_handlers import UserHandlers
from handlers.admin_handlers import AdminHandlers

# Import utilities
from utils import SecurityUtils, NotificationUtils

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CodeRootDemoBot:
    def __init__(self):
        """Initialize the demo bot"""
        
        # Validate configuration
        try:
            Config.validate_required_config()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)
        
        # Check if we have real credentials or demo mode
        if Config.API_ID == 12345678 or Config.API_HASH == "abcdef1234567890abcdef1234567890":
            logger.warning("⚠️ Using demo API credentials - some features may not work")
            logger.info("🎭 Running in full demo mode without Telegram connection")
            self.demo_mode_only = True
            self.app = None
        else:
            logger.info("🚀 Using real API credentials")
            self.demo_mode_only = False
            self.app = Client(
                "coderoot_demo_bot",
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                bot_token=Config.BOT_TOKEN
            )
            # Register handlers
            self.register_handlers()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def register_handlers(self):
        """Register all bot handlers"""
        
        if not self.app:
            return
        
        # Message handlers
        @self.app.on_message(filters.command("start"))
        async def start_handler(client, message):
            await UserHandlers.start_command(client, message)
        
        @self.app.on_message(filters.command("demo"))
        async def demo_handler(client, message):
            demo_text = """
🎭 حالت دمو CodeRoot

🎉 خوش آمدید به نسخه دمو ربات CodeRoot!

✨ ویژگی‌های دمو:
• ✅ تمام قابلیت‌های اصلی فعال
• ✅ ساخت فروشگاه بدون محدودیت
• ✅ پنل مدیریت کامل
• ✅ گزارش‌گیری و آمار
• ⚡ بدون نیاز به دیتابیس
• 🚀 آماده برای تست

🔄 برای شروع از دستور /start استفاده کنید
            """
            await message.reply_text(demo_text)
        
        @self.app.on_message(filters.text & filters.private)
        async def text_handler(client, message):
            # Handle user text messages
            await UserHandlers.handle_text_messages(client, message)
            # Handle admin text messages
            await AdminHandlers.handle_admin_text_messages(client, message)
        
        @self.app.on_message(filters.photo & filters.private)
        async def photo_handler(client, message):
            # Handle photo messages (payment receipts, etc.)
            await self.handle_photo_messages(client, message)
        
        # Callback query handlers
        @self.app.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            
            try:
                # Channel membership check
                if data == "check_membership":
                    await UserHandlers.check_membership_callback(client, callback_query)
                
                # Main user actions
                elif data == "create_shop":
                    await UserHandlers.create_shop_callback(client, callback_query)
                elif data.startswith("select_plan:"):
                    await UserHandlers.select_plan_callback(client, callback_query)
                elif data == "payment_done":
                    await UserHandlers.payment_done_callback(client, callback_query)
                elif data == "my_shop":
                    await UserHandlers.my_shop_callback(client, callback_query)
                elif data == "cancel":
                    await UserHandlers.cancel_callback(client, callback_query)
                elif data == "back_to_main":
                    await UserHandlers.back_to_main_callback(client, callback_query)
                
                # Admin panel actions
                elif data == "admin_panel":
                    await AdminHandlers.admin_panel_callback(client, callback_query)
                elif data == "admin_users":
                    await AdminHandlers.admin_users_callback(client, callback_query)
                elif data == "admin_users_list" or data.startswith("admin_users_list:"):
                    await AdminHandlers.admin_users_list_callback(client, callback_query)
                elif data == "admin_shops":
                    await AdminHandlers.admin_shops_callback(client, callback_query)
                elif data == "admin_shops_list" or data.startswith("admin_shops_list:"):
                    await AdminHandlers.admin_shops_list_callback(client, callback_query)
                elif data == "admin_finance":
                    await AdminHandlers.admin_finance_callback(client, callback_query)
                elif data == "admin_broadcast":
                    await AdminHandlers.admin_broadcast_callback(client, callback_query)
                elif data == "admin_stats":
                    await AdminHandlers.admin_stats_callback(client, callback_query)
                elif data == "admin_users_report":
                    await AdminHandlers.admin_users_report_callback(client, callback_query)
                elif data == "confirm_broadcast":
                    await AdminHandlers.confirm_broadcast_callback(client, callback_query)
                elif data == "cancel_admin":
                    await AdminHandlers.cancel_admin_callback(client, callback_query)
                
                # Shop management actions (demo responses)
                elif data == "add_product":
                    await self.handle_demo_feature(client, callback_query, "افزودن محصول")
                elif data == "manage_products":
                    await self.handle_demo_feature(client, callback_query, "مدیریت محصولات")
                elif data == "orders":
                    await self.handle_demo_feature(client, callback_query, "سفارش‌ها")
                elif data == "sales_report":
                    await self.handle_demo_feature(client, callback_query, "گزارش فروش")
                elif data == "shop_settings":
                    await self.handle_demo_feature(client, callback_query, "تنظیمات فروشگاه")
                elif data == "upgrade_plan":
                    await self.handle_demo_feature(client, callback_query, "ارتقاء پلن")
                elif data == "renew_subscription":
                    await self.handle_demo_feature(client, callback_query, "تمدید اشتراک")
                
                # Support and info actions
                elif data == "support":
                    await self.handle_support(client, callback_query)
                elif data == "tutorial":
                    await self.handle_tutorial(client, callback_query)
                elif data == "rules":
                    await self.handle_rules(client, callback_query)
                elif data == "reports":
                    await self.handle_demo_feature(client, callback_query, "گزارش‌ها")
                
                # Ignore page info callbacks
                elif data == "page_info":
                    await callback_query.answer()
                
                else:
                    await callback_query.answer("❌ عملیات نامعتبر!")
                    
            except Exception as e:
                logger.error(f"Error handling callback {data}: {e}")
                await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_demo_feature(self, client: Client, callback_query: CallbackQuery, feature_name: str):
        """Handle demo features with sample data"""
        demo_text = f"""
🎭 دمو: {feature_name}

✨ این بخش در نسخه دمو به صورت شبیه‌سازی شده نمایش داده می‌شود.

📊 داده‌های نمونه:
• محصولات: 5 محصول
• سفارش‌ها: 12 سفارش
• درآمد: 2,500,000 تومان
• مشتریان: 25 نفر

🚀 در نسخه اصلی تمام قابلیت‌ها کاملاً فعال است.
        """
        
        from utils import KeyboardMarkups
        keyboard = KeyboardMarkups.back_keyboard("my_shop")
        
        await callback_query.message.edit_text(demo_text, reply_markup=keyboard)
    
    async def handle_photo_messages(self, client: Client, message: Message):
        """Handle photo messages (payment receipts) - Demo version"""
        try:
            user_id = message.from_user.id
            
            # Check if user is in payment process
            from handlers.user_handlers import user_states
            
            if user_id in user_states and user_states[user_id].get('state') == 'waiting_payment_receipt':
                # Auto-approve payment in demo
                await message.reply_text(
                    "✅ رسید پرداخت در نسخه دمو خودکار تأیید شد!\n\n"
                    "🎉 فروشگاه شما فعال شده است.\n"
                    "🔄 از منوی اصلی بخش \"ورود به فروشگاه من\" را انتخاب کنید."
                )
                
                # Clear user state
                if user_id in user_states:
                    del user_states[user_id]
                
            else:
                await message.reply_text(
                    "📷 تصویر دریافت شد! \n\n"
                    "🎭 این نسخه دمو است و تصاویر خودکار پردازش می‌شوند."
                )
                
        except Exception as e:
            logger.error(f"Error handling photo message: {e}")
    
    async def handle_support(self, client: Client, callback_query: CallbackQuery):
        """Handle support callback - Demo version"""
        try:
            support_text = """
🆘 پشتیبانی CodeRoot (نسخه دمو)

📞 راه‌های ارتباط:
• تلگرام: @CodeRootSupport
• ایمیل: demo@coderoot.ir

⏰ ساعات کاری:
شنبه تا چهارشنبه: 9:00 - 18:00

❓ سوالات متداول دمو:
• چگونه نسخه کامل تهیه کنم؟
• قیمت‌گذاری چگونه است؟
• چه امکاناتی در نسخه اصلی است؟

🎭 این نسخه دمو برای نمایش قابلیت‌ها طراحی شده است.
            """
            
            from utils import KeyboardMarkups
            keyboard = KeyboardMarkups.back_keyboard("back_to_main")
            
            await callback_query.message.edit_text(support_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in support: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_tutorial(self, client: Client, callback_query: CallbackQuery):
        """Handle tutorial callback - Demo version"""
        try:
            tutorial_text = """
📚 آموزش CodeRoot (نسخه دمو)

🔸 مرحله 1: تست ساخت فروشگاه
• روی "ساخت فروشگاه" کلیک کنید
• یکی از پلن‌ها را انتخاب کنید
• در دمو همه چیز خودکار تأیید می‌شود

🔸 مرحله 2: بررسی پنل مدیریت
• اگر ادمین هستید پنل مدیریت را ببینید
• قابلیت‌های مختلف را تست کنید

🔸 مرحله 3: تست فروشگاه
• وارد "فروشگاه من" شوید
• منوهای مختلف را امتحان کنید

🎭 نسخه دمو: تمام قابلیت‌ها شبیه‌سازی شده
🚀 نسخه اصلی: با دیتابیس واقعی و قابلیت کامل
            """
            
            from utils import KeyboardMarkups
            keyboard = KeyboardMarkups.back_keyboard("back_to_main")
            
            await callback_query.message.edit_text(tutorial_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in tutorial: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_rules(self, client: Client, callback_query: CallbackQuery):
        """Handle rules callback - Demo version"""
        try:
            rules_text = """
📜 قوانین CodeRoot (نسخه دمو)

✅ نسخه دمو:
• تست رایگان تمام قابلیت‌ها
• داده‌های شبیه‌سازی شده
• بدون نیاز به اطلاعات واقعی

⚠️ محدودیت‌های دمو:
• اتصال به دیتابیس واقعی ندارد
• ربات‌های زیرمجموعه ایجاد نمی‌شوند
• پرداخت‌ها واقعی نیستند

✅ نسخه اصلی:
• تمام قابلیت‌ها کاملاً فعال
• دیتابیس و API های واقعی
• ساخت ربات‌های زیرمجموعه

💡 برای خرید نسخه کامل با پشتیبانی تماس بگیرید.
            """
            
            from utils import KeyboardMarkups
            keyboard = KeyboardMarkups.back_keyboard("back_to_main")
            
            await callback_query.message.edit_text(rules_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in rules: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}. Shutting down gracefully...")
        asyncio.create_task(self.shutdown())
    
    async def shutdown(self):
        """Graceful shutdown"""
        try:
            logger.info("Closing mock database connection...")
            await close_database()
            
            if self.app:
                logger.info("Stopping demo bot...")
                await self.app.stop()
            
            logger.info("Demo bot stopped successfully.")
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            sys.exit(1)
    
    async def start_demo_web_server(self):
        """Start a simple web server for demo when Telegram connection is not available"""
        from datetime import datetime
        
        logger.info("🎭 Starting demo web interface...")
        
        demo_info = f"""
        🎭 CodeRoot Demo Bot - حالت وب

        📊 اطلاعات دمو:
        • ربات: {Config.BOT_TOKEN[:10]}...
        • ادمین: {Config.ADMIN_USER_ID}
        • حالت: دمو کامل
        • زمان شروع: {datetime.now()}

        ✨ قابلیت‌های در دسترس:
        • مدیریت کاربران شبیه‌سازی شده
        • فروشگاه‌های دمو
        • پنل مدیریت کامل
        • گزارش‌گیری نمونه

        🔗 برای دسترسی کامل نیاز به API واقعی تلگرام دارید
        """
        
        logger.info(demo_info)
        
        # Keep the service running
        while True:
            await asyncio.sleep(30)
            logger.info("🎭 Demo service is running...")
    
    async def start(self):
        """Start the demo bot"""
        try:
            # Initialize mock database
            logger.info("Initializing mock database...")
            await init_database()
            
            if self.demo_mode_only:
                logger.info("🎭 Starting demo web service (no Telegram connection)...")
                await self.start_demo_web_server()
            else:
                # Start the bot with real connection
                logger.info("Starting CodeRoot Demo Bot...")
                await self.app.start()
                
                # Get bot info
                me = await self.app.get_me()
                logger.info(f"Demo Bot started successfully: @{me.username}")
                
                # Send startup notification to admin
                if Config.ADMIN_USER_ID:
                    try:
                        await self.app.send_message(
                            Config.ADMIN_USER_ID,
                            f"🎭 ربات دمو CodeRoot راه‌اندازی شد!\n\n"
                            f"🤖 ربات: @{me.username}\n"
                            f"✨ حالت: دمو (بدون دیتابیس)\n"
                            f"📅 زمان: {datetime.now()}\n\n"
                            f"💡 دستور /demo برای توضیحات"
                        )
                    except Exception as e:
                        logger.error(f"Failed to send startup notification: {e}")
                
                # Keep the bot running
                logger.info("Demo bot is running. Press Ctrl+C to stop.")
                await asyncio.Event().wait()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt. Shutting down...")
            await self.shutdown()
        except Exception as e:
            logger.error(f"Error starting demo bot: {e}")
            if not self.demo_mode_only:
                logger.info("Falling back to demo web service...")
                await self.start_demo_web_server()

async def main():
    """Main function"""
    bot = CodeRootDemoBot()
    await bot.start()

if __name__ == "__main__":
    try:
        from datetime import datetime
        print("🎭 Starting CodeRoot Demo Bot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Demo bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)