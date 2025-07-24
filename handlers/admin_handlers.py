import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Use mock database for demo
try:
    from database_mock import UserManager, ShopManager, ProductManager, OrderManager, PaymentManager
except ImportError:
    from database import UserManager, ShopManager, ProductManager, OrderManager, PaymentManager

from utils import (
    BotUtils, MessageTemplates, KeyboardMarkups, ValidationUtils, 
    SecurityUtils, NotificationUtils, TimeUtils, ExcelGenerator
)
from config import Config, PLANS

logger = logging.getLogger(__name__)

# Admin states for conversation flow
admin_states = {}

class AdminHandlers:
    """Admin-related message and callback handlers"""
    
    @staticmethod
    async def admin_panel_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin panel callback"""
        try:
            user_id = callback_query.from_user.id
            
            # Check if user is admin
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ شما دسترسی مدیریت ندارید!", show_alert=True)
                return
            
            # Get statistics
            users_count = await UserManager.get_users_count()
            shops_count = await ShopManager.get_shops_count()
            
            admin_text = f"""
🔧 پنل مدیریت CodeRoot (دمو)

📊 آمار کلی:
👥 کاربران: {users_count:,}
🏪 فروشگاه‌ها: {shops_count:,}

🎭 حالت دمو: داده‌ها شبیه‌سازی شده
📅 آخرین بروزرسانی: {BotUtils.format_date(datetime.utcnow())}
            """
            
            keyboard = KeyboardMarkups.admin_menu()
            await callback_query.message.edit_text(admin_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in admin panel: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_users_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin users management callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 لیست کاربران", callback_data="admin_users_list"),
                 InlineKeyboardButton("🔍 جستجوی کاربر", callback_data="admin_user_search")],
                [InlineKeyboardButton("📊 گزارش کاربران", callback_data="admin_users_report"),
                 InlineKeyboardButton("📤 ارسال پیام", callback_data="admin_send_message")],
                [InlineKeyboardButton("🔄 بازگشت", callback_data="admin_panel")]
            ])
            
            await callback_query.message.edit_text(
                "👥 مدیریت کاربران (دمو):\n\nلطفاً گزینه مورد نظر را انتخاب کنید:",
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in admin users: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_users_list_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin users list callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            # Get users with pagination
            page = 1
            if ":" in callback_query.data:
                page = int(callback_query.data.split(":")[1])
            
            limit = 10
            skip = (page - 1) * limit
            
            users = await UserManager.get_all_users(skip=skip, limit=limit)
            total_users = await UserManager.get_users_count()
            total_pages = max(1, (total_users + limit - 1) // limit)
            
            # Create demo data if no users exist
            if not users and total_users == 0:
                demo_users_text = f"👥 لیست کاربران دمو (صفحه {page} از 1):\n\n"
                demo_users_text += "1. کاربر دمو\n"
                demo_users_text += "   🆔 123456789\n"
                demo_users_text += "   📊 حرفه‌ای\n"
                demo_users_text += "   📅 امروز\n\n"
                demo_users_text += "🎭 در نسخه دمو داده‌های شبیه‌سازی شده نمایش داده می‌شوند."
            else:
                users_text = f"👥 لیست کاربران (صفحه {page} از {total_pages}):\n\n"
                
                for i, user in enumerate(users, 1):
                    subscription = user.get('subscription', {})
                    plan_name = PLANS.get(subscription.get('plan', 'free'), {}).get('name', 'نامشخص')
                    
                    users_text += f"{skip + i}. {user.get('first_name', 'نامشخص')}\n"
                    users_text += f"   🆔 {user['user_id']}\n"
                    users_text += f"   📊 {plan_name}\n"
                    users_text += f"   📅 {BotUtils.format_date(user.get('created_at', datetime.utcnow()))}\n\n"
                
                demo_users_text = users_text
            
            # Create pagination keyboard
            keyboard = []
            
            # Navigation buttons
            nav_row = []
            if page > 1:
                nav_row.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"admin_users_list:{page-1}"))
            
            nav_row.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="page_info"))
            
            if page < total_pages:
                nav_row.append(InlineKeyboardButton("بعدی ➡️", callback_data=f"admin_users_list:{page+1}"))
            
            if nav_row:
                keyboard.append(nav_row)
            
            # Back button
            keyboard.append([InlineKeyboardButton("🔄 بازگشت", callback_data="admin_users")])
            
            await callback_query.message.edit_text(
                demo_users_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
        except Exception as e:
            logger.error(f"Error in admin users list: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_shops_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin shops management callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🏪 لیست فروشگاه‌ها", callback_data="admin_shops_list"),
                 InlineKeyboardButton("⏳ در انتظار تأیید", callback_data="admin_shops_pending")],
                [InlineKeyboardButton("✅ تأیید فروشگاه", callback_data="admin_shop_approve"),
                 InlineKeyboardButton("❌ حذف فروشگاه", callback_data="admin_shop_delete")],
                [InlineKeyboardButton("📊 گزارش فروشگاه‌ها", callback_data="admin_shops_report")],
                [InlineKeyboardButton("🔄 بازگشت", callback_data="admin_panel")]
            ])
            
            await callback_query.message.edit_text(
                "🏪 مدیریت فروشگاه‌ها (دمو):\n\nلطفاً گزینه مورد نظر را انتخاب کنید:",
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in admin shops: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_shops_list_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin shops list callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            # Get shops with pagination
            page = 1
            if ":" in callback_query.data:
                page = int(callback_query.data.split(":")[1])
            
            limit = 10
            skip = (page - 1) * limit
            
            shops = await ShopManager.get_all_shops(skip=skip, limit=limit)
            total_shops = await ShopManager.get_shops_count()
            total_pages = max(1, (total_shops + limit - 1) // limit)
            
            # Create demo data if no shops exist
            if not shops and total_shops == 0:
                demo_shops_text = f"🏪 لیست فروشگاه‌ها دمو (صفحه {page} از 1):\n\n"
                demo_shops_text += "1. فروشگاه دمو\n"
                demo_shops_text += "   👤 مالک: 123456789\n"
                demo_shops_text += "   📊 پلن: حرفه‌ای\n"
                demo_shops_text += "   🔄 وضعیت: ✅ فعال\n"
                demo_shops_text += "   📅 امروز\n\n"
                demo_shops_text += "🎭 در نسخه دمو داده‌های شبیه‌سازی شده نمایش داده می‌شوند."
            else:
                shops_text = f"🏪 لیست فروشگاه‌ها (صفحه {page} از {total_pages}):\n\n"
                
                for i, shop in enumerate(shops, 1):
                    status_emoji = "✅" if shop.get('status') == 'active' else "⏳" if shop.get('status') == 'pending' else "❌"
                    
                    shops_text += f"{skip + i}. {shop.get('name', 'نامشخص')}\n"
                    shops_text += f"   👤 مالک: {shop['owner_id']}\n"
                    shops_text += f"   📊 پلن: {PLANS.get(shop.get('plan', 'free'), {}).get('name', 'نامشخص')}\n"
                    shops_text += f"   🔄 وضعیت: {status_emoji} {shop.get('status', 'نامشخص')}\n"
                    shops_text += f"   📅 {BotUtils.format_date(shop.get('created_at', datetime.utcnow()))}\n\n"
                
                demo_shops_text = shops_text
            
            # Create pagination keyboard
            keyboard = []
            
            # Navigation buttons
            nav_row = []
            if page > 1:
                nav_row.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"admin_shops_list:{page-1}"))
            
            nav_row.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="page_info"))
            
            if page < total_pages:
                nav_row.append(InlineKeyboardButton("بعدی ➡️", callback_data=f"admin_shops_list:{page+1}"))
            
            if nav_row:
                keyboard.append(nav_row)
            
            # Back button
            keyboard.append([InlineKeyboardButton("🔄 بازگشت", callback_data="admin_shops")])
            
            await callback_query.message.edit_text(
                demo_shops_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
        except Exception as e:
            logger.error(f"Error in admin shops list: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_finance_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin finance callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            # Demo finance data
            demo_finance_text = """
💰 مدیریت مالی (دمو)

📊 آمار مالی نمونه:
💳 پرداخت‌های امروز: 5 پرداخت
💰 درآمد امروز: 250,000 تومان
📈 درآمد ماهانه: 5,500,000 تومان
📊 کل درآمد: 12,750,000 تومان

🎭 داده‌های بالا شبیه‌سازی شده برای نمایش هستند.

💡 در نسخه اصلی:
• گزارش‌های دقیق مالی
• خروجی Excel
• نمودارهای تحلیلی
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 پرداخت‌های امروز", callback_data="admin_finance_today"),
                 InlineKeyboardButton("📊 گزارش ماهانه", callback_data="admin_finance_monthly")],
                [InlineKeyboardButton("💰 کل درآمد", callback_data="admin_finance_total"),
                 InlineKeyboardButton("📈 نمودار فروش", callback_data="admin_finance_chart")],
                [InlineKeyboardButton("📤 خروجی اکسل", callback_data="admin_finance_excel")],
                [InlineKeyboardButton("🔄 بازگشت", callback_data="admin_panel")]
            ])
            
            await callback_query.message.edit_text(demo_finance_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in admin finance: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_broadcast_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin broadcast callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            await callback_query.message.edit_text(
                "📢 ارسال پیام همگانی (دمو):\n\nپیام خود را تایپ کنید:\n\n🎭 در نسخه دمو، پیام فقط به شما ارسال می‌شود",
                reply_markup=KeyboardMarkups.cancel_keyboard()
            )
            
            # Set admin state
            if user_id not in admin_states:
                admin_states[user_id] = {}
            admin_states[user_id]['state'] = 'waiting_broadcast_message'
            
        except Exception as e:
            logger.error(f"Error in admin broadcast: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def handle_admin_text_messages(client: Client, message: Message):
        """Handle admin text messages based on state"""
        try:
            user_id = message.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                return
            
            if user_id not in admin_states:
                return
            
            state = admin_states[user_id].get('state')
            
            if state == 'waiting_broadcast_message':
                await AdminHandlers.handle_broadcast_message(client, message)
                
        except Exception as e:
            logger.error(f"Error handling admin text message: {e}")
    
    @staticmethod
    async def handle_broadcast_message(client: Client, message: Message):
        """Handle broadcast message"""
        try:
            user_id = message.from_user.id
            broadcast_text = SecurityUtils.sanitize_input(message.text)
            
            if len(broadcast_text) < 10:
                await message.reply_text(
                    "❌ پیام باید حداقل 10 کاراکتر باشد!\n\n🔄 دوباره تلاش کنید:",
                    reply_markup=KeyboardMarkups.cancel_keyboard()
                )
                return
            
            # Show confirmation
            confirmation_text = f"📢 پیش‌نمایش پیام همگانی (دمو):\n\n{broadcast_text}\n\n❓ آیا مطمئن هستید؟\n\n🎭 در دمو فقط به شما ارسال می‌شود"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ ارسال", callback_data="confirm_broadcast"),
                 InlineKeyboardButton("❌ لغو", callback_data="cancel_admin")]
            ])
            
            admin_states[user_id]['broadcast_message'] = broadcast_text
            
            await message.reply_text(confirmation_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error handling broadcast message: {e}")
    
    @staticmethod
    async def confirm_broadcast_callback(client: Client, callback_query: CallbackQuery):
        """Handle confirm broadcast callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            broadcast_message = admin_states.get(user_id, {}).get('broadcast_message')
            if not broadcast_message:
                await callback_query.answer("❌ پیام یافت نشد!", show_alert=True)
                return
            
            await callback_query.message.edit_text("📤 در حال ارسال پیام دمو...")
            
            # In demo mode, only send to admin
            try:
                await client.send_message(user_id, f"🎭 پیام دمو:\n\n{broadcast_message}")
                sent_count = 1
                failed_count = 0
            except Exception as e:
                sent_count = 0
                failed_count = 1
                logger.error(f"Failed to send demo message: {e}")
            
            # Clear admin state
            if user_id in admin_states:
                del admin_states[user_id]
            
            result_text = f"📊 نتیجه ارسال پیام دمو:\n\n✅ موفق: {sent_count}\n❌ ناموفق: {failed_count}\n\n🎭 در نسخه دمو فقط به مدیر ارسال شد\n📅 {BotUtils.format_date(datetime.utcnow())}"
            
            keyboard = KeyboardMarkups.admin_menu()
            await callback_query.message.edit_text(result_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error confirming broadcast: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_stats_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin statistics callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            # Get statistics
            users_count = await UserManager.get_users_count()
            shops_count = await ShopManager.get_shops_count()
            
            # Demo plan stats
            plan_stats = {'free': 15, 'professional': 8, 'vip': 3}
            
            stats_text = f"""
📊 آمار کامل سیستم (دمو)

👥 کاربران:
• کل: {users_count + 26:,}
• رایگان: {plan_stats['free']:,}
• حرفه‌ای: {plan_stats['professional']:,}
• VIP: {plan_stats['vip']:,}

🏪 فروشگاه‌ها:
• کل: {shops_count + 12:,}
• فعال: {shops_count + 10:,}
• معلق: 2

💰 مالی:
• درآمد ماهانه: 5,500,000 تومان
• کل درآمد: 12,750,000 تومان

🎭 داده‌های بالا نمونه برای دمو هستند
📅 آخرین بروزرسانی: {BotUtils.format_date(datetime.utcnow())}
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 بروزرسانی", callback_data="admin_stats")],
                [InlineKeyboardButton("🔄 بازگشت", callback_data="admin_panel")]
            ])
            
            await callback_query.message.edit_text(stats_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in admin stats: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def admin_users_report_callback(client: Client, callback_query: CallbackQuery):
        """Handle admin users report callback"""
        try:
            user_id = callback_query.from_user.id
            
            if not await SecurityUtils.is_user_admin(user_id):
                await callback_query.answer("❌ دسترسی مجاز نیست!", show_alert=True)
                return
            
            await callback_query.message.edit_text("📊 در حال تهیه گزارش دمو...")
            
            # Demo report
            demo_report = """
📊 گزارش کاربران (نسخه دمو)

🎭 این نسخه دمو است و گزارش واقعی ایجاد نمی‌شود.

💡 در نسخه اصلی:
• گزارش کامل کاربران در Excel
• اطلاعات جزئی هر کاربر
• آمار اشتراک‌ها و درآمدها
• قابلیت فیلتر و جستجو

📈 نمونه داده‌ها:
• کل کاربران: 26 نفر
• کاربران فعال: 24 نفر
• اشتراک‌های پولی: 11 نفر
• میانگین درآمد ماهانه: 450,000 تومان
            """
            
            await callback_query.message.edit_text(
                demo_report,
                reply_markup=KeyboardMarkups.back_keyboard("admin_users")
            )
            
        except Exception as e:
            logger.error(f"Error in admin users report: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def cancel_admin_callback(client: Client, callback_query: CallbackQuery):
        """Handle cancel admin callback"""
        try:
            user_id = callback_query.from_user.id
            
            # Clear admin state
            if user_id in admin_states:
                del admin_states[user_id]
            
            # Return to admin panel
            await AdminHandlers.admin_panel_callback(client, callback_query)
            
        except Exception as e:
            logger.error(f"Error in cancel admin: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")