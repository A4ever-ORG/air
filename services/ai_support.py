"""
AI Support Service for CodeRoot Bot
Integrates Liara AI API (Gemini 2.0 Flash) for intelligent customer support
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
from datetime import datetime
import json

from config import Config
from utils.language import translator

logger = logging.getLogger(__name__)

class AISupport:
    """AI-powered support system using Liara AI API"""
    
    def __init__(self):
        """Initialize AI client with configuration"""
        if Config.AI_ENABLED:
            self.client = OpenAI(
                base_url=Config.AI_BASE_URL,
                api_key=Config.AI_API_KEY
            )
            self.model = Config.AI_MODEL
            self.enabled = True
        else:
            self.client = None
            self.model = None
            self.enabled = False
        self.context_cache = {}
        self.translator = translator
        
    def get_system_context(self, language: str = 'fa') -> str:
        """Get comprehensive system context for AI training"""
        contexts = {
            'fa': """شما یک دستیار هوشمند برای ربات CodeRoot هستید. CodeRoot یک سیستم ایجاد فروشگاه آنلاین در تلگرام است.

🏪 اطلاعات کلی CodeRoot:
- ربات مادری که به کاربران امکان ایجاد فروشگاه آنلاین می‌دهد
- سه پلن اشتراک: رایگان، حرفه‌ای (20,000 تومان)، VIP (60,000 تومان)
- سیستم کارمزد 5% (به جز VIP که بدون کارمزد است)
- پشتیبانی از 3 زبان: فارسی، انگلیسی، عربی

📋 پلن‌های اشتراک:
1️⃣ رایگان: 10 محصول، درگاه بیل، گزارش ساده، 5% کارمزد
2️⃣ حرفه‌ای: 200 محصول، گزارش پیشرفته، پیام خودکار، تبلیغات، 5% کارمزد
3️⃣ VIP: نامحدود، درگاه اختصاصی، گزارش کامل، بدون کارمزد

🔧 قابلیت‌های اصلی:
- ایجاد و مدیریت محصولات
- سیستم سفارش‌گیری
- گزارش‌گیری فروش
- پنل مدیریت ادمین
- سیستم معرفی
- جوین اجباری کانال

💳 پرداخت:
- کارت به کارت دستی
- شماره کارت: 6037-9977-7766-5544
- نام صاحب کارت: حادی

🆘 مشکلات رایج و راه‌حل:
- مشکل ورود: بررسی عضویت در کانال
- مشکل پرداخت: ارسال رسید به ادمین
- مشکل محصولات: بررسی محدودیت پلن
- مشکل ربات: تماس با پشتیبانی

همیشه پاسخ‌های مفید، دقیق و مودبانه ارائه دهید.""",

            'en': """You are an intelligent assistant for CodeRoot bot. CodeRoot is an online store creation system on Telegram.

🏪 CodeRoot General Information:
- Mother bot that allows users to create online stores
- Three subscription plans: Free, Professional ($20,000 Toman), VIP ($60,000 Toman)
- 5% commission system (except VIP which is commission-free)
- Supports 3 languages: Persian, English, Arabic

📋 Subscription Plans:
1️⃣ Free: 10 products, Bale gateway, basic reports, 5% commission
2️⃣ Professional: 200 products, advanced reports, auto messages, ads, 5% commission
3️⃣ VIP: Unlimited, dedicated gateway, full reports, no commission

🔧 Main Features:
- Create and manage products
- Order management system
- Sales reporting
- Admin management panel
- Referral system
- Mandatory channel join

💳 Payment:
- Manual card-to-card
- Card number: 6037-9977-7766-5544
- Card holder: Hadi

🆘 Common Issues & Solutions:
- Login issues: Check channel membership
- Payment issues: Send receipt to admin
- Product issues: Check plan limitations
- Bot issues: Contact support

Always provide helpful, accurate, and polite responses.""",

            'ar': """أنت مساعد ذكي لبوت CodeRoot. CodeRoot هو نظام إنشاء متاجر إلكترونية على تليجرام.

🏪 معلومات عامة عن CodeRoot:
- بوت أم يتيح للمستخدمين إنشاء متاجر إلكترونية
- ثلاث خطط اشتراك: مجاني، احترافي (20,000 تومان)، VIP (60,000 تومان)
- نظام عمولة 5% (باستثناء VIP بدون عمولة)
- يدعم 3 لغات: الفارسية، الإنجليزية، العربية

📋 خطط الاشتراك:
1️⃣ مجاني: 10 منتجات، بوابة بيل، تقارير بسيطة، عمولة 5%
2️⃣ احترافي: 200 منتج، تقارير متقدمة، رسائل تلقائية، إعلانات، عمولة 5%
3️⃣ VIP: غير محدود، بوابة مخصصة، تقارير كاملة، بدون عمولة

🔧 الميزات الرئيسية:
- إنشاء وإدارة المنتجات
- نظام إدارة الطلبات
- تقارير المبيعات
- لوحة إدارة الأدمن
- نظام الإحالة
- انضمام إجباري للقناة

💳 الدفع:
- كارت إلى كارت يدوي
- رقم البطاقة: 6037-9977-7766-5544
- حامل البطاقة: حادي

🆘 المشاكل الشائعة والحلول:
- مشاكل الدخول: تحقق من عضوية القناة
- مشاكل الدفع: أرسل الإيصال للأدمن
- مشاكل المنتجات: تحقق من قيود الخطة
- مشاكل البوت: اتصل بالدعم

قدم دائماً إجابات مفيدة ودقيقة ومهذبة."""
        }
        
        return contexts.get(language, contexts['fa'])
    
    async def get_ai_response(self, user_message: str, language: str = 'fa', context: Optional[Dict] = None) -> str:
        """Get AI response for user support"""
        if not self.enabled or not self.client:
            fallbacks = {
                'fa': "سیستم هوش مصنوعی در حال حاضر غیرفعال است. لطفاً با پشتیبانی انسانی تماس بگیرید: @hadi_admin",
                'en': "AI system is currently disabled. Please contact human support: @hadi_admin",
                'ar': "نظام الذكاء الاصطناعي معطل حالياً. يرجى الاتصال بالدعم البشري: @hadi_admin"
            }
            return fallbacks.get(language, fallbacks['fa'])
        
        try:
            # Prepare system context
            system_context = self.get_system_context(language)
            
            # Add user context if available
            if context:
                system_context += f"\n\nمعلومات کاربر:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": system_context
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
            
            # Get AI response
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=Config.AI_MAX_TOKENS,
                temperature=Config.AI_TEMPERATURE,
                top_p=0.9
            )
            
            response = completion.choices[0].message.content
            logger.info(f"AI response generated for language: {language}")
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            
            # Fallback responses
            fallbacks = {
                'fa': "متأسفم، در حال حاضر امکان پاسخ‌گویی ندارم. لطفاً با پشتیبانی تماس بگیرید.",
                'en': "Sorry, I cannot respond right now. Please contact support.",
                'ar': "عذراً، لا يمكنني الرد الآن. يرجى الاتصال بالدعم."
            }
            return fallbacks.get(language, fallbacks['fa'])
    
    async def analyze_user_intent(self, message: str, language: str = 'fa') -> Dict[str, Any]:
        """Analyze user message to understand intent"""
        if not self.enabled or not self.client:
            return {
                "intent": "general",
                "confidence": 0,
                "keywords": [],
                "urgency": "medium"
            }
        
        try:
            intent_prompt = {
                'fa': f"""تحلیل کن که کاربر در پیام زیر چه سوالی داره:
پیام: "{message}"

لطفاً پاسخ رو در قالب JSON برگردان:
{{
    "intent": "نوع سوال (مثل: payment, product, technical, general)",
    "confidence": "درصد اطمینان (0-100)",
    "keywords": ["کلمات کلیدی"],
    "urgency": "high/medium/low"
}}""",
                'en': f"""Analyze what the user is asking in the following message:
Message: "{message}"

Please return the response in JSON format:
{{
    "intent": "question type (e.g., payment, product, technical, general)",
    "confidence": "confidence percentage (0-100)",
    "keywords": ["keywords"],
    "urgency": "high/medium/low"
}}""",
                'ar': f"""حلل ما يسأل عنه المستخدم في الرسالة التالية:
الرسالة: "{message}"

يرجى إرجاع الرد بصيغة JSON:
{{
    "intent": "نوع السؤال (مثل: payment, product, technical, general)",
    "confidence": "نسبة الثقة (0-100)",
    "keywords": ["الكلمات المفتاحية"],
    "urgency": "high/medium/low"
}}"""
            }
            
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": intent_prompt[language]}],
                max_tokens=200,
                temperature=0.3
            )
            
            response = completion.choices[0].message.content
            
            # Try to parse JSON response
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "intent": "general",
                    "confidence": 50,
                    "keywords": [],
                    "urgency": "medium"
                }
                
        except Exception as e:
            logger.error(f"Error analyzing user intent: {e}")
            return {
                "intent": "general",
                "confidence": 0,
                "keywords": [],
                "urgency": "medium"
            }
    
    async def generate_faq_response(self, question: str, language: str = 'fa') -> Optional[str]:
        """Generate FAQ-style response for common questions"""
        if not self.enabled or not self.client:
            return None
        
        try:
            faq_prompt = {
                'fa': f"""کاربر این سوال رو پرسیده: "{question}"

اگر این سوال در مورد CodeRoot (سیستم ایجاد فروشگاه تلگرام) هست، پاسخ کاملی بده.
اگر نیست، فقط بگو "این سوال مربوط به CodeRoot نیست"

سوالات معمول:
- چطور فروشگاه بسازم؟
- پلن‌ها چه قیمتی دارن؟
- چطور پرداخت کنم؟
- چطور محصول اضافه کنم؟
- مشکل ربات دارم چیکار کنم؟""",
                
                'en': f"""User asked this question: "{question}"

If this question is about CodeRoot (Telegram store creation system), give a complete answer.
If not, just say "This question is not related to CodeRoot"

Common questions:
- How to create a store?
- What are the plan prices?
- How to make payment?
- How to add products?
- Bot issues, what to do?""",
                
                'ar': f"""سأل المستخدم هذا السؤال: "{question}"

إذا كان هذا السؤال عن CodeRoot (نظام إنشاء متاجر تليجرام)، أعط إجابة كاملة.
إذا لم يكن كذلك، قل فقط "هذا السؤال غير متعلق بـ CodeRoot"

الأسئلة الشائعة:
- كيفية إنشاء متجر؟
- ما هي أسعار الخطط؟
- كيفية الدفع؟
- كيفية إضافة المنتجات؟
- مشاكل البوت، ماذا أفعل؟"""
            }
            
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": faq_prompt[language]}],
                max_tokens=500,
                temperature=0.5
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating FAQ response: {e}")
            return None
    
    async def get_contextual_help(self, user_state: str, language: str = 'fa') -> str:
        """Get contextual help based on user's current state"""
        if not self.enabled or not self.client:
            fallbacks = {
                'fa': "سیستم هوش مصنوعی غیرفعال است. برای کمک با @hadi_admin تماس بگیرید.",
                'en': "AI system is disabled. Contact @hadi_admin for help.",
                'ar': "نظام الذكاء الاصطناعي معطل. اتصل بـ @hadi_admin للمساعدة."
            }
            return fallbacks.get(language, fallbacks['fa'])
        
        try:
            state_contexts = {
                'fa': {
                    'shop_creation': 'کاربر در حال ایجاد فروشگاه است',
                    'product_management': 'کاربر در حال مدیریت محصولات است',
                    'payment': 'کاربر در حال پرداخت است',
                    'plan_selection': 'کاربر در حال انتخاب پلن است',
                    'order_management': 'کاربر در حال مدیریت سفارشات است'
                },
                'en': {
                    'shop_creation': 'User is creating a store',
                    'product_management': 'User is managing products',
                    'payment': 'User is making payment',
                    'plan_selection': 'User is selecting a plan',
                    'order_management': 'User is managing orders'
                },
                'ar': {
                    'shop_creation': 'المستخدم ينشئ متجراً',
                    'product_management': 'المستخدم يدير المنتجات',
                    'payment': 'المستخدم يقوم بالدفع',
                    'plan_selection': 'المستخدم يختار خطة',
                    'order_management': 'المستخدم يدير الطلبات'
                }
            }
            
            context = state_contexts.get(language, state_contexts['fa']).get(user_state, 'کاربر از ربات استفاده می‌کند')
            
            help_prompt = {
                'fa': f"""کاربر در این وضعیت است: {context}
لطفاً راهنمایی مفیدی برای ادامه کار ارائه دهید.""",
                'en': f"""User is in this state: {context}
Please provide helpful guidance to continue.""",
                'ar': f"""المستخدم في هذه الحالة: {context}
يرجى تقديم إرشادات مفيدة للمتابعة."""
            }
            
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": help_prompt[language]}],
                max_tokens=300,
                temperature=0.6
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting contextual help: {e}")
            return self.translator.get_text('support_contact', language)

class AISupportManager:
    """Manager for AI support integration with bot handlers"""
    
    def __init__(self):
        self.ai_support = AISupport()
        self.active_sessions = {}
    
    async def handle_support_request(self, user_id: int, message: str, language: str = 'fa', context: Optional[Dict] = None) -> str:
        """Handle user support request with AI"""
        try:
            # Analyze user intent first
            intent_analysis = await self.ai_support.analyze_user_intent(message, language)
            
            # Get AI response
            response = await self.ai_support.get_ai_response(message, language, context)
            
            # Log support interaction
            logger.info(f"AI Support - User: {user_id}, Intent: {intent_analysis.get('intent')}, Language: {language}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling support request: {e}")
            return self.ai_support.translator.get_text('support_contact', language)
    
    async def get_quick_help(self, user_state: str, language: str = 'fa') -> str:
        """Get quick contextual help"""
        return await self.ai_support.get_contextual_help(user_state, language)
    
    async def search_faq(self, question: str, language: str = 'fa') -> Optional[str]:
        """Search FAQ for relevant answers"""
        return await self.ai_support.generate_faq_response(question, language)

# Global AI support manager instance
ai_support_manager = AISupportManager()