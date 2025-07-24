"""
Multi-language support for CodeRoot Bot
پشتیبانی چندزبانه ربات CodeRoot
دعم متعدد اللغات لبوت CodeRoot
"""

from typing import Dict, Any

class Languages:
    """Language definitions"""
    PERSIAN = "fa"
    ENGLISH = "en" 
    ARABIC = "ar"

# Translation dictionaries
TRANSLATIONS = {
    "language_selection": {
        "fa": "🌍 **زبان خود را انتخاب کنید:**\n\nلطفاً زبان مورد نظر خود را برای ادامه انتخاب کنید.",
        "en": "🌍 **Select your language:**\n\nPlease choose your preferred language to continue.",
        "ar": "🌍 **اختر لغتك:**\n\nيرجى اختيار اللغة المفضلة لديك للمتابعة."
    },
    
    "welcome_new_user": {
        "fa": "🎉 **سلام {name}!**\n\nبه **CodeRoot** خوش آمدید! 🚀\n\n🏪 **ایجاد فروشگاه آنلاین**\n✨ **مدیریت محصولات**\n📊 **گزارش‌گیری پیشرفته**\n💰 **درآمدزایی**\n\n🆔 **کد معرف شما:** `{referral_code}`\n\n👇 برای شروع، یکی از گزینه‌های زیر را انتخاب کنید:",
        "en": "🎉 **Hello {name}!**\n\nWelcome to **CodeRoot**! 🚀\n\n🏪 **Create Online Store**\n✨ **Product Management**\n📊 **Advanced Reporting**\n💰 **Revenue Generation**\n\n🆔 **Your referral code:** `{referral_code}`\n\n👇 Choose one of the options below to get started:",
        "ar": "🎉 **أهلاً {name}!**\n\nمرحباً بك في **CodeRoot**! 🚀\n\n🏪 **إنشاء متجر إلكتروني**\n✨ **إدارة المنتجات**\n📊 **تقارير متقدمة**\n💰 **توليد الإيرادات**\n\n🆔 **كود الإحالة الخاص بك:** `{referral_code}`\n\n👇 اختر أحد الخيارات أدناه للبدء:"
    },
    
    "welcome_returning_user": {
        "fa": "🔄 **سلام مجدد {name}!**\n\nخوش برگشتید به **CodeRoot** 🎉\n\n📊 **آمار شما:**\n🏪 فروشگاه‌ها: {total_shops}\n🛒 سفارش‌ها: {total_orders}\n💰 درآمد کل: {total_revenue:,} تومان\n\n👇 گزینه مورد نظر را انتخاب کنید:",
        "en": "🔄 **Welcome back {name}!**\n\nWelcome back to **CodeRoot** 🎉\n\n📊 **Your Stats:**\n🏪 Stores: {total_shops}\n🛒 Orders: {total_orders}\n💰 Total Revenue: {total_revenue:,} Toman\n\n👇 Choose your desired option:",
        "ar": "🔄 **أهلاً بعودتك {name}!**\n\nمرحباً بعودتك إلى **CodeRoot** 🎉\n\n📊 **إحصائياتك:**\n🏪 المتاجر: {total_shops}\n🛒 الطلبات: {total_orders}\n💰 إجمالي الإيرادات: {total_revenue:,} تومان\n\n👇 اختر الخيار المطلوب:"
    },
    
    "main_menu": {
        "create_shop": {
            "fa": "🏪 ایجاد فروشگاه",
            "en": "🏪 Create Store", 
            "ar": "🏪 إنشاء متجر"
        },
        "my_shop": {
            "fa": "🛍 فروشگاه من",
            "en": "🛍 My Store",
            "ar": "🛍 متجري"
        },
        "profile": {
            "fa": "👤 پروفایل",
            "en": "👤 Profile",
            "ar": "👤 الملف الشخصي"
        },
        "referral": {
            "fa": "🎁 معرفی دوستان",
            "en": "🎁 Refer Friends",
            "ar": "🎁 إحالة الأصدقاء"
        },
        "support": {
            "fa": "🆘 پشتیبانی",
            "en": "🆘 Support",
            "ar": "🆘 الدعم"
        },
        "tutorial": {
            "fa": "📚 آموزش",
            "en": "📚 Tutorial",
            "ar": "📚 التعليمات"
        },
        "rules": {
            "fa": "📜 قوانین",
            "en": "📜 Rules",
            "ar": "📜 القواعد"
        },
        "settings": {
            "fa": "⚙️ تنظیمات",
            "en": "⚙️ Settings",
            "ar": "⚙️ الإعدادات"
        },
        "language": {
            "fa": "🌍 تغییر زبان",
            "en": "🌍 Change Language",
            "ar": "🌍 تغيير اللغة"
        }
    },
    
    "shop_plans": {
        "title": {
            "fa": "🏪 **ایجاد فروشگاه جدید**\n\nبرای شروع کسب‌وکار آنلاین، پلن مناسب خود را انتخاب کنید:\n\n👇 هر پلن شامل ویژگی‌های خاص خود است:",
            "en": "🏪 **Create New Store**\n\nTo start your online business, choose the right plan:\n\n👇 Each plan includes its special features:",
            "ar": "🏪 **إنشاء متجر جديد**\n\nلبدء عملك التجاري عبر الإنترنت، اختر الخطة المناسبة:\n\n👇 كل خطة تشمل ميزاتها الخاصة:"
        },
        "free": {
            "fa": "🆓 رایگان",
            "en": "🆓 Free",
            "ar": "🆓 مجاني"
        },
        "professional": {
            "fa": "⭐ حرفه‌ای",
            "en": "⭐ Professional", 
            "ar": "⭐ احترافي"
        },
        "vip": {
            "fa": "👑 VIP",
            "en": "👑 VIP",
            "ar": "👑 VIP"
        }
    },
    
    "errors": {
        "invalid_input": {
            "fa": "❌ ورودی نامعتبر است. لطفاً دوباره تلاش کنید.",
            "en": "❌ Invalid input. Please try again.",
            "ar": "❌ إدخال غير صالح. يرجى المحاولة مرة أخرى."
        },
        "permission_denied": {
            "fa": "❌ شما مجوز دسترسی به این بخش را ندارید.",
            "en": "❌ You don't have permission to access this section.",
            "ar": "❌ ليس لديك إذن للوصول إلى هذا القسم."
        },
        "something_went_wrong": {
            "fa": "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.",
            "en": "❌ Something went wrong. Please try again.",
            "ar": "❌ حدث خطأ ما. يرجى المحاولة مرة أخرى."
        }
    },
    
    "success": {
        "saved": {
            "fa": "✅ با موفقیت ذخیره شد.",
            "en": "✅ Successfully saved.",
            "ar": "✅ تم الحفظ بنجاح."
        },
        "updated": {
            "fa": "✅ با موفقیت بروزرسانی شد.",
            "en": "✅ Successfully updated.", 
            "ar": "✅ تم التحديث بنجاح."
        },
        "deleted": {
            "fa": "✅ با موفقیت حذف شد.",
            "en": "✅ Successfully deleted.",
            "ar": "✅ تم الحذف بنجاح."
        }
    },
    
    "channel_join_required": {
        "fa": "📢 **عضویت در کانال الزامی است**\n\nبرای استفاده از ربات، ابتدا در کانال ما عضو شوید:\n👇 @{channel}\n\nبعد از عضویت، دوباره /start کنید.",
        "en": "📢 **Channel membership required**\n\nTo use the bot, first join our channel:\n👇 @{channel}\n\nAfter joining, /start again.",
        "ar": "📢 **العضوية في القناة مطلوبة**\n\nلاستخدام البوت، انضم أولاً إلى قناتنا:\n👇 @{channel}\n\nبعد الانضمام، أعد كتابة /start."
    },
    
    "join_channel": {
        "fa": "🔗 عضویت در کانال",
        "en": "🔗 Join Channel",
        "ar": "🔗 انضم للقناة"
    },
    
    "joined": {
        "fa": "✅ عضو شدم",
        "en": "✅ I Joined",
        "ar": "✅ انضممت"
    },
    
    "help_text": {
        "fa": "📖 **راهنمای CodeRoot**\n\n🚀 **دستورات اصلی:**\n/start - شروع یا بازگشت به منوی اصلی\n/help - نمایش این راهنما\n/shop - مدیریت فروشگاه\n/profile - پروفایل کاربری\n/referral - سیستم معرفی\n\n🏪 **قابلیت‌های اصلی:**\n• ایجاد فروشگاه آنلاین\n• مدیریت محصولات\n• پردازش سفارش‌ها\n• گزارش‌گیری فروش\n• سیستم معرفی و درآمد\n\n🆘 برای پشتیبانی با مدیر تماس بگیرید.",
        "en": "📖 **CodeRoot Guide**\n\n🚀 **Main Commands:**\n/start - Start or return to main menu\n/help - Show this guide\n/shop - Manage store\n/profile - User profile\n/referral - Referral system\n\n🏪 **Main Features:**\n• Create online store\n• Product management\n• Order processing\n• Sales reporting\n• Referral and income system\n\nContact admin for support.",
        "ar": "📖 **دليل CodeRoot**\n\n🚀 **الأوامر الرئيسية:**\n/start - البدء أو العودة للقائمة الرئيسية\n/help - عرض هذا الدليل\n/shop - إدارة المتجر\n/profile - الملف الشخصي\n/referral - نظام الإحالة\n\n🏪 **الميزات الرئيسية:**\n• إنشاء متجر إلكتروني\n• إدارة المنتجات\n• معالجة الطلبات\n• تقارير المبيعات\n• نظام الإحالة والدخل\n\nاتصل بالمشرف للدعم."
    },
    
    "admin_panel": {
        "title": {
            "fa": "🔧 **پنل مدیریت CodeRoot**\n\n👋 سلام {name}!\n\n📊 **آمار کلی:**\n👥 کاربران: {users}\n🏪 فروشگاه‌ها: {shops}\n📦 محصولات: {products}\n\n⚙️ **عملیات مدیریت:**",
            "en": "🔧 **CodeRoot Admin Panel**\n\n👋 Hello {name}!\n\n📊 **General Stats:**\n👥 Users: {users}\n🏪 Stores: {shops}\n📦 Products: {products}\n\n⚙️ **Management Operations:**",
            "ar": "🔧 **لوحة إدارة CodeRoot**\n\n👋 أهلاً {name}!\n\n📊 **الإحصائيات العامة:**\n👥 المستخدمون: {users}\n🏪 المتاجر: {shops}\n📦 المنتجات: {products}\n\n⚙️ **عمليات الإدارة:**"
        },
        "manage_users": {
            "fa": "👥 مدیریت کاربران",
            "en": "👥 Manage Users",
            "ar": "👥 إدارة المستخدمين"
        },
        "manage_shops": {
            "fa": "🏪 مدیریت فروشگاه‌ها", 
            "en": "🏪 Manage Stores",
            "ar": "🏪 إدارة المتاجر"
        },
        "financial_report": {
            "fa": "💰 گزارش مالی",
            "en": "💰 Financial Report",
            "ar": "💰 التقرير المالي"
        },
        "statistics": {
            "fa": "📊 آمار کلی",
            "en": "📊 General Statistics", 
            "ar": "📊 الإحصائيات العامة"
        },
        "broadcast": {
            "fa": "📢 ارسال پیام همگانی",
            "en": "📢 Broadcast Message",
            "ar": "📢 إرسال رسالة جماعية"
        }
    },
    
    "buttons": {
        "back": {
            "fa": "🔙 بازگشت",
            "en": "🔙 Back",
            "ar": "🔙 رجوع"
        },
        "cancel": {
            "fa": "❌ لغو",
            "en": "❌ Cancel",
            "ar": "❌ إلغاء"
        },
        "confirm": {
            "fa": "✅ تأیید",
            "en": "✅ Confirm",
            "ar": "✅ تأكيد"
        },
        "next": {
            "fa": "▶️ بعدی",
            "en": "▶️ Next",
            "ar": "▶️ التالي"
        },
        "previous": {
            "fa": "◀️ قبلی",
            "en": "◀️ Previous",
            "ar": "◀️ السابق"
        },
        "home": {
            "fa": "🏠 منوی اصلی",
            "en": "🏠 Main Menu",
            "ar": "🏠 القائمة الرئيسية"
        }
    }
}

class Translator:
    """Translation utility class"""
    
    @staticmethod
    def get_text(key: str, lang: str = "fa", **kwargs) -> str:
        """Get translated text"""
        try:
            # Navigate through nested keys
            keys = key.split(".")
            text_dict = TRANSLATIONS
            
            for k in keys:
                text_dict = text_dict[k]
            
            # Get text for language or fallback to Persian
            text = text_dict.get(lang, text_dict.get("fa", key))
            
            # Format with provided kwargs
            if kwargs:
                return text.format(**kwargs)
            return text
            
        except (KeyError, TypeError):
            return key
    
    @staticmethod
    def get_language_selection_keyboard():
        """Get language selection keyboard"""
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")]
        ])
    
    @staticmethod
    def get_back_button(lang: str = "fa"):
        """Get back button in specified language"""
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        text = Translator.get_text("buttons.back", lang)
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text, callback_data="main_menu")]
        ])

# Language-specific formatting functions
class LocalFormatter:
    """Language-specific formatting utilities"""
    
    @staticmethod
    def format_number(number: int, lang: str = "fa") -> str:
        """Format number according to language"""
        if lang == "fa":
            # Persian digits
            persian_digits = "۰۱۲۳۴۵۶۷۸۹"
            english_digits = "0123456789"
            formatted = f"{number:,}"
            for i, digit in enumerate(english_digits):
                formatted = formatted.replace(digit, persian_digits[i])
            return formatted
        elif lang == "ar":
            # Arabic digits  
            arabic_digits = "٠١٢٣٤٥٦٧٨٩"
            english_digits = "0123456789"
            formatted = f"{number:,}"
            for i, digit in enumerate(english_digits):
                formatted = formatted.replace(digit, arabic_digits[i])
            return formatted
        else:
            return f"{number:,}"
    
    @staticmethod
    def format_currency(amount: float, lang: str = "fa") -> str:
        """Format currency according to language"""
        if lang == "fa":
            return f"{LocalFormatter.format_number(int(amount), lang)} تومان"
        elif lang == "ar":
            return f"{LocalFormatter.format_number(int(amount), lang)} تومان"
        else:
            return f"{LocalFormatter.format_number(int(amount), lang)} Toman"
    
    @staticmethod
    def format_date(date_obj, lang: str = "fa") -> str:
        """Format date according to language"""
        if lang == "fa":
            return date_obj.strftime("%Y/%m/%d")
        elif lang == "ar":
            return date_obj.strftime("%d/%m/%Y")
        else:
            return date_obj.strftime("%Y-%m-%d")

# Language detection
class LanguageDetector:
    """Detect user's preferred language"""
    
    @staticmethod
    def detect_from_text(text: str) -> str:
        """Detect language from text"""
        if not text:
            return Languages.PERSIAN
        
        # Simple character-based detection
        persian_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        arabic_chars = sum(1 for c in text if '\u0750' <= c <= '\u077F')
        english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        
        total_chars = len(text)
        if total_chars == 0:
            return Languages.PERSIAN
        
        persian_ratio = persian_chars / total_chars
        arabic_ratio = arabic_chars / total_chars  
        english_ratio = english_chars / total_chars
        
        if persian_ratio > 0.3:
            return Languages.PERSIAN
        elif arabic_ratio > 0.3:
            return Languages.ARABIC
        elif english_ratio > 0.3:
            return Languages.ENGLISH
        else:
            return Languages.PERSIAN
    
    @staticmethod
    def detect_from_locale(locale_code: str) -> str:
        """Detect language from locale code"""
        locale_map = {
            'fa': Languages.PERSIAN,
            'fa_IR': Languages.PERSIAN,
            'en': Languages.ENGLISH,
            'en_US': Languages.ENGLISH,
            'ar': Languages.ARABIC,
            'ar_SA': Languages.ARABIC
        }
        return locale_map.get(locale_code, Languages.PERSIAN)