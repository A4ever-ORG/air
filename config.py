import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for CodeRoot Bot"""
    
    # Telegram Bot Configuration (Required)
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # API Configuration - Use demo values if not provided
    API_ID = int(os.getenv("API_ID", "12345678"))  # Demo value
    API_HASH = os.getenv("API_HASH", "abcdef1234567890abcdef1234567890")  # Demo value
    
    # Admin Configuration
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "7707164235"))
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "hadi_admin")
    
    # Demo Mode
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
    
    # Payment Configuration (Optional in demo)
    CARD_NUMBER = os.getenv("CARD_NUMBER", "6037-9977-7766-5544")
    CARD_HOLDER_NAME = os.getenv("CARD_HOLDER_NAME", "حادی")
    
    # Channel Configuration (Optional in demo)
    MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID")
    MAIN_CHANNEL_USERNAME = os.getenv("MAIN_CHANNEL_USERNAME")
    
    # Subscription Plans Pricing (in Tomans)
    PROFESSIONAL_PLAN_PRICE = int(os.getenv("PROFESSIONAL_PLAN_PRICE", "20000"))
    VIP_PLAN_PRICE = int(os.getenv("VIP_PLAN_PRICE", "60000"))
    
    # Commission Rate (percentage)
    COMMISSION_RATE = int(os.getenv("COMMISSION_RATE", "5"))
    
    # Bot Settings
    BOT_USERNAME = os.getenv("BOT_USERNAME", "coderoot_demo_bot")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    # Database Configuration (Not used in demo)
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "coderoot_demo")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    @classmethod
    def validate_required_config(cls):
        """Validate required configuration for demo mode"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required!")
        
        if not cls.ADMIN_USER_ID:
            raise ValueError("ADMIN_USER_ID is required!")
        
        # In demo mode, we don't need real API_ID and API_HASH
        # Pyrogram will handle them or we'll use session string
        
        return True

# Subscription plans configuration
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
        "commission": 0,  # No commission for VIP
        "duration_days": 30
    }
}