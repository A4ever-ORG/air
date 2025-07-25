"""
AI Service for CodeRoot Bot - Intelligent Support System
Integrates with Liara AI (Gemini) for contextual support
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from openai import AsyncOpenAI
from datetime import datetime
import json

from config import Config
from utils.language import Translator

logger = logging.getLogger(__name__)

class AIService:
    """AI Service for intelligent customer support using Gemini model"""
    
    def __init__(self):
        """Initialize AI Service with Liara AI endpoint"""
        self.client = None
        self.translator = Translator()
        self.context_knowledge = self._build_coderoot_context()
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client with Liara AI endpoint"""
        try:
            if not Config.AI_API_KEY or not Config.AI_API_BASE_URL:
                logger.warning("AI service disabled - missing API credentials")
                return
                
            self.client = AsyncOpenAI(
                base_url=Config.AI_API_BASE_URL,
                api_key=Config.AI_API_KEY,
            )
            logger.info("AI Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            self.client = None
    
    def _build_coderoot_context(self) -> str:
        """Build comprehensive knowledge base about CodeRoot for AI training"""
        context = """
# CodeRoot Bot - Complete Knowledge Base

## What is CodeRoot?
CodeRoot is a Telegram mother bot that allows users to create their own individual shop bots. Users can register, choose subscription plans, and manage their online stores through Telegram.

## Core Features:
1. **Shop Creation System**
   - Users register and create their own shop bots
   - Choose from 3 subscription plans: Free, Professional, VIP
   - Manual card-to-card payment system
   - Shop information registration

2. **Subscription Plans:**
   - **Free Plan**: Up to 10 products, fixed buttons, 5% commission, Bale payment gateway
   - **Professional Plan**: Up to 200 products, advanced reports, welcome messages, custom ads, 5% commission (20,000 Toman/month)
   - **VIP Plan**: Unlimited products, dedicated payment gateway, no commission, special ads, custom buttons (60,000 Toman/month)

3. **User Features:**
   - Multi-language support (Persian, English, Arabic)
   - Product management (add, edit, delete)
   - Sales reports and analytics
   - Order management
   - Referral system with dedicated invitation links
   - Plan renewal and upgrades

4. **Admin Features:**
   - Shop approval and management
   - Subscription management
   - Financial reports and commission tracking
   - Broadcast messaging
   - User and shop analytics

5. **Technical Requirements:**
   - Mandatory channel membership before accessing shop panel
   - Automatic sub-bot creation for each shop
   - Plan renewal reminders
   - Email notifications
   - Secure payment processing

## Payment Information:
- Card Number: 6037-9977-7766-5544
- Card Holder: حادی
- Manual verification required for all payments

## Commission Structure:
- Free & Professional Plans: 5% commission on all sales
- VIP Plan: 0% commission

## Contact & Support:
- Main Channel: @coderoot_channel
- Admin Contact: @hadi_admin
- Support available in Persian, English, and Arabic

## Common Issues & Solutions:
1. **Bot not responding**: Check channel membership first
2. **Payment issues**: Contact admin with payment screenshot
3. **Shop creation problems**: Ensure all required information is provided
4. **Plan upgrades**: Contact admin for manual processing

## Revenue Model:
- Monthly subscription fees from sellers
- 5% commission on sales (Free/Pro plans)
- Plan upgrade fees

Always respond in the user's preferred language (Persian, English, or Arabic) and provide helpful, accurate information about CodeRoot features and services.
"""
        return context
    
    async def get_support_response(self, user_message: str, user_language: str = 'fa', user_context: Dict = None) -> str:
        """
        Get AI-powered support response for user queries
        
        Args:
            user_message: User's question or issue
            user_language: User's preferred language (fa/en/ar)
            user_context: Additional context about the user (plan, shop status, etc.)
        
        Returns:
            AI-generated support response in user's language
        """
        if not self.client:
            return self._get_fallback_response(user_message, user_language)
        
        try:
            # Build context-aware prompt
            system_prompt = self._build_system_prompt(user_language, user_context)
            
            # Create conversation messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Get AI response
            response = await self.client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=messages,
                max_tokens=Config.AI_MAX_TOKENS,
                temperature=Config.AI_TEMPERATURE,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Log the interaction
            logger.info(f"AI Support - User: {user_message[:50]}... | Response: {ai_response[:50]}...")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI service error: {e}")
            return self._get_fallback_response(user_message, user_language)
    
    def _build_system_prompt(self, user_language: str, user_context: Dict = None) -> str:
        """Build system prompt with CodeRoot context and user information"""
        
        language_names = {
            'fa': 'فارسی (Persian)',
            'en': 'English',
            'ar': 'العربية (Arabic)'
        }
        
        user_info = ""
        if user_context:
            user_info = f"""
User Context:
- Plan: {user_context.get('plan', 'Unknown')}
- Shop Status: {user_context.get('shop_status', 'Unknown')}
- Registration Date: {user_context.get('created_at', 'Unknown')}
- Last Activity: {user_context.get('last_activity', 'Unknown')}
"""
        
        system_prompt = f"""
You are an intelligent customer support assistant for CodeRoot Bot, a Telegram platform for creating shop bots.

{self.context_knowledge}

{user_info}

IMPORTANT INSTRUCTIONS:
1. Always respond in {language_names.get(user_language, 'Persian')} language
2. Be helpful, professional, and friendly
3. Provide specific solutions and actionable advice
4. If you don't know something, direct the user to contact admin @hadi_admin
5. Include relevant emojis to make responses engaging
6. Keep responses concise but comprehensive
7. Always prioritize user satisfaction and problem resolution

Current conversation language: {user_language}
"""
        return system_prompt
    
    def _get_fallback_response(self, user_message: str, user_language: str) -> str:
        """Provide fallback response when AI service is unavailable"""
        fallback_responses = {
            'fa': """
🤖 سیستم پشتیبانی هوشمند موقتاً در دسترس نیست.

📞 لطفاً با پشتیبانی تماس بگیرید:
👤 @hadi_admin

یا از طریق کانال اصلی:
📢 @coderoot_channel

⏰ پاسخگویی: ۹ صبح تا ۱۲ شب
""",
            'en': """
🤖 Smart support system is temporarily unavailable.

📞 Please contact support:
👤 @hadi_admin

Or through main channel:
📢 @coderoot_channel

⏰ Response time: 9 AM to 12 AM
""",
            'ar': """
🤖 نظام الدعم الذكي غير متاح مؤقتاً.

📞 يرجى الاتصال بالدعم:
👤 @hadi_admin

أو عبر القناة الرئيسية:
📢 @coderoot_channel

⏰ وقت الاستجابة: ٩ صباحاً إلى ١٢ منتصف الليل
"""
        }
        return fallback_responses.get(user_language, fallback_responses['fa'])
    
    async def analyze_user_intent(self, message: str, user_language: str) -> Dict[str, Any]:
        """
        Analyze user message to determine intent and extract key information
        
        Returns:
            Dictionary with intent, confidence, and extracted entities
        """
        if not self.client:
            return {"intent": "general_inquiry", "confidence": 0.5, "entities": {}}
        
        try:
            analysis_prompt = f"""
Analyze this user message and determine their intent. Respond with JSON only.

Message: "{message}"
Language: {user_language}

Possible intents:
- payment_issue
- shop_creation
- plan_upgrade
- technical_problem
- product_management
- order_inquiry
- general_inquiry
- complaint

Response format:
{{
    "intent": "intent_name",
    "confidence": 0.95,
    "entities": {{
        "plan_mentioned": "free/pro/vip or null",
        "urgency": "low/medium/high",
        "topic": "brief description"
    }}
}}
"""
            
            response = await self.client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result
            
        except Exception as e:
            logger.error(f"Intent analysis error: {e}")
            return {"intent": "general_inquiry", "confidence": 0.5, "entities": {}}
    
    async def generate_quick_replies(self, user_message: str, user_language: str) -> List[str]:
        """Generate quick reply suggestions based on user message"""
        if not self.client:
            return self._get_default_quick_replies(user_language)
        
        try:
            prompt = f"""
Generate 3 quick reply options for this user message in {user_language}.
Keep replies short (max 25 characters each).

User message: "{user_message}"

Format: Just return 3 lines, each with a quick reply.
"""
            
            response = await self.client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            replies = response.choices[0].message.content.strip().split('\n')
            return [reply.strip() for reply in replies if reply.strip()][:3]
            
        except Exception as e:
            logger.error(f"Quick replies generation error: {e}")
            return self._get_default_quick_replies(user_language)
    
    def _get_default_quick_replies(self, user_language: str) -> List[str]:
        """Default quick replies when AI is unavailable"""
        quick_replies = {
            'fa': ['💬 ادامه چت', '📞 تماس با پشتیبانی', '🏠 منوی اصلی'],
            'en': ['💬 Continue Chat', '📞 Contact Support', '🏠 Main Menu'],
            'ar': ['💬 متابعة المحادثة', '📞 اتصل بالدعم', '🏠 القائمة الرئيسية']
        }
        return quick_replies.get(user_language, quick_replies['fa'])
    
    async def train_on_conversation(self, user_id: int, conversation_history: List[Dict]):
        """
        Store conversation for future AI training and improvement
        This helps the AI learn from real user interactions
        """
        try:
            training_data = {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'conversation': conversation_history,
                'language': conversation_history[-1].get('language', 'fa') if conversation_history else 'fa'
            }
            
            # In a production environment, this would be stored in a database
            # or sent to a training pipeline
            logger.info(f"Conversation training data collected for user {user_id}")
            
        except Exception as e:
            logger.error(f"Training data collection error: {e}")
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on AI service"""
        if not self.client:
            return {
                'status': 'unavailable',
                'message': 'AI client not initialized',
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Test with a simple query
            test_response = await self.client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            return {
                'status': 'healthy',
                'model': Config.AI_MODEL,
                'message': 'AI service operational',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Global AI service instance
ai_service = AIService()