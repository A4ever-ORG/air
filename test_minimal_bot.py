#!/usr/bin/env python3
"""
Minimal CodeRoot Bot Test
This is a simplified version for testing API credentials and basic functionality
"""

import asyncio
import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM')
API_ID = int(os.getenv('API_ID', '17064702'))
API_HASH = os.getenv('API_HASH', 'f65880b9eededbee85346f874819bbc5')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '7707164235'))

# Initialize bot client
app = Client(
    "minimal_coderoot_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# User states
user_states = {}

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command with language selection"""
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "کاربر"
        
        # Language selection keyboard
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ],
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")]
        ])
        
        welcome_text = f"""🎉 سلام {first_name} عزیز!

به **CodeRoot** خوش آمدید! 🚀

🏪 سیستم ایجاد فروشگاه آنلاین
✨ مدیریت محصولات و سفارش‌ها
📊 گزارش‌گیری پیشرفته
💰 سیستم درآمدزایی

لطفاً زبان خود را انتخاب کنید:"""

        await message.reply_text(welcome_text, reply_markup=keyboard)
        
        # Log successful start
        logger.info(f"User {user_id} ({first_name}) started the bot")
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

@app.on_callback_query()
async def handle_callback(client: Client, callback_query):
    """Handle callback queries"""
    try:
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        if data.startswith("lang_"):
            # Language selection
            lang = data.split("_")[1]
            user_states[user_id] = {'language': lang}
            
            # Language-specific texts
            texts = {
                'fa': {
                    'selected': '✅ زبان فارسی انتخاب شد',
                    'menu': '🏪 منوی اصلی CodeRoot\n\nگزینه مورد نظر خود را انتخاب کنید:',
                    'shop': '🏪 فروشگاه من',
                    'create': '➕ ایجاد فروشگاه',
                    'profile': '👤 پروفایل',
                    'help': '❓ راهنما'
                },
                'en': {
                    'selected': '✅ English language selected',
                    'menu': '🏪 CodeRoot Main Menu\n\nChoose your desired option:',
                    'shop': '🏪 My Shop',
                    'create': '➕ Create Shop',
                    'profile': '👤 Profile',
                    'help': '❓ Help'
                },
                'ar': {
                    'selected': '✅ تم اختيار اللغة العربية',
                    'menu': '🏪 القائمة الرئيسية CodeRoot\n\nاختر الخيار المطلوب:',
                    'shop': '🏪 متجري',
                    'create': '➕ إنشاء متجر',
                    'profile': '👤 الملف الشخصي',
                    'help': '❓ مساعدة'
                }
            }
            
            text = texts.get(lang, texts['fa'])
            
            # Main menu keyboard
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text['shop'], callback_data='my_shop'),
                    InlineKeyboardButton(text['create'], callback_data='create_shop')
                ],
                [
                    InlineKeyboardButton(text['profile'], callback_data='profile'),
                    InlineKeyboardButton(text['help'], callback_data='help')
                ]
            ])
            
            await callback_query.edit_message_text(
                f"{text['selected']}\n\n{text['menu']}",
                reply_markup=keyboard
            )
            
        elif data == 'my_shop':
            lang = user_states.get(user_id, {}).get('language', 'fa')
            shop_texts = {
                'fa': '🏪 فروشگاه شما هنوز ایجاد نشده است.\n\nبرای ایجاد فروشگاه جدید روی دکمه زیر کلیک کنید:',
                'en': '🏪 Your shop has not been created yet.\n\nClick the button below to create a new shop:',
                'ar': '🏪 لم يتم إنشاء متجرك بعد.\n\nانقر على الزر أدناه لإنشاء متجر جديد:'
            }
            create_texts = {
                'fa': '➕ ایجاد فروشگاه',
                'en': '➕ Create Shop',
                'ar': '➕ إنشاء متجر'
            }
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(create_texts[lang], callback_data='create_shop')],
                [InlineKeyboardButton('🔙 بازگشت' if lang == 'fa' else '🔙 Back' if lang == 'en' else '🔙 العودة', callback_data='back_main')]
            ])
            
            await callback_query.edit_message_text(shop_texts[lang], reply_markup=keyboard)
            
        elif data == 'create_shop':
            lang = user_states.get(user_id, {}).get('language', 'fa')
            plans_texts = {
                'fa': """🏪 **انتخاب پلن اشتراک**

پلن مناسب خود را برای شروع کسب‌وکار انتخاب کنید:

🆓 **رایگان**
• 10 محصول
• درگاه بله
• گزارش‌های ساده
• کارمزد 5%

⭐ **حرفه‌ای** - 20,000 تومان
• 200 محصول
• گزارش‌های پیشرفته
• پیام‌های خودکار
• کارمزد 5%

👑 **VIP** - 60,000 تومان
• محصولات نامحدود
• درگاه اختصاصی
• گزارش‌های کامل
• بدون کارمزد""",
                'en': """🏪 **Select Subscription Plan**

Choose the right plan to start your business:

🆓 **Free**
• 10 products
• Bale gateway
• Simple reports
• 5% commission

⭐ **Professional** - 20,000 Tomans
• 200 products
• Advanced reports
• Auto messages
• 5% commission

👑 **VIP** - 60,000 Tomans
• Unlimited products
• Dedicated gateway
• Complete reports
• No commission""",
                'ar': """🏪 **اختيار خطة الاشتراك**

اختر الخطة المناسبة لبدء عملك:

🆓 **مجاني**
• 10 منتجات
• بوابة بيل
• تقارير بسيطة
• عمولة 5%

⭐ **احترافي** - 20,000 تومان
• 200 منتج
• تقارير متقدمة
• رسائل تلقائية
• عمولة 5%

👑 **VIP** - 60,000 تومان
• منتجات غير محدودة
• بوابة مخصصة
• تقارير كاملة
• بدون عمولة"""
            }
            
            plan_buttons = {
                'fa': ['🆓 رایگان', '⭐ حرفه‌ای', '👑 VIP'],
                'en': ['🆓 Free', '⭐ Professional', '👑 VIP'],
                'ar': ['🆓 مجاني', '⭐ احترافي', '👑 VIP']
            }
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(plan_buttons[lang][0], callback_data='plan_free')],
                [InlineKeyboardButton(plan_buttons[lang][1], callback_data='plan_pro')],
                [InlineKeyboardButton(plan_buttons[lang][2], callback_data='plan_vip')],
                [InlineKeyboardButton('🔙 بازگشت' if lang == 'fa' else '🔙 Back' if lang == 'en' else '🔙 العودة', callback_data='back_main')]
            ])
            
            await callback_query.edit_message_text(plans_texts[lang], reply_markup=keyboard)
            
        elif data.startswith('plan_'):
            plan = data.split('_')[1]
            lang = user_states.get(user_id, {}).get('language', 'fa')
            
            plan_names = {
                'free': {'fa': 'رایگان', 'en': 'Free', 'ar': 'مجاني'},
                'pro': {'fa': 'حرفه‌ای', 'en': 'Professional', 'ar': 'احترافي'},
                'vip': {'fa': 'VIP', 'en': 'VIP', 'ar': 'VIP'}
            }
            
            success_texts = {
                'fa': f'✅ پلن **{plan_names[plan][lang]}** انتخاب شد!\n\nاکنون نام فروشگاه خود را ارسال کنید:',
                'en': f'✅ **{plan_names[plan][lang]}** plan selected!\n\nNow send your shop name:',
                'ar': f'✅ تم اختيار خطة **{plan_names[plan][lang]}**!\n\nالآن أرسل اسم متجرك:'
            }
            
            user_states[user_id] = user_states.get(user_id, {})
            user_states[user_id]['state'] = 'waiting_shop_name'
            user_states[user_id]['selected_plan'] = plan
            
            await callback_query.edit_message_text(success_texts[lang])
            
        elif data == 'profile':
            lang = user_states.get(user_id, {}).get('language', 'fa')
            username = callback_query.from_user.username or 'ندارد'
            first_name = callback_query.from_user.first_name or 'نامشخص'
            
            profile_texts = {
                'fa': f"""👤 **پروفایل کاربری**

🆔 نام: {first_name}
📱 نام کاربری: @{username}
🗓 تاریخ عضویت: امروز
🎁 تعداد معرفی: 0
💰 درآمد کل: 0 تومان""",
                'en': f"""👤 **User Profile**

🆔 Name: {first_name}
📱 Username: @{username}
🗓 Join Date: Today
🎁 Referrals: 0
💰 Total Earnings: 0 Tomans""",
                'ar': f"""👤 **الملف الشخصي**

🆔 الاسم: {first_name}
📱 اسم المستخدم: @{username}
🗓 تاريخ الانضمام: اليوم
🎁 الإحالات: 0
💰 إجمالي الأرباح: 0 تومان"""
            }
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('🔙 بازگشت' if lang == 'fa' else '🔙 Back' if lang == 'en' else '🔙 العودة', callback_data='back_main')]
            ])
            
            await callback_query.edit_message_text(profile_texts[lang], reply_markup=keyboard)
            
        elif data == 'help':
            lang = user_states.get(user_id, {}).get('language', 'fa')
            help_texts = {
                'fa': """📖 **راهنمای CodeRoot**

🚀 **دستورات اصلی:**
/start - شروع یا بازگشت به منوی اصلی

🏪 **قابلیت‌های اصلی:**
• ایجاد فروشگاه آنلاین
• مدیریت محصولات
• پردازش سفارش‌ها
• گزارش‌گیری فروش
• سیستم معرفی و درآمد

📞 **پشتیبانی:** @support""",
                'en': """📖 **CodeRoot Guide**

🚀 **Main Commands:**
/start - Start or return to main menu

🏪 **Main Features:**
• Create online store
• Product management
• Order processing
• Sales reports
• Referral and earning system

📞 **Support:** @support""",
                'ar': """📖 **دليل CodeRoot**

🚀 **الأوامر الرئيسية:**
/start - البدء أو العودة للقائمة الرئيسية

🏪 **الميزات الرئيسية:**
• إنشاء متجر إلكتروني
• إدارة المنتجات
• معالجة الطلبات
• تقارير المبيعات
• نظام الإحالة والأرباح

📞 **الدعم:** @support"""
            }
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('🔙 بازگشت' if lang == 'fa' else '🔙 Back' if lang == 'en' else '🔙 العودة', callback_data='back_main')]
            ])
            
            await callback_query.edit_message_text(help_texts[lang], reply_markup=keyboard)
            
        elif data == 'back_main':
            # Go back to main menu
            lang = user_states.get(user_id, {}).get('language', 'fa')
            
            menu_texts = {
                'fa': '🏪 منوی اصلی CodeRoot\n\nگزینه مورد نظر خود را انتخاب کنید:',
                'en': '🏪 CodeRoot Main Menu\n\nChoose your desired option:',
                'ar': '🏪 القائمة الرئيسية CodeRoot\n\nاختر الخيار المطلوب:'
            }
            
            button_texts = {
                'fa': ['🏪 فروشگاه من', '➕ ایجاد فروشگاه', '👤 پروفایل', '❓ راهنما'],
                'en': ['🏪 My Shop', '➕ Create Shop', '👤 Profile', '❓ Help'],
                'ar': ['🏪 متجري', '➕ إنشاء متجر', '👤 الملف الشخصي', '❓ مساعدة']
            }
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(button_texts[lang][0], callback_data='my_shop'),
                    InlineKeyboardButton(button_texts[lang][1], callback_data='create_shop')
                ],
                [
                    InlineKeyboardButton(button_texts[lang][2], callback_data='profile'),
                    InlineKeyboardButton(button_texts[lang][3], callback_data='help')
                ]
            ])
            
            await callback_query.edit_message_text(menu_texts[lang], reply_markup=keyboard)
            
        await callback_query.answer()
        
    except Exception as e:
        logger.error(f"Error in callback handler: {e}")
        await callback_query.answer("خطایی رخ داد!")

@app.on_message(filters.text & ~filters.command(["start"]))
async def handle_text(client: Client, message: Message):
    """Handle text messages"""
    try:
        user_id = message.from_user.id
        text = message.text
        user_state = user_states.get(user_id, {})
        lang = user_state.get('language', 'fa')
        
        if user_state.get('state') == 'waiting_shop_name':
            # Process shop name
            selected_plan = user_state.get('selected_plan', 'free')
            
            plan_names = {
                'free': {'fa': 'رایگان', 'en': 'Free', 'ar': 'مجاني'},
                'pro': {'fa': 'حرفه‌ای', 'en': 'Professional', 'ar': 'احترافي'},
                'vip': {'fa': 'VIP', 'en': 'VIP', 'ar': 'VIP'}
            }
            
            success_texts = {
                'fa': f"""✅ **فروشگاه با موفقیت ایجاد شد!**

🏪 نام فروشگاه: **{text}**
💎 پلن: **{plan_names[selected_plan][lang]}**
📊 وضعیت: فعال

🎉 تبریک! فروشگاه شما آماده استفاده است.

برای مدیریت فروشگاه خود از منوی اصلی استفاده کنید.""",
                'en': f"""✅ **Shop created successfully!**

🏪 Shop Name: **{text}**
💎 Plan: **{plan_names[selected_plan][lang]}**
📊 Status: Active

🎉 Congratulations! Your shop is ready to use.

Use the main menu to manage your shop.""",
                'ar': f"""✅ **تم إنشاء المتجر بنجاح!**

🏪 اسم المتجر: **{text}**
💎 الخطة: **{plan_names[selected_plan][lang]}**
📊 الحالة: نشط

🎉 تهانينا! متجرك جاهز للاستخدام.

استخدم القائمة الرئيسية لإدارة متجرك."""
            }
            
            main_menu_texts = {
                'fa': '🏪 منوی اصلی',
                'en': '🏪 Main Menu',
                'ar': '🏪 القائمة الرئيسية'
            }
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(main_menu_texts[lang], callback_data='back_main')]
            ])
            
            await message.reply_text(success_texts[lang], reply_markup=keyboard)
            
            # Clear user state
            user_states[user_id] = {'language': lang}
            
            # Log shop creation
            logger.info(f"User {user_id} created shop: {text} with plan: {selected_plan}")
            
        else:
            # Unknown message
            unknown_texts = {
                'fa': '❓ پیام نامفهوم. لطفاً از منوی ربات استفاده کنید.\n\n/start را بزنید تا به منوی اصلی بروید.',
                'en': '❓ Unknown message. Please use the bot menu.\n\nPress /start to go to the main menu.',
                'ar': '❓ رسالة غير معروفة. يرجى استخدام قائمة البوت.\n\nاضغط /start للذهاب للقائمة الرئيسية.'
            }
            
            await message.reply_text(unknown_texts[lang])
        
    except Exception as e:
        logger.error(f"Error in text handler: {e}")
        await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

@app.on_message(filters.command("admin"))
async def admin_command(client: Client, message: Message):
    """Handle /admin command"""
    try:
        user_id = message.from_user.id
        
        if user_id != ADMIN_USER_ID:
            await message.reply_text("❌ شما مجوز دسترسی به پنل مدیریت را ندارید.")
            return
        
        admin_text = """🔧 **پنل مدیریت CodeRoot**

👋 سلام ادمین عزیز!

📊 **آمار کلی:**
• کاربران فعال: 1
• فروشگاه‌های ایجاد شده: 0
• درآمد امروز: 0 تومان

⚙️ **عملیات مدیریت:**
• مدیریت کاربران
• مدیریت فروشگاه‌ها
• مدیریت پرداخت‌ها
• ارسال پیام همگانی"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 مدیریت کاربران", callback_data="admin_users")],
            [InlineKeyboardButton("🏪 مدیریت فروشگاه‌ها", callback_data="admin_shops")],
            [InlineKeyboardButton("💰 گزارش مالی", callback_data="admin_finance")],
            [InlineKeyboardButton("📢 پیام همگانی", callback_data="admin_broadcast")]
        ])
        
        await message.reply_text(admin_text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Error in admin command: {e}")

async def main():
    """Main function to run the bot"""
    try:
        logger.info("🚀 Starting Minimal CodeRoot Bot...")
        await app.start()
        logger.info("✅ Bot started successfully!")
        logger.info(f"Bot info: @{(await app.get_me()).username}")
        await app.idle()
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
    finally:
        await app.stop()
        logger.info("🛑 Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())