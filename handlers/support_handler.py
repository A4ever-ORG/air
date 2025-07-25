"""
Support Handler for CodeRoot Bot
Handles support requests and integrates AI for intelligent responses
"""

import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import db_manager
from services.ai_service import ai_service
from utils.keyboards import Keyboards
from utils.language import translator
from utils.bot_utils import BotUtils
from utils.notifications import NotificationManager
from config import Config

logger = logging.getLogger(__name__)

# Support states for conversation flow
support_states = {}

class SupportHandler:
    """Handles all support-related functionality"""
    
    @staticmethod
    async def show_support_menu(client: Client, callback_query: CallbackQuery):
        """Show support menu with options"""
        try:
            user_id = callback_query.from_user.id
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            support_text = translator.get_text('support_menu', user_lang)
            keyboard = Keyboards.support_menu_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                support_text,
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error showing support menu: {e}")
            await callback_query.answer("خطایی رخ داد", show_alert=True)
    
    @staticmethod
    async def start_ai_support(client: Client, callback_query: CallbackQuery):
        """Start AI-powered support chat"""
        try:
            user_id = callback_query.from_user.id
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            # Test AI connection first
            if not await ai_service.test_ai_connection():
                fallback_text = translator.get_text('ai_unavailable', user_lang)
                keyboard = Keyboards.support_menu_keyboard(user_lang)
                await callback_query.edit_message_text(fallback_text, reply_markup=keyboard)
                return
            
            # Start AI conversation
            welcome_text = translator.get_text('ai_support_welcome', user_lang)
            ai_response = await ai_service.get_ai_response(
                user_id, 
                "سلام! من برای دریافت پشتیبانی هوشمند آماده هستم.", 
                user_lang
            )
            
            full_message = f"{welcome_text}\n\n🤖 **CodeRoot AI:**\n{ai_response}"
            
            # Set user state for AI conversation
            support_states[user_id] = {
                'mode': 'ai_chat',
                'language': user_lang,
                'started_at': datetime.now()
            }
            
            keyboard = Keyboards.ai_support_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                full_message,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error starting AI support: {e}")
            await callback_query.answer("خطایی رخ داد", show_alert=True)
    
    @staticmethod
    async def handle_ai_question(client: Client, message: Message):
        """Handle AI support questions"""
        try:
            user_id = message.from_user.id
            
            # Check if user is in AI support mode
            if support_states.get(user_id) != 'ai_support':
                return
            
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            # Show typing action
            await client.send_chat_action(message.chat.id, "typing")
            
            # Build user context for AI
            user_context = {
                'user_id': user_id,
                'language': user_lang,
                'plan': user.get('plan', 'free') if user else 'none',
                'shop_status': user.get('shop_status', 'none') if user else 'none',
                'registration_date': user.get('created_at', 'unknown') if user else 'unknown'
            }
            
            # Get AI response
            ai_response = await ai_service.get_support_response(
                message.text,
                user_lang,
                user_context
            )
            
            # Create keyboard with options
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        translator.get_text('continue_ai_chat', user_lang), 
                        callback_data='ai_continue'
                    ),
                    InlineKeyboardButton(
                        translator.get_text('contact_human', user_lang), 
                        callback_data='support_human'
                    )
                ],
                [
                    InlineKeyboardButton(
                        translator.get_text('support_menu', user_lang), 
                        callback_data='support_menu'
                    ),
                    InlineKeyboardButton(
                        translator.get_text('main_menu', user_lang), 
                        callback_data='main_menu'
                    )
                ]
            ])
            
            await message.reply_text(ai_response, reply_markup=keyboard)
            
            # Record analytics
            if db_manager.analytics:
                await db_manager.analytics.record_event('ai_support_used', user_id, {
                    'question_length': len(message.text),
                    'language': user_lang
                })
            
        except Exception as e:
            logger.error(f"Error handling AI question: {e}")
            await message.reply_text("متاسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    
    @staticmethod
    async def get_feature_help(client: Client, callback_query: CallbackQuery):
        """Get help about specific features"""
        try:
            user_id = callback_query.from_user.id
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            # Extract feature from callback data
            feature = callback_query.data.split('_')[-1]
            
            # Show typing action
            await client.send_chat_action(callback_query.message.chat.id, "typing")
            
            # Get AI explanation of feature
            explanation = await ai_service.get_feature_explanation(feature, user_lang)
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        translator.get_text('back_to_support', user_lang), 
                        callback_data='support_menu'
                    ),
                    InlineKeyboardButton(
                        translator.get_text('ask_ai', user_lang), 
                        callback_data='support_ai'
                    )
                ]
            ])
            
            await callback_query.edit_message_text(explanation, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error getting feature help: {e}")
            await callback_query.answer("خطایی رخ داد", show_alert=True)
    
    @staticmethod
    async def suggest_plan_upgrade(client: Client, callback_query: CallbackQuery):
        """Get AI-powered plan upgrade suggestions"""
        try:
            user_id = callback_query.from_user.id
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            current_plan = user.get('plan', 'free') if user else 'none'
            
            # Show typing action
            await client.send_chat_action(callback_query.message.chat.id, "typing")
            
            # Default user needs based on current plan
            user_needs = f"User has {current_plan} plan and wants to know upgrade options"
            
            # Get AI recommendation
            recommendation = await ai_service.suggest_plan_upgrade(current_plan, user_needs, user_lang)
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        translator.get_text('view_plans', user_lang), 
                        callback_data='shop_plans'
                    ),
                    InlineKeyboardButton(
                        translator.get_text('upgrade_now', user_lang), 
                        callback_data='shop_upgrade'
                    )
                ],
                [
                    InlineKeyboardButton(
                        translator.get_text('back_to_support', user_lang), 
                        callback_data='support_menu'
                    )
                ]
            ])
            
            await callback_query.edit_message_text(recommendation, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error suggesting plan upgrade: {e}")
            await callback_query.answer("خطایی رخ داد", show_alert=True)
    
    @staticmethod
    async def contact_human_support(client: Client, callback_query: CallbackQuery):
        """Contact human support (admin)"""
        try:
            user_id = callback_query.from_user.id
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            support_states[user_id] = 'human_support'
            
            human_support_text = translator.get_text('human_support_intro', user_lang)
            keyboard = Keyboards.human_support_keyboard(user_lang)
            
            await callback_query.edit_message_text(
                human_support_text,
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error contacting human support: {e}")
            await callback_query.answer("خطایی رخ داد", show_alert=True)
    
    @staticmethod
    async def handle_human_support_message(client: Client, message: Message):
        """Handle messages to human support"""
        try:
            user_id = message.from_user.id
            
            # Check if user is in human support mode
            if support_states.get(user_id) != 'human_support':
                return
            
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            # Forward message to admin
            admin_message = f"""
🆘 **پیام پشتیبانی جدید**

👤 **کاربر:** {message.from_user.first_name} (@{message.from_user.username or 'بدون یوزرنیم'})
🆔 **شناسه:** `{user_id}`
🌍 **زبان:** {user_lang}
📅 **تاریخ:** {BotUtils.format_datetime_persian(message.date)}

💬 **پیام:**
{message.text}
"""
            
            try:
                await client.send_message(Config.ADMIN_USER_ID, admin_message)
                
                confirmation = translator.get_text('support_message_sent', user_lang)
                keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            translator.get_text('back_to_support', user_lang), 
                            callback_data='support_menu'
                        )
                    ]
                ])
                
                await message.reply_text(confirmation, reply_markup=keyboard)
                
                # Clear support state
                support_states.pop(user_id, None)
                
            except Exception as e:
                logger.error(f"Failed to send message to admin: {e}")
                await message.reply_text(
                    translator.get_text('support_message_failed', user_lang)
                )
            
        except Exception as e:
            logger.error(f"Error handling human support message: {e}")
            await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    
    @staticmethod
    async def analyze_user_issue(client: Client, callback_query: CallbackQuery):
        """Analyze user issue with AI"""
        try:
            user_id = callback_query.from_user.id
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            support_states[user_id] = 'issue_analysis'
            
            analysis_prompt = translator.get_text('describe_issue', user_lang)
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        translator.get_text('cancel', user_lang), 
                        callback_data='support_menu'
                    )
                ]
            ])
            
            await callback_query.edit_message_text(analysis_prompt, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error starting issue analysis: {e}")
            await callback_query.answer("خطایی رخ داد", show_alert=True)
    
    @staticmethod
    async def handle_issue_description(client: Client, message: Message):
        """Handle issue description for AI analysis"""
        try:
            user_id = message.from_user.id
            
            # Check if user is in issue analysis mode
            if support_states.get(user_id) != 'issue_analysis':
                return
            
            user = await db_manager.users.get_user(user_id)
            user_lang = user.get('language', Config.DEFAULT_LANGUAGE) if user else Config.DEFAULT_LANGUAGE
            
            # Show typing action
            await client.send_chat_action(message.chat.id, "typing")
            
            # Get user data for analysis
            user_data = {
                'plan': user.get('plan', 'free') if user else 'none',
                'shop_status': user.get('shop_status', 'none') if user else 'none',
                'language': user_lang,
                'registration_date': str(user.get('created_at', 'unknown')) if user else 'unknown'
            }
            
            # Get AI analysis
            analysis = await ai_service.analyze_user_issue(
                message.text,
                user_data,
                user_lang
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        translator.get_text('contact_admin', user_lang), 
                        callback_data='support_human'
                    ),
                    InlineKeyboardButton(
                        translator.get_text('try_again', user_lang), 
                        callback_data='support_analyze'
                    )
                ],
                [
                    InlineKeyboardButton(
                        translator.get_text('back_to_support', user_lang), 
                        callback_data='support_menu'
                    )
                ]
            ])
            
            await message.reply_text(analysis, reply_markup=keyboard)
            
            # Clear state
            support_states.pop(user_id, None)
            
        except Exception as e:
            logger.error(f"Error handling issue description: {e}")
            await message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

# Register handlers for text messages in support modes
async def handle_support_text_messages(client: Client, message: Message):
    """Route text messages based on support state"""
    user_id = message.from_user.id
    current_state = support_states.get(user_id)
    
    if current_state == 'ai_support':
        await SupportHandler.handle_ai_question(client, message)
    elif current_state == 'human_support':
        await SupportHandler.handle_human_support_message(client, message)
    elif current_state == 'issue_analysis':
        await SupportHandler.handle_issue_description(client, message)