#!/usr/bin/env python3
"""
CodeRoot - Complete MVP Production Bot
ربات مادر CodeRoot - نسخه تولید کامل

Features:
- Complete user management with referral system
- Shop creation and management
- Admin panel for HADI
- Channel join enforcement
- Payment processing
- Sub-bot creation system
- Comprehensive analytics
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Optional
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from aiohttp import web
import threading

from config import Config
from database import DatabaseManager
from utils.keyboards import Keyboards
from utils.validation import Validation
from utils.bot_utils import BotUtils
from utils.notifications import NotificationManager
from utils.security import Security
from utils.language import translator
from services.ai_service import ai_service
from services.email_service import EmailService
from services.file_storage import file_storage
from services.backup_service import BackupService, backup_service as global_backup_service

# Global instances
app = None
db_manager = None
email_service = None

# User states for conversation flow
user_states = {}
admin_states = {}

def register_handlers(app_instance):
    """Register all message and callback handlers"""
    
    # Start command handler
    @app_instance.on_message(filters.command("start"))
    async def start_command(client: Client, message: Message):
        """Handle /start command"""
        try:
            user_id = message.from_user.id
            
            # Update user activity
            if db_manager.users:
                await db_manager.users.update_last_activity(user_id)
            
            # Check if user exists
            user = await db_manager.users.get_user(user_id) if db_manager.users else None
            
            if not user:
                # Create new user
                user_data = {
                    'user_id': user_id,
                    'username': message.from_user.username,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'language': Config.DEFAULT_LANGUAGE
                }
                
                # Check for referral code
                args = message.text.split()
                if len(args) > 1 and args[1].startswith('ref_'):
                    referral_code = args[1][4:]  # Remove 'ref_' prefix
                    referrer = await db_manager.users.get_user_by_referral_code(referral_code)
                    if referrer:
                        user_data['referred_by'] = referrer['user_id']
                
                if db_manager.users:
                    user = await db_manager.users.create_user(user_data)
                    
                    # Send welcome notification to admin
                    await NotificationManager.notify_new_user(client, user)
            
            # Show language selection if not set
            if not user or not user.get('language'):
                keyboard = translator.get_language_selection_keyboard()
                await message.reply_text(
                    "🌍 لطفاً زبان خود را انتخاب کنید:\nPlease select your language:\nيرجى اختيار لغتك:",
                    reply_markup=keyboard
                )
                user_states[user_id] = 'selecting_language'
                return
            
            # Set user language
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE)
            
            # Check channel membership if required
            if Config.MAIN_CHANNEL_USERNAME and not await BotUtils.check_channel_membership(client, user_id, Config.MAIN_CHANNEL_USERNAME):
                welcome_msg = translator.get_text('channel_join_required', user_lang)
                keyboard = Keyboards.channel_join_keyboard(Config.MAIN_CHANNEL_USERNAME, user_lang)
                await message.reply_text(welcome_msg, reply_markup=keyboard)
                return
            
            # Send main menu
            welcome_msg = translator.get_text('welcome_message', user_lang).format(
                name=message.from_user.first_name or "کاربر"
            )
            keyboard = Keyboards.main_menu_keyboard(user_lang)
            
            await message.reply_text(welcome_msg, reply_markup=keyboard)
            
            # Record analytics
            if db_manager.analytics:
                await db_manager.analytics.record_event('user_start', user_id)
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

    # Help command
    @app_instance.on_message(filters.command("help"))
    async def help_command(client: Client, message: Message):
        """Handle /help command"""
        try:
            user_id = message.from_user.id
            user = await db_manager.users.get_user(user_id) if db_manager.users else None
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            help_text = translator.get_text('help_message', user_lang)
            await message.reply_text(help_text)
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")

    # Callback query handler
    @app_instance.on_callback_query()
    async def callback_handler(client: Client, callback_query: CallbackQuery):
        """Handle all callback queries"""
        try:
            data = callback_query.data
            user_id = callback_query.from_user.id
            
            # Route to appropriate handler
            if data.startswith('lang_'):
                await handle_language_selection(client, callback_query)
            elif data.startswith('shop_'):
                await handle_shop_callbacks(client, callback_query)
            elif data.startswith('admin_'):
                await handle_admin_callbacks(client, callback_query)
            elif data.startswith('payment_'):
                await handle_payment_callbacks(client, callback_query)
            elif data.startswith('profile_'):
                await handle_profile_callbacks(client, callback_query)
            elif data.startswith('support_'):
                await handle_support_callbacks(client, callback_query)
            elif data == 'support_contact':
                await SupportHandler.show_support_menu(client, callback_query)
            elif data.startswith('ai_'):
                await handle_ai_support_callbacks(client, callback_query)
            else:
                await callback_query.answer("عملیات نامشخص")
            
        except Exception as e:
            logger.error(f"Error in callback handler: {e}")
            await callback_query.answer("خطایی رخ داد")

    # Text message handler
    @app_instance.on_message(filters.text & ~filters.command)
    async def text_message_handler(client: Client, message: Message):
        """Handle text messages and AI support conversations"""
        try:
            user_id = message.from_user.id
            text = sanitize_input(message.text)
            
            # Check if user is in any support mode
            await handle_support_text_messages(client, message)
            
            # Check if user is in AI support mode (fallback)
            if user_states.get(user_id) == 'ai_support':
                await handle_ai_support_message(client, message, text)
                return
            
            # Update user activity
            if db_manager.users:
                await db_manager.users.update_last_activity(user_id)
            
            # Check for special keywords or commands
            if any(keyword in text.lower() for keyword in ['سلام', 'hello', 'hi', 'مرحبا']):
                user = await db_manager.users.get_user(user_id) if db_manager.users else None
                user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
                
                welcome_msg = translator.get_text('welcome_message', user_lang).format(
                    name=message.from_user.first_name or "کاربر"
                )
                keyboard = Keyboards.main_menu_keyboard(user_lang)
                
                await message.reply_text(welcome_msg, reply_markup=keyboard)
            else:
                # For any other text, offer help
                user = await db_manager.users.get_user(user_id) if db_manager.users else None
                user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
                
                help_texts = {
                    'fa': "🤔 متوجه نشدم!\n\nلطفاً از منوی اصلی یا دستورات ربات استفاده کنید.\n\n💡 برای کمک از گزینه پشتیبانی استفاده کنید.",
                    'en': "🤔 I didn't understand!\n\nPlease use the main menu or bot commands.\n\n💡 Use Support option for help.",
                    'ar': "🤔 لم أفهم!\n\nيرجى استخدام القائمة الرئيسية أو أوامر البوت.\n\n💡 استخدم خيار الدعم للمساعدة."
                }
                
                keyboard = Keyboards.main_menu_keyboard(user_lang)
                await message.reply_text(help_texts[user_lang], reply_markup=keyboard)
                
        except Exception as e:
            logger.error(f"Error in text message handler: {e}")
            await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

    # Photo handler
    @app_instance.on_message(filters.photo)
    async def photo_handler(client: Client, message: Message):
        """Handle photo uploads"""
        try:
            user_id = message.from_user.id
            state = user_states.get(user_id)
            
            if state == 'uploading_product_image':
                await process_product_image(client, message)
            elif state == 'uploading_payment_receipt':
                await process_payment_receipt(client, message)
            else:
                await message.reply_text("تصویر دریافت شد اما در حال حاضر منتظر تصویری نیستم.")
            
        except Exception as e:
            logger.error(f"Error in photo handler: {e}")

    # Document handler
    @app_instance.on_message(filters.document)
    async def document_handler(client: Client, message: Message):
        """Handle document uploads"""
        try:
            user_id = message.from_user.id
            state = user_states.get(user_id)
            
            if state == 'uploading_product_document':
                await process_product_document(client, message)
            else:
                await message.reply_text("فایل دریافت شد اما در حال حاضر منتظر فایلی نیستم.")
            
        except Exception as e:
            logger.error(f"Error in document handler: {e}")

    # Support command
    @app_instance.on_message(filters.command("support"))
    async def support_command(client: Client, message: Message):
        """Handle /support command with AI assistance"""
        try:
            user_id = message.from_user.id
            user = await db_manager.users.get_user(user_id) if db_manager.users else None
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            # Check if user has a specific question
            args = message.text.split(maxsplit=1)
            if len(args) > 1:
                question = args[1]
                
                # Get user context for AI
                context = {
                    'user_id': user_id,
                    'language': user_lang,
                    'has_shop': bool(user and user.get('shop_id')),
                    'plan': user.get('subscription_plan', 'free') if user else 'free'
                }
                
                # Get AI response
                ai_response = await ai_service.handle_support_request(
                    user_id, question, user_lang, context
                )
                
                await message.reply_text(f"🤖 **پاسخ هوشمند:**\n\n{ai_response}")
                
            else:
                # Show support menu
                support_messages = {
                    'fa': "🆘 **سیستم پشتیبانی هوشمند CodeRoot**\n\n✨ از هوش مصنوعی برای پاسخ سوالات استفاده کنید:\n\n💬 برای پرسیدن سوال:\n`/support سوال شما`\n\n🔹 مثال:\n`/support چطور فروشگاه بسازم؟`\n\n📞 تماس مستقیم با پشتیبانی:\n@hadi_admin",
                    'en': "🆘 **CodeRoot AI Support System**\n\n✨ Use AI to answer your questions:\n\n💬 To ask a question:\n`/support your question`\n\n🔹 Example:\n`/support how to create a shop?`\n\n📞 Direct support contact:\n@hadi_admin",
                    'ar': "🆘 **نظام الدعم الذكي CodeRoot**\n\n✨ استخدم الذكاء الاصطناعي للإجابة على أسئلتك:\n\n💬 لطرح سؤال:\n`/support سؤالك`\n\n🔹 مثال:\n`/support كيف أنشئ متجر؟`\n\n📞 الاتصال المباشر بالدعم:\n@hadi_admin"
                }
                
                support_text = support_messages.get(user_lang, support_messages['fa'])
                await message.reply_text(support_text)
            
            # Record analytics
            if db_manager.analytics:
                await db_manager.analytics.record_event('support_accessed', user_id)
                
        except Exception as e:
            logger.error(f"Error in support command: {e}")
            await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

    # Admin command
    @app_instance.on_message(filters.command("admin"))
    async def admin_command(client: Client, message: Message):
        """Handle /admin command"""
        try:
            user_id = message.from_user.id
            
            if not Security.is_admin(user_id):
                await message.reply_text("❌ شما مجوز دسترسی به پنل مدیریت را ندارید.")
                return
            
            keyboard = Keyboards.admin_main_keyboard()
            await message.reply_text(
                "🔧 پنل مدیریت CodeRoot\n\nگزینه مورد نظر خود را انتخاب کنید:",
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in admin command: {e}")

    # Shop command
    @app_instance.on_message(filters.command("shop"))
    async def shop_command(client: Client, message: Message):
        """Handle /shop command"""
        try:
            user_id = message.from_user.id
            
            # Check if user has a shop
            shop = await db_manager.shops.get_shop_by_owner(user_id) if db_manager.shops else None
            
            if shop:
                # Show shop management
                user = await db_manager.users.get_user(user_id) if db_manager.users else None
                user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
                
                keyboard = Keyboards.shop_management_keyboard(user_lang)
                shop_info = translator.get_text('shop_info', user_lang).format(
                    shop_name=shop['name'],
                    plan=shop['plan'],
                    status=shop['status']
                )
                await message.reply_text(shop_info, reply_markup=keyboard)
            else:
                # Show shop creation options
                user = await db_manager.users.get_user(user_id) if db_manager.users else None
                user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
                
                keyboard = Keyboards.shop_plans_keyboard(user_lang)
                plans_info = translator.get_text('shop_plans_info', user_lang)
                await message.reply_text(plans_info, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in shop command: {e}")

    # Profile command
    @app_instance.on_message(filters.command("profile"))
    async def profile_command(client: Client, message: Message):
        """Handle /profile command"""
        try:
            user_id = message.from_user.id
            user = await db_manager.users.get_user(user_id) if db_manager.users else None
            
            if not user:
                await message.reply_text("کاربری یافت نشد. لطفاً /start را بزنید.")
                return
            
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE)
            
            profile_text = translator.get_text('profile_info', user_lang).format(
                name=user.get('first_name', 'نامشخص'),
                username=f"@{user.get('username')}" if user.get('username') else 'ندارد',
                join_date=user.get('created_at', datetime.now()).strftime('%Y/%m/%d'),
                referral_count=user.get('referral_count', 0),
                total_earnings=f"{user.get('total_earnings', 0):,} تومان"
            )
            
            keyboard = Keyboards.profile_keyboard(user_lang)
            await message.reply_text(profile_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in profile command: {e}")

    # Referral command
    @app_instance.on_message(filters.command("referral"))
    async def referral_command(client: Client, message: Message):
        """Handle /referral command"""
        try:
            user_id = message.from_user.id
            user = await db_manager.users.get_user(user_id) if db_manager.users else None
            
            if not user:
                await message.reply_text("کاربری یافت نشد. لطفاً /start را بزنید.")
                return
            
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE)
            
            # Generate referral code if not exists
            referral_code = user.get('referral_code')
            if not referral_code:
                referral_code = BotUtils.generate_random_string(8)
                await db_manager.users.update_user(user_id, {'referral_code': referral_code})
            
            bot_username = Config.BOT_USERNAME
            referral_link = f"https://t.me/{bot_username}?start=ref_{referral_code}"
            
            referral_text = translator.get_text('referral_info', user_lang).format(
                referral_code=referral_code,
                referral_link=referral_link,
                referral_count=user.get('referral_count', 0),
                commission=Config.REFERRAL_COMMISSION
            )
            
            keyboard = Keyboards.referral_keyboard(user_lang)
            await message.reply_text(referral_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in referral command: {e}")

async def startup():
    """Bot startup initialization"""
    try:
        logger.info("🚀 CodeRoot Bot starting up...")
        
        # Initialize database
        await db_manager.connect()
        
        # Test database connection
        if await db_manager.test_connection():
            logger.info("✅ Database connected successfully")
        else:
            logger.error("❌ Database connection failed")
            return
            
        # Initialize backup service
        await global_backup_service.start()
        
        logger.info("✅ CodeRoot Bot startup complete!")
        
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")
        raise

# Shutdown event
async def shutdown():
    """Clean shutdown"""
    try:
        await db_manager.disconnect()
        logger.info("🛑 CodeRoot Bot shutdown complete")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")

async def health_check(request):
    """Health check endpoint for Render"""
    return web.Response(text="OK", status=200)

async def start_health_server():
    """Start health check server"""
    try:
        app_web = web.Application()
        app_web.router.add_get('/health', health_check)
        app_web.router.add_get('/', health_check)
        
        runner = web.AppRunner(app_web)
        await runner.setup()
        
        port = int(os.environ.get('PORT', 8000))
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        
        logger.info(f"🏥 Health check server started on port {port}")
    except Exception as e:
        logger.error(f"❌ Failed to start health server: {e}")

# Language selection handler
async def handle_language_selection(client: Client, callback_query: CallbackQuery):
    """Handle language selection"""
    try:
        user_id = callback_query.from_user.id
        lang_code = callback_query.data.split('_')[1]
        
        # Update user language
        if db_manager.users:
            await db_manager.users.update_user(user_id, {'language': lang_code})
        
        # Remove language selection state
        user_states.pop(user_id, None)
        
        # Send welcome message in selected language
        welcome_msg = translator.get_text('welcome_message', lang_code).format(
            name=callback_query.from_user.first_name or "کاربر"
        )
        keyboard = Keyboards.main_menu_keyboard(lang_code)
        
        await callback_query.message.edit_text(welcome_msg, reply_markup=keyboard)
        await callback_query.answer(translator.get_text('language_selected', lang_code))
        
    except Exception as e:
        logger.error(f"Error in language selection: {e}")

# Shop callbacks handler
async def handle_shop_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle shop-related callbacks"""
    try:
        user_id = callback_query.from_user.id
        action = callback_query.data.split('_', 1)[1]
        
        if action == 'create':
            await start_shop_creation(client, callback_query)
        elif action.startswith('plan_'):
            await select_plan(client, callback_query)
        elif action == 'manage':
            await show_shop_management(client, callback_query)
        elif action == 'products':
            await show_products_menu(client, callback_query)
        elif action == 'orders':
            await show_orders_menu(client, callback_query)
        elif action == 'reports':
            await show_reports_menu(client, callback_query)
        else:
            await callback_query.answer("عملیات نامشخص")
        
    except Exception as e:
        logger.error(f"Error in shop callbacks: {e}")

# Admin callbacks handler
async def handle_admin_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle admin panel callbacks"""
    try:
        user_id = callback_query.from_user.id
        
        if not Security.is_admin(user_id):
            await callback_query.answer("❌ عدم دسترسی")
            return
        
        action = callback_query.data.split('_', 1)[1]
        
        if action == 'users':
            await show_admin_users(client, callback_query)
        elif action == 'shops':
            await show_admin_shops(client, callback_query)
        elif action == 'stats':
            await show_admin_stats(client, callback_query)
        elif action == 'payments':
            await show_admin_payments(client, callback_query)
        elif action == 'broadcast':
            await start_broadcast(client, callback_query)
        else:
            await callback_query.answer("عملیات نامشخص")
        
    except Exception as e:
        logger.error(f"Error in admin callbacks: {e}")

# Payment callbacks handler
async def handle_payment_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle payment-related callbacks"""
    try:
        user_id = callback_query.from_user.id
        action = callback_query.data.split('_', 1)[1]
        
        if action == 'submit':
            await process_payment_submission(client, callback_query)
        elif action.startswith('verify_'):
            await verify_payment(client, callback_query)
        else:
            await callback_query.answer("عملیات نامشخص")
        
    except Exception as e:
        logger.error(f"Error in payment callbacks: {e}")

# Profile callbacks handler
async def handle_profile_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle profile-related callbacks"""
    try:
        user_id = callback_query.from_user.id
        action = callback_query.data.split('_', 1)[1]
        
        if action == 'settings':
            await show_profile_settings(client, callback_query)
        elif action == 'referrals':
            await show_referral_info(client, callback_query)
        else:
            await callback_query.answer("عملیات نامشخص")
        
    except Exception as e:
        logger.error(f"Error in profile callbacks: {e}")

# Support callbacks handler
async def handle_support_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle support-related callbacks"""
    try:
        data = callback_query.data
        
        if data == 'support_menu':
            await SupportHandler.show_support_menu(client, callback_query)
        elif data == 'support_ai':
            await SupportHandler.start_ai_support(client, callback_query)
        elif data == 'support_human':
            await SupportHandler.contact_human_support(client, callback_query)
        elif data == 'support_features':
            # Feature help with AI
            await SupportHandler.get_feature_help(client, callback_query)
        elif data == 'support_plans':
            await SupportHandler.suggest_plan_upgrade(client, callback_query)
        elif data == 'support_analyze':
            await SupportHandler.analyze_user_issue(client, callback_query)
        else:
            await callback_query.answer("گزینه پشتیبانی نامشخص")
            
    except Exception as e:
        logger.error(f"Support callback error: {e}")
        await callback_query.answer("خطا در پردازش درخواست")

async def handle_ai_support_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle AI support related callbacks"""
    try:
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        user = await db_manager.users.get_user(user_id)
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        if data == 'ai_help_shop':
            # Pre-defined help for shop creation
            await handle_ai_predefined_help(client, callback_query, 'shop_creation', user_lang)
        elif data == 'ai_help_payment':
            # Pre-defined help for payment issues
            await handle_ai_predefined_help(client, callback_query, 'payment_issue', user_lang)
        elif data == 'ai_help_plans':
            # Pre-defined help for plans
            await handle_ai_predefined_help(client, callback_query, 'plan_upgrade', user_lang)
        elif data == 'ai_help_technical':
            # Pre-defined help for technical issues
            await handle_ai_predefined_help(client, callback_query, 'technical_problem', user_lang)
        elif data == 'ai_human_support':
            # Transfer to human support
            support_text = translator.get_text('support_contact', user_lang)
            keyboard = Keyboards.main_menu_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                support_text,
                reply_markup=keyboard
            )
            
            # End AI support mode
            user_states.pop(user_id, None)
            
        elif data == 'ai_new_question':
            # Clear AI conversation history and start fresh
            ai_service.clear_conversation_history(user_id)
            welcome_text = translator.get_text('ai_support_welcome', user_lang)
            keyboard = Keyboards.ai_support_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                welcome_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        elif data == 'ai_end_chat':
            # End AI support session
            end_text = translator.get_text('ai_support_ended', user_lang) if hasattr(translator, 'get_text') else "پایان گفتگوی هوشمند. از استفاده از CodeRoot متشکرم!"
            keyboard = Keyboards.main_menu_keyboard(user_lang)
            
            # Clear support state
            from handlers.support_handler import support_states
            support_states.pop(user_id, None)
            user_states.pop(user_id, None)
            
            await callback_query.edit_message_text(
                end_text,
                reply_markup=keyboard
            )
            
        elif data == 'ai_end_support':
            # End AI support session (legacy)
            end_text = translator.get_text('ai_support_ended', user_lang) if hasattr(translator, 'get_text') else "پایان گفتگوی هوشمند. از استفاده از CodeRoot متشکرم!"
            keyboard = Keyboards.main_menu_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                end_text,
                reply_markup=keyboard
            )
            
            # End AI support mode
            user_states.pop(user_id, None)
            
        elif data == 'ai_continue':
            # Continue with AI support
            continue_text = translator.get_text('ai_support_intro', user_lang)
            keyboard = Keyboards.ai_support_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                continue_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data == 'ai_feedback_helpful':
            await callback_query.answer("✅ ممنون از بازخورد شما!")
            # Log positive feedback
            if db_manager.analytics:
                await db_manager.analytics.record_event('ai_feedback_positive', user_id)
                
        elif data == 'ai_feedback_not_helpful':
            await callback_query.answer("📝 بازخورد شما ثبت شد. سعی می‌کنیم بهتر شویم!")
            # Log negative feedback
            if db_manager.analytics:
                await db_manager.analytics.record_event('ai_feedback_negative', user_id)
            
        elif data == 'main_menu':
            # Return to main menu
            welcome_msg = translator.get_text('welcome_message', user_lang).format(
                name=callback_query.from_user.first_name or "کاربر"
            )
            keyboard = Keyboards.main_menu_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                welcome_msg,
                reply_markup=keyboard
            )
            
            # Clear user state
            user_states.pop(user_id, None)
            
    except Exception as e:
        logger.error(f"AI support callback error: {e}")
        await callback_query.answer("خطا در پردازش درخواست")

async def handle_ai_predefined_help(client: Client, callback_query: CallbackQuery, help_type: str, user_lang: str):
    """Handle predefined AI help topics"""
    try:
        user_id = callback_query.from_user.id
        
        # Show thinking message
        thinking_text = translator.get_text('ai_thinking', user_lang)
        await callback_query.edit_message_text(thinking_text)
        
        # Get user context
        user = await db_manager.users.get_user(user_id)
        user_context = {
            'plan': user.get('subscription_plan', 'free') if user else 'free',
            'shop_status': 'active' if user and user.get('shop_id') else 'none',
            'created_at': user.get('created_at', 'Unknown') if user else 'Unknown',
            'last_activity': user.get('last_activity', 'Unknown') if user else 'Unknown'
        }
        
        # Generate predefined help message based on topic
        help_queries = {
            'shop_creation': 'How do I create a new shop? What are the steps?',
            'payment_issue': 'I have a payment problem. How can I resolve it?',
            'plan_upgrade': 'What are the differences between plans? How do I upgrade?',
            'technical_problem': 'I am having technical issues with the bot. Can you help?'
        }
        
        query_text = help_queries.get(help_type, 'How can you help me?')
        
        # Get AI response
        if ai_service.is_available():
            ai_response = await ai_service.get_support_response(
                query_text,
                user_lang,
                user_context
            )
        else:
            # Fallback response
            ai_response = ai_service._get_fallback_response(query_text, user_lang)
        
        # Show AI response with interaction keyboard
        keyboard = Keyboards.ai_response_keyboard(user_lang)
        
        await callback_query.edit_message_text(
            ai_response,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Record analytics
        if db_manager.analytics:
            await db_manager.analytics.record_event(f'ai_help_{help_type}', user_id)
            
    except Exception as e:
        logger.error(f"AI predefined help error: {e}")
        await callback_query.answer("خطا در دریافت کمک")

# Text message handler
async def handle_ai_conversation(client: Client, message: Message, user_lang: str):
    """Handle AI conversation in support mode"""
    try:
        user_id = message.from_user.id
        user_message = message.text.strip()
        
        # Show thinking indicator
        thinking_text = translator.get_text('ai_thinking', user_lang) if hasattr(translator, 'get_text') else "🤔 در حال فکر..."
        thinking_msg = await message.reply_text(thinking_text)
        
        # Get user context for better AI response
        user = await db_manager.users.get_user(user_id)
        user_context = {
            'plan': user.get('subscription_plan', 'free') if user else 'free',
            'shop_status': 'active' if user and user.get('shop_id') else 'none',
            'registration_date': user.get('created_at') if user else None,
            'language': user_lang
        }
        
        # Get AI response
        ai_response = await ai_service.get_ai_response(
            user_id, 
            user_message, 
            user_lang, 
            user_context
        )
        
        # Delete thinking message and send AI response
        await thinking_msg.delete()
        
        # Create response with AI branding
        response_text = f"🤖 **CodeRoot AI:**\n\n{ai_response}"
        
        # Add quick action buttons
        keyboard = Keyboards.ai_support_keyboard(user_lang)
        
        await message.reply_text(
            response_text, 
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error in AI conversation: {e}")
        fallback_text = "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید یا با پشتیبانی انسانی تماس بگیرید."
        keyboard = Keyboards.support_menu_keyboard(user_lang)
        await message.reply_text(fallback_text, reply_markup=keyboard)

async def handle_ai_support_message(client: Client, message: Message, user_message: str):
    """Handle AI support conversation (Legacy)"""
    try:
        user_id = message.from_user.id
        
        # Get user info
        user = await db_manager.users.get_user(user_id)
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        # Use the new AI conversation handler
        await handle_ai_conversation(client, message, user_lang)
        
    except Exception as e:
        logger.error(f"Error in legacy AI support: {e}")

async def handle_ai_support_message_old(client: Client, message: Message, user_message: str):
    """Handle AI support conversation"""
    try:
        user_id = message.from_user.id
        
        # Get user info
        user = await db_manager.users.get_user(user_id)
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        # Show thinking message
        thinking_text = translator.get_text('ai_thinking', user_lang)
        thinking_msg = await message.reply_text(thinking_text)
        
        # Get user context for better AI response
        user_context = {
            'plan': user.get('subscription_plan', 'free') if user else 'free',
            'shop_status': 'active' if user and user.get('shop_id') else 'none',
            'created_at': user.get('created_at', 'Unknown') if user else 'Unknown',
            'last_activity': user.get('last_activity', 'Unknown') if user else 'Unknown'
        }
        
        # Get AI response
        if ai_service.is_available():
            ai_response = await ai_service.get_support_response(
                user_message,
                user_lang,
                user_context
            )
            
            # Analyze user intent for analytics
            intent_data = await ai_service.analyze_user_intent(user_message, user_lang)
            
            # Generate quick replies
            quick_replies = await ai_service.generate_quick_replies(user_message, user_lang)
            
        else:
            # Fallback response
            ai_response = ai_service._get_fallback_response(user_message, user_lang)
            intent_data = {"intent": "general_inquiry", "confidence": 0.5}
            quick_replies = ai_service._get_default_quick_replies(user_lang)
        
        # Delete thinking message
        await thinking_msg.delete()
        
        # Create response keyboard
        keyboard = Keyboards.ai_response_keyboard(user_lang)
        
        # Send AI response
        await message.reply_text(
            ai_response,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Record analytics
        if db_manager.analytics:
            await db_manager.analytics.record_event('ai_conversation', user_id, {
                'intent': intent_data.get('intent', 'unknown'),
                'confidence': intent_data.get('confidence', 0.0),
                'message_length': len(user_message),
                'language': user_lang
            })
        
        # Store conversation for AI training
        conversation_history = [
            {'role': 'user', 'content': user_message, 'language': user_lang},
            {'role': 'assistant', 'content': ai_response, 'language': user_lang}
        ]
        await ai_service.train_on_conversation(user_id, conversation_history)
        
    except Exception as e:
        logger.error(f"AI support message error: {e}")
        # Delete thinking message if it exists
        try:
            await thinking_msg.delete()
        except:
            pass
        
        error_texts = {
            'fa': "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید یا با پشتیبان انسانی تماس بگیرید.",
            'en': "❌ Sorry, an error occurred. Please try again or contact human support.",
            'ar': "❌ عذراً، حدث خطأ. يرجى المحاولة مرة أخرى أو الاتصال بالدعم البشري."
        }
        
        user = await db_manager.users.get_user(user_id)
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        keyboard = Keyboards.ai_support_keyboard(user_lang)
        await message.reply_text(error_texts[user_lang], reply_markup=keyboard)

# Photo handler
async def process_product_image(client: Client, message: Message):
    """Process product image upload"""
    await message.reply_text("آپلود تصویر محصول - در حال توسعه")

async def process_payment_receipt(client: Client, message: Message):
    """Process payment receipt upload"""
    await message.reply_text("آپلود رسید پرداخت - در حال توسعه")

async def process_product_document(client: Client, message: Message):
    """Process product document upload"""
    await message.reply_text("آپلود مستندات محصول - در حال توسعه")

# Helper functions for shop creation
async def start_shop_creation(client: Client, callback_query: CallbackQuery):
    """Start shop creation process"""
    try:
        user_id = callback_query.from_user.id
        
        # Check if user already has a shop
        shop = await db_manager.shops.get_shop_by_owner(user_id) if db_manager.shops else None
        if shop:
            await callback_query.answer("شما قبلاً فروشگاه ایجاد کرده‌اید")
            return
        
        user = await db_manager.users.get_user(user_id) if db_manager.users else None
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        # Start shop creation flow
        prompt_text = translator.get_text('enter_shop_name', user_lang)
        await callback_query.message.edit_text(prompt_text)
        user_states[user_id] = 'entering_shop_name'
        await callback_query.answer()
        
    except Exception as e:
        logger.error(f"Error starting shop creation: {e}")

async def create_sub_bot(shop_name: str) -> Optional[str]:
    """Create a sub-bot for the shop"""
    try:
        # For production, this would integrate with BotFather API
        # For now, return a placeholder token that can be used for testing
        if Config.DEMO_MODE:
            # Generate a demo token for testing
            import secrets
            demo_token = f"demo_{secrets.token_hex(8)}:{secrets.token_hex(16)}"
            logger.info(f"Demo sub-bot token generated for shop {shop_name}")
            return demo_token
        
        # In production, this would:
        # 1. Call BotFather API to create new bot
        # 2. Set bot name and username based on shop name
        # 3. Get bot token from BotFather
        # 4. Return the token
        
        logger.warning("Sub-bot creation not implemented for production mode")
        return None
        
    except Exception as e:
        logger.error(f"Error creating sub-bot for {shop_name}: {e}")
        return None

async def create_user_shop(user_id: int, shop_data: dict) -> dict:
    """Create a new shop for user"""
    try:
        if not db_manager.shops:
            return None
        
        # Create shop in database
        shop = await db_manager.shops.create_shop(shop_data)
        
        # Create sub-bot for the shop
        try:
            shop_token = await create_sub_bot(shop['name'])
            if shop_token:
                await db_manager.shops.update_shop(shop['_id'], {'bot_token': shop_token})
                logger.info(f"Sub-bot created for shop {shop['name']}")
            else:
                logger.warning(f"Failed to create sub-bot for shop {shop['name']}")
        except Exception as e:
            logger.error(f"Error creating sub-bot for shop {shop['name']}: {e}")
        
        # Send notification to admin
        await NotificationManager.notify_new_shop(None, shop)  # client will be passed properly in real implementation
        
        return shop
        
    except Exception as e:
        logger.error(f"Error creating user shop: {e}")
        return None

async def process_shop_name(client: Client, message: Message):
    """Process shop name input"""
    try:
        user_id = message.from_user.id
        shop_name = message.text.strip()
        
        # Validate shop name
        if not Validation.validate_shop_name(shop_name):
            await message.reply_text("نام فروشگاه نامعتبر است. لطفاً نام دیگری انتخاب کنید.")
            return
        
        # Store shop name and ask for description
        user_states[user_id] = 'entering_shop_description'
        admin_states[user_id] = {'shop_name': shop_name}
        
        await message.reply_text("✅ نام فروشگاه ثبت شد.\n\nحالا توضیح کوتاهی درباره فروشگاه خود بنویسید:")
        
    except Exception as e:
        logger.error(f"Error processing shop name: {e}")

async def process_shop_description(client: Client, message: Message):
    """Process shop description input"""
    try:
        user_id = message.from_user.id
        description = message.text.strip()
        
        shop_data = admin_states.get(user_id, {})
        shop_data.update({
            'description': description,
            'owner_id': user_id
        })
        
        # Create the shop
        shop = await create_user_shop(user_id, shop_data)
        
        if shop:
            user_states.pop(user_id, None)
            admin_states.pop(user_id, None)
            
            success_msg = f"🎉 فروشگاه '{shop['name']}' با موفقیت ایجاد شد!\n\n"
            success_msg += "فروشگاه شما در حال بررسی است و پس از تأیید، فعال خواهد شد."
            
            keyboard = Keyboards.shop_created_keyboard()
            await message.reply_text(success_msg, reply_markup=keyboard)
        else:
            await message.reply_text("خطا در ایجاد فروشگاه. لطفاً دوباره تلاش کنید.")
        
    except Exception as e:
        logger.error(f"Error processing shop description: {e}")

# Placeholder implementations for missing functions
async def select_plan(client: Client, callback_query: CallbackQuery):
    """Handle plan selection"""
    await callback_query.answer("انتخاب پلن - در حال توسعه")

async def show_shop_management(client: Client, callback_query: CallbackQuery):
    """Show shop management menu"""
    await callback_query.answer("مدیریت فروشگاه - در حال توسعه")

async def show_products_menu(client: Client, callback_query: CallbackQuery):
    """Show products management menu"""
    await callback_query.answer("مدیریت محصولات - در حال توسعه")

async def show_orders_menu(client: Client, callback_query: CallbackQuery):
    """Show orders menu"""
    await callback_query.answer("مدیریت سفارشات - در حال توسعه")

async def show_reports_menu(client: Client, callback_query: CallbackQuery):
    """Show reports menu"""
    await callback_query.answer("گزارشات - در حال توسعه")

async def show_admin_users(client: Client, callback_query: CallbackQuery):
    """Show admin users management"""
    await callback_query.answer("مدیریت کاربران - در حال توسعه")

async def show_admin_shops(client: Client, callback_query: CallbackQuery):
    """Show admin shops management"""
    await callback_query.answer("مدیریت فروشگاه‌ها - در حال توسعه")

async def show_admin_stats(client: Client, callback_query: CallbackQuery):
    """Show admin statistics"""
    await callback_query.answer("آمار و گزارشات - در حال توسعه")

async def show_admin_payments(client: Client, callback_query: CallbackQuery):
    """Show admin payments"""
    await callback_query.answer("مدیریت پرداخت‌ها - در حال توسعه")

async def start_broadcast(client: Client, callback_query: CallbackQuery):
    """Start broadcast message"""
    await callback_query.answer("ارسال پیام همگانی - در حال توسعه")

async def process_payment_submission(client: Client, callback_query: CallbackQuery):
    """Process payment submission"""
    await callback_query.answer("ثبت پرداخت - در حال توسعه")

async def verify_payment(client: Client, callback_query: CallbackQuery):
    """Verify payment by admin"""
    await callback_query.answer("تأیید پرداخت - در حال توسعه")

async def show_profile_settings(client: Client, callback_query: CallbackQuery):
    """Show profile settings"""
    await callback_query.answer("تنظیمات پروفایل - در حال توسعه")

async def show_referral_info(client: Client, callback_query: CallbackQuery):
    """Show referral information"""
    await callback_query.answer("اطلاعات معرفی - در حال توسعه")

async def process_product_name(client: Client, message: Message):
    """Process product name input"""
    await message.reply_text("ثبت نام محصول - در حال توسعه")

async def process_product_price(client: Client, message: Message):
    """Process product price input"""
    await message.reply_text("ثبت قیمت محصول - در حال توسعه")

async def process_broadcast_message(client: Client, message: Message):
    """Process broadcast message"""
    await message.reply_text("ارسال پیام همگانی - در حال توسعه")

# Main function
async def main():
    """Main function to run the bot"""
    global app, db_manager, email_service, logger
    
    try:
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
        
        # Initialize bot client
        app = Client(
            "coderoot_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )
        
        # Initialize services
        email_service = EmailService()
        db_manager = DatabaseManager()
        
        logger.info("🚀 CodeRoot Bot starting up...")
        
        # Start the bot
        await app.start()
        
        # Register all handlers
        register_handlers(app)
        
        # Call startup function
        await startup()
        
        # Start health check server for Render
        await start_health_server()
        
        logger.info("🤖 CodeRoot Bot is running...")
        
        # Keep the bot running
        await app.idle()
        
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")
        raise
    finally:
        await shutdown()

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    # Remove dangerous characters and limit length
    import re
    sanitized = re.sub(r'[<>"\']', '', text)
    return sanitized[:1000]  # Limit to 1000 characters

async def handle_support_text_messages(client: Client, message: Message):
    """Handle support-related text messages"""
    try:
        user_id = message.from_user.id
        
        # Check if user is in support mode
        state = user_states.get(user_id)
        
        if state == 'ai_support':
            user = await db_manager.users.get_user(user_id) if db_manager.users else None
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            await handle_ai_conversation(client, message, user_lang)
        elif state in ['entering_shop_name']:
            await process_shop_name(client, message)
        elif state in ['entering_shop_description']:
            await process_shop_description(client, message)
        # Add other state handlers as needed
            
    except Exception as e:
        logger.error(f"Error handling support text messages: {e}")

class SupportHandler:
    """Support system handler"""
    
    @staticmethod
    async def show_support_menu(client: Client, callback_query: CallbackQuery):
        """Show support menu"""
        user_id = callback_query.from_user.id
        user = await db_manager.users.get_user(user_id) if db_manager.users else None
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        support_text = translator.get_text('support_menu', user_lang)
        keyboard = Keyboards.support_menu_keyboard(user_lang)
        
        await callback_query.edit_message_text(support_text, reply_markup=keyboard)
    
    @staticmethod
    async def start_ai_support(client: Client, callback_query: CallbackQuery):
        """Start AI support session"""
        user_id = callback_query.from_user.id
        user = await db_manager.users.get_user(user_id) if db_manager.users else None
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        welcome_text = translator.get_text('ai_support_welcome', user_lang)
        keyboard = Keyboards.ai_support_keyboard(user_lang)
        
        user_states[user_id] = 'ai_support'
        
        await callback_query.edit_message_text(welcome_text, reply_markup=keyboard)
        await callback_query.answer("پشتیبانی هوشمند فعال شد")
    
    @staticmethod
    async def contact_human_support(client: Client, callback_query: CallbackQuery):
        """Contact human support"""
        user_id = callback_query.from_user.id
        user = await db_manager.users.get_user(user_id) if db_manager.users else None
        user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
        
        contact_text = translator.get_text('support_contact', user_lang)
        keyboard = Keyboards.main_menu_keyboard(user_lang)
        
        await callback_query.edit_message_text(contact_text, reply_markup=keyboard)
    
    @staticmethod
    async def get_feature_help(client: Client, callback_query: CallbackQuery):
        """Get feature help"""
        await callback_query.answer("راهنمای ویژگی‌ها - در حال توسعه")
    
    @staticmethod
    async def suggest_plan_upgrade(client: Client, callback_query: CallbackQuery):
        """Suggest plan upgrade"""
        await callback_query.answer("پیشنهاد ارتقا پلن - در حال توسعه")
    
    @staticmethod
    async def analyze_user_issue(client: Client, callback_query: CallbackQuery):
        """Analyze user issue"""
        await callback_query.answer("تحلیل مشکل - در حال توسعه")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")