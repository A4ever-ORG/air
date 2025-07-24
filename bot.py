import asyncio
import logging
import signal
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

# Import configuration
from config import Config

# Import database
from database import init_database, close_database

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
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CodeRootBot:
    def __init__(self):
        """Initialize the bot"""
        self.app = Client(
            "coderoot_bot",
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
        
        # Message handlers
        @self.app.on_message(filters.command("start"))
        async def start_handler(client, message):
            await UserHandlers.start_command(client, message)
        
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
                
                # Shop management actions
                elif data == "add_product":
                    await self.handle_add_product(client, callback_query)
                elif data == "manage_products":
                    await self.handle_manage_products(client, callback_query)
                elif data == "orders":
                    await self.handle_orders(client, callback_query)
                elif data == "sales_report":
                    await self.handle_sales_report(client, callback_query)
                elif data == "shop_settings":
                    await self.handle_shop_settings(client, callback_query)
                elif data == "upgrade_plan":
                    await self.handle_upgrade_plan(client, callback_query)
                elif data == "renew_subscription":
                    await self.handle_renew_subscription(client, callback_query)
                
                # Support and info actions
                elif data == "support":
                    await self.handle_support(client, callback_query)
                elif data == "tutorial":
                    await self.handle_tutorial(client, callback_query)
                elif data == "rules":
                    await self.handle_rules(client, callback_query)
                elif data == "reports":
                    await self.handle_reports(client, callback_query)
                
                # Ignore page info callbacks
                elif data == "page_info":
                    await callback_query.answer()
                
                else:
                    await callback_query.answer("❌ عملیات نامعتبر!")
                    
            except Exception as e:
                logger.error(f"Error handling callback {data}: {e}")
                await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_photo_messages(self, client: Client, message: Message):
        """Handle photo messages (payment receipts)"""
        try:
            user_id = message.from_user.id
            
            # Check if user is in payment process
            from handlers.user_handlers import user_states
            
            if user_id in user_states and user_states[user_id].get('state') == 'waiting_payment_receipt':
                # Handle payment receipt
                await message.reply_text(
                    "📷 رسید پرداخت دریافت شد!\n\n"
                    "✅ رسید شما در حال بررسی است و در صورت تأیید، فروشگاه شما فعال خواهد شد.\n"
                    "⏰ مدت زمان بررسی: 24 ساعت\n\n"
                    "📞 در صورت نیاز به پیگیری با پشتیبانی تماس بگیرید."
                )
                
                # Notify admin about payment receipt
                await NotificationUtils.send_admin_notification(
                    client,
                    f"رسید پرداخت جدید:\n"
                    f"👤 کاربر: {message.from_user.first_name}\n"
                    f"🆔 شناسه: {user_id}\n"
                    f"📊 پلن: {user_states[user_id].get('selected_plan', 'نامشخص')}"
                )
                
                # Forward receipt to admin
                await message.forward(Config.ADMIN_USER_ID)
                
                # Clear user state
                del user_states[user_id]
                
            else:
                await message.reply_text("📷 تصویر دریافت شد، اما در حال حاضر نیازی به ارسال تصویر نیست.")
                
        except Exception as e:
            logger.error(f"Error handling photo message: {e}")
    
    async def handle_add_product(self, client: Client, callback_query: CallbackQuery):
        """Handle add product callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_manage_products(self, client: Client, callback_query: CallbackQuery):
        """Handle manage products callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_orders(self, client: Client, callback_query: CallbackQuery):
        """Handle orders callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_sales_report(self, client: Client, callback_query: CallbackQuery):
        """Handle sales report callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_shop_settings(self, client: Client, callback_query: CallbackQuery):
        """Handle shop settings callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_upgrade_plan(self, client: Client, callback_query: CallbackQuery):
        """Handle upgrade plan callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_renew_subscription(self, client: Client, callback_query: CallbackQuery):
        """Handle renew subscription callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    async def handle_support(self, client: Client, callback_query: CallbackQuery):
        """Handle support callback"""
        try:
            support_text = """
🆘 پشتیبانی CodeRoot

📞 راه‌های ارتباط:
• تلگرام: @YourSupportUsername
• ایمیل: support@coderoot.ir

⏰ ساعات کاری:
شنبه تا چهارشنبه: 9:00 - 18:00
پنج‌شنبه: 9:00 - 13:00

❓ سوالات متداول:
• چگونه فروشگاه بسازم؟
• چگونه محصول اضافه کنم؟
• چگونه پلن خود را ارتقا دهم؟

📚 برای آموزش کامل روی دکمه آموزش کلیک کنید.
            """
            
            from utils import KeyboardMarkups
            keyboard = KeyboardMarkups.back_keyboard("back_to_main")
            
            await callback_query.message.edit_text(support_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in support: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_tutorial(self, client: Client, callback_query: CallbackQuery):
        """Handle tutorial callback"""
        try:
            tutorial_text = """
📚 آموزش استفاده از CodeRoot

🔸 مرحله 1: ایجاد فروشگاه
• روی "ساخت فروشگاه" کلیک کنید
• پلن مورد نظر را انتخاب کنید
• نام فروشگاه را وارد کنید
• توکن ربات را از @BotFather دریافت کنید

🔸 مرحله 2: افزودن محصولات
• به فروشگاه خود وارد شوید
• روی "افزودن محصول" کلیک کنید
• اطلاعات محصول را وارد کنید

🔸 مرحله 3: مدیریت سفارش‌ها
• سفارش‌ها را از بخش "سفارش‌ها" مشاهده کنید
• وضعیت سفارش‌ها را بروزرسانی کنید

🎥 ویدیوهای آموزشی: @YourTutorialChannel
            """
            
            from utils import KeyboardMarkups
            keyboard = KeyboardMarkups.back_keyboard("back_to_main")
            
            await callback_query.message.edit_text(tutorial_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in tutorial: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_rules(self, client: Client, callback_query: CallbackQuery):
        """Handle rules callback"""
        try:
            rules_text = """
📜 قوانین و مقررات CodeRoot

✅ مجاز:
• فروش محصولات قانونی
• استفاده صحیح از امکانات ربات
• رعایت حقوق مشتریان

❌ ممنوع:
• فروش محصولات غیرقانونی
• کلاهبرداری و تقلب
• استفاده از ربات برای اسپم
• نقض حقوق مالکیت معنوی

⚖️ پیامدهای نقض قوانین:
• اخطار کتبی
• تعلیق موقت حساب
• حذف دائمی حساب

📞 گزارش تخلف:
در صورت مشاهده هرگونه تخلف، با پشتیبانی تماس بگیرید.

🔒 حریم خصوصی:
اطلاعات شما محفوظ و طبق قوانین حریم خصوصی حفاظت می‌شود.
            """
            
            from utils import KeyboardMarkups
            keyboard = KeyboardMarkups.back_keyboard("back_to_main")
            
            await callback_query.message.edit_text(rules_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in rules: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    async def handle_reports(self, client: Client, callback_query: CallbackQuery):
        """Handle reports callback"""
        await callback_query.answer("🚧 این بخش در حال توسعه است!")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}. Shutting down gracefully...")
        asyncio.create_task(self.shutdown())
    
    async def shutdown(self):
        """Graceful shutdown"""
        try:
            logger.info("Closing database connection...")
            await close_database()
            
            logger.info("Stopping bot...")
            await self.app.stop()
            
            logger.info("Bot stopped successfully.")
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            sys.exit(1)
    
    async def start(self):
        """Start the bot"""
        try:
            # Initialize database
            logger.info("Initializing database...")
            await init_database()
            
            # Start the bot
            logger.info("Starting CodeRoot bot...")
            await self.app.start()
            
            # Get bot info
            me = await self.app.get_me()
            logger.info(f"Bot started successfully: @{me.username}")
            
            # Send startup notification to admin
            if Config.ADMIN_USER_ID:
                try:
                    await self.app.send_message(
                        Config.ADMIN_USER_ID,
                        f"🚀 ربات CodeRoot با موفقیت راه‌اندازی شد!\n\n"
                        f"🤖 نام ربات: @{me.username}\n"
                        f"📅 زمان راه‌اندازی: {logging.Formatter().formatTime(logging.LogRecord('', 0, '', 0, '', (), None))}"
                    )
                except Exception as e:
                    logger.error(f"Failed to send startup notification: {e}")
            
            # Keep the bot running
            logger.info("Bot is running. Press Ctrl+C to stop.")
            await asyncio.Event().wait()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt. Shutting down...")
            await self.shutdown()
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            await self.shutdown()

async def main():
    """Main function"""
    bot = CodeRootBot()
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)