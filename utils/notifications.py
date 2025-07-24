"""
Notification utilities for CodeRoot Bot
ابزارهای اطلاع‌رسانی ربات CodeRoot
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config, NOTIFICATION_TEMPLATES

logger = logging.getLogger(__name__)


class NotificationUtils:
    """Notification utilities class"""
    
    @staticmethod
    async def send_admin_notification(client: Client, message: str, keyboard: Optional[InlineKeyboardMarkup] = None) -> bool:
        """Send notification to admin"""
        try:
            await client.send_message(
                Config.ADMIN_USER_ID,
                f"🔔 **اطلاع‌رسانی مدیریت**\n\n{message}\n\n🕐 {datetime.now().strftime('%Y/%m/%d %H:%M')}",
                reply_markup=keyboard
            )
            return True
        except Exception as e:
            logger.error(f"Error sending admin notification: {e}")
            return False
    
    @staticmethod
    async def send_user_notification(client: Client, user_id: int, template_key: str, **kwargs) -> bool:
        """Send templated notification to user"""
        try:
            template = NOTIFICATION_TEMPLATES.get(template_key)
            if not template:
                logger.error(f"Notification template '{template_key}' not found")
                return False
            
            message = template.format(**kwargs)
            await client.send_message(user_id, message)
            return True
        except Exception as e:
            logger.error(f"Error sending user notification to {user_id}: {e}")
            return False
    
    @staticmethod
    async def notify_new_user(client: Client, user_data: Dict) -> bool:
        """Notify admin about new user registration"""
        try:
            message = (
                f"👤 **کاربر جدید ثبت‌نام کرد**\n\n"
                f"🆔 شناسه: {user_data.get('user_id')}\n"
                f"👤 نام: {user_data.get('first_name', 'نامشخص')}\n"
                f"📱 یوزرنیم: @{user_data.get('username', 'ندارد')}\n"
                f"🎁 معرف: {user_data.get('referred_by', 'ندارد')}\n"
                f"🕐 زمان: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👤 مشاهده پروفایل", callback_data=f"view_user_{user_data.get('user_id')}")],
                [InlineKeyboardButton("👥 مدیریت کاربران", callback_data="admin_users")]
            ])
            
            return await NotificationUtils.send_admin_notification(client, message, keyboard)
        except Exception as e:
            logger.error(f"Error notifying new user: {e}")
            return False
    
    @staticmethod
    async def notify_new_shop(client: Client, shop_data: Dict, user_data: Dict) -> bool:
        """Notify admin about new shop creation"""
        try:
            message = (
                f"🏪 **فروشگاه جدید ایجاد شد**\n\n"
                f"📛 نام فروشگاه: {shop_data.get('name')}\n"
                f"👤 مالک: {user_data.get('first_name')} ({user_data.get('user_id')})\n"
                f"💎 پلن: {shop_data.get('plan', 'free')}\n"
                f"🤖 توکن: {shop_data.get('bot_token', '')[:15]}...\n"
                f"📱 تلفن: {shop_data.get('phone', 'ندارد')}\n"
                f"📝 توضیحات: {shop_data.get('description', 'ندارد')[:50]}...\n"
                f"🕐 زمان: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ تأیید فروشگاه", callback_data=f"approve_shop_{shop_data.get('_id')}")],
                [InlineKeyboardButton("❌ رد کردن", callback_data=f"reject_shop_{shop_data.get('_id')}")],
                [InlineKeyboardButton("🏪 مدیریت فروشگاه‌ها", callback_data="admin_shops")]
            ])
            
            return await NotificationUtils.send_admin_notification(client, message, keyboard)
        except Exception as e:
            logger.error(f"Error notifying new shop: {e}")
            return False
    
    @staticmethod
    async def notify_payment_received(client: Client, payment_data: Dict, user_data: Dict) -> bool:
        """Notify admin about payment received"""
        try:
            message = (
                f"💰 **پرداخت جدید دریافت شد**\n\n"
                f"👤 کاربر: {user_data.get('first_name')} ({user_data.get('user_id')})\n"
                f"💵 مبلغ: {payment_data.get('amount'):,} تومان\n"
                f"📋 نوع: {payment_data.get('payment_type')}\n"
                f"💳 روش: {payment_data.get('payment_method', 'card_to_card')}\n"
                f"📝 توضیحات: {payment_data.get('description', 'ندارد')}\n"
                f"🕐 زمان: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ تأیید پرداخت", callback_data=f"confirm_payment_{payment_data.get('_id')}")],
                [InlineKeyboardButton("❌ رد پرداخت", callback_data=f"reject_payment_{payment_data.get('_id')}")],
                [InlineKeyboardButton("💰 مدیریت مالی", callback_data="admin_finance")]
            ])
            
            return await NotificationUtils.send_admin_notification(client, message, keyboard)
        except Exception as e:
            logger.error(f"Error notifying payment: {e}")
            return False
    
    @staticmethod
    async def notify_subscription_expiring(client: Client, user_id: int, days_remaining: int) -> bool:
        """Notify user about subscription expiring"""
        try:
            message = (
                f"⚠️ **هشدار انقضای اشتراک**\n\n"
                f"اشتراک شما {days_remaining} روز دیگر منقضی می‌شود.\n\n"
                f"برای تمدید اشتراک و استفاده مداوم از خدمات، "
                f"هم‌اکنون اقدام کنید.\n\n"
                f"💎 مزایای تمدید:\n"
                f"• ادامه دسترسی به تمام امکانات\n"
                f"• عدم قطع خدمات فروشگاه\n"
                f"• حفظ اطلاعات و تنظیمات"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 تمدید اشتراک", callback_data="renew_subscription")],
                [InlineKeyboardButton("💎 مشاهده پلن‌ها", callback_data="shop_plans")],
                [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")]
            ])
            
            await client.send_message(user_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying subscription expiring for user {user_id}: {e}")
            return False
    
    @staticmethod
    async def notify_subscription_expired(client: Client, user_id: int) -> bool:
        """Notify user about subscription expired"""
        try:
            message = (
                f"❌ **اشتراک شما منقضی شد**\n\n"
                f"متأسفانه اشتراک شما به پایان رسیده است.\n\n"
                f"🚫 محدودیت‌های فعلی:\n"
                f"• عدم دسترسی به فروشگاه\n"
                f"• توقف دریافت سفارش‌ها\n"
                f"• غیرفعال شدن ربات فروشگاه\n\n"
                f"برای بازگرداندن دسترسی، لطفاً اشتراک خود را تمدید کنید."
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 تمدید فوری", callback_data="renew_subscription")],
                [InlineKeyboardButton("💎 مشاهده پلن‌ها", callback_data="shop_plans")],
                [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")]
            ])
            
            await client.send_message(user_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying subscription expired for user {user_id}: {e}")
            return False
    
    @staticmethod
    async def notify_new_order(client: Client, shop_owner_id: int, order_data: Dict) -> bool:
        """Notify shop owner about new order"""
        try:
            items_text = ""
            for item in order_data.get('items', []):
                items_text += f"• {item.get('name')} x{item.get('quantity')} - {item.get('price'):,} تومان\n"
            
            message = (
                f"🛒 **سفارش جدید دریافت شد!**\n\n"
                f"📋 شماره سفارش: {order_data.get('order_number')}\n"
                f"👤 مشتری: {order_data.get('customer_info', {}).get('name', 'نامعلوم')}\n"
                f"📱 تلفن: {order_data.get('customer_info', {}).get('phone', 'ندارد')}\n\n"
                f"🛍 **اقلام سفارش:**\n{items_text}\n"
                f"💰 مبلغ کل: {order_data.get('totals', {}).get('total', 0):,} تومان\n"
                f"📝 یادداشت: {order_data.get('notes', 'ندارد')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ تأیید سفارش", callback_data=f"order_confirm_{order_data.get('_id')}")],
                [InlineKeyboardButton("📞 تماس با مشتری", callback_data=f"contact_customer_{order_data.get('customer_id')}")],
                [InlineKeyboardButton("🛒 مشاهده سفارش‌ها", callback_data="orders")]
            ])
            
            await client.send_message(shop_owner_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying new order: {e}")
            return False
    
    @staticmethod
    async def notify_order_status_change(client: Client, customer_id: int, order_data: Dict, new_status: str) -> bool:
        """Notify customer about order status change"""
        try:
            status_messages = {
                'confirmed': 'تأیید شد',
                'processing': 'در حال آماده‌سازی است',
                'shipped': 'ارسال شد',
                'delivered': 'تحویل داده شد',
                'cancelled': 'لغو شد'
            }
            
            status_emojis = {
                'confirmed': '✅',
                'processing': '📦',
                'shipped': '🚚',
                'delivered': '📬',
                'cancelled': '❌'
            }
            
            status_text = status_messages.get(new_status, new_status)
            status_emoji = status_emojis.get(new_status, '📋')
            
            message = (
                f"{status_emoji} **بروزرسانی سفارش**\n\n"
                f"سفارش شما با شماره {order_data.get('order_number')} {status_text}.\n\n"
                f"💰 مبلغ: {order_data.get('totals', {}).get('total', 0):,} تومان\n"
                f"🕐 زمان بروزرسانی: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            )
            
            if new_status == 'shipped':
                tracking_number = order_data.get('shipping', {}).get('tracking_number')
                if tracking_number:
                    message += f"\n📦 کد پیگیری: {tracking_number}"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 جزئیات سفارش", callback_data=f"order_details_{order_data.get('_id')}")],
                [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")]
            ])
            
            await client.send_message(customer_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying order status change: {e}")
            return False
    
    @staticmethod
    async def notify_referral_bonus(client: Client, user_id: int, bonus_amount: float, referred_user_name: str) -> bool:
        """Notify user about referral bonus"""
        try:
            message = (
                f"🎁 **پاداش معرفی دریافت کردید!**\n\n"
                f"کاربر {referred_user_name} با لینک معرفی شما ثبت‌نام کرد.\n\n"
                f"💰 پاداش شما: {bonus_amount:,} تومان\n"
                f"🕐 زمان: {datetime.now().strftime('%Y/%m/%d %H:%M')}\n\n"
                f"🚀 بیشتر دعوت کنید، بیشتر درآمد کسب کنید!"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎁 دعوت دوستان", callback_data="referral")],
                [InlineKeyboardButton("💰 درآمد معرفی", callback_data="referral_earnings")],
                [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")]
            ])
            
            await client.send_message(user_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying referral bonus: {e}")
            return False
    
    @staticmethod
    async def notify_shop_approved(client: Client, user_id: int, shop_name: str) -> bool:
        """Notify user about shop approval"""
        try:
            message = (
                f"🎉 **فروشگاه شما تأیید شد!**\n\n"
                f"فروشگاه «{shop_name}» با موفقیت تأیید و فعال شد.\n\n"
                f"✅ امکانات فعال:\n"
                f"• دریافت سفارش از مشتریان\n"
                f"• مدیریت محصولات\n"
                f"• گزارش‌گیری فروش\n"
                f"• پشتیبانی کامل\n\n"
                f"🚀 حالا می‌توانید محصولات خود را اضافه کنید!"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🏪 مدیریت فروشگاه", callback_data="my_shop")],
                [InlineKeyboardButton("📦 افزودن محصول", callback_data="add_product")],
                [InlineKeyboardButton("📚 آموزش", callback_data="tutorial")]
            ])
            
            await client.send_message(user_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying shop approval: {e}")
            return False
    
    @staticmethod
    async def notify_shop_rejected(client: Client, user_id: int, shop_name: str, reason: str = "") -> bool:
        """Notify user about shop rejection"""
        try:
            message = (
                f"❌ **فروشگاه شما تأیید نشد**\n\n"
                f"متأسفانه فروشگاه «{shop_name}» تأیید نشد.\n\n"
            )
            
            if reason:
                message += f"📝 **دلیل:** {reason}\n\n"
            
            message += (
                f"🔄 **اقدامات بعدی:**\n"
                f"• موارد مشکل‌دار را اصلاح کنید\n"
                f"• مجدداً درخواست ایجاد فروشگاه دهید\n"
                f"• با پشتیبانی تماس بگیرید\n\n"
                f"💡 نکته: از قوانین سایت مطمئن شوید."
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 ایجاد مجدد", callback_data="shop_create")],
                [InlineKeyboardButton("📜 قوانین", callback_data="rules")],
                [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")]
            ])
            
            await client.send_message(user_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error notifying shop rejection: {e}")
            return False
    
    @staticmethod
    async def broadcast_message(client: Client, user_ids: List[int], message: str, 
                              keyboard: Optional[InlineKeyboardMarkup] = None) -> Dict[str, int]:
        """Broadcast message to multiple users"""
        sent_count = 0
        failed_count = 0
        
        for user_id in user_ids:
            try:
                await client.send_message(user_id, message, reply_markup=keyboard)
                sent_count += 1
                
                # Small delay to avoid rate limiting
                if sent_count % 20 == 0:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to send broadcast to {user_id}: {e}")
        
        return {'sent': sent_count, 'failed': failed_count}
    
    @staticmethod
    async def schedule_reminder(client: Client, user_id: int, reminder_type: str, 
                              delay_hours: int, **kwargs) -> bool:
        """Schedule a reminder notification (placeholder for future implementation)"""
        # This would typically use a task queue like Celery or Redis
        # For now, we'll log the reminder request
        logger.info(f"Reminder scheduled: {reminder_type} for user {user_id} in {delay_hours} hours")
        return True
    
    @staticmethod
    async def send_daily_stats(client: Client, admin_id: int, stats_data: Dict) -> bool:
        """Send daily statistics to admin"""
        try:
            message = (
                f"📊 **گزارش روزانه {datetime.now().strftime('%Y/%m/%d')}**\n\n"
                f"👥 کاربران جدید: {stats_data.get('new_users', 0)}\n"
                f"🏪 فروشگاه‌های جدید: {stats_data.get('new_shops', 0)}\n"
                f"🛒 سفارش‌های جدید: {stats_data.get('new_orders', 0)}\n"
                f"💰 درآمد روز: {stats_data.get('daily_revenue', 0):,} تومان\n"
                f"📈 نرخ تبدیل: {stats_data.get('conversion_rate', 0):.1f}%\n\n"
                f"🎯 **اهداف:**\n"
                f"• کاربران فعال: {stats_data.get('active_users', 0)}\n"
                f"• فروشگاه‌های فعال: {stats_data.get('active_shops', 0)}\n"
                f"• حجم معاملات: {stats_data.get('transaction_volume', 0):,} تومان"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 گزارش کامل", callback_data="admin_stats")],
                [InlineKeyboardButton("📈 نمودار رشد", callback_data="growth_chart")],
                [InlineKeyboardButton("💰 گزارش مالی", callback_data="admin_finance")]
            ])
            
            await client.send_message(admin_id, message, reply_markup=keyboard)
            return True
        except Exception as e:
            logger.error(f"Error sending daily stats: {e}")
            return False