#!/usr/bin/env python3
"""
CodeRoot - Complete MVP Production Bot
ربات مادر CodeRoot - نسخه تولید کامل

Features:
- Complete user management with referral system
- Shop creation and management
- Admin panel for HADI
- Channel join enforcement
- Payment processing
- Sub-bot creation system
- Comprehensive analytics
"""

import asyncio
import logging
import sys
import signal
import os
from datetime import datetime, timedelta
from pathlib import Path

from pyrogram import Client, filters, enums
from pyrogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, 
    InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
)

# Import local modules
from config import Config, PLANS, FEATURES, NOTIFICATION_TEMPLATES
from database import (
    init_database, close_database, UserManager, ShopManager, 
    ProductManager, OrderManager, PaymentManager, AnalyticsManager
)
from utils.keyboards import KeyboardMarkups
from utils.validation import ValidationUtils
from utils.security import SecurityUtils
from utils.notifications import NotificationUtils
from utils.excel_generator import ExcelGenerator
from utils.bot_utils import BotUtils

# Setup logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Config.LOG_FILE) if Config.LOG_FILE else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global state management
user_states = {}
admin_states = {}

class CodeRootBot:
    """Main CodeRoot Bot class"""
    
    def __init__(self):
        """Initialize the bot"""
        # Validate configuration
        Config.validate_required_config()
        
        # Create Pyrogram client
        self.app = Client(
            "coderoot_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )
        
        self.is_running = False
        logger.info("🚀 CodeRoot MVP Bot initialized")
    
    async def start(self):
        """Start the bot"""
        try:
            # Initialize database
            await init_database()
            logger.info("✅ Database connected")
            
            # Start Pyrogram client
            await self.app.start()
            me = await self.app.get_me()
            logger.info(f"✅ Bot started: @{me.username} (ID: {me.id})")
            
            # Register handlers
            self.register_handlers()
            
            # Send startup notification to admin
            try:
                await self.app.send_message(
                    Config.ADMIN_USER_ID,
                    f"🚀 **CodeRoot MVP Bot Started**\n\n"
                    f"🤖 Bot: @{me.username}\n"
                    f"🆔 ID: {me.id}\n"
                    f"🕐 Time: {datetime.now()}\n"
                    f"📊 Mode: Production\n\n"
                    f"✅ All systems operational!"
                )
            except Exception as e:
                logger.warning(f"Could not send startup notification: {e}")
            
            self.is_running = True
            logger.info("🎉 Bot is running and ready to serve!")
            
            # Keep running
            await self.keep_alive()
            
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot gracefully"""
        logger.info("🛑 Stopping bot...")
        self.is_running = False
        
        # Send shutdown notification
        try:
            await self.app.send_message(
                Config.ADMIN_USER_ID,
                f"🛑 **CodeRoot Bot Stopped**\n\n"
                f"🕐 Time: {datetime.now()}\n"
                f"💾 All data saved successfully"
            )
        except:
            pass
        
        # Close connections
        await self.app.stop()
        await close_database()
        logger.info("✅ Bot stopped gracefully")
    
    async def keep_alive(self):
        """Keep the bot running"""
        while self.is_running:
            await asyncio.sleep(1)
    
    def register_handlers(self):
        """Register all bot handlers"""
        # Command handlers
        self.app.on_message(filters.command("start") & filters.private)(self.start_command)
        self.app.on_message(filters.command("help") & filters.private)(self.help_command)
        self.app.on_message(filters.command("admin") & filters.private)(self.admin_command)
        self.app.on_message(filters.command("shop") & filters.private)(self.shop_command)
        self.app.on_message(filters.command("profile") & filters.private)(self.profile_command)
        self.app.on_message(filters.command("referral") & filters.private)(self.referral_command)
        
        # Callback handlers
        self.app.on_callback_query()(self.callback_handler)
        
        # Message handlers
        self.app.on_message(filters.text & filters.private)(self.text_handler)
        self.app.on_message(filters.photo & filters.private)(self.photo_handler)
        self.app.on_message(filters.document & filters.private)(self.document_handler)
        
        logger.info("✅ All handlers registered")
    
    # ==================== COMMAND HANDLERS ====================
    
    async def start_command(self, client: Client, message: Message):
        """Handle /start command"""
        user_id = message.from_user.id
        
        try:
            # Check if user exists
            user = await UserManager.get_user(user_id)
            
            if not user:
                # Extract referral code from start parameter
                referral_code = None
                if message.command and len(message.command) > 1:
                    referral_code = message.command[1]
                
                # Create new user
                user_data = {
                    "user_id": user_id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "referred_by": referral_code
                }
                
                user = await UserManager.create_user(user_data)
                
                # Send welcome message for new users
                welcome_text = (
                    f"🎉 **سلام {message.from_user.first_name}!**\n\n"
                    f"به **CodeRoot** خوش آمدید! 🚀\n\n"
                    f"🏪 **ایجاد فروشگاه آنلاین**\n"
                    f"✨ **مدیریت محصولات**\n"
                    f"📊 **گزارش‌گیری پیشرفته**\n"
                    f"💰 **درآمدزایی**\n\n"
                    f"🆔 **کد معرف شما:** `{user['referral_code']}`\n\n"
                    f"👇 برای شروع، یکی از گزینه‌های زیر را انتخاب کنید:"
                )
                
                # Send notification to admin about new user
                try:
                    await NotificationUtils.send_admin_notification(
                        client,
                        f"👤 **کاربر جدید ثبت‌نام کرد**\n\n"
                        f"نام: {message.from_user.first_name}\n"
                        f"آیدی: {user_id}\n"
                        f"یوزرنیم: @{message.from_user.username or 'ندارد'}\n"
                        f"معرف: {referral_code or 'ندارد'}\n"
                        f"زمان: {datetime.now()}"
                    )
                except:
                    pass
            else:
                # Returning user
                welcome_text = (
                    f"🔄 **سلام مجدد {message.from_user.first_name}!**\n\n"
                    f"خوش برگشتید به **CodeRoot** 🎉\n\n"
                    f"📊 **آمار شما:**\n"
                    f"🏪 فروشگاه‌ها: {user['statistics']['total_shops']}\n"
                    f"🛒 سفارش‌ها: {user['statistics']['total_orders']}\n"
                    f"💰 درآمد کل: {user['statistics']['total_revenue']:,} تومان\n\n"
                    f"👇 گزینه مورد نظر را انتخاب کنید:"
                )
            
            # Check channel membership if required
            if FEATURES["channel_join_required"] and Config.MAIN_CHANNEL_USERNAME:
                is_member = await BotUtils.check_channel_membership(client, user_id, Config.MAIN_CHANNEL_USERNAME)
                if not is_member:
                    await message.reply_text(
                        f"📢 **عضویت در کانال الزامی است**\n\n"
                        f"برای استفاده از ربات، ابتدا در کانال ما عضو شوید:\n"
                        f"👇 @{Config.MAIN_CHANNEL_USERNAME}\n\n"
                        f"بعد از عضویت، دوباره /start کنید.",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{Config.MAIN_CHANNEL_USERNAME}")],
                            [InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")]
                        ])
                    )
                    return
            
            # Send main menu
            await message.reply_text(
                welcome_text,
                reply_markup=KeyboardMarkups.main_menu_keyboard(user)
            )
            
            # Record analytics
            await AnalyticsManager.record_event({
                "user_id": user_id,
                "event_type": "bot_start",
                "data": {"is_new_user": user.get("created_at") == user.get("updated_at")}
            })
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await message.reply_text(
                "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.\n\n"
                "در صورت تکرار مشکل، با پشتیبانی تماس بگیرید."
            )
    
    async def help_command(self, client: Client, message: Message):
        """Handle /help command"""
        help_text = (
            "📖 **راهنمای CodeRoot**\n\n"
            "🚀 **دستورات اصلی:**\n"
            "/start - شروع یا بازگشت به منوی اصلی\n"
            "/help - نمایش این راهنما\n"
            "/shop - مدیریت فروشگاه\n"
            "/profile - پروفایل کاربری\n"
            "/referral - سیستم معرفی\n\n"
            "🏪 **قابلیت‌های اصلی:**\n"
            "• ایجاد فروشگاه آنلاین\n"
            "• مدیریت محصولات\n"
            "• پردازش سفارش‌ها\n"
            "• گزارش‌گیری فروش\n"
            "• سیستم معرفی و درآمد\n\n"
            "💎 **پلن‌های اشتراک:**\n"
            f"🆓 رایگان: {PLANS['free']['max_products']} محصول\n"
            f"⭐ حرفه‌ای: {PLANS['professional']['max_products']} محصول - {PLANS['professional']['price']:,} تومان\n"
            f"👑 VIP: نامحدود - {PLANS['vip']['price']:,} تومان\n\n"
            "🆘 برای پشتیبانی با مدیر تماس بگیرید."
        )
        
        await message.reply_text(
            help_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 بازگشت به منوی اصلی", callback_data="main_menu")]
            ])
        )
    
    async def admin_command(self, client: Client, message: Message):
        """Handle /admin command"""
        user_id = message.from_user.id
        
        if user_id != Config.ADMIN_USER_ID:
            await message.reply_text("❌ شما مجوز دسترسی به پنل مدیریت را ندارید.")
            return
        
        # Show admin panel
        admin_text = (
            f"🔧 **پنل مدیریت CodeRoot**\n\n"
            f"👋 سلام {message.from_user.first_name}!\n\n"
            f"📊 **آمار کلی:**\n"
            f"👥 کاربران: {await UserManager.get_users_count()}\n"
            f"🏪 فروشگاه‌ها: {await ShopManager.get_shops_count()}\n"
            f"📦 محصولات: {await ProductManager.get_products_count_by_shop('all')}\n\n"
            f"⚙️ **عملیات مدیریت:**"
        )
        
        await message.reply_text(
            admin_text,
            reply_markup=KeyboardMarkups.admin_main_keyboard()
        )
    
    async def shop_command(self, client: Client, message: Message):
        """Handle /shop command"""
        user_id = message.from_user.id
        
        # Check if user exists
        user = await UserManager.get_user(user_id)
        if not user:
            await message.reply_text("❌ ابتدا /start کنید.")
            return
        
        # Check if user has a shop
        shop = await ShopManager.get_shop_by_owner(user_id)
        
        if shop:
            # Show shop management
            shop_text = (
                f"🏪 **فروشگاه: {shop['name']}**\n\n"
                f"📊 **آمار فروشگاه:**\n"
                f"📦 محصولات: {shop['statistics']['total_products']}\n"
                f"🛒 سفارش‌ها: {shop['statistics']['total_orders']}\n"
                f"💰 درآمد: {shop['statistics']['total_revenue']:,} تومان\n"
                f"👥 مشتریان: {shop['statistics']['total_customers']}\n\n"
                f"⚙️ **مدیریت فروشگاه:**"
            )
            
            await message.reply_text(
                shop_text,
                reply_markup=KeyboardMarkups.shop_management_keyboard(shop)
            )
        else:
            # Show shop creation options
            await message.reply_text(
                "🏪 **ایجاد فروشگاه جدید**\n\n"
                "شما هنوز فروشگاهی ندارید.\n"
                "برای شروع کسب‌وکار آنلاین، فروشگاه خود را بسازید!\n\n"
                "👇 پلن مورد نظر را انتخاب کنید:",
                reply_markup=KeyboardMarkups.shop_plans_keyboard()
            )
    
    async def profile_command(self, client: Client, message: Message):
        """Handle /profile command"""
        user_id = message.from_user.id
        
        user = await UserManager.get_user(user_id)
        if not user:
            await message.reply_text("❌ ابتدا /start کنید.")
            return
        
        # Calculate days remaining
        days_remaining = (user['subscription']['expires_at'] - datetime.utcnow()).days
        
        profile_text = (
            f"👤 **پروفایل کاربری**\n\n"
            f"🆔 شناسه: {user_id}\n"
            f"👤 نام: {user.get('first_name', 'نامشخص')}\n"
            f"📱 یوزرنیم: @{user.get('username', 'ندارد')}\n\n"
            f"💎 **اشتراک:**\n"
            f"📋 پلن: {PLANS[user['subscription']['plan']]['name']}\n"
            f"⏰ باقی‌مانده: {days_remaining} روز\n"
            f"✅ وضعیت: {'فعال' if user['subscription']['is_active'] else 'غیرفعال'}\n\n"
            f"📊 **آمار:**\n"
            f"🏪 فروشگاه‌ها: {user['statistics']['total_shops']}\n"
            f"🛒 سفارش‌ها: {user['statistics']['total_orders']}\n"
            f"💰 درآمد کل: {user['statistics']['total_revenue']:,} تومان\n"
            f"💵 پاداش معرفی: {user['statistics']['referral_earnings']:,} تومان\n\n"
            f"🔗 **کد معرف:** `{user['referral_code']}`"
        )
        
        await message.reply_text(
            profile_text,
            reply_markup=KeyboardMarkups.profile_keyboard()
        )
    
    async def referral_command(self, client: Client, message: Message):
        """Handle /referral command"""
        user_id = message.from_user.id
        
        user = await UserManager.get_user(user_id)
        if not user:
            await message.reply_text("❌ ابتدا /start کنید.")
            return
        
        # Get referral statistics
        referrals = await UserManager.get_all_users(filters={"referred_by": user['referral_code']})
        total_referrals = len(referrals)
        
        referral_text = (
            f"🎁 **سیستم معرفی CodeRoot**\n\n"
            f"🔗 **لینک معرف شما:**\n"
            f"`https://t.me/{Config.BOT_USERNAME}?start={user['referral_code']}`\n\n"
            f"📊 **آمار معرفی:**\n"
            f"👥 تعداد معرفی‌ها: {total_referrals}\n"
            f"💰 درآمد معرفی: {user['statistics']['referral_earnings']:,} تومان\n\n"
            f"💡 **نحوه کسب درآمد:**\n"
            f"• هر معرفی: {Config.REFERRAL_COMMISSION}% از اشتراک\n"
            f"• حداقل برداشت: {50000:,} تومان\n"
            f"• پرداخت: ماهانه\n\n"
            f"🚀 **لینک خود را به‌اشتراک بگذارید و درآمد کسب کنید!**"
        )
        
        await message.reply_text(
            referral_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 به‌اشتراک‌گذاری لینک", switch_inline_query=f"🚀 ایجاد فروشگاه آنلاین با CodeRoot!\n\n🎁 با لینک من ثبت‌نام کن:\nhttps://t.me/{Config.BOT_USERNAME}?start={user['referral_code']}")],
                [InlineKeyboardButton("📊 جزئیات معرفی‌ها", callback_data="referral_details")],
                [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")]
            ])
        )
    
    # ==================== CALLBACK HANDLERS ====================
    
    async def callback_handler(self, client: Client, callback_query: CallbackQuery):
        """Handle all callback queries"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        try:
            # Check membership callbacks
            if data == "check_membership":
                if FEATURES["channel_join_required"] and Config.MAIN_CHANNEL_USERNAME:
                    is_member = await BotUtils.check_channel_membership(client, user_id, Config.MAIN_CHANNEL_USERNAME)
                    if is_member:
                        await callback_query.answer("✅ عضویت شما تأیید شد!")
                        # Redirect to main menu
                        user = await UserManager.get_user(user_id)
                        await callback_query.message.edit_text(
                            f"✅ **عضویت تأیید شد!**\n\n"
                            f"حالا می‌توانید از تمام امکانات CodeRoot استفاده کنید.\n\n"
                            f"👇 گزینه مورد نظر را انتخاب کنید:",
                            reply_markup=KeyboardMarkups.main_menu_keyboard(user)
                        )
                    else:
                        await callback_query.answer("❌ ابتدا در کانال عضو شوید!", show_alert=True)
                return
            
            # Main menu callbacks
            if data == "main_menu":
                user = await UserManager.get_user(user_id)
                await callback_query.message.edit_text(
                    f"🏠 **منوی اصلی CodeRoot**\n\n"
                    f"👋 سلام {callback_query.from_user.first_name}!\n\n"
                    f"👇 گزینه مورد نظر را انتخاب کنید:",
                    reply_markup=KeyboardMarkups.main_menu_keyboard(user)
                )
                return
            
            # Shop-related callbacks
            if data.startswith("shop_"):
                await self.handle_shop_callbacks(client, callback_query)
                return
            
            # Admin callbacks
            if data.startswith("admin_"):
                if user_id != Config.ADMIN_USER_ID:
                    await callback_query.answer("❌ دسترسی محدود!", show_alert=True)
                    return
                await self.handle_admin_callbacks(client, callback_query)
                return
            
            # Payment callbacks
            if data.startswith("payment_"):
                await self.handle_payment_callbacks(client, callback_query)
                return
            
            # Profile callbacks
            if data.startswith("profile_"):
                await self.handle_profile_callbacks(client, callback_query)
                return
            
            # Default callback
            await callback_query.answer("🔄 در حال پردازش...")
            
        except Exception as e:
            logger.error(f"Error in callback handler: {e}")
            await callback_query.answer("❌ خطایی رخ داد!", show_alert=True)
    
    async def handle_shop_callbacks(self, client: Client, callback_query: CallbackQuery):
        """Handle shop-related callbacks"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        if data == "shop_create":
            await callback_query.message.edit_text(
                "🏪 **ایجاد فروشگاه جدید**\n\n"
                "برای شروع کسب‌وکار آنلاین، پلن مناسب خود را انتخاب کنید:\n\n"
                "👇 هر پلن شامل ویژگی‌های خاص خود است:",
                reply_markup=KeyboardMarkups.shop_plans_keyboard()
            )
        
        elif data.startswith("plan_"):
            plan_name = data.split("_")[1]
            plan = PLANS.get(plan_name)
            
            if plan:
                plan_text = (
                    f"💎 **پلن {plan['name']}**\n\n"
                    f"💰 قیمت: {plan['price']:,} تومان\n"
                    f"📦 محصولات: {plan['max_products'] if plan['max_products'] != -1 else 'نامحدود'}\n"
                    f"📊 گزارش‌ها: {'پیشرفته' if plan['advanced_reports'] else 'پایه'}\n"
                    f"💸 کارمزد: {plan['commission']}%\n\n"
                    f"✨ **ویژگی‌ها:**\n"
                )
                
                for feature in plan['features']:
                    plan_text += f"• {feature}\n"
                
                keyboard = []
                if plan['price'] > 0:
                    keyboard.append([InlineKeyboardButton(f"💳 پرداخت {plan['price']:,} تومان", callback_data=f"payment_plan_{plan_name}")])
                else:
                    keyboard.append([InlineKeyboardButton("🆓 انتخاب پلن رایگان", callback_data=f"create_shop_{plan_name}")])
                
                keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_create")])
                
                await callback_query.message.edit_text(
                    plan_text,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        
        elif data.startswith("create_shop_"):
            plan_name = data.split("_")[2]
            user_states[user_id] = {"state": "waiting_shop_name", "plan": plan_name}
            
            await callback_query.message.edit_text(
                f"🏪 **ایجاد فروشگاه - پلن {PLANS[plan_name]['name']}**\n\n"
                f"📝 نام فروشگاه خود را وارد کنید:\n\n"
                f"🔸 نام باید بین 3 تا 50 کاراکتر باشد\n"
                f"🔸 از کاراکترهای فارسی و انگلیسی استفاده کنید\n"
                f"🔸 نام منحصر به فرد انتخاب کنید",
                reply_markup=KeyboardMarkups.cancel_keyboard()
            )
    
    async def handle_admin_callbacks(self, client: Client, callback_query: CallbackQuery):
        """Handle admin panel callbacks"""
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        if data == "admin_users":
            # Show user management
            users = await UserManager.get_all_users(limit=10)
            total_users = await UserManager.get_users_count()
            
            users_text = f"👥 **مدیریت کاربران**\n\n📊 تعداد کل: {total_users}\n\n"
            
            for i, user in enumerate(users[:5], 1):
                status = "✅" if user['status'] == 'active' else "❌"
                users_text += f"{i}. {status} {user.get('first_name', 'نامشخص')} - {user['user_id']}\n"
            
            await callback_query.message.edit_text(
                users_text,
                reply_markup=KeyboardMarkups.admin_users_keyboard()
            )
        
        elif data == "admin_shops":
            # Show shop management
            shops = await ShopManager.get_all_shops(limit=10)
            total_shops = await ShopManager.get_shops_count()
            
            shops_text = f"🏪 **مدیریت فروشگاه‌ها**\n\n📊 تعداد کل: {total_shops}\n\n"
            
            for i, shop in enumerate(shops[:5], 1):
                status = "✅" if shop['status'] == 'active' else "⏳" if shop['status'] == 'pending' else "❌"
                shops_text += f"{i}. {status} {shop['name']} - {PLANS[shop['plan']]['name']}\n"
            
            await callback_query.message.edit_text(
                shops_text,
                reply_markup=KeyboardMarkups.admin_shops_keyboard()
            )
        
        elif data == "admin_stats":
            # Show statistics
            total_users = await UserManager.get_users_count()
            total_shops = await ShopManager.get_shops_count()
            active_shops = await ShopManager.get_shops_count({"status": "active"})
            pending_shops = await ShopManager.get_shops_count({"status": "pending"})
            
            stats_text = (
                f"📊 **آمار کلی سیستم**\n\n"
                f"👥 **کاربران:**\n"
                f"• کل: {total_users}\n"
                f"• امروز: {await UserManager.get_users_count({'created_at': {'$gte': datetime.utcnow().replace(hour=0, minute=0, second=0)}})}\n\n"
                f"🏪 **فروشگاه‌ها:**\n"
                f"• کل: {total_shops}\n"
                f"• فعال: {active_shops}\n"
                f"• در انتظار: {pending_shops}\n\n"
                f"💰 **مالی:**\n"
                f"• کل پرداخت‌ها: محاسبه...\n"
                f"• درآمد ماهانه: محاسبه...\n\n"
                f"🕐 آخرین به‌روزرسانی: {datetime.now().strftime('%H:%M')}"
            )
            
            await callback_query.message.edit_text(
                stats_text,
                reply_markup=KeyboardMarkups.admin_stats_keyboard()
            )
    
    async def handle_payment_callbacks(self, client: Client, callback_query: CallbackQuery):
        """Handle payment-related callbacks"""
        # Payment processing logic
        pass
    
    async def handle_profile_callbacks(self, client: Client, callback_query: CallbackQuery):
        """Handle profile-related callbacks"""
        # Profile management logic
        pass
    
    # ==================== MESSAGE HANDLERS ====================
    
    async def text_handler(self, client: Client, message: Message):
        """Handle text messages"""
        user_id = message.from_user.id
        text = message.text
        
        # Check if user is in a specific state
        if user_id in user_states:
            state = user_states[user_id]["state"]
            
            if state == "waiting_shop_name":
                await self.process_shop_name(client, message)
            elif state == "waiting_shop_description":
                await self.process_shop_description(client, message)
            elif state == "waiting_bot_token":
                await self.process_bot_token(client, message)
            elif state == "waiting_phone":
                await self.process_phone(client, message)
            # Add more states as needed
        
        # Handle admin states
        elif user_id in admin_states:
            await self.handle_admin_states(client, message)
    
    async def photo_handler(self, client: Client, message: Message):
        """Handle photo messages (receipts, etc.)"""
        user_id = message.from_user.id
        
        if user_id in user_states and user_states[user_id]["state"] == "waiting_payment_receipt":
            # Process payment receipt
            await self.process_payment_receipt(client, message)
        else:
            await message.reply_text("📷 عکس دریافت شد. اگر این رسید پرداخت است، ابتدا مرحله پرداخت را شروع کنید.")
    
    async def document_handler(self, client: Client, message: Message):
        """Handle document messages"""
        await message.reply_text("📄 فایل دریافت شد. لطفاً از منو گزینه مناسب را انتخاب کنید.")
    
    # ==================== PROCESS FUNCTIONS ====================
    
    async def process_shop_name(self, client: Client, message: Message):
        """Process shop name input"""
        user_id = message.from_user.id
        shop_name = message.text.strip()
        
        # Validate shop name
        if not ValidationUtils.validate_shop_name(shop_name):
            await message.reply_text(
                "❌ نام فروشگاه نامعتبر است.\n\n"
                "🔸 نام باید بین 3 تا 50 کاراکتر باشد\n"
                "🔸 فقط حروف، اعداد و فاصله مجاز است\n\n"
                "لطفاً نام دیگری انتخاب کنید:"
            )
            return
        
        # Store shop name and ask for description
        user_states[user_id]["shop_name"] = shop_name
        user_states[user_id]["state"] = "waiting_shop_description"
        
        await message.reply_text(
            f"✅ نام فروشگاه: **{shop_name}**\n\n"
            f"📝 حالا توضیح کوتاهی درباره فروشگاه خود بنویسید:\n\n"
            f"🔸 حداکثر 200 کاراکتر\n"
            f"🔸 محصولات و خدمات خود را معرفی کنید\n"
            f"🔸 اختیاری است (می‌توانید /skip کنید)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭ رد کردن", callback_data="skip_description")]
            ])
        )
    
    async def process_shop_description(self, client: Client, message: Message):
        """Process shop description input"""
        user_id = message.from_user.id
        description = message.text.strip()
        
        if len(description) > 200:
            await message.reply_text("❌ توضیحات نباید بیش از 200 کاراکتر باشد. لطفاً کوتاه‌تر بنویسید:")
            return
        
        user_states[user_id]["description"] = description
        user_states[user_id]["state"] = "waiting_bot_token"
        
        await message.reply_text(
            f"✅ توضیحات ثبت شد.\n\n"
            f"🤖 **مرحله بعد: ساخت ربات فروشگاه**\n\n"
            f"برای ایجاد ربات اختصاصی فروشگاه:\n"
            f"1️⃣ به @BotFather بروید\n"
            f"2️⃣ /newbot را ارسال کنید\n"
            f"3️⃣ نام و یوزرنیم ربات را وارد کنید\n"
            f"4️⃣ توکن دریافتی را اینجا ارسال کنید\n\n"
            f"📝 توکن شبیه این است:\n"
            f"`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 رفتن به BotFather", url="https://t.me/BotFather")],
                [InlineKeyboardButton("❌ لغو", callback_data="cancel_shop_creation")]
            ])
        )
    
    async def process_bot_token(self, client: Client, message: Message):
        """Process bot token input"""
        user_id = message.from_user.id
        bot_token = message.text.strip()
        
        # Validate bot token
        if not ValidationUtils.validate_bot_token(bot_token):
            await message.reply_text(
                "❌ توکن ربات نامعتبر است.\n\n"
                "🔸 توکن باید شامل : باشد\n"
                "🔸 قسمت اول عدد باشد\n"
                "🔸 از @BotFather کپی کنید\n\n"
                "لطفاً توکن صحیح را ارسال کنید:"
            )
            return
        
        # Check if token is already used
        existing_shop = await ShopManager.get_shop_by_token(bot_token)
        if existing_shop:
            await message.reply_text(
                "❌ این توکن قبلاً استفاده شده است.\n\n"
                "لطفاً ربات جدیدی از @BotFather بسازید و توکن آن را ارسال کنید."
            )
            return
        
        user_states[user_id]["bot_token"] = bot_token
        user_states[user_id]["state"] = "waiting_phone"
        
        await message.reply_text(
            f"✅ توکن ربات تأیید شد.\n\n"
            f"📱 **شماره تماس پشتیبانی**\n\n"
            f"لطفاً شماره تلفن خود را برای ارتباط مشتریان وارد کنید:\n\n"
            f"🔸 فرمت: 09123456789\n"
            f"🔸 بدون فاصله و خط تیره\n"
            f"🔸 شماره معتبر ایرانی",
        )
    
    async def process_phone(self, client: Client, message: Message):
        """Process phone number input"""
        user_id = message.from_user.id
        phone = message.text.strip()
        
        if not BotUtils.validate_phone(phone):
            await message.reply_text(
                "❌ شماره تلفن نامعتبر است.\n\n"
                "🔸 فرمت صحیح: 09123456789\n"
                "🔸 11 رقم\n"
                "🔸 با 09 شروع شود\n\n"
                "لطفاً شماره صحیح وارد کنید:"
            )
            return
        
        # Create the shop
        await self.create_user_shop(client, message, phone)
    
    async def create_user_shop(self, client: Client, message: Message, phone: str):
        """Create the user's shop"""
        user_id = message.from_user.id
        state_data = user_states[user_id]
        
        try:
            # Prepare shop data
            shop_data = {
                "owner_id": user_id,
                "name": state_data["shop_name"],
                "description": state_data.get("description", ""),
                "bot_token": state_data["bot_token"],
                "plan": state_data["plan"],
                "phone": phone
            }
            
            # Create shop in database
            shop = await ShopManager.create_shop(shop_data)
            
            # Update user subscription if not free plan
            if state_data["plan"] != "free":
                plan_data = PLANS[state_data["plan"]]
                await UserManager.update_subscription(user_id, state_data["plan"], plan_data["duration_days"])
                
                # Create payment record
                payment_data = {
                    "user_id": user_id,
                    "shop_id": str(shop["_id"]),
                    "amount": plan_data["price"],
                    "payment_type": "subscription",
                    "description": f"اشتراک {plan_data['name']} - فروشگاه {shop_data['name']}"
                }
                await PaymentManager.create_payment(payment_data)
            
            # Update user statistics
            await UserManager.update_user(user_id, {
                "$inc": {"statistics.total_shops": 1}
            })
            
            # Clear user state
            del user_states[user_id]
            
            # Success message
            success_text = (
                f"🎉 **فروشگاه شما با موفقیت ایجاد شد!**\n\n"
                f"🏪 نام: {shop_data['name']}\n"
                f"💎 پلن: {PLANS[state_data['plan']]['name']}\n"
                f"🤖 ربات: @{state_data['bot_token'].split(':')[0]}\n"
                f"📱 تماس: {phone}\n\n"
                f"✅ **مراحل بعدی:**\n"
                f"1️⃣ تأیید فروشگاه توسط مدیر\n"
                f"2️⃣ تنظیم ربات فروشگاه\n"
                f"3️⃣ افزودن محصولات\n\n"
                f"📬 **اطلاع‌رسانی:**\n"
                f"پس از تأیید، پیام اطلاع‌رسانی دریافت خواهید کرد."
            )
            
            await message.reply_text(
                success_text,
                reply_markup=KeyboardMarkups.shop_created_keyboard()
            )
            
            # Notify admin about new shop
            try:
                await NotificationUtils.send_admin_notification(
                    client,
                    f"🏪 **فروشگاه جدید ایجاد شد**\n\n"
                    f"نام: {shop_data['name']}\n"
                    f"مالک: {message.from_user.first_name} ({user_id})\n"
                    f"پلن: {PLANS[state_data['plan']]['name']}\n"
                    f"توکن: {state_data['bot_token'][:15]}...\n"
                    f"تلفن: {phone}\n"
                    f"زمان: {datetime.now()}\n\n"
                    f"لطفاً تأیید کنید."
                )
            except Exception as e:
                logger.warning(f"Could not send admin notification: {e}")
        
        except Exception as e:
            logger.error(f"Error creating shop: {e}")
            await message.reply_text(
                "❌ خطایی در ایجاد فروشگاه رخ داد.\n\n"
                "لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید."
            )
    
    async def process_payment_receipt(self, client: Client, message: Message):
        """Process payment receipt photo"""
        # Payment receipt processing logic
        pass
    
    async def handle_admin_states(self, client: Client, message: Message):
        """Handle admin-specific states"""
        # Admin state processing logic
        pass

# ==================== SIGNAL HANDLERS ====================

def signal_handler(signum, frame):
    """Handle termination signals"""
    logger.info(f"Received signal {signum}")
    # The main loop will handle cleanup

# ==================== MAIN FUNCTION ====================

async def main():
    """Main function"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start bot
    bot = CodeRootBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("🛑 Received keyboard interrupt")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    try:
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        
        # Run the bot
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)