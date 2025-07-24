"""
Notification utilities for CodeRoot Bot
Provides centralized notification system for admins and users
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserIsBlocked, UserDeactivated, ChatWriteForbidden

from config import Config, NOTIFICATION_TEMPLATES

logger = logging.getLogger(__name__)


class NotificationManager:
    """Centralized notification management"""
    
    @staticmethod
    async def send_admin_notification(client: Client, message: str, keyboard: InlineKeyboardMarkup = None) -> bool:
        """Send notification to admin"""
        try:
            await client.send_message(
                Config.ADMIN_USER_ID,
                message,
                reply_markup=keyboard
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send admin notification: {e}")
            return False
    
    @staticmethod
    async def send_user_notification(
        client: Client, 
        user_id: int, 
        message: str, 
        keyboard: InlineKeyboardMarkup = None,
        silent: bool = False
    ) -> bool:
        """Send notification to user"""
        try:
            await client.send_message(
                user_id,
                message,
                reply_markup=keyboard,
                disable_notification=silent
            )
            return True
        except (UserIsBlocked, UserDeactivated, ChatWriteForbidden) as e:
            logger.warning(f"Cannot send notification to user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send user notification to {user_id}: {e}")
            return False
    
    @staticmethod
    async def notify_new_user(client: Client, user: Dict) -> bool:
        """Notify admin about new user registration"""
        try:
            message = (
                f"👤 **کاربر جدید ثبت‌نام کرد**\n\n"
                f"🆔 آیدی: `{user['user_id']}`\n"
                f"👤 نام: {user.get('first_name', 'نامشخص')}\n"
                f"📝 یوزرنیم: @{user.get('username', 'ندارد')}\n"
                f"🎯 معرف: {user.get('referred_by', 'ندارد')}\n"
                f"🕐 زمان: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n"
                f"🌍 زبان: {user.get('language', 'fa')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("👁 مشاهده پروفایل", callback_data=f"admin_view_user_{user['user_id']}"),
                    InlineKeyboardButton("💬 ارسال پیام", callback_data=f"admin_message_user_{user['user_id']}")
                ]
            ])
            
            return await NotificationManager.send_admin_notification(client, message, keyboard)
            
        except Exception as e:
            logger.error(f"Error notifying new user: {e}")
            return False
    
    @staticmethod
    async def notify_new_shop(client: Client, shop: Dict) -> bool:
        """Notify admin about new shop creation"""
        try:
            message = (
                f"🏪 **فروشگاه جدید ایجاد شد**\n\n"
                f"🏪 نام: {shop['name']}\n"
                f"👤 مالک: {shop['owner_id']}\n"
                f"💎 پلن: {shop.get('plan', 'free')}\n"
                f"📝 توضیحات: {shop.get('description', 'ندارد')}\n"
                f"🕐 زمان: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n"
                f"📊 وضعیت: {shop.get('status', 'pending')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ تأیید فروشگاه", callback_data=f"admin_approve_shop_{shop['_id']}"),
                    InlineKeyboardButton("❌ رد کردن", callback_data=f"admin_reject_shop_{shop['_id']}")
                ],
                [
                    InlineKeyboardButton("👁 مشاهده جزئیات", callback_data=f"admin_shop_details_{shop['_id']}")
                ]
            ])
            
            return await NotificationManager.send_admin_notification(client, message, keyboard)
            
        except Exception as e:
            logger.error(f"Error notifying new shop: {e}")
            return False
    
    @staticmethod
    async def notify_payment_received(client: Client, payment: Dict, user: Dict) -> bool:
        """Notify admin about payment received"""
        try:
            message = (
                f"💰 **پرداخت جدید دریافت شد**\n\n"
                f"👤 کاربر: {user.get('first_name', 'نامشخص')} (`{user['user_id']}`)\n"
                f"💵 مبلغ: {payment['amount']:,} تومان\n"
                f"📋 نوع: {payment.get('payment_type', 'اشتراک')}\n"
                f"🏪 فروشگاه: {payment.get('shop_id', 'ندارد')}\n"
                f"🕐 زمان: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n"
                f"📊 وضعیت: {payment.get('status', 'pending')}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ تأیید پرداخت", callback_data=f"admin_confirm_payment_{payment['_id']}"),
                    InlineKeyboardButton("❌ رد پرداخت", callback_data=f"admin_reject_payment_{payment['_id']}")
                ]
            ])
            
            return await NotificationManager.send_admin_notification(client, message, keyboard)
            
        except Exception as e:
            logger.error(f"Error notifying payment: {e}")
            return False
    
    @staticmethod
    async def notify_subscription_expiring(client: Client, user: Dict, shop: Dict, days_left: int) -> bool:
        """Notify user about subscription expiring"""
        try:
            user_lang = user.get('language', 'fa')
            
            if user_lang == 'fa':
                message = (
                    f"⚠️ **هشدار انقضای اشتراک**\n\n"
                    f"🏪 فروشگاه: {shop['name']}\n"
                    f"📅 باقی‌مانده: {days_left} روز\n\n"
                    f"برای تمدید اشتراک خود اقدام کنید تا خدمات فروشگاه شما قطع نشود."
                )
            elif user_lang == 'en':
                message = (
                    f"⚠️ **Subscription Expiring Warning**\n\n"
                    f"🏪 Shop: {shop['name']}\n"
                    f"📅 Days left: {days_left}\n\n"
                    f"Please renew your subscription to avoid service interruption."
                )
            else:  # Arabic
                message = (
                    f"⚠️ **تحذير انتهاء الاشتراك**\n\n"
                    f"🏪 المتجر: {shop['name']}\n"
                    f"📅 الأيام المتبقية: {days_left}\n\n"
                    f"يرجى تجديد اشتراكك لتجنب انقطاع الخدمة."
                )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 تمدید اشتراک", callback_data=f"renew_subscription_{shop['_id']}")]
            ])
            
            return await NotificationManager.send_user_notification(
                client, user['user_id'], message, keyboard
            )
            
        except Exception as e:
            logger.error(f"Error notifying subscription expiring: {e}")
            return False
    
    @staticmethod
    async def notify_subscription_expired(client: Client, user: Dict, shop: Dict) -> bool:
        """Notify user about subscription expired"""
        try:
            user_lang = user.get('language', 'fa')
            
            if user_lang == 'fa':
                message = (
                    f"❌ **اشتراک منقضی شد**\n\n"
                    f"🏪 فروشگاه: {shop['name']}\n"
                    f"📅 تاریخ انقضا: {shop.get('subscription', {}).get('expires_at', 'نامشخص')}\n\n"
                    f"فروشگاه شما غیرفعال شده است. برای فعال‌سازی مجدد، اشتراک خود را تمدید کنید."
                )
            elif user_lang == 'en':
                message = (
                    f"❌ **Subscription Expired**\n\n"
                    f"🏪 Shop: {shop['name']}\n"
                    f"📅 Expired on: {shop.get('subscription', {}).get('expires_at', 'Unknown')}\n\n"
                    f"Your shop has been deactivated. Renew your subscription to reactivate it."
                )
            else:  # Arabic
                message = (
                    f"❌ **انتهى الاشتراك**\n\n"
                    f"🏪 المتجر: {shop['name']}\n"
                    f"📅 انتهى في: {shop.get('subscription', {}).get('expires_at', 'غير معروف')}\n\n"
                    f"تم إلغاء تفعيل متجرك. جدد اشتراكك لإعادة تفعيله."
                )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 تمدید اشتراک", callback_data=f"renew_subscription_{shop['_id']}")]
            ])
            
            return await NotificationManager.send_user_notification(
                client, user['user_id'], message, keyboard
            )
            
        except Exception as e:
            logger.error(f"Error notifying subscription expired: {e}")
            return False
    
    @staticmethod
    async def notify_new_order(client: Client, shop_owner: Dict, order: Dict) -> bool:
        """Notify shop owner about new order"""
        try:
            user_lang = shop_owner.get('language', 'fa')
            
            if user_lang == 'fa':
                message = (
                    f"🛒 **سفارش جدید**\n\n"
                    f"📦 شماره سفارش: {order['order_number']}\n"
                    f"👤 مشتری: {order.get('customer_info', {}).get('name', 'نامشخص')}\n"
                    f"💰 مبلغ: {order.get('totals', {}).get('total', 0):,} تومان\n"
                    f"🕐 زمان: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}"
                )
            elif user_lang == 'en':
                message = (
                    f"🛒 **New Order**\n\n"
                    f"📦 Order #: {order['order_number']}\n"
                    f"👤 Customer: {order.get('customer_info', {}).get('name', 'Unknown')}\n"
                    f"💰 Amount: {order.get('totals', {}).get('total', 0):,} Tomans\n"
                    f"🕐 Time: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}"
                )
            else:  # Arabic
                message = (
                    f"🛒 **طلب جديد**\n\n"
                    f"📦 رقم الطلب: {order['order_number']}\n"
                    f"👤 العميل: {order.get('customer_info', {}).get('name', 'غير معروف')}\n"
                    f"💰 المبلغ: {order.get('totals', {}).get('total', 0):,} تومان\n"
                    f"🕐 الوقت: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}"
                )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("👁 مشاهده سفارش", callback_data=f"view_order_{order['_id']}"),
                    InlineKeyboardButton("✅ تأیید", callback_data=f"confirm_order_{order['_id']}")
                ]
            ])
            
            return await NotificationManager.send_user_notification(
                client, shop_owner['user_id'], message, keyboard
            )
            
        except Exception as e:
            logger.error(f"Error notifying new order: {e}")
            return False
    
    @staticmethod
    async def notify_order_status_change(client: Client, customer: Dict, order: Dict, new_status: str) -> bool:
        """Notify customer about order status change"""
        try:
            user_lang = customer.get('language', 'fa')
            
            status_texts = {
                'fa': {
                    'confirmed': 'تأیید شد',
                    'processing': 'در حال پردازش',
                    'shipped': 'ارسال شد',
                    'delivered': 'تحویل داده شد',
                    'cancelled': 'لغو شد'
                },
                'en': {
                    'confirmed': 'Confirmed',
                    'processing': 'Processing',
                    'shipped': 'Shipped',
                    'delivered': 'Delivered',
                    'cancelled': 'Cancelled'
                },
                'ar': {
                    'confirmed': 'مؤكد',
                    'processing': 'قيد المعالجة',
                    'shipped': 'تم الشحن',
                    'delivered': 'تم التسليم',
                    'cancelled': 'ملغي'
                }
            }
            
            status_text = status_texts.get(user_lang, status_texts['fa']).get(new_status, new_status)
            
            if user_lang == 'fa':
                message = (
                    f"📦 **به‌روزرسانی سفارش**\n\n"
                    f"📦 شماره: {order['order_number']}\n"
                    f"📊 وضعیت جدید: {status_text}\n"
                    f"🕐 زمان: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}"
                )
            elif user_lang == 'en':
                message = (
                    f"📦 **Order Update**\n\n"
                    f"📦 Order #: {order['order_number']}\n"
                    f"📊 New Status: {status_text}\n"
                    f"🕐 Time: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}"
                )
            else:  # Arabic
                message = (
                    f"📦 **تحديث الطلب**\n\n"
                    f"📦 رقم الطلب: {order['order_number']}\n"
                    f"📊 الحالة الجديدة: {status_text}\n"
                    f"🕐 الوقت: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}"
                )
            
            return await NotificationManager.send_user_notification(
                client, customer['user_id'], message
            )
            
        except Exception as e:
            logger.error(f"Error notifying order status change: {e}")
            return False
    
    @staticmethod
    async def notify_referral_bonus(client: Client, user: Dict, referred_user: Dict, bonus_amount: int) -> bool:
        """Notify user about referral bonus"""
        try:
            user_lang = user.get('language', 'fa')
            
            if user_lang == 'fa':
                message = (
                    f"🎁 **پاداش معرفی دریافت کردید!**\n\n"
                    f"👤 کاربر معرفی شده: {referred_user.get('first_name', 'نامشخص')}\n"
                    f"💰 پاداش: {bonus_amount:,} تومان\n"
                    f"🕐 زمان: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n\n"
                    f"از معرفی کاربران جدید متشکریم! 🙏"
                )
            elif user_lang == 'en':
                message = (
                    f"🎁 **Referral Bonus Received!**\n\n"
                    f"👤 Referred User: {referred_user.get('first_name', 'Unknown')}\n"
                    f"💰 Bonus: {bonus_amount:,} Tomans\n"
                    f"🕐 Time: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n\n"
                    f"Thank you for referring new users! 🙏"
                )
            else:  # Arabic
                message = (
                    f"🎁 **تم استلام مكافأة الإحالة!**\n\n"
                    f"👤 المستخدم المُحال: {referred_user.get('first_name', 'غير معروف')}\n"
                    f"💰 المكافأة: {bonus_amount:,} تومان\n"
                    f"🕐 الوقت: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n\n"
                    f"شكراً لإحالة مستخدمين جدد! 🙏"
                )
            
            return await NotificationManager.send_user_notification(
                client, user['user_id'], message
            )
            
        except Exception as e:
            logger.error(f"Error notifying referral bonus: {e}")
            return False
    
    @staticmethod
    async def notify_shop_approved(client: Client, user: Dict, shop: Dict) -> bool:
        """Notify user about shop approval"""
        try:
            user_lang = user.get('language', 'fa')
            
            if user_lang == 'fa':
                message = (
                    f"✅ **فروشگاه شما تأیید شد!**\n\n"
                    f"🏪 نام فروشگاه: {shop['name']}\n"
                    f"💎 پلن: {shop.get('plan', 'free')}\n"
                    f"🕐 زمان تأیید: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n\n"
                    f"حالا می‌توانید محصولات خود را اضافه کنید و شروع به فروش کنید! 🎉"
                )
            elif user_lang == 'en':
                message = (
                    f"✅ **Your Shop Has Been Approved!**\n\n"
                    f"🏪 Shop Name: {shop['name']}\n"
                    f"💎 Plan: {shop.get('plan', 'free')}\n"
                    f"🕐 Approved At: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n\n"
                    f"You can now add products and start selling! 🎉"
                )
            else:  # Arabic
                message = (
                    f"✅ **تمت الموافقة على متجرك!**\n\n"
                    f"🏪 اسم المتجر: {shop['name']}\n"
                    f"💎 الخطة: {shop.get('plan', 'free')}\n"
                    f"🕐 وقت الموافقة: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n\n"
                    f"يمكنك الآن إضافة منتجات وبدء البيع! 🎉"
                )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🏪 مدیریت فروشگاه", callback_data=f"manage_shop_{shop['_id']}"),
                    InlineKeyboardButton("📦 افزودن محصول", callback_data=f"add_product_{shop['_id']}")
                ]
            ])
            
            return await NotificationManager.send_user_notification(
                client, user['user_id'], message, keyboard
            )
            
        except Exception as e:
            logger.error(f"Error notifying shop approval: {e}")
            return False
    
    @staticmethod
    async def notify_shop_rejected(client: Client, user: Dict, shop: Dict, reason: str = "") -> bool:
        """Notify user about shop rejection"""
        try:
            user_lang = user.get('language', 'fa')
            
            if user_lang == 'fa':
                message = (
                    f"❌ **فروشگاه شما تأیید نشد**\n\n"
                    f"🏪 نام فروشگاه: {shop['name']}\n"
                    f"🕐 زمان بررسی: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n"
                )
                if reason:
                    message += f"\n📝 دلیل: {reason}\n"
                message += "\nبرای اطلاعات بیشتر با پشتیبانی تماس بگیرید."
            elif user_lang == 'en':
                message = (
                    f"❌ **Your Shop Was Not Approved**\n\n"
                    f"🏪 Shop Name: {shop['name']}\n"
                    f"🕐 Review Time: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n"
                )
                if reason:
                    message += f"\n📝 Reason: {reason}\n"
                message += "\nPlease contact support for more information."
            else:  # Arabic
                message = (
                    f"❌ **لم تتم الموافقة على متجرك**\n\n"
                    f"🏪 اسم المتجر: {shop['name']}\n"
                    f"🕐 وقت المراجعة: {datetime.utcnow().strftime('%Y/%m/%d %H:%M')}\n"
                )
                if reason:
                    message += f"\n📝 السبب: {reason}\n"
                message += "\nيرجى الاتصال بالدعم للحصول على مزيد من المعلومات."
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🆘 تماس با پشتیبانی", url="https://t.me/hadi_admin")]
            ])
            
            return await NotificationManager.send_user_notification(
                client, user['user_id'], message, keyboard
            )
            
        except Exception as e:
            logger.error(f"Error notifying shop rejection: {e}")
            return False
    
    @staticmethod
    async def broadcast_message(
        client: Client, 
        users: List[Dict], 
        message: str, 
        keyboard: InlineKeyboardMarkup = None,
        silent: bool = False
    ) -> Dict[str, int]:
        """Broadcast message to multiple users"""
        results = {"sent": 0, "failed": 0, "blocked": 0}
        
        for user in users:
            try:
                success = await NotificationManager.send_user_notification(
                    client, user['user_id'], message, keyboard, silent
                )
                if success:
                    results["sent"] += 1
                else:
                    results["blocked"] += 1
                    
                # Small delay to avoid flood limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to send broadcast to user {user['user_id']}: {e}")
                results["failed"] += 1
        
        return results
    
    @staticmethod
    async def schedule_reminder(client: Client, user_id: int, message: str, delay_hours: int):
        """Schedule a reminder message (placeholder for future implementation)"""
        # This would typically use a task queue like Celery or RQ
        # For now, just log the intention
        logger.info(f"Reminder scheduled for user {user_id} in {delay_hours} hours: {message[:50]}...")
        
        # TODO: Implement with actual scheduling system
        pass
    
    @staticmethod
    async def send_daily_stats(client: Client, stats: Dict) -> bool:
        """Send daily statistics to admin"""
        try:
            message = (
                f"📊 **آمار روزانه CodeRoot**\n"
                f"📅 {datetime.utcnow().strftime('%Y/%m/%d')}\n\n"
                f"👥 کاربران جدید: {stats.get('new_users', 0)}\n"
                f"🏪 فروشگاه‌های جدید: {stats.get('new_shops', 0)}\n"
                f"🛒 سفارش‌های جدید: {stats.get('new_orders', 0)}\n"
                f"💰 پرداخت‌های جدید: {stats.get('new_payments', 0)}\n"
                f"💵 کل درآمد: {stats.get('total_revenue', 0):,} تومان\n"
                f"📈 رشد کاربران: {stats.get('user_growth', 0)}%\n"
                f"🎯 نرخ تبدیل: {stats.get('conversion_rate', 0)}%"
            )
            
            return await NotificationManager.send_admin_notification(client, message)
            
        except Exception as e:
            logger.error(f"Error sending daily stats: {e}")
            return False