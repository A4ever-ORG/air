"""
Multi-language support for CodeRoot Bot
Provides translation system for Persian, English, and Arabic languages
"""

import re
from enum import Enum
from typing import Dict, Optional, Any
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Languages(Enum):
    """Supported languages"""
    PERSIAN = "fa"
    ENGLISH = "en"
    ARABIC = "ar"


class Translator:
    """Translation and localization manager"""
    
    def __init__(self, default_language: str = "fa"):
        self.default_language = default_language
        self.translations = TRANSLATIONS
    
    def get_text(self, key: str, language: str = None, **kwargs) -> str:
        """Get translated text by key"""
        lang = language or self.default_language
        
        # Get translation from nested structure
        text = self._get_nested_text(self.translations, key, lang)
        
        if text is None:
            # Fallback to default language
            text = self._get_nested_text(self.translations, key, self.default_language)
        
        if text is None:
            return key  # Return key if no translation found
        
        # Format with provided arguments
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    
    def _get_nested_text(self, data: Dict, key: str, language: str) -> Optional[str]:
        """Get text from nested dictionary structure"""
        try:
            # Split key by dots for nested access
            keys = key.split('.')
            
            # Navigate through nested structure
            current = data
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return None
            
            # Return text for the language
            if isinstance(current, dict) and language in current:
                return current[language]
            
            return None
        except:
            return None
    
    def get_language_selection_keyboard(self) -> InlineKeyboardMarkup:
        """Generate language selection keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ],
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")]
        ])
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return {
            "fa": "🇮🇷 فارسی",
            "en": "🇺🇸 English", 
            "ar": "🇸🇦 العربية"
        }
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on character sets"""
        if not text:
            return self.default_language
        
        # Count characters in different scripts
        persian_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F]', text))
        latin_chars = len(re.findall(r'[a-zA-Z]', text))
        
        total_chars = len(re.findall(r'[a-zA-Z\u0600-\u06FF\u0750-\u077F]', text))
        
        if total_chars == 0:
            return self.default_language
        
        # Simple heuristic
        if persian_chars / total_chars > 0.3:
            return "fa"
        elif latin_chars / total_chars > 0.5:
            return "en"
        elif arabic_chars / total_chars > 0.3:
            return "ar"
        
        return self.default_language


class LocalFormatter:
    """Locale-specific formatting"""
    
    @staticmethod
    def format_number(number: int, language: str = "fa") -> str:
        """Format number according to locale"""
        if language == "fa":
            # Persian numbers
            persian_digits = "۰۱۲۳۴۵۶۷۸۹"
            english_digits = "0123456789"
            
            formatted = f"{number:,}"
            for i, digit in enumerate(english_digits):
                formatted = formatted.replace(digit, persian_digits[i])
            
            return formatted
        elif language == "ar":
            # Arabic numbers
            arabic_digits = "٠١٢٣٤٥٦٧٨٩"
            english_digits = "0123456789"
            
            formatted = f"{number:,}"
            for i, digit in enumerate(english_digits):
                formatted = formatted.replace(digit, arabic_digits[i])
            
            return formatted
        else:
            return f"{number:,}"
    
    @staticmethod
    def format_currency(amount: int, language: str = "fa") -> str:
        """Format currency according to locale"""
        formatted_number = LocalFormatter.format_number(amount, language)
        
        if language == "fa":
            return f"{formatted_number} تومان"
        elif language == "ar":
            return f"{formatted_number} تومان"
        else:
            return f"{formatted_number} Tomans"
    
    @staticmethod
    def format_date(date_str: str, language: str = "fa") -> str:
        """Format date according to locale"""
        # This is a simplified version - in production you'd use proper date libraries
        if language == "fa":
            # Convert to Persian calendar if needed
            return date_str  # Placeholder
        elif language == "ar":
            return date_str  # Placeholder
        else:
            return date_str


class LanguageDetector:
    """Advanced language detection"""
    
    @staticmethod
    def detect_from_text(text: str) -> str:
        """Detect language from text content"""
        if not text:
            return "fa"
        
        # Character frequency analysis
        char_counts = {
            'persian': 0,
            'arabic': 0,
            'english': 0
        }
        
        for char in text:
            if '\u0600' <= char <= '\u06FF':  # Persian/Arabic range
                if char in 'پچژگ':  # Persian-specific characters
                    char_counts['persian'] += 2
                else:
                    char_counts['persian'] += 1
                    char_counts['arabic'] += 1
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                char_counts['english'] += 1
        
        # Return language with highest score
        max_lang = max(char_counts, key=char_counts.get)
        
        if max_lang == 'persian':
            return 'fa'
        elif max_lang == 'arabic':
            return 'ar'
        else:
            return 'en'
    
    @staticmethod
    def detect_from_locale(locale_str: str) -> str:
        """Detect language from locale string"""
        locale_map = {
            'fa': 'fa', 'fa_IR': 'fa', 'persian': 'fa',
            'en': 'en', 'en_US': 'en', 'en_GB': 'en', 'english': 'en',
            'ar': 'ar', 'ar_SA': 'ar', 'arabic': 'ar'
        }
        
        return locale_map.get(locale_str.lower(), 'fa')


# Translation dictionary with nested structure
TRANSLATIONS = {
    # Welcome and basic messages
    "welcome_message": {
        "fa": "🎉 سلام {name} عزیز!\n\nبه **CodeRoot** خوش آمدید! 🚀\n\n🏪 ایجاد فروشگاه آنلاین\n✨ مدیریت محصولات\n📊 گزارش‌گیری پیشرفته\n💰 درآمدزایی\n\nیکی از گزینه‌های زیر را انتخاب کنید:",
        "en": "🎉 Hello dear {name}!\n\nWelcome to **CodeRoot**! 🚀\n\n🏪 Create Online Store\n✨ Manage Products\n📊 Advanced Reports\n💰 Earn Money\n\nChoose one of the options below:",
        "ar": "🎉 مرحباً عزيزي {name}!\n\nأهلاً بك في **CodeRoot**! 🚀\n\n🏪 إنشاء متجر إلكتروني\n✨ إدارة المنتجات\n📊 تقارير متقدمة\n💰 كسب المال\n\nاختر أحد الخيارات أدناه:"
    },
    
    "help_message": {
        "fa": "📖 **راهنمای CodeRoot**\n\n🚀 **دستورات اصلی:**\n/start - شروع یا بازگشت به منوی اصلی\n/help - نمایش این راهنما\n/shop - مدیریت فروشگاه\n/profile - پروفایل کاربری\n/referral - سیستم معرفی\n\n🏪 **قابلیت‌های اصلی:**\n• ایجاد فروشگاه آنلاین\n• مدیریت محصولات\n• پردازش سفارش‌ها\n• گزارش‌گیری فروش\n• سیستم معرفی و درآمد",
        "en": "📖 **CodeRoot Guide**\n\n🚀 **Main Commands:**\n/start - Start or return to main menu\n/help - Show this guide\n/shop - Shop management\n/profile - User profile\n/referral - Referral system\n\n🏪 **Main Features:**\n• Create online store\n• Product management\n• Order processing\n• Sales reports\n• Referral and earning system",
        "ar": "📖 **دليل CodeRoot**\n\n🚀 **الأوامر الرئيسية:**\n/start - البدء أو العودة للقائمة الرئيسية\n/help - عرض هذا الدليل\n/shop - إدارة المتجر\n/profile - الملف الشخصي\n/referral - نظام الإحالة\n\n🏪 **الميزات الرئيسية:**\n• إنشاء متجر إلكتروني\n• إدارة المنتجات\n• معالجة الطلبات\n• تقارير المبيعات\n• نظام الإحالة والأرباح"
    },
    
    "unknown_command": {
        "fa": "❓ دستور نامشخص. لطفاً از منوی زیر انتخاب کنید:",
        "en": "❓ Unknown command. Please choose from the menu below:",
        "ar": "❓ أمر غير معروف. يرجى الاختيار من القائمة أدناه:"
    },
    
    "language_selected": {
        "fa": "✅ زبان فارسی انتخاب شد",
        "en": "✅ English language selected",
        "ar": "✅ تم اختيار اللغة العربية"
    },
    
    # Channel membership
    "channel_join_required": {
        "fa": "📢 **عضویت در کانال الزامی است**\n\nبرای استفاده از ربات، ابتدا در کانال ما عضو شوید و سپس دکمه «عضو شدم» را بزنید.",
        "en": "📢 **Channel membership required**\n\nTo use the bot, first join our channel and then click the 'I Joined' button.",
        "ar": "📢 **العضوية في القناة مطلوبة**\n\nلاستخدام البوت، انضم أولاً لقناتنا ثم اضغط على زر 'انضممت'."
    },
    
    # Shop related
    "shop_plans_info": {
        "fa": "🏪 **انتخاب پلن اشتراک**\n\nپلن مناسب خود را برای شروع کسب‌وکار انتخاب کنید:\n\n🆓 **رایگان:** 10 محصول، درگاه بله، کارمزد 5%\n⭐ **حرفه‌ای:** 200 محصول، گزارش پیشرفته، کارمزد 5%\n👑 **VIP:** نامحدود، درگاه اختصاصی، بدون کارمزد",
        "en": "🏪 **Select Subscription Plan**\n\nChoose the right plan to start your business:\n\n🆓 **Free:** 10 products, Bale gateway, 5% commission\n⭐ **Professional:** 200 products, advanced reports, 5% commission\n👑 **VIP:** Unlimited, dedicated gateway, no commission",
        "ar": "🏪 **اختيار خطة الاشتراك**\n\nاختر الخطة المناسبة لبدء عملك:\n\n🆓 **مجاني:** 10 منتجات، بوابة بيل، عمولة 5%\n⭐ **احترافي:** 200 منتج، تقارير متقدمة، عمولة 5%\n👑 **VIP:** غير محدود، بوابة مخصصة، بدون عمولة"
    },
    
    "shop_info": {
        "fa": "🏪 **فروشگاه: {shop_name}**\n\n💎 پلن: {plan}\n📊 وضعیت: {status}\n\nاز منوی زیر گزینه مورد نظر را انتخاب کنید:",
        "en": "🏪 **Shop: {shop_name}**\n\n💎 Plan: {plan}\n📊 Status: {status}\n\nChoose your desired option from the menu below:",
        "ar": "🏪 **المتجر: {shop_name}**\n\n💎 الخطة: {plan}\n📊 الحالة: {status}\n\nاختر الخيار المطلوب من القائمة أدناه:"
    },
    
    "enter_shop_name": {
        "fa": "🏪 **ایجاد فروشگاه جدید**\n\nنام فروشگاه خود را وارد کنید:\n\n🔸 نام باید بین 3 تا 50 کاراکتر باشد\n🔸 از کاراکترهای فارسی و انگلیسی استفاده کنید",
        "en": "🏪 **Create New Shop**\n\nEnter your shop name:\n\n🔸 Name should be 3-50 characters\n🔸 Use Persian and English characters",
        "ar": "🏪 **إنشاء متجر جديد**\n\nأدخل اسم متجرك:\n\n🔸 يجب أن يكون الاسم 3-50 حرفاً\n🔸 استخدم الأحرف الفارسية والإنجليزية"
    },
    
    # Profile related
    "profile_info": {
        "fa": "👤 **پروفایل کاربری**\n\n🆔 شناسه: {name}\n📱 یوزرنیم: {username}\n📅 تاریخ عضویت: {join_date}\n🎁 تعداد معرفی‌ها: {referral_count}\n💰 کل درآمد: {total_earnings}",
        "en": "👤 **User Profile**\n\n🆔 ID: {name}\n📱 Username: {username}\n📅 Join Date: {join_date}\n🎁 Referrals: {referral_count}\n💰 Total Earnings: {total_earnings}",
        "ar": "👤 **الملف الشخصي**\n\n🆔 المعرف: {name}\n📱 اسم المستخدم: {username}\n📅 تاريخ الانضمام: {join_date}\n🎁 الإحالات: {referral_count}\n💰 إجمالي الأرباح: {total_earnings}"
    },
    
    # Referral system
    "referral_info": {
        "fa": "🎁 **سیستم معرفی CodeRoot**\n\n🔗 **کد معرف شما:** `{referral_code}`\n📱 **لینک معرف:**\n{referral_link}\n\n📊 **آمار معرفی:**\n👥 تعداد: {referral_count}\n💰 کمیسیون: {commission}%\n\n🚀 لینک خود را به‌اشتراک بگذارید!",
        "en": "🎁 **CodeRoot Referral System**\n\n🔗 **Your Referral Code:** `{referral_code}`\n📱 **Referral Link:**\n{referral_link}\n\n📊 **Referral Stats:**\n👥 Count: {referral_count}\n💰 Commission: {commission}%\n\n🚀 Share your link!",
        "ar": "🎁 **نظام إحالة CodeRoot**\n\n🔗 **كود الإحالة:** `{referral_code}`\n📱 **رابط الإحالة:**\n{referral_link}\n\n📊 **إحصائيات الإحالة:**\n👥 العدد: {referral_count}\n💰 العمولة: {commission}%\n\n🚀 شارك رابطك!"
    },
    
    # Error messages
    "error": {
        "generic": {
            "fa": "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.",
            "en": "❌ An error occurred. Please try again.",
            "ar": "❌ حدث خطأ. يرجى المحاولة مرة أخرى."
        },
        "permission_denied": {
            "fa": "❌ شما مجوز انجام این عملیات را ندارید.",
            "en": "❌ You don't have permission to perform this action.",
            "ar": "❌ ليس لديك إذن لتنفيذ هذا الإجراء."
        },
        "invalid_input": {
            "fa": "❌ ورودی نامعتبر. لطفاً دوباره تلاش کنید.",
            "en": "❌ Invalid input. Please try again.",
            "ar": "❌ إدخال غير صالح. يرجى المحاولة مرة أخرى."
        }
    },
    
    # Success messages
    "success": {
        "generic": {
            "fa": "✅ عملیات با موفقیت انجام شد.",
            "en": "✅ Operation completed successfully.",
            "ar": "✅ تمت العملية بنجاح."
        },
        "saved": {
            "fa": "✅ اطلاعات ذخیره شد.",
            "en": "✅ Information saved.",
            "ar": "✅ تم حفظ المعلومات."
        }
    },
    
    # Buttons and actions
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
        "save": {
            "fa": "💾 ذخیره",
            "en": "💾 Save",
            "ar": "💾 حفظ"
        },
        "edit": {
            "fa": "✏️ ویرایش",
            "en": "✏️ Edit",
            "ar": "✏️ تحرير"
        },
        "delete": {
            "fa": "🗑 حذف",
            "en": "🗑 Delete",
            "ar": "🗑 حذف"
        },
        "view": {
            "fa": "👁 مشاهده",
            "en": "👁 View",
            "ar": "👁 عرض"
        }
    },
    
    # Status messages
    "status": {
        "active": {
            "fa": "فعال",
            "en": "Active",
            "ar": "نشط"
        },
        "inactive": {
            "fa": "غیرفعال",
            "en": "Inactive",
            "ar": "غير نشط"
        },
        "pending": {
            "fa": "در انتظار",
            "en": "Pending",
            "ar": "معلق"
        },
        "suspended": {
            "fa": "تعلیق شده",
            "en": "Suspended",
            "ar": "معلق"
        },
        "completed": {
            "fa": "تکمیل شده",
            "en": "Completed",
            "ar": "مكتمل"
        },
        "cancelled": {
            "fa": "لغو شده",
            "en": "Cancelled",
            "ar": "ملغي"
        }
    },
    
    # Time and date
    "time": {
        "days": {
            "fa": "روز",
            "en": "days",
            "ar": "أيام"
        },
        "hours": {
            "fa": "ساعت",
            "en": "hours",
            "ar": "ساعات"
        },
        "minutes": {
            "fa": "دقیقه",
            "en": "minutes",
            "ar": "دقائق"
        },
        "seconds": {
            "fa": "ثانیه",
            "en": "seconds",
            "ar": "ثواني"
        }
    },
    
    # Currencies and numbers
    "currency": {
        "toman": {
            "fa": "تومان",
            "en": "Tomans",
            "ar": "تومان"
        },
        "rial": {
            "fa": "ریال",
            "en": "Rials",
            "ar": "ريال"
        }
    },
    
    "support_contact": {
        "fa": "برای تماس با پشتیبانی از طریق:\n📞 @hadi_admin\n📢 @coderoot_channel",
        "en": "To contact support via:\n📞 @hadi_admin\n📢 @coderoot_channel",
        "ar": "للاتصال بالدعم عبر:\n📞 @hadi_admin\n📢 @coderoot_channel"
    },
    
    # AI Support System
    "ai_support_intro": {
        "fa": "🤖 **پشتیبانی هوشمند CodeRoot**\n\nسلام! من دستیار هوشمند CodeRoot هستم. می‌تونم در موارد زیر کمکتون کنم:\n\n🏪 ایجاد فروشگاه\n💰 مسائل پرداخت\n📊 گزارش‌گیری\n🔧 مشکلات فنی\n📦 مدیریت محصولات\n\n**سوال خود را بپرسید یا از گزینه‌های زیر انتخاب کنید:**",
        "en": "🤖 **CodeRoot Smart Support**\n\nHello! I'm CodeRoot's AI assistant. I can help you with:\n\n🏪 Shop Creation\n💰 Payment Issues\n📊 Reports\n🔧 Technical Problems\n📦 Product Management\n\n**Ask your question or choose from options below:**",
        "ar": "🤖 **دعم CodeRoot الذكي**\n\nمرحباً! أنا مساعد CodeRoot الذكي. يمكنني مساعدتك في:\n\n🏪 إنشاء المتجر\n💰 مشاكل الدفع\n📊 التقارير\n🔧 المشاكل التقنية\n📦 إدارة المنتجات\n\n**اسأل سؤالك أو اختر من الخيارات أدناه:**"
    },
    
    "ai_thinking": {
        "fa": "🤔 در حال پردازش پاسخ...",
        "en": "🤔 Processing your response...",
        "ar": "🤔 معالجة ردك..."
    },
    
    "ai_support_ended": {
        "fa": "✅ پشتیبانی هوشمند پایان یافت.\n\nبرای مراجعه مجدد از منوی اصلی گزینه پشتیبانی را انتخاب کنید.",
        "en": "✅ Smart support session ended.\n\nTo return, select Support from the main menu.",
        "ar": "✅ انتهت جلسة الدعم الذكي.\n\nللعودة، اختر الدعم من القائمة الرئيسية."
    }
}