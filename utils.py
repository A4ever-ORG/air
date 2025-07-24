import asyncio
import re
import jdatetime
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import qrcode
from io import BytesIO
import logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config, PLANS

logger = logging.getLogger(__name__)

class BotUtils:
    """Utility functions for bot operations"""
    
    @staticmethod
    def format_price(amount: int) -> str:
        """Format price with Persian numbers and currency"""
        formatted = f"{amount:,}".replace(',', '٬')
        return f"{formatted} تومان"
    
    @staticmethod
    def format_date(date: datetime) -> str:
        """Format date to Persian"""
        jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
        return jalali_date.strftime("%Y/%m/%d - %H:%M")
    
    @staticmethod
    def format_duration(days: int) -> str:
        """Format duration in Persian"""
        if days == 1:
            return "یک روز"
        elif days == 7:
            return "یک هفته"
        elif days == 30:
            return "یک ماه"
        elif days == 365:
            return "یک سال"
        else:
            return f"{days} روز"
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Iranian phone number"""
        pattern = r'^09\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """Validate Iranian bank card number"""
        # Remove spaces and dashes
        card_number = re.sub(r'[\s-]', '', card_number)
        
        # Check if it's 16 digits
        if not re.match(r'^\d{16}$', card_number):
            return False
        
        # Luhn algorithm for card validation
        total = 0
        reverse_digits = card_number[::-1]
        
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n = (n // 10) + (n % 10)
            total += n
        
        return total % 10 == 0
    
    @staticmethod
    def generate_qr_code(data: str) -> BytesIO:
        """Generate QR code for data"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return img_buffer
    
    @staticmethod
    async def check_channel_membership(app, user_id: int, channel_username: str) -> bool:
        """Check if user is member of channel"""
        try:
            member = await app.get_chat_member(channel_username, user_id)
            return member.status not in ["kicked", "left"]
        except Exception as e:
            logger.error(f"Error checking channel membership: {e}")
            return False
    
    @staticmethod
    def create_pagination_keyboard(current_page: int, total_pages: int, callback_prefix: str) -> InlineKeyboardMarkup:
        """Create pagination keyboard"""
        keyboard = []
        row = []
        
        if current_page > 1:
            row.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"{callback_prefix}:{current_page-1}"))
        
        row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="page_info"))
        
        if current_page < total_pages:
            row.append(InlineKeyboardButton("بعدی ➡️", callback_data=f"{callback_prefix}:{current_page+1}"))
        
        if row:
            keyboard.append(row)
        
        return InlineKeyboardMarkup(keyboard)

class MessageTemplates:
    """Message templates for the bot"""
    
    WELCOME_MESSAGE = """
🎉 به ربات CodeRoot خوش آمدید!

با این ربات می‌توانید:
🏪 فروشگاه اختصاصی خود را بسازید
📦 محصولات خود را مدیریت کنید  
💰 درآمد کسب کنید

برای شروع از منوی زیر استفاده کنید:
    """
    
    SHOP_CREATED_MESSAGE = """
🎊 تبریک! فروشگاه شما با موفقیت ایجاد شد

📋 اطلاعات فروشگاه:
🏪 نام: {shop_name}
🤖 ربات: @{bot_username}
📊 پلن: {plan_name}
⏰ انقضا: {expires_date}

✅ فروشگاه شما در حال بررسی است و بزودی فعال خواهد شد.
    """
    
    PAYMENT_REQUEST_MESSAGE = """
💳 درخواست پرداخت

💰 مبلغ: {amount}
📋 شرح: {description}
⏰ مهلت پرداخت: 24 ساعت

🏦 اطلاعات کارت:
شماره کارت: {card_number}
نام صاحب کارت: {card_holder}

📝 پس از پرداخت، تصویر رسید را ارسال کنید.
    """
    
    SUBSCRIPTION_EXPIRED_MESSAGE = """
⚠️ اشتراک شما منقضی شده است

برای ادامه استفاده از خدمات، لطفاً اشتراک خود را تمدید کنید.

💡 برای تمدید از دکمه زیر استفاده کنید:
    """

class KeyboardMarkups:
    """Keyboard markups for the bot"""
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("🛍 ساخت فروشگاه", callback_data="create_shop")],
            [InlineKeyboardButton("🏪 ورود به فروشگاه من", callback_data="my_shop")],
            [InlineKeyboardButton("📊 گزارش‌ها", callback_data="reports"), 
             InlineKeyboardButton("💳 تمدید اشتراک", callback_data="renew_subscription")],
            [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support"), 
             InlineKeyboardButton("📚 آموزش", callback_data="tutorial")],
            [InlineKeyboardButton("📜 قوانین", callback_data="rules")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_menu() -> InlineKeyboardMarkup:
        """Admin menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("👥 مدیریت فروشنده‌ها", callback_data="admin_users"),
             InlineKeyboardButton("🏪 مدیریت فروشگاه‌ها", callback_data="admin_shops")],
            [InlineKeyboardButton("💰 گزارش مالی", callback_data="admin_finance"),
             InlineKeyboardButton("📊 آمارها", callback_data="admin_stats")],
            [InlineKeyboardButton("📢 ارسال پیام", callback_data="admin_broadcast"),
             InlineKeyboardButton("⚙️ تنظیمات", callback_data="admin_settings")],
            [InlineKeyboardButton("🔄 بازگشت", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def plans_menu() -> InlineKeyboardMarkup:
        """Plans selection keyboard"""
        keyboard = []
        
        for plan_key, plan_data in PLANS.items():
            if plan_key == "free":
                text = f"🆓 {plan_data['name']} (رایگان)"
            else:
                text = f"💎 {plan_data['name']} ({plan_data['price']:,} تومان)"
            
            keyboard.append([InlineKeyboardButton(text, callback_data=f"select_plan:{plan_key}")])
        
        keyboard.append([InlineKeyboardButton("🔄 بازگشت", callback_data="back_to_main")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def shop_management_menu() -> InlineKeyboardMarkup:
        """Shop management keyboard"""
        keyboard = [
            [InlineKeyboardButton("➕ افزودن محصول", callback_data="add_product"),
             InlineKeyboardButton("📦 مدیریت محصولات", callback_data="manage_products")],
            [InlineKeyboardButton("📋 سفارش‌ها", callback_data="orders"),
             InlineKeyboardButton("📊 گزارش فروش", callback_data="sales_report")],
            [InlineKeyboardButton("⚙️ تنظیمات فروشگاه", callback_data="shop_settings"),
             InlineKeyboardButton("🎁 ارتقاء پلن", callback_data="upgrade_plan")],
            [InlineKeyboardButton("🔄 بازگشت", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirmation_keyboard(action: str) -> InlineKeyboardMarkup:
        """Confirmation keyboard"""
        keyboard = [
            [InlineKeyboardButton("✅ تأیید", callback_data=f"confirm:{action}"),
             InlineKeyboardButton("❌ لغو", callback_data="cancel")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_keyboard(callback_data: str = "back") -> InlineKeyboardMarkup:
        """Back button keyboard"""
        keyboard = [
            [InlineKeyboardButton("🔄 بازگشت", callback_data=callback_data)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def cancel_keyboard() -> InlineKeyboardMarkup:
        """Cancel button keyboard"""
        keyboard = [
            [InlineKeyboardButton("❌ لغو", callback_data="cancel")]
        ]
        return InlineKeyboardMarkup(keyboard)

class ValidationUtils:
    """Validation utilities"""
    
    @staticmethod
    def validate_shop_name(name: str) -> bool:
        """Validate shop name"""
        if len(name) < 3 or len(name) > 50:
            return False
        
        # Check for invalid characters
        invalid_chars = ['@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/']
        for char in invalid_chars:
            if char in name:
                return False
        
        return True
    
    @staticmethod
    def validate_product_name(name: str) -> bool:
        """Validate product name"""
        return 3 <= len(name) <= 100
    
    @staticmethod
    def validate_product_price(price: str) -> Optional[int]:
        """Validate and convert product price"""
        try:
            price_int = int(price.replace(',', '').replace('٬', ''))
            if price_int > 0:
                return price_int
        except ValueError:
            pass
        return None
    
    @staticmethod
    def validate_bot_token(token: str) -> bool:
        """Validate Telegram bot token format"""
        pattern = r'^\d+:[a-zA-Z0-9_-]{35}$'
        return bool(re.match(pattern, token))

class ExcelGenerator:
    """Excel file generation utilities"""
    
    @staticmethod
    async def generate_users_report(users: List[Dict]) -> BytesIO:
        """Generate users report in Excel format"""
        try:
            import pandas as pd
            
            # Prepare data
            data = []
            for user in users:
                data.append({
                    'شناسه کاربری': user.get('user_id', ''),
                    'نام کاربری': user.get('username', ''),
                    'نام': user.get('first_name', ''),
                    'نام خانوادگی': user.get('last_name', ''),
                    'شماره تلفن': user.get('phone', ''),
                    'پلن اشتراک': PLANS.get(user.get('subscription', {}).get('plan', 'free'), {}).get('name', 'نامشخص'),
                    'تاریخ انقضا': BotUtils.format_date(user.get('subscription', {}).get('expires_at', datetime.utcnow())),
                    'تعداد سفارش‌ها': user.get('statistics', {}).get('total_orders', 0),
                    'کل درآمد': BotUtils.format_price(user.get('statistics', {}).get('total_revenue', 0)),
                    'تاریخ عضویت': BotUtils.format_date(user.get('created_at', datetime.utcnow()))
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='گزارش کاربران', index=False)
            
            output.seek(0)
            return output
            
        except ImportError:
            logger.error("pandas library not found. Cannot generate Excel report.")
            return None
        except Exception as e:
            logger.error(f"Error generating Excel report: {e}")
            return None

class SecurityUtils:
    """Security utilities"""
    
    @staticmethod
    async def is_user_admin(user_id: int) -> bool:
        """Check if user is admin"""
        return user_id == Config.ADMIN_USER_ID
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        # Remove HTML tags
        import re
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        
        # Remove script tags
        script = re.compile('<script.*?</script>')
        text = re.sub(script, '', text, flags=re.DOTALL)
        
        return text.strip()
    
    @staticmethod
    def generate_shop_token() -> str:
        """Generate unique shop token"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))

class NotificationUtils:
    """Notification utilities"""
    
    @staticmethod
    async def send_admin_notification(app, message: str):
        """Send notification to admin"""
        try:
            await app.send_message(Config.ADMIN_USER_ID, f"🔔 اعلان مدیریت:\n\n{message}")
        except Exception as e:
            logger.error(f"Failed to send admin notification: {e}")
    
    @staticmethod
    async def send_subscription_reminder(app, user_id: int, days_left: int):
        """Send subscription expiration reminder"""
        try:
            message = f"⚠️ یادآوری انقضای اشتراک\n\n{days_left} روز تا پایان اشتراک شما باقی مانده است.\n\nبرای تمدید اشتراک از دکمه زیر استفاده کنید."
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 تمدید اشتراک", callback_data="renew_subscription")]
            ])
            
            await app.send_message(user_id, message, reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Failed to send subscription reminder: {e}")

# Time utilities
class TimeUtils:
    """Time related utilities"""
    
    @staticmethod
    def get_persian_weekday(date: datetime) -> str:
        """Get Persian weekday name"""
        weekdays = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه', 'یکشنبه']
        return weekdays[date.weekday()]
    
    @staticmethod
    def get_time_ago(date: datetime) -> str:
        """Get time ago in Persian"""
        now = datetime.utcnow()
        diff = now - date
        
        if diff.days > 0:
            return f"{diff.days} روز پیش"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} ساعت پیش"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} دقیقه پیش"
        else:
            return "همین الان"
    
    @staticmethod
    def is_subscription_expired(expires_at: datetime) -> bool:
        """Check if subscription is expired"""
        return datetime.utcnow() > expires_at
    
    @staticmethod
    def days_until_expiration(expires_at: datetime) -> int:
        """Get days until subscription expiration"""
        diff = expires_at - datetime.utcnow()
        return max(0, diff.days)