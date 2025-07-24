import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Use mock database for demo
try:
    from database_mock import UserManager, ShopManager, PaymentManager
except ImportError:
    from database import UserManager, ShopManager, PaymentManager

from utils import (
    BotUtils, MessageTemplates, KeyboardMarkups, ValidationUtils, 
    SecurityUtils, NotificationUtils, TimeUtils
)
from config import Config, PLANS

logger = logging.getLogger(__name__)

# User states for conversation flow
user_states = {}

class UserHandlers:
    """User-related message and callback handlers"""
    
    @staticmethod
    async def start_command(client: Client, message: Message):
        """Handle /start command"""
        try:
            user_id = message.from_user.id
            
            # Check if user exists
            user = await UserManager.get_user(user_id)
            
            if not user:
                # Create new user
                user_data = {
                    "user_id": user_id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "phone": None
                }
                user = await UserManager.create_user(user_data)
                
                # Send welcome message for new users
                welcome_text = MessageTemplates.WELCOME_MESSAGE
                
                # Notify admin about new user (skip in demo mode)
                try:
                    await NotificationUtils.send_admin_notification(
                        client, 
                        f"کاربر جدید:\n👤 {message.from_user.first_name}\n🆔 {user_id}\n📱 @{message.from_user.username or 'بدون نام کاربری'}"
                    )
                except:
                    pass  # Ignore in demo mode
            else:
                welcome_text = f"👋 سلام {user['first_name']}!\n\nبه ربات CodeRoot خوش برگشتید."
            
            # Skip channel membership check in demo mode
            skip_channel_check = True
            
            if not skip_channel_check and Config.MAIN_CHANNEL_USERNAME:
                is_member = await BotUtils.check_channel_membership(
                    client, user_id, Config.MAIN_CHANNEL_USERNAME
                )
                
                if not is_member:
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{Config.MAIN_CHANNEL_USERNAME}")],
                        [InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")]
                    ])
                    
                    await message.reply_text(
                        "🔒 برای استفاده از ربات ابتدا باید در کانال ما عضو شوید:",
                        reply_markup=keyboard
                    )
                    return
            
            # Show main menu
            keyboard = KeyboardMarkups.main_menu()
            
            # Add admin menu for admin users
            if await SecurityUtils.is_user_admin(user_id):
                admin_button = [InlineKeyboardButton("⚙️ پنل مدیریت", callback_data="admin_panel")]
                keyboard.inline_keyboard.insert(0, admin_button)
            
            await message.reply_text(welcome_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await message.reply_text("❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    
    @staticmethod
    async def check_membership_callback(client: Client, callback_query: CallbackQuery):
        """Handle membership check callback"""
        try:
            user_id = callback_query.from_user.id
            
            # Auto-approve in demo mode
            await callback_query.answer("✅ عضویت شما تأیید شد!")
            
            # Show main menu
            keyboard = KeyboardMarkups.main_menu()
            
            if await SecurityUtils.is_user_admin(user_id):
                admin_button = [InlineKeyboardButton("⚙️ پنل مدیریت", callback_data="admin_panel")]
                keyboard.inline_keyboard.insert(0, admin_button)
            
            await callback_query.message.edit_text(
                MessageTemplates.WELCOME_MESSAGE,
                reply_markup=keyboard
            )
                
        except Exception as e:
            logger.error(f"Error checking membership: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def create_shop_callback(client: Client, callback_query: CallbackQuery):
        """Handle create shop callback"""
        try:
            user_id = callback_query.from_user.id
            
            # Check if user already has a shop
            existing_shop = await ShopManager.get_shop_by_owner(user_id)
            if existing_shop:
                await callback_query.answer("⚠️ شما قبلاً فروشگاه ایجاد کرده‌اید!", show_alert=True)
                return
            
            # Show plans menu
            keyboard = KeyboardMarkups.plans_menu()
            
            plans_text = "💎 انتخاب پلن اشتراک:\n\n"
            
            for plan_key, plan_data in PLANS.items():
                emoji = "🆓" if plan_key == "free" else "💎"
                price_text = "رایگان" if plan_data['price'] == 0 else f"{plan_data['price']:,} تومان"
                
                plans_text += f"{emoji} {plan_data['name']} - {price_text}\n"
                plans_text += f"   📦 تا {plan_data['max_products'] if plan_data['max_products'] != -1 else 'نامحدود'} محصول\n"
                if plan_data['advanced_reports']:
                    plans_text += "   📊 گزارش‌های حرفه‌ای\n"
                if plan_data['auto_messages']:
                    plans_text += "   🤖 پیام‌های خودکار\n"
                if plan_data['discounts']:
                    plans_text += "   🎁 سیستم تخفیف\n"
                if plan_data['commission'] == 0:
                    plans_text += "   💰 بدون کارمزد\n"
                else:
                    plans_text += f"   💰 {plan_data['commission']}% کارمزد\n"
                plans_text += "\n"
            
            await callback_query.message.edit_text(plans_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in create shop: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def select_plan_callback(client: Client, callback_query: CallbackQuery):
        """Handle plan selection callback"""
        try:
            user_id = callback_query.from_user.id
            plan_key = callback_query.data.split(":")[1]
            
            if plan_key not in PLANS:
                await callback_query.answer("❌ پلن نامعتبر!", show_alert=True)
                return
            
            plan_data = PLANS[plan_key]
            
            # Store selected plan in user state
            if user_id not in user_states:
                user_states[user_id] = {}
            user_states[user_id]['selected_plan'] = plan_key
            
            # In demo mode, skip payment for all plans
            await callback_query.message.edit_text(
                "🏪 نام فروشگاه خود را وارد کنید:\n\n📝 نام باید بین 3 تا 50 کاراکتر باشد\n\n🎭 نسخه دمو: پرداخت نیاز نیست",
                reply_markup=KeyboardMarkups.cancel_keyboard()
            )
            user_states[user_id]['state'] = 'waiting_shop_name'
            
        except Exception as e:
            logger.error(f"Error selecting plan: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def payment_done_callback(client: Client, callback_query: CallbackQuery):
        """Handle payment done callback"""
        try:
            user_id = callback_query.from_user.id
            
            await callback_query.message.edit_text(
                "📷 لطفاً تصویر رسید پرداخت را ارسال کنید:\n\n🎭 در نسخه دمو خودکار تأیید می‌شود",
                reply_markup=KeyboardMarkups.cancel_keyboard()
            )
            
            # Update user state
            if user_id not in user_states:
                user_states[user_id] = {}
            user_states[user_id]['state'] = 'waiting_payment_receipt'
            
        except Exception as e:
            logger.error(f"Error in payment done: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def handle_text_messages(client: Client, message: Message):
        """Handle text messages based on user state"""
        try:
            user_id = message.from_user.id
            
            if user_id not in user_states:
                return
            
            state = user_states[user_id].get('state')
            
            if state == 'waiting_shop_name':
                await UserHandlers.handle_shop_name_input(client, message)
            elif state == 'waiting_bot_token':
                await UserHandlers.handle_bot_token_input(client, message)
            elif state == 'waiting_phone':
                await UserHandlers.handle_phone_input(client, message)
                
        except Exception as e:
            logger.error(f"Error handling text message: {e}")
    
    @staticmethod
    async def handle_shop_name_input(client: Client, message: Message):
        """Handle shop name input"""
        try:
            user_id = message.from_user.id
            shop_name = SecurityUtils.sanitize_input(message.text)
            
            if not ValidationUtils.validate_shop_name(shop_name):
                await message.reply_text(
                    "❌ نام فروشگاه نامعتبر است!\n\n"
                    "📝 نام باید:\n"
                    "• بین 3 تا 50 کاراکتر باشد\n"
                    "• شامل کاراکترهای خاص نباشد\n\n"
                    "🔄 دوباره تلاش کنید:",
                    reply_markup=KeyboardMarkups.cancel_keyboard()
                )
                return
            
            # Store shop name
            user_states[user_id]['shop_name'] = shop_name
            
            # In demo mode, use fake token
            await message.reply_text(
                "🤖 توکن ربات فروشگاه خود را وارد کنید:\n\n"
                "🎭 نسخه دمو: هر متنی وارد کنید (توکن شبیه‌سازی می‌شود)\n\n"
                "📝 در نسخه اصلی:\n"
                "1️⃣ به @BotFather مراجعه کنید\n"
                "2️⃣ ربات جدید بسازید\n"
                "3️⃣ توکن دریافتی را اینجا ارسال کنید",
                reply_markup=KeyboardMarkups.cancel_keyboard()
            )
            
            user_states[user_id]['state'] = 'waiting_bot_token'
            
        except Exception as e:
            logger.error(f"Error handling shop name: {e}")
    
    @staticmethod
    async def handle_bot_token_input(client: Client, message: Message):
        """Handle bot token input"""
        try:
            user_id = message.from_user.id
            bot_token = message.text.strip()
            
            # In demo mode, accept any input and generate fake token
            fake_token = f"123456789:demo_token_for_{user_id}"
            
            # Store bot token
            user_states[user_id]['bot_token'] = fake_token
            
            # Ask for phone number
            await message.reply_text(
                "📱 شماره تلفن خود را وارد کنید:\n\n"
                "🎭 نسخه دمو: هر شماره‌ای وارد کنید\n"
                "📝 مثال: 09123456789\n\n"
                "⚠️ در نسخه اصلی این شماره برای تماس در مواقع ضروری استفاده می‌شود",
                reply_markup=KeyboardMarkups.cancel_keyboard()
            )
            
            user_states[user_id]['state'] = 'waiting_phone'
            
        except Exception as e:
            logger.error(f"Error handling bot token: {e}")
    
    @staticmethod
    async def handle_phone_input(client: Client, message: Message):
        """Handle phone number input"""
        try:
            user_id = message.from_user.id
            phone = message.text.strip()
            
            # In demo mode, accept any phone format
            if len(phone) < 10:
                await message.reply_text(
                    "❌ شماره تلفن کوتاه است!\n\n"
                    "🎭 در نسخه دمو: حداقل 10 رقم وارد کنید\n"
                    "📝 مثال: 09123456789\n\n"
                    "🔄 دوباره تلاش کنید:",
                    reply_markup=KeyboardMarkups.cancel_keyboard()
                )
                return
            
            # Create shop
            await UserHandlers.create_shop_final(client, message, phone)
            
        except Exception as e:
            logger.error(f"Error handling phone: {e}")
    
    @staticmethod
    async def create_shop_final(client: Client, message: Message, phone: str):
        """Create shop with all collected information"""
        try:
            user_id = message.from_user.id
            state_data = user_states.get(user_id, {})
            
            selected_plan = state_data.get('selected_plan', 'free')
            shop_name = state_data.get('shop_name')
            bot_token = state_data.get('bot_token')
            
            if not all([shop_name, bot_token]):
                await message.reply_text("❌ اطلاعات ناقص است. لطفاً دوباره شروع کنید.")
                return
            
            # Update user phone
            await UserManager.update_user(user_id, {"phone": phone})
            
            # Create shop
            shop_data = {
                "owner_id": user_id,
                "name": shop_name,
                "bot_token": bot_token,
                "bot_username": f"demo_shop_{user_id}",
                "plan": selected_plan,
                "settings": {
                    "welcome_message": f"🛍 به فروشگاه {shop_name} خوش آمدید!",
                    "auto_approve_orders": False,
                    "payment_methods": ["card_to_card"],
                    "delivery_info": "تحویل حضوری یا پست پیشتاز"
                }
            }
            
            shop = await ShopManager.create_shop(shop_data)
            
            # Update user subscription
            plan_data = PLANS[selected_plan]
            await UserManager.update_subscription(user_id, selected_plan, plan_data['duration_days'])
            
            # Create payment record (auto-confirmed in demo)
            payment_data = {
                "user_id": user_id,
                "shop_id": str(shop['_id']),
                "amount": plan_data['price'],
                "payment_type": "subscription",
                "plan": selected_plan,
                "description": f"خرید اشتراک {plan_data['name']} (دمو)"
            }
            await PaymentManager.create_payment(payment_data)
            
            # Clear user state
            if user_id in user_states:
                del user_states[user_id]
            
            # Send success message
            expires_date = BotUtils.format_date(datetime.utcnow() + timedelta(days=plan_data['duration_days']))
            
            success_message = f"""
🎊 تبریک! فروشگاه دمو شما ایجاد شد

📋 اطلاعات فروشگاه:
🏪 نام: {shop_name}
🤖 ربات: @{shop_data['bot_username']}
📊 پلن: {plan_data['name']}
⏰ انقضا: {expires_date}

🎭 حالت دمو: فروشگاه شما فوراً فعال شد!
✅ از منوی اصلی وارد "فروشگاه من" شوید
            """
            
            keyboard = KeyboardMarkups.main_menu()
            await message.reply_text(success_message, reply_markup=keyboard)
            
            # Notify admin (skip in demo mode)
            try:
                await NotificationUtils.send_admin_notification(
                    client,
                    f"فروشگاه دمو جدید:\n🏪 {shop_name}\n👤 {message.from_user.first_name}\n📊 {plan_data['name']}"
                )
            except:
                pass
            
        except Exception as e:
            logger.error(f"Error creating shop: {e}")
            await message.reply_text("❌ خطایی در ایجاد فروشگاه رخ داد. لطفاً با پشتیبانی تماس بگیرید.")
    
    @staticmethod
    async def my_shop_callback(client: Client, callback_query: CallbackQuery):
        """Handle my shop callback"""
        try:
            user_id = callback_query.from_user.id
            
            # Get user's shop
            shop = await ShopManager.get_shop_by_owner(user_id)
            if not shop:
                await callback_query.answer("❌ شما هنوز فروشگاهی ندارید!", show_alert=True)
                return
            
            # Get user subscription info
            user = await UserManager.get_user(user_id)
            subscription = user.get('subscription', {})
            plan_key = subscription.get('plan', 'free')
            plan_data = PLANS.get(plan_key, PLANS['free'])
            
            # Check subscription status
            expires_at = subscription.get('expires_at', datetime.utcnow())
            is_expired = TimeUtils.is_subscription_expired(expires_at)
            days_left = TimeUtils.days_until_expiration(expires_at)
            
            shop_info = f"🏪 فروشگاه: {shop['name']}\n"
            shop_info += f"🤖 ربات: @{shop.get('bot_username', 'نامشخص')}\n"
            shop_info += f"📊 پلن: {plan_data['name']}\n"
            shop_info += f"📅 انقضا: {BotUtils.format_date(expires_at)}\n"
            shop_info += f"⏰ باقی‌مانده: {days_left} روز\n"
            shop_info += f"📊 وضعیت: {'❌ منقضی شده' if is_expired else '✅ فعال'}\n\n"
            
            # Add statistics (demo data)
            shop_info += f"📦 محصولات: 5 (دمو)\n"
            shop_info += f"🛒 سفارش‌ها: 12 (دمو)\n"
            shop_info += f"💰 درآمد: {BotUtils.format_price(2500000)} (دمو)\n\n"
            shop_info += "🎭 داده‌های بالا نمونه برای دمو هستند"
            
            keyboard = KeyboardMarkups.shop_management_menu()
            await callback_query.message.edit_text(shop_info, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in my shop: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def cancel_callback(client: Client, callback_query: CallbackQuery):
        """Handle cancel callback"""
        try:
            user_id = callback_query.from_user.id
            
            # Clear user state
            if user_id in user_states:
                del user_states[user_id]
            
            # Return to main menu
            keyboard = KeyboardMarkups.main_menu()
            
            if await SecurityUtils.is_user_admin(user_id):
                admin_button = [InlineKeyboardButton("⚙️ پنل مدیریت", callback_data="admin_panel")]
                keyboard.inline_keyboard.insert(0, admin_button)
            
            await callback_query.message.edit_text(
                MessageTemplates.WELCOME_MESSAGE,
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in cancel: {e}")
            await callback_query.answer("❌ خطایی رخ داد!")
    
    @staticmethod
    async def back_to_main_callback(client: Client, callback_query: CallbackQuery):
        """Handle back to main callback"""
        await UserHandlers.cancel_callback(client, callback_query)