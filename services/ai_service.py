"""
AI Service for CodeRoot Bot
Integrates with Liara AI API (Gemini 2.0 Flash) for intelligent support
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    """AI Service for intelligent support and assistance"""
    
    def __init__(self):
        """Initialize AI service with Liara credentials"""
        self.client = OpenAI(
            base_url="https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2ODdhNzhmZjI3NGUxYzRlNjgzZTEwZTkiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc1MzEwMzg3Nn0.EiwQySwDwWXZn9BLEbKaNoClUE-Ndz_6Xl4K1J5W_cE"
        )
        self.model = "google/gemini-2.0-flash-001"
        self.context_knowledge = self._build_context_knowledge()
    
    def _build_context_knowledge(self) -> str:
        """Build comprehensive context about CodeRoot bot features"""
        return """
CodeRoot Bot - Complete Feature Guide:

🤖 ABOUT CODEROOT:
CodeRoot is a Telegram bot that allows users to create their own online shops. It's a "mother bot" that generates individual shop bots for each seller.

👥 USER TYPES:
1. Sellers: Create and manage their own shops
2. Buyers: Purchase from seller shops
3. Admin (HADI): Manages the entire platform

🏪 SHOP CREATION PROCESS:
1. User starts with /start command
2. Selects language (Persian/English/Arabic)
3. Must join mandatory channel
4. Creates shop with plan selection
5. Makes payment (card-to-card)
6. Gets approved by admin
7. Receives their own shop bot

📋 SUBSCRIPTION PLANS:
🆓 FREE PLAN:
- Up to 10 products
- Fixed buttons only
- Basic reports
- 5% commission on sales
- Bale payment gateway

💼 PROFESSIONAL PLAN (20,000 Toman/month):
- Up to 200 products
- Advanced reporting
- Auto-welcome messages
- Custom advertisements
- 5% commission on sales
- Better dashboard

👑 VIP PLAN (60,000 Toman/month):
- Unlimited products
- Dedicated payment gateway
- Full & smart reports
- Advanced auto-messages
- Advanced discount system
- Special advertisements
- Custom buttons
- 0% commission (NO FEES!)

🛠️ SELLER FEATURES:
- Add/Edit/Delete products
- View product lists
- Sales reports & analytics
- Order management
- Plan upgrades/renewals
- Auto-welcome messages (Pro+)
- Custom shop branding

👑 ADMIN FEATURES (HADI):
- Approve/reject new shops
- View all seller data
- Manage subscriptions
- Financial reports & commissions
- Broadcast messages
- Sub-bot management
- Platform settings

🎁 REFERRAL SYSTEM:
- Each user gets unique referral link
- Earn commissions from referrals
- Multi-level referral tracking
- Bonus rewards for active referrers

🌍 LANGUAGE SUPPORT:
- Persian (فارسی) - Default
- English 
- Arabic (العربية)
- Auto-detection and switching

💰 PAYMENT SYSTEM:
- Manual card-to-card verification
- Admin approval required
- Commission tracking
- Automated billing reminders

🔧 TECHNICAL FEATURES:
- MongoDB database
- Redis caching
- Email notifications
- Excel report generation
- Security & validation
- Analytics tracking
- Backup systems

🆘 SUPPORT TOPICS:
1. Shop creation help
2. Plan comparisons
3. Payment issues
4. Product management
5. Order tracking
6. Technical problems
7. Account issues
8. Feature requests

📞 CONTACT INFO:
- Support through bot messages
- Admin contact: @hadi_admin
- Main channel: @coderoot_channel

🎯 REVENUE MODEL:
- Monthly subscriptions
- 5% commission (Free & Pro plans)
- 0% commission (VIP plan)
- Referral bonuses
"""

    async def get_support_response(self, user_message: str, user_language: str = 'fa', context: Optional[Dict] = None) -> str:
        """Get AI-powered support response"""
        try:
            # Build the conversation context
            system_prompt = f"""
You are CodeRoot AI Assistant, an expert support agent for the CodeRoot Telegram bot platform.

CONTEXT KNOWLEDGE:
{self.context_knowledge}

RESPONSE GUIDELINES:
1. Always respond in {self._get_language_name(user_language)} language
2. Be helpful, professional, and friendly
3. Provide step-by-step instructions when needed
4. Reference specific bot features and plans accurately
5. If unsure, direct user to admin contact
6. Keep responses concise but complete
7. Use appropriate emojis for better UX
8. Always provide actionable solutions

USER CONTEXT: {json.dumps(context) if context else 'No additional context'}

Respond to the user's question professionally and helpfully.
"""

            # Prepare messages for AI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]

            # Make API call to Liara AI
            completion = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7,
                    top_p=0.9
                )
            )

            response = completion.choices[0].message.content
            
            # Add footer with contact info
            footer = self._get_footer(user_language)
            return f"{response}\n\n{footer}"

        except Exception as e:
            logger.error(f"AI service error: {e}")
            return self._get_fallback_response(user_language)

    async def get_feature_explanation(self, feature: str, user_language: str = 'fa') -> str:
        """Get detailed explanation of a specific feature"""
        feature_prompt = f"""
Explain the '{feature}' feature of CodeRoot bot in detail.
Include:
1. What it does
2. How to use it
3. Which plans support it
4. Step-by-step instructions
5. Common issues and solutions

Respond in {self._get_language_name(user_language)} language.
"""

        try:
            completion = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are CodeRoot AI Assistant.\n\n{self.context_knowledge}"},
                        {"role": "user", "content": feature_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.5
                )
            )

            return completion.choices[0].message.content

        except Exception as e:
            logger.error(f"Feature explanation error: {e}")
            return self._get_fallback_response(user_language)

    async def analyze_user_issue(self, issue_description: str, user_data: Dict, user_language: str = 'fa') -> str:
        """Analyze user issue and provide targeted solution"""
        analysis_prompt = f"""
ISSUE ANALYSIS REQUEST:
User Issue: {issue_description}
User Data: {json.dumps(user_data)}

Please analyze this issue and provide:
1. Likely cause of the problem
2. Step-by-step solution
3. Prevention tips
4. When to contact admin

Focus on CodeRoot bot specific solutions.
Respond in {self._get_language_name(user_language)} language.
"""

        try:
            completion = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are CodeRoot Technical Support AI.\n\n{self.context_knowledge}"},
                        {"role": "user", "content": analysis_prompt}
                    ],
                    max_tokens=1200,
                    temperature=0.3
                )
            )

            return completion.choices[0].message.content

        except Exception as e:
            logger.error(f"Issue analysis error: {e}")
            return self._get_fallback_response(user_language)

    async def suggest_plan_upgrade(self, current_plan: str, user_needs: str, user_language: str = 'fa') -> str:
        """Suggest appropriate plan upgrade based on user needs"""
        upgrade_prompt = f"""
PLAN RECOMMENDATION REQUEST:
Current Plan: {current_plan}
User Needs: {user_needs}

Based on CodeRoot's plan features, recommend:
1. Best plan for their needs
2. Why this plan is suitable
3. Cost-benefit analysis
4. Migration process
5. Timeline for upgrade

Available plans: Free (10 products, 5% commission), Professional (200 products, 5% commission, 20k Toman), VIP (unlimited, 0% commission, 60k Toman)

Respond in {self._get_language_name(user_language)} language.
"""

        try:
            completion = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are CodeRoot Sales Assistant AI.\n\n{self.context_knowledge}"},
                        {"role": "user", "content": upgrade_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.4
                )
            )

            return completion.choices[0].message.content

        except Exception as e:
            logger.error(f"Plan suggestion error: {e}")
            return self._get_fallback_response(user_language)

    def _get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        language_names = {
            'fa': 'Persian (فارسی)',
            'en': 'English',
            'ar': 'Arabic (العربية)'
        }
        return language_names.get(lang_code, 'Persian (فارسی)')

    def _get_footer(self, language: str) -> str:
        """Get support footer in specified language"""
        footers = {
            'fa': "🆘 نیاز به کمک بیشتر؟ با ادمین تماس بگیرید: @hadi_admin",
            'en': "🆘 Need more help? Contact admin: @hadi_admin",
            'ar': "🆘 تحتاج المزيد من المساعدة؟ اتصل بالمشرف: @hadi_admin"
        }
        return footers.get(language, footers['fa'])

    def _get_fallback_response(self, language: str) -> str:
        """Get fallback response when AI fails"""
        fallbacks = {
            'fa': """
🤖 متاسفانه در حال حاضر سیستم هوش مصنوعی دردسترس نیست.

لطفاً سوال خود را مستقیماً با ادمین مطرح کنید:
👤 @hadi_admin

یا از منوی راهنما استفاده کنید:
📱 /help
""",
            'en': """
🤖 Unfortunately, the AI system is currently unavailable.

Please contact the admin directly:
👤 @hadi_admin

Or use the help menu:
📱 /help
""",
            'ar': """
🤖 عذراً، نظام الذكاء الاصطناعي غير متاح حالياً.

يرجى التواصل مع المشرف مباشرة:
👤 @hadi_admin

أو استخدم قائمة المساعدة:
📱 /help
"""
        }
        return fallbacks.get(language, fallbacks['fa'])

# Initialize AI service instance
ai_service = AIService()