"""
AI Service for CodeRoot Bot
Provides intelligent support using Liara AI API (Gemini 2.0)
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
    """AI Service for intelligent support and assistance"""
    
    def __init__(self):
        """Initialize AI service with Liara AI API"""
        self.client = OpenAI(
            base_url="https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2ODdhNzhmZjI3NGUxYzRlNjgzZTEwZTkiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc1MzEwMzg3Nn0.EiwQySwDwWXZn9BLEbKaNoClUE-Ndz_6Xl4K1J5W_cE"
        )
        self.model = "google/gemini-2.0-flash-001"
        self.conversation_history: Dict[int, List[Dict]] = {}
        
        # Initialize AI context with CodeRoot knowledge
        self.system_context = self._build_system_context()
    
    def _build_system_context(self) -> str:
        """Build comprehensive system context for AI support"""
        return """You are CodeRoot AI Assistant, a professional support agent for the CodeRoot Telegram bot platform.

CODEROOT PLATFORM OVERVIEW:
CodeRoot is a Telegram bot creation platform that allows users to create their own online shop bots. The main bot (@Code_Root_Bot) serves as a "mother bot" that manages multiple shop sub-bots.

CORE FEATURES YOU SUPPORT:
1. 🏪 SHOP CREATION SYSTEM
   - Users can create their own Telegram shop bots
   - Each shop gets a unique sub-bot connected to the mother bot
   - Shop owners can manage products, orders, and customers

2. 📊 SUBSCRIPTION PLANS
   - FREE PLAN: Up to 10 products, basic features, 5% commission
   - PROFESSIONAL PLAN: Up to 200 products, advanced reports, welcome messages, 5% commission (20,000 Toman/month)
   - VIP PLAN: Unlimited products, dedicated payment gateway, 0% commission, special features (60,000 Toman/month)

3. 🛒 PRODUCT MANAGEMENT
   - Add/edit/delete products with images, descriptions, prices
   - Inventory tracking and stock management
   - Product categories and organization

4. 💰 PAYMENT SYSTEM
   - Manual card-to-card payments for subscriptions
   - Automatic commission calculation
   - Financial reports and analytics

5. 📈 ADMIN PANEL
   - Shop approval and management
   - Subscription monitoring and renewal alerts
   - Financial reports and commission tracking
   - Broadcast messaging to all users

6. 🌍 MULTI-LANGUAGE SUPPORT
   - Persian (فارسی) - Primary language
   - English - Secondary language  
   - Arabic (العربية) - Additional language

7. 🎯 REFERRAL SYSTEM
   - Users get unique referral links
   - Earn commissions from referred users
   - Multi-level referral tracking

COMMON USER QUESTIONS & ANSWERS:

Q: How do I create a shop?
A: Use /start command, select "Create Shop", choose your plan, make payment, and register your shop details.

Q: What's the difference between plans?
A: Free (10 products, 5% fee), Professional (200 products, advanced features, 5% fee), VIP (unlimited, no fees, premium features).

Q: How do I add products?
A: Go to "My Shop" → "Add Product" → Fill in name, description, price, and upload image.

Q: How does payment work?
A: For subscriptions: Manual card-to-card transfer. For shop sales: Integrated payment gateway (VIP) or manual processing.

Q: Can I upgrade my plan?
A: Yes! Go to "My Shop" → "Plan Renewal" → Select new plan and make payment.

Q: How do I get support?
A: Use the "Support" button in main menu or contact admin directly.

RESPONSE GUIDELINES:
- Always respond in the user's preferred language (Persian, English, or Arabic)
- Be helpful, professional, and encouraging
- Provide step-by-step instructions when needed
- If unsure about technical details, suggest contacting admin
- Promote CodeRoot features naturally in conversations
- Use emojis appropriately to make responses friendly

TECHNICAL ISSUES TO HELP WITH:
- Bot not responding: Check internet connection, restart bot
- Payment problems: Verify card details, contact admin for confirmation
- Product upload issues: Check image size/format, try again
- Shop not appearing: Wait for admin approval (usually 24 hours)

Remember: You represent CodeRoot brand. Be professional, helpful, and always try to solve user problems efficiently."""

    async def get_ai_response(
        self, 
        user_id: int, 
        message: str, 
        user_language: str = 'fa',
        context: Optional[Dict] = None
    ) -> str:
        """Get AI response for user query"""
        try:
            # Build conversation context
            conversation = self._get_conversation_history(user_id)
            
            # Add system context and user message
            messages = [
                {"role": "system", "content": self.system_context},
            ]
            
            # Add conversation history (last 10 messages)
            messages.extend(conversation[-10:])
            
            # Add current user message with context
            user_content = message
            if context:
                user_content += f"\n\nContext: {json.dumps(context, ensure_ascii=False)}"
            
            messages.append({
                "role": "user", 
                "content": f"Language: {user_language}\nUser Message: {user_content}"
            })
            
            # Get AI response
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9
            )
            
            response = completion.choices[0].message.content
            
            # Update conversation history
            self._update_conversation_history(user_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"AI Service error: {e}")
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
            context = {
                "shop_name": shop_data.get('name'),
                "plan": shop_data.get('plan'),
                "products_count": shop_data.get('products_count', 0),
                "status": shop_data.get('status'),
                "created_date": shop_data.get('created_at')
            }
            
            return await self.get_ai_response(
                user_id, 
                f"Shop Support Issue: {issue}", 
                user_language, 
                context
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
        """Get AI assistance for admin queries"""
        try:
            admin_context = """You are now assisting a CodeRoot administrator. Provide detailed, technical responses about:
            - User management and shop approvals
            - Financial reports and commission tracking  
            - System monitoring and troubleshooting
            - Business insights and recommendations
            - Platform optimization suggestions"""
            
            messages = [
                {"role": "system", "content": self.system_context + "\n\n" + admin_context},
                {"role": "user", "content": f"Admin Query: {query}"}
            ]
            
            if admin_data:
                messages[-1]["content"] += f"\n\nAdmin Context: {json.dumps(admin_data, ensure_ascii=False)}"
            
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=1500,
                temperature=0.6
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
        """Analyze user behavior and provide insights"""
        try:
            analysis_prompt = f"""Analyze this user's behavior and provide insights:

User Data: {json.dumps(user_data, ensure_ascii=False)}
Recent Activity: {json.dumps(activity_log[-20:], ensure_ascii=False)}

Provide analysis in JSON format with:
- engagement_level (high/medium/low)
- recommended_actions (list)
- potential_issues (list)
- upgrade_suggestions (list)
- risk_factors (list)"""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst for CodeRoot platform."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=800,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            return json.loads(completion.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"User behavior analysis error: {e}")
            return {
                "engagement_level": "unknown",
                "recommended_actions": [],
                "potential_issues": [],
                "upgrade_suggestions": [],
                "risk_factors": []
            }
    
    async def generate_content_suggestions(
        self, 
        shop_data: Dict, 
        target_audience: str = "general"
    ) -> List[str]:
        """Generate content suggestions for shop marketing"""
        try:
            prompt = f"""Generate marketing content suggestions for this CodeRoot shop:

Shop Details: {json.dumps(shop_data, ensure_ascii=False)}
Target Audience: {target_audience}

Provide 5 creative marketing suggestions in Persian that this shop owner can use to promote their products."""

            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a marketing expert for e-commerce shops."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            response = completion.choices[0].message.content
            # Split response into suggestions
            suggestions = [s.strip() for s in response.split('\n') if s.strip() and len(s.strip()) > 10]
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            logger.error(f"Content suggestions error: {e}")
            return [
                "محتوای جذاب و خلاقانه برای محصولات خود بسازید",
                "از استوری‌ها و پست‌های تعاملی استفاده کنید",
                "تخفیف‌های ویژه برای مشتریان وفادار ارائه دهید",
                "محتوای آموزشی درباره محصولات تولید کنید",
                "از بازخوردهای مشتریان به عنوان محتوا استفاده کنید"
            ]
    
    def _get_conversation_history(self, user_id: int) -> List[Dict]:
        """Get conversation history for user"""
        return self.conversation_history.get(user_id, [])
    
    def _update_conversation_history(
        self, 
        user_id: int, 
        user_message: str, 
        ai_response: str
    ):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": ai_response}
        ])
        
        # Keep only last 20 messages
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
    
    def _get_fallback_response(self, language: str) -> str:
        """Get fallback response when AI fails"""
        fallback_responses = {
            'fa': "متأسفانه در حال حاضر امکان پاسخگویی هوشمند وجود ندارد. لطفاً با پشتیبانی تماس بگیرید.",
            'en': "Sorry, intelligent response is currently unavailable. Please contact support.",
            'ar': "عذراً، الاستجابة الذكية غير متاحة حالياً. يرجى الاتصال بالدعم."
        }
        return fallback_responses.get(language, fallback_responses['fa'])
    
    def clear_conversation_history(self, user_id: int):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
    
    async def test_ai_connection(self) -> bool:
        """Test AI service connection"""
        try:
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"AI connection test failed: {e}")
            return False

# Global AI service instance
ai_service = AIService()