import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    API_ID = int(os.getenv('API_ID')) if os.getenv('API_ID') else None
    API_HASH = os.getenv('API_HASH')
    
    # Admin Configuration
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID')) if os.getenv('ADMIN_USER_ID') else None
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    
    # Mode Configuration
    DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    PRODUCTION_MODE = os.getenv('PRODUCTION_MODE', 'true').lower() == 'true'
    
    # Database Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'coderoot_production')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Payment Configuration
    CARD_NUMBER = os.getenv('CARD_NUMBER', '6037-9977-7766-5544')
    CARD_HOLDER_NAME = os.getenv('CARD_HOLDER_NAME', 'حادی')
    
    # Channel Configuration
    MAIN_CHANNEL_ID = int(os.getenv('MAIN_CHANNEL_ID', '-1001234567890'))
    MAIN_CHANNEL_USERNAME = os.getenv('MAIN_CHANNEL_USERNAME', 'coderoot_channel')
    
    # Pricing Configuration
    PROFESSIONAL_PLAN_PRICE = int(os.getenv('PROFESSIONAL_PLAN_PRICE', '20000'))
    VIP_PLAN_PRICE = int(os.getenv('VIP_PLAN_PRICE', '60000'))
    COMMISSION_RATE = int(os.getenv('COMMISSION_RATE', '5'))
    
    # Bot Settings
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'coderoot_main_bot')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    
    # Sub-bot Creation
    BOTFATHER_TOKEN = os.getenv('BOTFATHER_TOKEN', '')
    SUB_BOT_PREFIX = os.getenv('SUB_BOT_PREFIX', 'shop_')
    
    # Backup and Logging
    BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/coderoot.log')
    
    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@coderoot.com')
    
    # Notification Settings
    TELEGRAM_NOTIFICATIONS = os.getenv('TELEGRAM_NOTIFICATIONS', 'true').lower() == 'true'
    EMAIL_NOTIFICATIONS = os.getenv('EMAIL_NOTIFICATIONS', 'false').lower() == 'true'
    
    # Security
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', '5'))
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')
    
    # Performance
    MAX_CONCURRENT_USERS = int(os.getenv('MAX_CONCURRENT_USERS', '1000'))
    CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))
    
    # Referral System
    REFERRAL_COMMISSION = int(os.getenv('REFERRAL_COMMISSION', '10'))
    REFERRAL_LEVELS = int(os.getenv('REFERRAL_LEVELS', '3'))
    
    # Language Settings
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'fa')
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'fa,en,ar').split(',')
    
    # AI Service Configuration (Enhanced with Gemini 2.0 Flash)
    AI_ENABLED = os.getenv('AI_ENABLED', 'true').lower() == 'true'
    AI_BASE_URL = os.getenv('AI_BASE_URL', '')
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'google/gemini-2.0-flash-001')
    AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '1200'))
    AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))
    AI_TOP_P = float(os.getenv('AI_TOP_P', '0.9'))
    AI_FREQUENCY_PENALTY = float(os.getenv('AI_FREQUENCY_PENALTY', '0.1'))
    AI_PRESENCE_PENALTY = float(os.getenv('AI_PRESENCE_PENALTY', '0.1'))
    
    # File Storage Configuration (S3/MinIO)
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'coderoot-files')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', '')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', '')
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', '')
    S3_REGION = os.getenv('S3_REGION', 'us-east-1')
    
    # Backup Configuration
    BACKUP_S3_BUCKET = os.getenv('BACKUP_S3_BUCKET', 'coderoot-backups')
    BACKUP_INTERVAL_HOURS = int(os.getenv('BACKUP_INTERVAL_HOURS', '24'))
    BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
    AUTO_BACKUP_ENABLED = os.getenv('AUTO_BACKUP_ENABLED', 'true').lower() == 'true'
    
    @classmethod
    def validate_required_config(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            ('BOT_TOKEN', cls.BOT_TOKEN),
            ('API_ID', cls.API_ID),
            ('API_HASH', cls.API_HASH),
            ('ADMIN_USER_ID', cls.ADMIN_USER_ID)
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)
        
        if missing_vars:
            raise ValueError(f"Missing required configuration: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_database_url(cls):
        """Get the complete database URL"""
        return f"{cls.MONGO_URI}{cls.DATABASE_NAME}"

# Subscription Plans Configuration
PLANS = {
    'free': {
        'name': 'رایگان',
        'name_en': 'Free',
        'name_ar': 'مجاني',
        'price': 0,
        'max_products': 10,
        'features': {
            'payment_gateway': 'bale',
            'reports': 'basic',
            'auto_messages': False,
            'discounts': False,
            'ads': False,
            'commission': 5,
            'priority_support': False,
            'custom_domain': False,
            'analytics': 'basic',
            'bulk_upload': False,
            'api_access': False
        },
        'description': 'پلن رایگان برای شروع کسب و کار',
        'description_en': 'Free plan to start your business',
        'description_ar': 'خطة مجانية لبدء عملك',
        'duration_days': 30
    },
    'professional': {
        'name': 'حرفه‌ای',
        'name_en': 'Professional',
        'name_ar': 'محترف',
        'price': Config.PROFESSIONAL_PLAN_PRICE,
        'max_products': 200,
        'features': {
            'payment_gateway': 'bale_plus',
            'reports': 'advanced',
            'auto_messages': True,
            'discounts': True,
            'ads': True,
            'commission': 5,
            'priority_support': True,
            'custom_domain': False,
            'analytics': 'advanced',
            'bulk_upload': True,
            'api_access': False
        },
        'description': 'پلن حرفه‌ای برای فروشندگان جدی',
        'description_en': 'Professional plan for serious sellers',
        'description_ar': 'خطة احترافية للبائعين الجادين',
        'duration_days': 30
    },
    'vip': {
        'name': 'VIP',
        'name_en': 'VIP',
        'name_ar': 'VIP',
        'price': Config.VIP_PLAN_PRICE,
        'max_products': float('inf'),
        'features': {
            'payment_gateway': 'dedicated',
            'reports': 'complete',
            'auto_messages': True,
            'discounts': True,
            'ads': 'premium',
            'commission': 0,
            'priority_support': True,
            'custom_domain': True,
            'analytics': 'complete',
            'bulk_upload': True,
            'api_access': True
        },
        'description': 'پلن VIP با امکانات کامل و بدون کارمزد',
        'description_en': 'VIP plan with full features and zero commission',
        'description_ar': 'خطة VIP مع ميزات كاملة وبدون عمولة',
        'duration_days': 30
    }
}

# Referral System Configuration
REFERRAL_CONFIG = {
    'commission_percentage': Config.REFERRAL_COMMISSION,
    'max_levels': Config.REFERRAL_LEVELS,
    'min_payout': 50000,  # Minimum amount for payout in Tomans
    'code_length': 8,
    'code_prefix': 'CR',
    'bonus_for_first_referral': 10000  # Bonus for first successful referral
}

# Bot Features Configuration
FEATURES = {
    'channel_join_required': True,
    'auto_backup': Config.BACKUP_ENABLED,
    'multi_language': True,
    'referral_system': True,
    'email_notifications': Config.EMAIL_NOTIFICATIONS,
    'analytics_tracking': True,
    'sub_bot_creation': True,
    'payment_reminders': True,
    'bulk_operations': True
}

# Notification Templates
NOTIFICATION_TEMPLATES = {
    'welcome': {
        'fa': '🎉 به CodeRoot خوش آمدید!\n\nشما می‌توانید فروشگاه اختصاصی خود را بسازید.',
        'en': '🎉 Welcome to CodeRoot!\n\nYou can create your own exclusive shop.',
        'ar': '🎉 مرحبا بك في CodeRoot!\n\nيمكنك إنشاء متجرك الحصري.'
    },
    'shop_created': {
        'fa': '✅ فروشگاه شما با موفقیت ایجاد شد!\n\nنام فروشگاه: {shop_name}\nربات فروشگاه: @{bot_username}',
        'en': '✅ Your shop has been created successfully!\n\nShop Name: {shop_name}\nShop Bot: @{bot_username}',
        'ar': '✅ تم إنشاء متجرك بنجاح!\n\nاسم المتجر: {shop_name}\nبوت المتجر: @{bot_username}'
    },
    'payment_received': {
        'fa': '💰 پرداخت شما دریافت شد!\n\nمبلغ: {amount} تومان\nپلن: {plan_name}',
        'en': '💰 Your payment has been received!\n\nAmount: {amount} Tomans\nPlan: {plan_name}',
        'ar': '💰 تم استلام دفعتك!\n\nالمبلغ: {amount} تومان\nالخطة: {plan_name}'
    }
}

# Upload Limits
UPLOAD_LIMITS = {
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'allowed_image_formats': ['jpg', 'jpeg', 'png', 'webp'],
    'allowed_video_formats': ['mp4', 'mov', 'avi'],
    'allowed_document_formats': ['pdf', 'doc', 'docx', 'txt'],
    'max_images_per_product': 10,
    'max_videos_per_product': 3
}

# Rate Limits
RATE_LIMITS = {
    'messages_per_minute': 30,
    'commands_per_minute': 10,
    'shop_creation_per_day': 1,
    'product_creation_per_hour': 50,
    'admin_commands_per_minute': 100
}