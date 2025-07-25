"""
AI Service for CodeRoot Bot - Enhanced with Comprehensive Training
Provides intelligent support using Liara AI API (Gemini 2.0)
Fully trained and optimized for CodeRoot platform support
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    """Enhanced AI Service with comprehensive CodeRoot knowledge"""
    
    def __init__(self):
        """Initialize AI service with Liara AI API and enhanced training"""
        self.client = OpenAI(
            base_url="https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2ODdhNzhmZjI3NGUxYzRlNjgzZTEwZTkiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc1MzEwMzg3Nn0.EiwQySwDwWXZn9BLEbKaNoClUE-Ndz_6Xl4K1J5W_cE"
        )
        self.model = "google/gemini-2.0-flash-001"
        self.conversation_history: Dict[int, List[Dict]] = {}
        self.user_context_cache: Dict[int, Dict] = {}
        
        # Initialize comprehensive AI context with enhanced CodeRoot knowledge
        self.system_context = self._build_enhanced_system_context()
        self.conversation_starters = self._get_conversation_starters()
        self.quick_response_templates = self._get_quick_response_templates()
    
    def _build_enhanced_system_context(self) -> str:
        """Build comprehensive and enhanced system context for AI support"""
        return """🤖 شما CodeRoot AI Assistant هستید - دستیار هوشمند و حرفه‌ای پلتفرم CodeRoot

═══════════════════════════════════════════════════════════════════════════════════
🏪 CODEROOT PLATFORM - اطلاعات کامل پلتفرم
═══════════════════════════════════════════════════════════════════════════════════

📋 خلاصه کلی CodeRoot:
CodeRoot یک پلتفرم پیشرفته ایجاد فروشگاه آنلاین در تلگرام است که به کاربران امکان ساخت ربات فروشگاهی اختصاصی را می‌دهد. ربات اصلی (@Code_Root_Bot) به عنوان "ربات مادر" عمل کرده و زیرربات‌های فروشگاهی را مدیریت می‌کند.

🎯 مشخصات کلیدی:
- مالک: حادی (آیدی ادمین: 7707164235)
- پشتیبانی از 3 زبان: فارسی (اصلی)، انگلیسی، عربی
- سیستم کارمزد: 5% (به جز پلن VIP)
- درگاه پرداخت: کارت به کارت دستی
- شماره کارت: 6037-9977-7766-5544 (حادی)

═══════════════════════════════════════════════════════════════════════════════════
📊 پلن‌های اشتراک - جزئیات کامل
═══════════════════════════════════════════════════════════════════════════════════

1️⃣ پلن رایگان (FREE):
   ✅ حداکثر 10 محصول
   ✅ درگاه پرداخت بیل
   ✅ گزارش‌گیری ساده
   ✅ دکمه‌های ثابت
   ❌ 5% کارمزد
   ❌ محدودیت در ویژگی‌ها

2️⃣ پلن حرفه‌ای (PROFESSIONAL) - 20,000 تومان/ماه:
   ✅ حداکثر 200 محصول
   ✅ گزارش‌گیری پیشرفته
   ✅ پیام‌های خوش‌آمدگویی خودکار
   ✅ تبلیغات دلخواه در ربات
   ✅ قابلیت‌های تخفیف
   ❌ 5% کارمزد
   ✅ پشتیبانی اولویت‌دار

3️⃣ پلن VIP - 60,000 تومان/ماه:
   ✅ محصولات نامحدود
   ✅ درگاه پرداخت اختصاصی
   ✅ گزارش‌گیری کامل و هوشمند
   ✅ پیام‌های خوش‌آمدگویی پیشرفته
   ✅ تبلیغات ویژه و تخصصی
   ✅ دکمه‌های شخصی‌سازی شده
   ✅ بدون کارمزد (0%)
   ✅ پشتیبانی 24/7

═══════════════════════════════════════════════════════════════════════════════════
🔧 قابلیت‌های سیستم - راهنمای کامل
═══════════════════════════════════════════════════════════════════════════════════

🏪 مدیریت فروشگاه:
- ایجاد فروشگاه با انتخاب پلن
- ثبت اطلاعات کامل فروشگاه
- تایید توسط ادمین (معمولاً 24 ساعت)
- ایجاد خودکار زیرربات اختصاصی

🛍️ مدیریت محصولات:
- افزودن محصول با عکس، توضیحات، قیمت
- ویرایش و حذف محصولات
- دسته‌بندی محصولات
- مدیریت موجودی

📊 گزارش‌گیری:
- گزارش فروش روزانه/ماهانه
- آمار مشتریان
- گزارش مالی
- تحلیل عملکرد

💰 سیستم پرداخت:
- پرداخت اشتراک: کارت به کارت دستی
- فروش محصولات: درگاه متصل یا دستی
- محاسبه خودکار کارمزد

🎁 سیستم معرفی:
- لینک معرفی اختصاصی
- کسب درآمد از معرفی
- پیگیری معرفی‌ها

🔐 امنیت و کنترل:
- جوین اجباری کانال
- تایید هویت
- کنترل دسترسی

═══════════════════════════════════════════════════════════════════════════════════
🆘 مشکلات رایج و راه‌حل‌های کامل
═══════════════════════════════════════════════════════════════════════════════════

❌ ربات جواب نمی‌دهد:
✅ بررسی اتصال اینترنت
✅ راه‌اندازی مجدد ربات (/start)
✅ بررسی عضویت در کانال اصلی
✅ در صورت ادامه مشکل، تماس با پشتیبانی

❌ مشکل پرداخت:
✅ بررسی صحت شماره کارت
✅ ارسال رسید واریز به ادمین
✅ صبر 24 ساعت برای تایید
✅ پیگیری از طریق پشتیبانی

❌ فروشگاه تایید نمی‌شود:
✅ بررسی کامل بودن اطلاعات
✅ صبر 24-48 ساعت
✅ عدم نقض قوانین
✅ تماس با ادمین در صورت تاخیر

❌ مشکل آپلود محصول:
✅ بررسی سایز عکس (حداکثر 10MB)
✅ فرمت‌های مجاز: JPG, PNG
✅ بررسی محدودیت تعداد (بر اساس پلن)
✅ تلاش مجدد

❌ گزارش‌ها نمایش داده نمی‌شود:
✅ حداقل یک فروش انجام شده باشد
✅ بررسی اتصال دیتابیس
✅ رفرش صفحه
✅ تماس با پشتیبانی فنی

═══════════════════════════════════════════════════════════════════════════════════
💬 راهنمای مکالمه و پاسخگویی
═══════════════════════════════════════════════════════════════════════════════════

📝 اصول پاسخگویی:
- همیشه در زبان کاربر پاسخ دهید (فارسی/انگلیسی/عربی)
- حرفه‌ای، مودب و مفید باشید
- از ایموجی برای جذاب‌تر کردن پاسخ استفاده کنید
- راه‌حل‌های عملی و قابل اجرا ارائه دهید
- در صورت عدم اطمینان، کاربر را به ادمین ارجاع دهید

🎯 اهداف مکالمه:
- حل مشکل کاربر
- آموزش استفاده از قابلیت‌ها
- ترغیب به ارتقای پلن (در صورت نیاز)
- ایجاد تجربه مثبت از برند CodeRoot

🚀 ترویج طبیعی ویژگی‌ها:
- در مکالمه، قابلیت‌های CodeRoot را معرفی کنید
- مزایای ارتقای پلن را توضیح دهید
- موفقیت‌های سایر کاربران را مثال بزنید

═══════════════════════════════════════════════════════════════════════════════════
🌍 پشتیبانی چندزبانه
═══════════════════════════════════════════════════════════════════════════════════

فارسی (زبان اصلی):
- استفاده از لهجه رسمی اما دوستانه
- ایموجی‌های مناسب فرهنگ ایرانی
- واژگان فنی ساده و قابل فهم

English (Secondary):
- Professional but friendly tone
- Clear, concise explanations
- Technical terms with simple explanations

العربية (Additional):
- Formal Arabic with respectful tone
- Cultural sensitivity
- Clear step-by-step instructions

یادآوری مهم: شما نماینده برند CodeRoot هستید. همیشه مثبت، حل‌محور و حرفه‌ای عمل کنید."""

    def _get_conversation_starters(self) -> Dict[str, List[str]]:
        """Get conversation starters for different languages"""
        return {
            'fa': [
                "👋 سلام! چطور می‌تونم کمکتون کنم؟",
                "🎉 به CodeRoot خوش آمدید! چه سوالی دارید؟",
                "🤖 من دستیار هوشمند CodeRoot هستم. چیکار کنم برات؟",
                "💡 آماده راهنماییتون در مورد فروشگاه آنلاین هستم!",
                "🚀 بیایید باهم فروشگاه رویاهاتون رو بسازیم!"
            ],
            'en': [
                "👋 Hello! How can I help you today?",
                "🎉 Welcome to CodeRoot! What questions do you have?",
                "🤖 I'm CodeRoot's AI assistant. How can I assist you?",
                "💡 Ready to guide you through your online store journey!",
                "🚀 Let's build your dream store together!"
            ],
            'ar': [
                "👋 مرحباً! كيف يمكنني مساعدتك؟",
                "🎉 أهلاً بك في CodeRoot! ما هي أسئلتك؟",
                "🤖 أنا مساعد CodeRoot الذكي. كيف يمكنني مساعدتك؟",
                "💡 مستعد لإرشادك في رحلة متجرك الإلكتروني!",
                "🚀 دعنا نبني متجر أحلامك معاً!"
            ]
        }

    def _get_quick_response_templates(self) -> Dict[str, Dict[str, str]]:
        """Get quick response templates for common queries"""
        return {
            'shop_creation': {
                'fa': """🏪 برای ایجاد فروشگاه این مراحل رو دنبال کنید:

1️⃣ دکمه "ایجاد فروشگاه" رو بزنید
2️⃣ پلن مناسب رو انتخاب کنید:
   • رایگان: 10 محصول
   • حرفه‌ای: 200 محصول (20,000 تومان)
   • VIP: نامحدود (60,000 تومان)
3️⃣ پرداخت رو انجام بدید
4️⃣ اطلاعات فروشگاه رو وارد کنید
5️⃣ تایید ادمین رو منتظر بمونید (24 ساعت)

💡 توصیه: پلن حرفه‌ای برای شروع بهترین انتخابه!""",
                
                'en': """🏪 To create your shop, follow these steps:

1️⃣ Click "Create Shop" button
2️⃣ Choose your plan:
   • Free: 10 products
   • Professional: 200 products ($20,000 Toman)
   • VIP: Unlimited ($60,000 Toman)
3️⃣ Make payment
4️⃣ Enter shop information
5️⃣ Wait for admin approval (24 hours)

💡 Tip: Professional plan is best for starting!""",
                
                'ar': """🏪 لإنشاء متجرك، اتبع هذه الخطوات:

1️⃣ اضغط على زر "إنشاء متجر"
2️⃣ اختر خطتك:
   • مجاني: 10 منتجات
   • احترافي: 200 منتج (20,000 تومان)
   • VIP: غير محدود (60,000 تومان)
3️⃣ قم بالدفع
4️⃣ أدخل معلومات المتجر
5️⃣ انتظر موافقة المدير (24 ساعة)

💡 نصيحة: الخطة الاحترافية هي الأفضل للبداية!"""
            },
            
            'payment_help': {
                'fa': """💳 راهنمای پرداخت:

🏦 شماره کارت: 6037-9977-7766-5544
👤 نام صاحب حساب: حادی

📋 مراحل پرداخت:
1️⃣ مبلغ رو به شماره کارت واریز کنید
2️⃣ عکس رسید رو ارسال کنید
3️⃣ حداکثر 24 ساعت صبر کنید
4️⃣ پس از تایید، پلنتون فعال میشه

⚠️ نکته مهم: حتماً رسید رو ارسال کنید تا پرداختتون تایید بشه!""",
                
                'en': """💳 Payment Guide:

🏦 Card Number: 6037-9977-7766-5544
👤 Account Holder: Hadi

📋 Payment Steps:
1️⃣ Transfer amount to card number
2️⃣ Send receipt photo
3️⃣ Wait up to 24 hours
4️⃣ After confirmation, your plan activates

⚠️ Important: Make sure to send receipt for confirmation!""",
                
                'ar': """💳 دليل الدفع:

🏦 رقم البطاقة: 6037-9977-7766-5544
👤 صاحب الحساب: حادي

📋 خطوات الدفع:
1️⃣ احول المبلغ إلى رقم البطاقة
2️⃣ أرسل صورة الإيصال
3️⃣ انتظر حتى 24 ساعة
4️⃣ بعد التأكيد، ستتم تفعيل خطتك

⚠️ هام: تأكد من إرسال الإيصال للتأكيد!"""
            }
        }

    async def get_ai_response(
        self, 
        user_id: int, 
        message: str, 
        user_language: str = 'fa',
        context: Optional[Dict] = None
    ) -> str:
        """Get enhanced AI response for user query"""
        try:
            # Build comprehensive conversation context
            conversation = self._get_conversation_history(user_id)
            
            # Enhanced system context with user context
            enhanced_context = self.system_context
            if context:
                enhanced_context += f"\n\nمعلومات کاربر فعلی:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            
            # Build messages array
            messages = [
                {"role": "system", "content": enhanced_context},
            ]
            
            # Add relevant conversation history (last 6 messages for context)
            messages.extend(conversation[-6:])
            
            # Add current user message with language specification
            user_content = f"زبان کاربر: {user_language}\nپیام کاربر: {message}"
            if context:
                user_content += f"\nمتن اضافی: {json.dumps(context, ensure_ascii=False)}"
            
            messages.append({
                "role": "user", 
                "content": user_content
            })
            
            # Get AI response with enhanced parameters
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=1200,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            response = completion.choices[0].message.content
            
            # Update conversation history
            self._update_conversation_history(user_id, message, response)
            
            # Cache user context
            if context:
                self.user_context_cache[user_id] = context
            
            return response
            
        except Exception as e:
            logger.error(f"Enhanced AI Service error: {e}")
            return self._get_fallback_response(user_language)

    async def get_support_response(
        self,
        message: str,
        user_language: str = 'fa',
        user_context: Optional[Dict] = None
    ) -> str:
        """Get specialized support response"""
        try:
            support_context = """شما در حال ارائه پشتیبانی تخصصی CodeRoot هستید. تمرکز کنید روی:
            - حل مشکلات فنی
            - راهنمایی گام به گام
            - ارائه راه‌حل‌های عملی
            - انتقال به پشتیبانی انسانی در صورت نیاز"""
            
            enhanced_context = self.system_context + "\n\n" + support_context
            if user_context:
                enhanced_context += f"\n\nاطلاعات کاربر: {json.dumps(user_context, ensure_ascii=False)}"
            
            messages = [
                {"role": "system", "content": enhanced_context},
                {"role": "user", "content": f"زبان: {user_language}\nدرخواست پشتیبانی: {message}"}
            ]
            
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.6,
                top_p=0.8
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Support response error: {e}")
            return self._get_fallback_response(user_language)

    async def get_shop_support(
        self, 
        user_id: int, 
        shop_data: Dict, 
        issue: str, 
        user_language: str = 'fa'
    ) -> str:
        """Get AI support specifically for shop-related issues"""
        try:
            shop_context = {
                "shop_name": shop_data.get('name', 'نامشخص'),
                "plan": shop_data.get('plan', 'رایگان'),
                "products_count": shop_data.get('products_count', 0),
                "status": shop_data.get('status', 'نامشخص'),
                "created_date": shop_data.get('created_at', 'نامشخص'),
                "last_sale": shop_data.get('last_sale', 'ندارد'),
                "total_sales": shop_data.get('total_sales', 0)
            }
            
            context_message = f"مشکل فروشگاه: {issue}\nاطلاعات فروشگاه: {json.dumps(shop_context, ensure_ascii=False)}"
            
            return await self.get_ai_response(
                user_id, 
                context_message,
                user_language, 
                shop_context
            )
            
        except Exception as e:
            logger.error(f"Shop support error: {e}")
            return self._get_fallback_response(user_language)

    async def get_admin_assistance(
        self, 
        admin_id: int, 
        query: str, 
        admin_data: Optional[Dict] = None
    ) -> str:
        """Get AI assistance for admin queries with enhanced capabilities"""
        try:
            admin_context = """شما به ادمین CodeRoot (حادی) کمک می‌کنید. اطلاعات تخصصی ارائه دهید در مورد:
            - مدیریت کاربران و فروشگاه‌ها
            - تحلیل گزارش‌های مالی و فروش
            - نظارت بر سیستم و رفع اشکال
            - بینش‌های تجاری و پیشنهادات بهینه‌سازی
            - استراتژی‌های افزایش درآمد
            - مدیریت ربات‌های زیرمجموعه
            - امنیت و کنترل کیفیت"""
            
            enhanced_admin_context = self.system_context + "\n\n" + admin_context
            
            messages = [
                {"role": "system", "content": enhanced_admin_context},
                {"role": "user", "content": f"سوال ادمین: {query}"}
            ]
            
            if admin_data:
                messages[-1]["content"] += f"\n\nداده‌های ادمین: {json.dumps(admin_data, ensure_ascii=False)}"
            
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=1500,
                temperature=0.6,
                top_p=0.8
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Admin assistance error: {e}")
            return "خطایی در سیستم هوش مصنوعی رخ داد. لطفاً دوباره تلاش کنید."

    async def analyze_user_behavior(
        self, 
        user_data: Dict, 
        activity_log: List[Dict]
    ) -> Dict[str, Any]:
        """Enhanced user behavior analysis with comprehensive insights"""
        try:
            analysis_prompt = f"""تحلیل جامع رفتار کاربر CodeRoot:

اطلاعات کاربر: {json.dumps(user_data, ensure_ascii=False, indent=2)}
فعالیت‌های اخیر: {json.dumps(activity_log[-20:], ensure_ascii=False, indent=2)}

لطفاً تحلیل کاملی ارائه دهید شامل:
- سطح مشارکت (بالا/متوسط/پایین)
- اقدامات پیشنهادی برای بهبود تجربه
- مشکلات احتمالی
- پیشنهادات ارتقای پلن
- عوامل ریسک
- نقاط قوت و ضعف
- پیشنهادات شخصی‌سازی

پاسخ را در فرمت JSON ارائه دهید."""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل داده برای پلتفرم CodeRoot هستید."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=1000,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            analysis_result = json.loads(completion.choices[0].message.content)
            return analysis_result
            
        except Exception as e:
            logger.error(f"Enhanced user behavior analysis error: {e}")
            return {
                "engagement_level": "نامشخص",
                "recommended_actions": ["بررسی دستی توسط ادمین"],
                "potential_issues": ["خطا در تحلیل خودکار"],
                "upgrade_suggestions": [],
                "risk_factors": [],
                "strengths": [],
                "weaknesses": [],
                "personalization_tips": []
            }

    async def generate_content_suggestions(
        self, 
        shop_data: Dict, 
        target_audience: str = "عمومی"
    ) -> List[str]:
        """Generate enhanced marketing content suggestions"""
        try:
            prompt = f"""ایجاد پیشنهادات بازاریابی خلاقانه برای فروشگاه CodeRoot:

اطلاعات فروشگاه: {json.dumps(shop_data, ensure_ascii=False, indent=2)}
مخاطب هدف: {target_audience}

لطفاً 8 پیشنهاد خلاقانه و عملی ارائه دهید که شامل:
- استراتژی‌های محتوایی
- ایده‌های تبلیغاتی
- روش‌های جذب مشتری
- تکنیک‌های فروش
- ایده‌های تعامل با مشتری

هر پیشنهاد باید قابل اجرا، مؤثر و مناسب برای تلگرام باشد."""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "شما یک متخصص بازاریابی دیجیتال برای فروشگاه‌های آنلاین هستید."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.8,
                top_p=0.9
            )
            
            response = completion.choices[0].message.content
            # Extract suggestions
            suggestions = []
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('✅') or len(line) > 20):
                    # Clean up the line
                    clean_line = line.lstrip('-•✅ ').strip()
                    if len(clean_line) > 15:
                        suggestions.append(clean_line)
            
            return suggestions[:8] if suggestions else self._get_default_content_suggestions()
            
        except Exception as e:
            logger.error(f"Enhanced content suggestions error: {e}")
            return self._get_default_content_suggestions()

    def _get_default_content_suggestions(self) -> List[str]:
        """Get default content suggestions as fallback"""
        return [
            "🎯 محتوای داستانی درباره محصولات خود بسازید و تجربیات مشتریان را به اشتراک بگذارید",
            "📸 عکس‌های با کیفیت و جذاب از محصولات با زوایای مختلف تهیه کنید",
            "🎁 تخفیف‌های محدود زمانی برای ایجاد احساس فوریت در مشتریان",
            "📺 ویدیوهای کوتاه آموزشی نحوه استفاده از محصولات",
            "⭐ نمایش نظرات و بازخوردهای مثبت مشتریان به عنوان اعتماد‌ساز",
            "🔄 مسابقات و قرعه‌کشی برای افزایش تعامل و جذب دنبال‌کننده",
            "💡 محتوای آموزشی مرتبط با حوزه کاری‌تان برای ایجاد اعتبار",
            "🤝 همکاری با اینفلوئنسرها و صفحات مرتبط برای معرفی بیشتر"
        ]

    async def analyze_user_intent(self, message: str, language: str = 'fa') -> Dict[str, Any]:
        """Analyze user intent with enhanced accuracy"""
        try:
            intent_prompt = f"""تحلیل قصد کاربر از پیام زیر:

پیام: "{message}"
زبان: {language}

لطفاً قصد کاربر را در فرمت JSON مشخص کنید شامل:
- intent: نوع قصد (shop_creation, payment_help, technical_support, product_management, plan_upgrade, general_inquiry)
- confidence: درجه اطمینان (0.0 تا 1.0)
- keywords: کلمات کلیدی شناسایی شده
- suggested_response_type: نوع پاسخ پیشنهادی
- urgency: درجه فوریت (low, medium, high)"""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "شما متخصص تحلیل متن و شناسایی قصد کاربر هستید."},
                    {"role": "user", "content": intent_prompt}
                ],
                max_tokens=300,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(completion.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Intent analysis error: {e}")
            return {
                "intent": "general_inquiry",
                "confidence": 0.5,
                "keywords": [],
                "suggested_response_type": "general",
                "urgency": "medium"
            }

    async def generate_quick_replies(self, message: str, language: str = 'fa') -> List[str]:
        """Generate contextual quick reply suggestions"""
        try:
            quick_replies_prompt = f"""برای پیام "{message}" در زبان {language}، 4 پیشنهاد پاسخ سریع مناسب ایجاد کنید.

پاسخ‌ها باید:
- کوتاه و مفید باشند (حداکثر 25 کاراکتر)
- مرتبط با پیام کاربر باشند
- کاربردی و عملی باشند
- مناسب برای دکمه‌های سریع تلگرام باشند

فقط متن پاسخ‌ها را در خطوط جداگانه بنویسید."""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "شما متخصص طراحی تعامل کاربری برای ربات‌های تلگرام هستید."},
                    {"role": "user", "content": quick_replies_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            response = completion.choices[0].message.content
            quick_replies = [r.strip() for r in response.split('\n') if r.strip() and len(r.strip()) <= 25]
            
            return quick_replies[:4] if quick_replies else self._get_default_quick_replies(language)
            
        except Exception as e:
            logger.error(f"Quick replies generation error: {e}")
            return self._get_default_quick_replies(language)

    def _get_default_quick_replies(self, language: str) -> List[str]:
        """Get default quick replies based on language"""
        defaults = {
            'fa': ["راهنما", "پشتیبانی", "فروشگاه من", "پلن‌ها"],
            'en': ["Help", "Support", "My Shop", "Plans"],
            'ar': ["مساعدة", "الدعم", "متجري", "الخطط"]
        }
        return defaults.get(language, defaults['fa'])

    async def train_on_conversation(self, user_id: int, conversation_history: List[Dict]):
        """Train AI on conversation patterns (for future improvement)"""
        try:
            # This is a placeholder for future conversation analysis and training
            # In production, this could store patterns for improving responses
            logger.info(f"Training data collected for user {user_id}: {len(conversation_history)} messages")
        except Exception as e:
            logger.error(f"Training error: {e}")

    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None

    def _get_conversation_history(self, user_id: int) -> List[Dict]:
        """Get conversation history for user"""
        return self.conversation_history.get(user_id, [])
    
    def _update_conversation_history(
        self, 
        user_id: int, 
        user_message: str, 
        ai_response: str
    ):
        """Update conversation history with context awareness"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": ai_response}
        ])
        
        # Keep only last 30 messages for better context
        if len(self.conversation_history[user_id]) > 30:
            self.conversation_history[user_id] = self.conversation_history[user_id][-30:]
    
    def _get_fallback_response(self, language: str) -> str:
        """Get enhanced fallback response when AI fails"""
        fallback_responses = {
            'fa': """🤖 متأسفانه در حال حاضر امکان پاسخگویی هوشمند وجود ندارد.
            
🆘 گزینه‌های پشتیبانی:
• تماس با ادمین: @hadi_admin
• ارسال پیام مستقیم
• بررسی راهنمای کاربری
• تلاش مجدد بعد از چند دقیقه

✨ ما همیشه در خدمت شما هستیم!""",
            
            'en': """🤖 Sorry, intelligent response is currently unavailable.
            
🆘 Support options:
• Contact admin: @hadi_admin
• Send direct message
• Check user guide
• Try again in a few minutes

✨ We're always here to help!""",
            
            'ar': """🤖 عذراً، الاستجابة الذكية غير متاحة حالياً.
            
🆘 خيارات الدعم:
• اتصل بالمدير: @hadi_admin
• أرسل رسالة مباشرة
• راجع دليل المستخدم
• حاول مرة أخرى بعد دقائق

✨ نحن هنا دائماً لمساعدتك!"""
        }
        return fallback_responses.get(language, fallback_responses['fa'])
    
    def clear_conversation_history(self, user_id: int):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        if user_id in self.user_context_cache:
            del self.user_context_cache[user_id]
    
    async def test_ai_connection(self) -> bool:
        """Test AI service connection with enhanced verification"""
        try:
            test_completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": "Test connection - respond with 'OK'"}],
                max_tokens=10,
                temperature=0.1
            )
            
            response = test_completion.choices[0].message.content.strip().upper()
            return "OK" in response
            
        except Exception as e:
            logger.error(f"Enhanced AI connection test failed: {e}")
            return False

    async def get_feature_explanation(self, feature: str, language: str = 'fa') -> str:
        """Get detailed explanation of CodeRoot features"""
        try:
            explanation_prompt = f"""کاربر درباره قابلیت "{feature}" در CodeRoot سوال دارد.
            
لطفاً توضیح کاملی ارائه دهید شامل:
- عملکرد این قابلیت
- نحوه استفاده
- مزایا و کاربردها
- مثال‌های عملی
- نکات مهم

زبان پاسخ: {language}"""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_context},
                    {"role": "user", "content": explanation_prompt}
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Feature explanation error: {e}")
            return self._get_fallback_response(language)

    async def suggest_plan_upgrade(self, current_plan: str, user_needs: Dict, language: str = 'fa') -> str:
        """Suggest plan upgrade based on user needs"""
        try:
            upgrade_prompt = f"""کاربر پلن "{current_plan}" دارد و نیازهای زیر را دارد:
            {json.dumps(user_needs, ensure_ascii=False)}
            
آیا ارتقای پلن پیشنهاد می‌دهید؟ چرا؟
- مزایای ارتقا
- هزینه-فایده
- پیشنهاد پلن مناسب
- توجیه اقتصادی

زبان پاسخ: {language}"""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_context + "\n\nشما مشاور فروش متخصص CodeRoot هستید."},
                    {"role": "user", "content": upgrade_prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Plan upgrade suggestion error: {e}")
            return self._get_fallback_response(language)

    async def analyze_user_issue(self, issue_description: str, user_context: Dict, language: str = 'fa') -> Dict[str, Any]:
        """Analyze user issue and provide structured solution"""
        try:
            analysis_prompt = f"""کاربر مشکل زیر را دارد:
            "{issue_description}"
            
اطلاعات کاربر: {json.dumps(user_context, ensure_ascii=False)}

لطفاً تحلیل کاملی در فرمت JSON ارائه دهید شامل:
- problem_category: دسته‌بندی مشکل
- severity: شدت مشکل (low, medium, high, critical)
- possible_causes: علل احتمالی
- step_by_step_solution: راه‌حل گام به گام
- prevention_tips: نکات پیشگیری
- escalation_needed: نیاز به ارجاع به ادمین (true/false)"""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "شما متخصص رفع عیب فنی CodeRoot هستید."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=800,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            return json.loads(completion.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Issue analysis error: {e}")
            return {
                "problem_category": "general",
                "severity": "medium",
                "possible_causes": ["مشخص نیست"],
                "step_by_step_solution": ["تماس با پشتیبانی"],
                "prevention_tips": ["مراجعه به راهنما"],
                "escalation_needed": True
            }

# Enhanced global AI service instance
ai_service = AIService()