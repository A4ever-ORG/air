import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH")
    
    # Database Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "coderoot_bot")
    
    # Redis Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Admin Configuration
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    
    # Payment Configuration
    CARD_NUMBER = os.getenv("CARD_NUMBER")
    CARD_HOLDER_NAME = os.getenv("CARD_HOLDER_NAME")
    
    # Channel Configuration
    MAIN_CHANNEL_ID = int(os.getenv("MAIN_CHANNEL_ID", 0))
    MAIN_CHANNEL_USERNAME = os.getenv("MAIN_CHANNEL_USERNAME")
    
    # Subscription Plans Pricing (in Tomans)
    PROFESSIONAL_PLAN_PRICE = int(os.getenv("PROFESSIONAL_PLAN_PRICE", 20000))
    VIP_PLAN_PRICE = int(os.getenv("VIP_PLAN_PRICE", 60000))
    
    # Commission Rate (percentage)
    COMMISSION_RATE = int(os.getenv("COMMISSION_RATE", 5))
    
    # Bot Settings
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Subscription Plans
PLANS = {
    "free": {
        "name": "رایگان",
        "price": 0,
        "max_products": 10,
        "payment_gateway": True,
        "advanced_reports": False,
        "auto_messages": False,
        "discounts": False,
        "ads": False,
        "commission": 5,
        "duration_days": 30
    },
    "professional": {
        "name": "حرفه‌ای",
        "price": Config.PROFESSIONAL_PLAN_PRICE,
        "max_products": 200,
        "payment_gateway": True,
        "advanced_reports": True,
        "auto_messages": True,
        "discounts": True,
        "ads": True,
        "commission": 5,
        "duration_days": 30
    },
    "vip": {
        "name": "VIP",
        "price": Config.VIP_PLAN_PRICE,
        "max_products": -1,  # Unlimited
        "payment_gateway": True,
        "advanced_reports": True,
        "auto_messages": True,
        "discounts": True,
        "ads": True,
        "commission": 0,  # No commission
        "duration_days": 30
    }
}