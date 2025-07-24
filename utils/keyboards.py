"""
Keyboard markups for CodeRoot Bot
صفحه کلیدهای ربات CodeRoot
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import PLANS

class KeyboardMarkups:
    """Keyboard markup generator class"""
    
    @staticmethod
    def main_menu_keyboard(user):
        """Main menu keyboard"""
        buttons = [
            [InlineKeyboardButton("🏪 ایجاد فروشگاه", callback_data="shop_create")],
            [InlineKeyboardButton("🛍 فروشگاه من", callback_data="my_shop")],
            [InlineKeyboardButton("👤 پروفایل", callback_data="profile")],
            [InlineKeyboardButton("🎁 معرفی دوستان", callback_data="referral")]
        ]
        
        # Add admin button for admin user
        if user and user.get('permissions', {}).get('admin_access'):
            buttons.append([InlineKeyboardButton("🔧 پنل مدیریت", callback_data="admin_panel")])
        
        buttons.extend([
            [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support"), 
             InlineKeyboardButton("📚 آموزش", callback_data="tutorial")],
            [InlineKeyboardButton("📜 قوانین", callback_data="rules")]
        ])
        
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def shop_plans_keyboard():
        """Shop plans selection keyboard"""
        buttons = []
        
        for plan_key, plan in PLANS.items():
            price_text = "رایگان" if plan['price'] == 0 else f"{plan['price']:,} تومان"
            buttons.append([
                InlineKeyboardButton(
                    f"💎 {plan['name']} - {price_text}",
                    callback_data=f"plan_{plan_key}"
                )
            ])
        
        buttons.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def shop_management_keyboard(shop):
        """Shop management keyboard"""
        buttons = [
            [InlineKeyboardButton("📦 مدیریت محصولات", callback_data="manage_products")],
            [InlineKeyboardButton("🛒 سفارش‌ها", callback_data="orders"),
             InlineKeyboardButton("📊 گزارش فروش", callback_data="sales_report")],
            [InlineKeyboardButton("⚙️ تنظیمات فروشگاه", callback_data="shop_settings")],
            [InlineKeyboardButton("💎 ارتقاء پلن", callback_data="upgrade_plan"),
             InlineKeyboardButton("🔄 تمدید اشتراک", callback_data="renew_subscription")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def admin_main_keyboard():
        """Admin main menu keyboard"""
        buttons = [
            [InlineKeyboardButton("👥 مدیریت کاربران", callback_data="admin_users")],
            [InlineKeyboardButton("🏪 مدیریت فروشگاه‌ها", callback_data="admin_shops")],
            [InlineKeyboardButton("💰 گزارش مالی", callback_data="admin_finance")],
            [InlineKeyboardButton("📊 آمار کلی", callback_data="admin_stats")],
            [InlineKeyboardButton("📢 ارسال پیام همگانی", callback_data="admin_broadcast")],
            [InlineKeyboardButton("📋 گزارش اکسل", callback_data="admin_excel_report")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def admin_users_keyboard():
        """Admin users management keyboard"""
        buttons = [
            [InlineKeyboardButton("📋 لیست کاربران", callback_data="admin_users_list")],
            [InlineKeyboardButton("🔍 جستجوی کاربر", callback_data="admin_search_user")],
            [InlineKeyboardButton("📊 آمار کاربران", callback_data="admin_users_stats")],
            [InlineKeyboardButton("📄 گزارش کاربران", callback_data="admin_users_report")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def admin_shops_keyboard():
        """Admin shops management keyboard"""
        buttons = [
            [InlineKeyboardButton("📋 لیست فروشگاه‌ها", callback_data="admin_shops_list")],
            [InlineKeyboardButton("⏳ فروشگاه‌های در انتظار", callback_data="admin_pending_shops")],
            [InlineKeyboardButton("✅ تأیید فروشگاه‌ها", callback_data="admin_approve_shops")],
            [InlineKeyboardButton("📊 آمار فروشگاه‌ها", callback_data="admin_shops_stats")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def admin_stats_keyboard():
        """Admin statistics keyboard"""
        buttons = [
            [InlineKeyboardButton("👥 آمار کاربران", callback_data="admin_users_stats")],
            [InlineKeyboardButton("🏪 آمار فروشگاه‌ها", callback_data="admin_shops_stats")],
            [InlineKeyboardButton("💰 آمار مالی", callback_data="admin_financial_stats")],
            [InlineKeyboardButton("📈 آمار رشد", callback_data="admin_growth_stats")],
            [InlineKeyboardButton("🔄 بروزرسانی", callback_data="admin_stats")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def profile_keyboard():
        """Profile management keyboard"""
        buttons = [
            [InlineKeyboardButton("📝 ویرایش پروفایل", callback_data="edit_profile")],
            [InlineKeyboardButton("💎 ارتقاء اشتراک", callback_data="upgrade_subscription")],
            [InlineKeyboardButton("🎁 دعوت دوستان", callback_data="referral")],
            [InlineKeyboardButton("📊 آمار من", callback_data="my_stats")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def payment_keyboard(plan_name, amount):
        """Payment keyboard"""
        buttons = [
            [InlineKeyboardButton(f"💳 پرداخت {amount:,} تومان", callback_data=f"pay_{plan_name}")],
            [InlineKeyboardButton("📱 شماره کارت", callback_data="show_card_number")],
            [InlineKeyboardButton("📷 ارسال رسید", callback_data="upload_receipt")],
            [InlineKeyboardButton("❌ لغو", callback_data="cancel_payment")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def cancel_keyboard():
        """Cancel operation keyboard"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ لغو", callback_data="cancel")]
        ])
    
    @staticmethod
    def back_keyboard(callback_data):
        """Back button keyboard"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data=callback_data)]
        ])
    
    @staticmethod
    def confirmation_keyboard(action):
        """Confirmation keyboard"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ تأیید", callback_data=f"confirm_{action}"),
             InlineKeyboardButton("❌ لغو", callback_data=f"cancel_{action}")]
        ])
    
    @staticmethod
    def shop_created_keyboard():
        """Shop created success keyboard"""
        buttons = [
            [InlineKeyboardButton("🏪 مدیریت فروشگاه", callback_data="my_shop")],
            [InlineKeyboardButton("📦 افزودن محصول", callback_data="add_product")],
            [InlineKeyboardButton("📚 آموزش مدیریت", callback_data="shop_tutorial")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def pagination_keyboard(current_page, total_pages, callback_prefix):
        """Pagination keyboard"""
        buttons = []
        
        # Navigation buttons
        nav_buttons = []
        if current_page > 1:
            nav_buttons.append(InlineKeyboardButton("⏮ اول", callback_data=f"{callback_prefix}:1"))
            nav_buttons.append(InlineKeyboardButton("◀️ قبلی", callback_data=f"{callback_prefix}:{current_page-1}"))
        
        nav_buttons.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="page_info"))
        
        if current_page < total_pages:
            nav_buttons.append(InlineKeyboardButton("▶️ بعدی", callback_data=f"{callback_prefix}:{current_page+1}"))
            nav_buttons.append(InlineKeyboardButton("⏭ آخر", callback_data=f"{callback_prefix}:{total_pages}"))
        
        if nav_buttons:
            # Split navigation buttons into rows of 3
            for i in range(0, len(nav_buttons), 3):
                buttons.append(nav_buttons[i:i+3])
        
        return buttons
    
    @staticmethod
    def product_management_keyboard():
        """Product management keyboard"""
        buttons = [
            [InlineKeyboardButton("➕ افزودن محصول", callback_data="add_product")],
            [InlineKeyboardButton("📋 لیست محصولات", callback_data="list_products")],
            [InlineKeyboardButton("📂 مدیریت دسته‌بندی", callback_data="manage_categories")],
            [InlineKeyboardButton("📊 آمار محصولات", callback_data="products_stats")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="my_shop")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def order_status_keyboard(order_id):
        """Order status management keyboard"""
        buttons = [
            [InlineKeyboardButton("✅ تأیید", callback_data=f"order_confirm_{order_id}")],
            [InlineKeyboardButton("📦 در حال آماده‌سازی", callback_data=f"order_processing_{order_id}")],
            [InlineKeyboardButton("🚚 ارسال شده", callback_data=f"order_shipped_{order_id}")],
            [InlineKeyboardButton("📬 تحویل داده شده", callback_data=f"order_delivered_{order_id}")],
            [InlineKeyboardButton("❌ لغو", callback_data=f"order_cancel_{order_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="orders")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def referral_keyboard(referral_code):
        """Referral system keyboard"""
        buttons = [
            [InlineKeyboardButton("🔄 به‌اشتراک‌گذاری", 
                                switch_inline_query=f"🚀 ایجاد فروشگاه آنلاین با CodeRoot!\n\n🎁 با لینک من ثبت‌نام کن و مزایای ویژه بگیر!\n\nhttps://t.me/coderoot_main_bot?start={referral_code}")],
            [InlineKeyboardButton("📊 آمار معرفی", callback_data="referral_stats")],
            [InlineKeyboardButton("💰 درآمد معرفی", callback_data="referral_earnings")],
            [InlineKeyboardButton("📋 قوانین معرفی", callback_data="referral_rules")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def contact_keyboard():
        """Contact and support keyboard"""
        buttons = [
            [InlineKeyboardButton("📞 تماس با پشتیبانی", callback_data="contact_support")],
            [InlineKeyboardButton("💬 چت آنلاین", callback_data="live_chat")],
            [InlineKeyboardButton("📧 ایمیل", callback_data="email_support")],
            [InlineKeyboardButton("❓ سوالات متداول", callback_data="faq")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def settings_keyboard():
        """Settings keyboard"""
        buttons = [
            [InlineKeyboardButton("🔔 تنظیمات اطلاع‌رسانی", callback_data="notification_settings")],
            [InlineKeyboardButton("🌐 تغییر زبان", callback_data="language_settings")],
            [InlineKeyboardButton("🔐 تنظیمات امنیتی", callback_data="security_settings")],
            [InlineKeyboardButton("💳 روش‌های پرداخت", callback_data="payment_methods")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="profile")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def shop_status_keyboard(shop_id, current_status):
        """Shop status management for admin"""
        buttons = []
        
        if current_status == "pending":
            buttons.append([InlineKeyboardButton("✅ تأیید فروشگاه", callback_data=f"approve_shop_{shop_id}")])
        
        if current_status == "active":
            buttons.append([InlineKeyboardButton("⏸ تعلیق فروشگاه", callback_data=f"suspend_shop_{shop_id}")])
        elif current_status == "suspended":
            buttons.append([InlineKeyboardButton("▶️ فعال‌سازی فروشگاه", callback_data=f"activate_shop_{shop_id}")])
        
        buttons.extend([
            [InlineKeyboardButton("🗑 حذف فروشگاه", callback_data=f"delete_shop_{shop_id}")],
            [InlineKeyboardButton("📊 جزئیات کامل", callback_data=f"shop_details_{shop_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_shops")]
        ])
        
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def user_management_keyboard(user_id):
        """User management keyboard for admin"""
        buttons = [
            [InlineKeyboardButton("👤 مشاهده پروفایل", callback_data=f"view_user_{user_id}")],
            [InlineKeyboardButton("🏪 فروشگاه‌های کاربر", callback_data=f"user_shops_{user_id}")],
            [InlineKeyboardButton("💰 تاریخچه پرداخت", callback_data=f"user_payments_{user_id}")],
            [InlineKeyboardButton("🔒 مسدود کردن", callback_data=f"block_user_{user_id}")],
            [InlineKeyboardButton("💬 ارسال پیام", callback_data=f"message_user_{user_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_users")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def quick_reply_keyboard():
        """Quick reply keyboard for common messages"""
        keyboard = ReplyKeyboardMarkup([
            [KeyboardButton("🏪 فروشگاه من"), KeyboardButton("👤 پروفایل")],
            [KeyboardButton("🎁 معرفی دوستان"), KeyboardButton("🆘 پشتیبانی")],
            [KeyboardButton("📊 آمار"), KeyboardButton("⚙️ تنظیمات")]
        ], resize_keyboard=True, placeholder="گزینه مورد نظر را انتخاب کنید...")
        return keyboard
    
    @staticmethod
    def remove_keyboard():
        """Remove reply keyboard"""
        from pyrogram.types import ReplyKeyboardRemove
        return ReplyKeyboardRemove()