"""
Keyboard markups for CodeRoot Bot
Contains all inline and reply keyboards used throughout the bot
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import PLANS


class Keyboards:
    """Static methods for generating keyboard markups"""
    
    @staticmethod
    def main_menu_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        texts = {
            'fa': {
                'shop': '🏪 فروشگاه من',
                'create_shop': '➕ ایجاد فروشگاه',
                'profile': '👤 پروفایل',
                'referral': '🎁 سیستم معرفی',
                'help': '❓ راهنما',
                'support': '🆘 پشتیبانی'
            },
            'en': {
                'shop': '🏪 My Shop',
                'create_shop': '➕ Create Shop',
                'profile': '👤 Profile',
                'referral': '🎁 Referral System',
                'help': '❓ Help',
                'support': '🆘 Support'
            },
            'ar': {
                'shop': '🏪 متجري',
                'create_shop': '➕ إنشاء متجر',
                'profile': '👤 الملف الشخصي',
                'referral': '🎁 نظام الإحالة',
                'help': '❓ مساعدة',
                'support': '🆘 الدعم'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['shop'], callback_data='shop_manage'),
                InlineKeyboardButton(text['create_shop'], callback_data='shop_create')
            ],
            [
                InlineKeyboardButton(text['profile'], callback_data='profile_show'),
                InlineKeyboardButton(text['referral'], callback_data='profile_referrals')
            ],
            [
                InlineKeyboardButton(text['help'], callback_data='help_show'),
                InlineKeyboardButton(text['support'], callback_data='support_contact')
            ]
        ])
    
    @staticmethod
    def shop_plans_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Shop subscription plans keyboard"""
        texts = {
            'fa': {
                'free': f"🆓 رایگان - {PLANS['free']['max_products']} محصول",
                'professional': f"⭐ حرفه‌ای - {PLANS['professional']['price']:,} تومان",
                'vip': f"👑 VIP - {PLANS['vip']['price']:,} تومان",
                'back': '🔙 بازگشت'
            },
            'en': {
                'free': f"🆓 Free - {PLANS['free']['max_products']} products",
                'professional': f"⭐ Professional - {PLANS['professional']['price']:,} Tomans",
                'vip': f"👑 VIP - {PLANS['vip']['price']:,} Tomans",
                'back': '🔙 Back'
            },
            'ar': {
                'free': f"🆓 مجاني - {PLANS['free']['max_products']} منتجات",
                'professional': f"⭐ احترافي - {PLANS['professional']['price']:,} تومان",
                'vip': f"👑 VIP - {PLANS['vip']['price']:,} تومان",
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text['free'], callback_data='shop_plan_free')],
            [InlineKeyboardButton(text['professional'], callback_data='shop_plan_professional')],
            [InlineKeyboardButton(text['vip'], callback_data='shop_plan_vip')],
            [InlineKeyboardButton(text['back'], callback_data='main_menu')]
        ])
    
    @staticmethod
    def shop_management_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Shop management keyboard"""
        texts = {
            'fa': {
                'products': '📦 مدیریت محصولات',
                'orders': '🛒 سفارش‌ها',
                'reports': '📊 گزارشات',
                'settings': '⚙️ تنظیمات',
                'bot': '🤖 ربات فروشگاه',
                'back': '🔙 بازگشت'
            },
            'en': {
                'products': '📦 Manage Products',
                'orders': '🛒 Orders',
                'reports': '📊 Reports',
                'settings': '⚙️ Settings',
                'bot': '🤖 Shop Bot',
                'back': '🔙 Back'
            },
            'ar': {
                'products': '📦 إدارة المنتجات',
                'orders': '🛒 الطلبات',
                'reports': '📊 التقارير',
                'settings': '⚙️ الإعدادات',
                'bot': '🤖 بوت المتجر',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['products'], callback_data='shop_products'),
                InlineKeyboardButton(text['orders'], callback_data='shop_orders')
            ],
            [
                InlineKeyboardButton(text['reports'], callback_data='shop_reports'),
                InlineKeyboardButton(text['settings'], callback_data='shop_settings')
            ],
            [InlineKeyboardButton(text['bot'], callback_data='shop_bot')],
            [InlineKeyboardButton(text['back'], callback_data='main_menu')]
        ])
    
    @staticmethod
    def admin_main_keyboard() -> InlineKeyboardMarkup:
        """Admin panel main keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton('👥 مدیریت کاربران', callback_data='admin_users'),
                InlineKeyboardButton('🏪 مدیریت فروشگاه‌ها', callback_data='admin_shops')
            ],
            [
                InlineKeyboardButton('📊 آمار و گزارشات', callback_data='admin_stats'),
                InlineKeyboardButton('💰 مدیریت پرداخت‌ها', callback_data='admin_payments')
            ],
            [
                InlineKeyboardButton('📢 ارسال پیام همگانی', callback_data='admin_broadcast'),
                InlineKeyboardButton('⚙️ تنظیمات سیستم', callback_data='admin_settings')
            ],
            [InlineKeyboardButton('🔙 بازگشت', callback_data='main_menu')]
        ])
    
    @staticmethod
    def admin_users_keyboard() -> InlineKeyboardMarkup:
        """Admin users management keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton('📋 لیست کاربران', callback_data='admin_users_list'),
                InlineKeyboardButton('🔍 جستجوی کاربر', callback_data='admin_users_search')
            ],
            [
                InlineKeyboardButton('📊 آمار کاربران', callback_data='admin_users_stats'),
                InlineKeyboardButton('🚫 مسدود کردن', callback_data='admin_users_block')
            ],
            [InlineKeyboardButton('🔙 بازگشت', callback_data='admin_main')]
        ])
    
    @staticmethod
    def admin_shops_keyboard() -> InlineKeyboardMarkup:
        """Admin shops management keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton('📋 لیست فروشگاه‌ها', callback_data='admin_shops_list'),
                InlineKeyboardButton('✅ تأیید فروشگاه‌ها', callback_data='admin_shops_approve')
            ],
            [
                InlineKeyboardButton('📊 آمار فروشگاه‌ها', callback_data='admin_shops_stats'),
                InlineKeyboardButton('🗑 حذف فروشگاه', callback_data='admin_shops_delete')
            ],
            [InlineKeyboardButton('🔙 بازگشت', callback_data='admin_main')]
        ])
    
    @staticmethod
    def admin_stats_keyboard() -> InlineKeyboardMarkup:
        """Admin statistics keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton('📈 آمار امروز', callback_data='admin_stats_today'),
                InlineKeyboardButton('📊 آمار هفتگی', callback_data='admin_stats_weekly')
            ],
            [
                InlineKeyboardButton('📋 آمار ماهانه', callback_data='admin_stats_monthly'),
                InlineKeyboardButton('💾 دریافت گزارش Excel', callback_data='admin_stats_export')
            ],
            [InlineKeyboardButton('🔙 بازگشت', callback_data='admin_main')]
        ])
    
    @staticmethod
    def profile_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """User profile keyboard"""
        texts = {
            'fa': {
                'settings': '⚙️ تنظیمات',
                'referrals': '🎁 معرفی‌ها',
                'payments': '💰 پرداخت‌ها',
                'language': '🌍 تغییر زبان',
                'back': '🔙 بازگشت'
            },
            'en': {
                'settings': '⚙️ Settings',
                'referrals': '🎁 Referrals',
                'payments': '💰 Payments',
                'language': '🌍 Change Language',
                'back': '🔙 Back'
            },
            'ar': {
                'settings': '⚙️ الإعدادات',
                'referrals': '🎁 الإحالات',
                'payments': '💰 المدفوعات',
                'language': '🌍 تغيير اللغة',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['settings'], callback_data='profile_settings'),
                InlineKeyboardButton(text['referrals'], callback_data='profile_referrals')
            ],
            [
                InlineKeyboardButton(text['payments'], callback_data='profile_payments'),
                InlineKeyboardButton(text['language'], callback_data='profile_language')
            ],
            [InlineKeyboardButton(text['back'], callback_data='main_menu')]
        ])
    
    @staticmethod
    def payment_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Payment keyboard"""
        texts = {
            'fa': {
                'card_to_card': '💳 کارت به کارت',
                'upload_receipt': '📤 آپلود رسید',
                'cancel': '❌ لغو'
            },
            'en': {
                'card_to_card': '💳 Card to Card',
                'upload_receipt': '📤 Upload Receipt',
                'cancel': '❌ Cancel'
            },
            'ar': {
                'card_to_card': '💳 من بطاقة إلى بطاقة',
                'upload_receipt': '📤 رفع الإيصال',
                'cancel': '❌ إلغاء'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text['card_to_card'], callback_data='payment_card_to_card')],
            [InlineKeyboardButton(text['upload_receipt'], callback_data='payment_upload_receipt')],
            [InlineKeyboardButton(text['cancel'], callback_data='payment_cancel')]
        ])
    
    @staticmethod
    def cancel_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Simple cancel keyboard"""
        texts = {
            'fa': '❌ لغو',
            'en': '❌ Cancel',
            'ar': '❌ إلغاء'
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text, callback_data='cancel')]
        ])
    
    @staticmethod
    def back_keyboard(language: str = 'fa', callback_data: str = 'main_menu') -> InlineKeyboardMarkup:
        """Simple back keyboard"""
        texts = {
            'fa': '🔙 بازگشت',
            'en': '🔙 Back',
            'ar': '🔙 رجوع'
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text, callback_data=callback_data)]
        ])
    
    @staticmethod
    def confirmation_keyboard(language: str = 'fa', confirm_data: str = 'confirm', cancel_data: str = 'cancel') -> InlineKeyboardMarkup:
        """Confirmation keyboard with yes/no options"""
        texts = {
            'fa': {
                'confirm': '✅ تأیید',
                'cancel': '❌ لغو'
            },
            'en': {
                'confirm': '✅ Confirm',
                'cancel': '❌ Cancel'
            },
            'ar': {
                'confirm': '✅ تأكيد',
                'cancel': '❌ إلغاء'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['confirm'], callback_data=confirm_data),
                InlineKeyboardButton(text['cancel'], callback_data=cancel_data)
            ]
        ])
    
    @staticmethod
    def shop_created_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Keyboard shown after shop creation"""
        texts = {
            'fa': {
                'manage': '🏪 مدیریت فروشگاه',
                'menu': '🏠 منوی اصلی'
            },
            'en': {
                'manage': '🏪 Manage Shop',
                'menu': '🏠 Main Menu'
            },
            'ar': {
                'manage': '🏪 إدارة المتجر',
                'menu': '🏠 القائمة الرئيسية'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text['manage'], callback_data='shop_manage')],
            [InlineKeyboardButton(text['menu'], callback_data='main_menu')]
        ])
    
    @staticmethod
    def pagination_keyboard(page: int, total_pages: int, prefix: str, language: str = 'fa') -> InlineKeyboardMarkup:
        """Pagination keyboard"""
        texts = {
            'fa': {
                'prev': '◀️ قبلی',
                'next': '▶️ بعدی',
                'page': f'صفحه {page}/{total_pages}'
            },
            'en': {
                'prev': '◀️ Previous',
                'next': '▶️ Next',
                'page': f'Page {page}/{total_pages}'
            },
            'ar': {
                'prev': '◀️ السابق',
                'next': '▶️ التالي',
                'page': f'صفحة {page}/{total_pages}'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        buttons = []
        
        if page > 1:
            buttons.append(InlineKeyboardButton(text['prev'], callback_data=f'{prefix}_page_{page-1}'))
        
        buttons.append(InlineKeyboardButton(text['page'], callback_data='current_page'))
        
        if page < total_pages:
            buttons.append(InlineKeyboardButton(text['next'], callback_data=f'{prefix}_page_{page+1}'))
        
        return InlineKeyboardMarkup([buttons])
    
    @staticmethod
    def product_management_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Product management keyboard"""
        texts = {
            'fa': {
                'add': '➕ افزودن محصول',
                'list': '📋 لیست محصولات',
                'categories': '📂 دسته‌بندی‌ها',
                'import': '📥 ورود از فایل',
                'back': '🔙 بازگشت'
            },
            'en': {
                'add': '➕ Add Product',
                'list': '📋 Product List',
                'categories': '📂 Categories',
                'import': '📥 Import from File',
                'back': '🔙 Back'
            },
            'ar': {
                'add': '➕ إضافة منتج',
                'list': '📋 قائمة المنتجات',
                'categories': '📂 الفئات',
                'import': '📥 استيراد من ملف',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['add'], callback_data='product_add'),
                InlineKeyboardButton(text['list'], callback_data='product_list')
            ],
            [
                InlineKeyboardButton(text['categories'], callback_data='product_categories'),
                InlineKeyboardButton(text['import'], callback_data='product_import')
            ],
            [InlineKeyboardButton(text['back'], callback_data='shop_manage')]
        ])
    
    @staticmethod
    def order_status_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Order status management keyboard"""
        texts = {
            'fa': {
                'pending': '⏳ در انتظار',
                'confirmed': '✅ تأیید شده',
                'processing': '🔄 در حال پردازش',
                'shipped': '🚚 ارسال شده',
                'delivered': '📦 تحویل شده',
                'cancelled': '❌ لغو شده'
            },
            'en': {
                'pending': '⏳ Pending',
                'confirmed': '✅ Confirmed',
                'processing': '🔄 Processing',
                'shipped': '🚚 Shipped',
                'delivered': '📦 Delivered',
                'cancelled': '❌ Cancelled'
            },
            'ar': {
                'pending': '⏳ معلق',
                'confirmed': '✅ مؤكد',
                'processing': '🔄 قيد المعالجة',
                'shipped': '🚚 تم الشحن',
                'delivered': '📦 تم التسليم',
                'cancelled': '❌ ملغي'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['pending'], callback_data='order_status_pending'),
                InlineKeyboardButton(text['confirmed'], callback_data='order_status_confirmed')
            ],
            [
                InlineKeyboardButton(text['processing'], callback_data='order_status_processing'),
                InlineKeyboardButton(text['shipped'], callback_data='order_status_shipped')
            ],
            [
                InlineKeyboardButton(text['delivered'], callback_data='order_status_delivered'),
                InlineKeyboardButton(text['cancelled'], callback_data='order_status_cancelled')
            ]
        ])
    
    @staticmethod
    def referral_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Referral system keyboard"""
        texts = {
            'fa': {
                'share': '📤 اشتراک‌گذاری لینک',
                'stats': '📊 آمار معرفی‌ها',
                'withdraw': '💰 برداشت درآمد',
                'back': '🔙 بازگشت'
            },
            'en': {
                'share': '📤 Share Link',
                'stats': '📊 Referral Stats',
                'withdraw': '💰 Withdraw Earnings',
                'back': '🔙 Back'
            },
            'ar': {
                'share': '📤 مشاركة الرابط',
                'stats': '📊 إحصائيات الإحالة',
                'withdraw': '💰 سحب الأرباح',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['share'], switch_inline_query='referral_link'),
                InlineKeyboardButton(text['stats'], callback_data='referral_stats')
            ],
            [InlineKeyboardButton(text['withdraw'], callback_data='referral_withdraw')],
            [InlineKeyboardButton(text['back'], callback_data='profile_show')]
        ])
    
    @staticmethod
    def contact_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Contact/Support keyboard"""
        texts = {
            'fa': {
                'admin': '👨‍💼 تماس با مدیر',
                'channel': '📢 کانال ما',
                'faq': '❓ سوالات متداول',
                'back': '🔙 بازگشت'
            },
            'en': {
                'admin': '👨‍💼 Contact Admin',
                'channel': '📢 Our Channel',
                'faq': '❓ FAQ',
                'back': '🔙 Back'
            },
            'ar': {
                'admin': '👨‍💼 الاتصال بالمدير',
                'channel': '📢 قناتنا',
                'faq': '❓ الأسئلة الشائعة',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text['admin'], url='https://t.me/hadi_admin')],
            [InlineKeyboardButton(text['channel'], url='https://t.me/coderoot_channel')],
            [InlineKeyboardButton(text['faq'], callback_data='support_faq')],
            [InlineKeyboardButton(text['back'], callback_data='main_menu')]
        ])
    
    @staticmethod
    def settings_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """Settings keyboard"""
        texts = {
            'fa': {
                'notifications': '🔔 اطلاع‌رسانی',
                'language': '🌍 زبان',
                'privacy': '🔒 حریم خصوصی',
                'backup': '💾 پشتیبان‌گیری',
                'back': '🔙 بازگشت'
            },
            'en': {
                'notifications': '🔔 Notifications',
                'language': '🌍 Language',
                'privacy': '🔒 Privacy',
                'backup': '💾 Backup',
                'back': '🔙 Back'
            },
            'ar': {
                'notifications': '🔔 الإشعارات',
                'language': '🌍 اللغة',
                'privacy': '🔒 الخصوصية',
                'backup': '💾 النسخ الاحتياطي',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['notifications'], callback_data='settings_notifications'),
                InlineKeyboardButton(text['language'], callback_data='settings_language')
            ],
            [
                InlineKeyboardButton(text['privacy'], callback_data='settings_privacy'),
                InlineKeyboardButton(text['backup'], callback_data='settings_backup')
            ],
            [InlineKeyboardButton(text['back'], callback_data='profile_show')]
        ])
    
    @staticmethod
    def shop_status_keyboard(status: str, language: str = 'fa') -> InlineKeyboardMarkup:
        """Shop status management keyboard"""
        texts = {
            'fa': {
                'activate': '✅ فعال‌سازی',
                'suspend': '⏸ تعلیق',
                'delete': '🗑 حذف',
                'back': '🔙 بازگشت'
            },
            'en': {
                'activate': '✅ Activate',
                'suspend': '⏸ Suspend',
                'delete': '🗑 Delete',
                'back': '🔙 Back'
            },
            'ar': {
                'activate': '✅ تفعيل',
                'suspend': '⏸ تعليق',
                'delete': '🗑 حذف',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        buttons = []
        
        if status == 'pending':
            buttons.append([InlineKeyboardButton(text['activate'], callback_data='shop_status_activate')])
        elif status == 'active':
            buttons.append([InlineKeyboardButton(text['suspend'], callback_data='shop_status_suspend')])
        elif status == 'suspended':
            buttons.append([InlineKeyboardButton(text['activate'], callback_data='shop_status_activate')])
        
        buttons.extend([
            [InlineKeyboardButton(text['delete'], callback_data='shop_status_delete')],
            [InlineKeyboardButton(text['back'], callback_data='admin_shops')]
        ])
        
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def user_management_keyboard(language: str = 'fa') -> InlineKeyboardMarkup:
        """User management keyboard for admins"""
        texts = {
            'fa': {
                'view': '👁 مشاهده جزئیات',
                'block': '🚫 مسدود کردن',
                'unblock': '✅ رفع مسدودی',
                'message': '💬 ارسال پیام',
                'back': '🔙 بازگشت'
            },
            'en': {
                'view': '👁 View Details',
                'block': '🚫 Block',
                'unblock': '✅ Unblock',
                'message': '💬 Send Message',
                'back': '🔙 Back'
            },
            'ar': {
                'view': '👁 عرض التفاصيل',
                'block': '🚫 حظر',
                'unblock': '✅ إلغاء الحظر',
                'message': '💬 إرسال رسالة',
                'back': '🔙 رجوع'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text['view'], callback_data='user_view'),
                InlineKeyboardButton(text['block'], callback_data='user_block')
            ],
            [
                InlineKeyboardButton(text['unblock'], callback_data='user_unblock'),
                InlineKeyboardButton(text['message'], callback_data='user_message')
            ],
            [InlineKeyboardButton(text['back'], callback_data='admin_users')]
        ])
    
    @staticmethod
    def quick_reply_keyboard(language: str = 'fa') -> ReplyKeyboardMarkup:
        """Quick reply keyboard for common actions"""
        texts = {
            'fa': [
                ['🏪 فروشگاه من', '➕ ایجاد فروشگاه'],
                ['👤 پروفایل', '🎁 معرفی'],
                ['🆘 پشتیبانی', '📊 آمار']
            ],
            'en': [
                ['🏪 My Shop', '➕ Create Shop'],
                ['👤 Profile', '🎁 Referral'],
                ['🆘 Support', '📊 Stats']
            ],
            'ar': [
                ['🏪 متجري', '➕ إنشاء متجر'],
                ['👤 الملف الشخصي', '🎁 الإحالة'],
                ['🆘 الدعم', '📊 الإحصائيات']
            ]
        }
        
        buttons = texts.get(language, texts['fa'])
        
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(btn) for btn in row] for row in buttons],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    
    @staticmethod
    def remove_keyboard() -> ReplyKeyboardMarkup:
        """Remove reply keyboard"""
        return ReplyKeyboardMarkup(
            keyboard=[],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    
    @staticmethod
    def channel_join_keyboard(channel_username: str, language: str = 'fa') -> InlineKeyboardMarkup:
        """Channel join requirement keyboard"""
        texts = {
            'fa': {
                'join': '🔗 عضویت در کانال',
                'check': '✅ عضو شدم'
            },
            'en': {
                'join': '🔗 Join Channel',
                'check': '✅ I Joined'
            },
            'ar': {
                'join': '🔗 انضمام للقناة',
                'check': '✅ انضممت'
            }
        }
        
        text = texts.get(language, texts['fa'])
        
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text['join'], url=f'https://t.me/{channel_username}')],
            [InlineKeyboardButton(text['check'], callback_data='check_membership')]
        ])