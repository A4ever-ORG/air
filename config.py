import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Production Configuration for CodeRoot Bot"""
    
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID", "17064702"))
    API_HASH = os.getenv("API_HASH", "f65880b9eededbee85346f874819bbc5")
    
    # Admin Configuration
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "7707164235"))
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "hadi_admin")
    
    # Mode Configuration
    DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
    PRODUCTION_MODE = os.getenv("PRODUCTION_MODE", "true").lower() == "true"
    
    # Database Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "coderoot_production")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Payment Configuration
    CARD_NUMBER = os.getenv("CARD_NUMBER", "6037-9977-7766-5544")
    CARD_HOLDER_NAME = os.getenv("CARD_HOLDER_NAME", "حادی")
    
    # Channel Configuration (Required for join enforcement)
    MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID")
    MAIN_CHANNEL_USERNAME = os.getenv("MAIN_CHANNEL_USERNAME")
    
    # Subscription Plans Pricing (in Tomans)
    PROFESSIONAL_PLAN_PRICE = int(os.getenv("PROFESSIONAL_PLAN_PRICE", "20000"))
    VIP_PLAN_PRICE = int(os.getenv("VIP_PLAN_PRICE", "60000"))
    
    # Commission Rate (percentage)
    COMMISSION_RATE = int(os.getenv("COMMISSION_RATE", "5"))
    
    # Bot Settings
    BOT_USERNAME = os.getenv("BOT_USERNAME", "coderoot_main_bot")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    # Sub-bot Creation
    BOTFATHER_TOKEN = os.getenv("BOTFATHER_TOKEN")
    SUB_BOT_PREFIX = os.getenv("SUB_BOT_PREFIX", "shop_")
    
    # Backup and Logging
    BACKUP_ENABLED = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/coderoot.log")
    
    # Notification Settings
    TELEGRAM_NOTIFICATIONS = os.getenv("TELEGRAM_NOTIFICATIONS", "true").lower() == "true"
    EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS", "false").lower() == "true"
    
    # Security
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")
    
    # Performance
    MAX_CONCURRENT_USERS = int(os.getenv("MAX_CONCURRENT_USERS", "1000"))
    CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
    
    # Referral System
    REFERRAL_COMMISSION = int(os.getenv("REFERRAL_COMMISSION", "10"))  # Percentage
    REFERRAL_LEVELS = int(os.getenv("REFERRAL_LEVELS", "3"))  # Max referral levels
    
    @classmethod
    def validate_required_config(cls):
        """Validate required configuration"""
        required_fields = [
            ("BOT_TOKEN", cls.BOT_TOKEN),
            ("API_ID", cls.API_ID),
            ("API_HASH", cls.API_HASH),
            ("ADMIN_USER_ID", cls.ADMIN_USER_ID),
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value or (isinstance(field_value, int) and field_value == 0):
                missing_fields.append(field_name)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        
        return True
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get complete database URL"""
        return f"{cls.MONGO_URI.rstrip('/')}/{cls.DATABASE_NAME}"

# Subscription Plans Configuration
PLANS = {
    "free": {
        "name": "رایگان",
        "name_en": "Free",
        "price": 0,
        "max_products": 10,
        "max_categories": 3,
        "payment_gateway": True,
        "advanced_reports": False,
        "auto_messages": False,
        "discounts": False,
        "ads": False,
        "custom_buttons": False,
        "commission": 5,
        "duration_days": 30,
        "features": [
            "تا 10 محصول",
            "3 دسته‌بندی",
            "گزارش پایه",
            "5% کارمزد",
            "پشتیبانی عمومی"
        ],
        "limits": {
            "daily_orders": 50,
            "monthly_revenue": 5000000,  # 5M Toman
            "image_size": 5,  # MB
            "video_size": 10  # MB
        }
    },
    "professional": {
        "name": "حرفه‌ای",
        "name_en": "Professional", 
        "price": Config.PROFESSIONAL_PLAN_PRICE,
        "max_products": 200,
        "max_categories": 20,
        "payment_gateway": True,
        "advanced_reports": True,
        "auto_messages": True,
        "discounts": True,
        "ads": True,
        "custom_buttons": True,
        "commission": 5,
        "duration_days": 30,
        "features": [
            "تا 200 محصول", 
            "20 دسته‌بندی",
            "گزارش‌های حرفه‌ای",
            "پیام‌های خودکار",
            "سیستم تخفیف",
            "تبلیغات درون‌رباتی",
            "دکمه‌های سفارشی",
            "5% کارمزد",
            "پشتیبانی اولویت‌دار"
        ],
        "limits": {
            "daily_orders": 500,
            "monthly_revenue": 50000000,  # 50M Toman
            "image_size": 10,  # MB
            "video_size": 25  # MB
        }
    },
    "vip": {
        "name": "VIP",
        "name_en": "VIP",
        "price": Config.VIP_PLAN_PRICE,
        "max_products": -1,  # Unlimited
        "max_categories": -1,  # Unlimited
        "payment_gateway": True,
        "advanced_reports": True,
        "auto_messages": True,
        "discounts": True,
        "ads": True,
        "custom_buttons": True,
        "commission": 0,  # No commission
        "duration_days": 30,
        "features": [
            "محصولات نامحدود",
            "دسته‌بندی نامحدود", 
            "گزارش‌های پیشرفته",
            "پیام‌های هوشمند",
            "تخفیف‌های پیشرفته",
            "تبلیغات ویژه",
            "درگاه پرداخت اختصاصی",
            "بدون کارمزد",
            "پشتیبانی 24/7",
            "ربات اختصاصی"
        ],
        "limits": {
            "daily_orders": -1,  # Unlimited
            "monthly_revenue": -1,  # Unlimited
            "image_size": 50,  # MB
            "video_size": 100  # MB
        }
    }
}

# Referral Configuration
REFERRAL_CONFIG = {
    "commission_rate": Config.REFERRAL_COMMISSION,
    "max_levels": Config.REFERRAL_LEVELS,
    "min_payout": 50000,  # Minimum payout in Tomans
    "payout_schedule": "monthly",  # weekly, monthly, quarterly
    "bonus_tiers": {
        1: 10,   # 1 referral = 10% bonus
        5: 15,   # 5 referrals = 15% bonus  
        10: 20,  # 10 referrals = 20% bonus
        25: 25,  # 25 referrals = 25% bonus
        50: 30   # 50+ referrals = 30% bonus
    }
}

# Bot Features Configuration
FEATURES = {
    "channel_join_required": True,
    "referral_system": True,
    "auto_backup": True,
    "analytics": True,
    "multi_language": False,  # Future feature
    "api_access": False,      # Future feature
    "webhook_support": True,
    "custom_domain": False,   # VIP feature
    "white_label": False      # Enterprise feature
}

# Notification Templates
NOTIFICATION_TEMPLATES = {
    "welcome": "🎉 خوش آمدید به CodeRoot!\n\nشما با موفقیت عضو شدید.",
    "shop_created": "🏪 فروشگاه شما ایجاد شد!\n\nنام: {shop_name}\nپلن: {plan_name}",
    "payment_received": "💰 پرداخت شما دریافت شد!\n\nمبلغ: {amount:,} تومان",
    "subscription_expiring": "⚠️ اشتراک شما {days} روز دیگر منقضی می‌شود.",
    "subscription_expired": "❌ اشتراک شما منقضی شد. برای تمدید اقدام کنید.",
    "new_order": "🛒 سفارش جدید!\n\nمحصول: {product_name}\nمشتری: {customer_name}",
    "referral_bonus": "🎁 پاداش معرفی!\n\nشما {amount:,} تومان پاداش دریافت کردید."
}

# File Upload Limits
UPLOAD_LIMITS = {
    "image": {
        "max_size": 10 * 1024 * 1024,  # 10MB
        "allowed_formats": ["jpg", "jpeg", "png", "webp"],
        "max_resolution": (2048, 2048)
    },
    "video": {
        "max_size": 50 * 1024 * 1024,  # 50MB  
        "allowed_formats": ["mp4", "avi", "mov", "mkv"],
        "max_duration": 120  # seconds
    },
    "document": {
        "max_size": 20 * 1024 * 1024,  # 20MB
        "allowed_formats": ["pdf", "doc", "docx", "txt"]
    }
}

# Rate Limiting
RATE_LIMITS = {
    "message_per_minute": 30,
    "api_calls_per_hour": 1000,
    "file_uploads_per_day": 100,
    "shop_creation_per_day": 1,
    "password_attempts": 5
}