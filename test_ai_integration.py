#!/usr/bin/env python3
"""
Test AI Integration for CodeRoot Bot
Tests the enhanced AI service with Liara API (Gemini 2.0 Flash)
"""

import asyncio
import logging
import json
from datetime import datetime
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import ai_service
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_ai_connection():
    """Test basic AI connection"""
    print("🔌 Testing AI Connection...")
    try:
        is_connected = await ai_service.test_ai_connection()
        if is_connected:
            print("✅ AI Connection: SUCCESS")
            return True
        else:
            print("❌ AI Connection: FAILED")
            return False
    except Exception as e:
        print(f"❌ AI Connection Error: {e}")
        return False

async def test_persian_support():
    """Test Persian language support"""
    print("\n🇮🇷 Testing Persian Support...")
    try:
        test_user_id = 12345
        persian_question = "چطور فروشگاه بسازم؟"
        
        response = await ai_service.get_ai_response(
            user_id=test_user_id,
            message=persian_question,
            user_language='fa'
        )
        
        print(f"سوال: {persian_question}")
        print(f"پاسخ AI: {response[:200]}...")
        
        if "فروشگاه" in response and "CodeRoot" in response:
            print("✅ Persian Support: SUCCESS")
            return True
        else:
            print("❌ Persian Support: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Persian Support Error: {e}")
        return False

async def test_english_support():
    """Test English language support"""
    print("\n🇺🇸 Testing English Support...")
    try:
        test_user_id = 12346
        english_question = "How do I create a shop?"
        
        response = await ai_service.get_ai_response(
            user_id=test_user_id,
            message=english_question,
            user_language='en'
        )
        
        print(f"Question: {english_question}")
        print(f"AI Response: {response[:200]}...")
        
        if "shop" in response.lower() and ("create" in response.lower() or "CodeRoot" in response):
            print("✅ English Support: SUCCESS")
            return True
        else:
            print("❌ English Support: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ English Support Error: {e}")
        return False

async def test_arabic_support():
    """Test Arabic language support"""
    print("\n🇸🇦 Testing Arabic Support...")
    try:
        test_user_id = 12347
        arabic_question = "كيف أنشئ متجراً؟"
        
        response = await ai_service.get_ai_response(
            user_id=test_user_id,
            message=arabic_question,
            user_language='ar'
        )
        
        print(f"السؤال: {arabic_question}")
        print(f"إجابة AI: {response[:200]}...")
        
        if "متجر" in response and ("CodeRoot" in response or "إنشاء" in response):
            print("✅ Arabic Support: SUCCESS")
            return True
        else:
            print("❌ Arabic Support: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Arabic Support Error: {e}")
        return False

async def test_shop_specific_support():
    """Test shop-specific AI support"""
    print("\n🏪 Testing Shop-Specific Support...")
    try:
        test_user_id = 12348
        shop_data = {
            'name': 'تست شاپ',
            'plan': 'professional',
            'products_count': 15,
            'status': 'active',
            'created_at': '2024-01-01',
            'total_sales': 5
        }
        
        issue = "محصولاتم در ربات نمایش داده نمیشن"
        
        response = await ai_service.get_shop_support(
            user_id=test_user_id,
            shop_data=shop_data,
            issue=issue,
            user_language='fa'
        )
        
        print(f"مشکل فروشگاه: {issue}")
        print(f"پاسخ AI: {response[:200]}...")
        
        if "محصول" in response and ("بررسی" in response or "راه‌حل" in response):
            print("✅ Shop Support: SUCCESS")
            return True
        else:
            print("❌ Shop Support: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Shop Support Error: {e}")
        return False

async def test_admin_assistance():
    """Test admin assistance functionality"""
    print("\n👑 Testing Admin Assistance...")
    try:
        admin_id = Config.ADMIN_USER_ID
        admin_query = "چند تا فروشگاه فعال داریم و درآمد ماهانه چقدره؟"
        
        response = await ai_service.get_admin_assistance(
            admin_id=admin_id,
            query=admin_query
        )
        
        print(f"سوال ادمین: {admin_query}")
        print(f"پاسخ AI: {response[:200]}...")
        
        if "فروشگاه" in response and ("ادمین" in response or "گزارش" in response):
            print("✅ Admin Assistance: SUCCESS")
            return True
        else:
            print("❌ Admin Assistance: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Admin Assistance Error: {e}")
        return False

async def test_user_intent_analysis():
    """Test user intent analysis"""
    print("\n🎯 Testing Intent Analysis...")
    try:
        test_messages = [
            "میخوام فروشگاه بسازم",
            "مشکل پرداخت دارم",
            "ربات جواب نمیده",
            "چطور محصول اضافه کنم؟"
        ]
        
        for message in test_messages:
            intent_data = await ai_service.analyze_user_intent(message, 'fa')
            print(f"پیام: {message}")
            print(f"قصد: {intent_data.get('intent', 'نامشخص')}")
            print(f"اطمینان: {intent_data.get('confidence', 0):.2f}")
            print("---")
        
        print("✅ Intent Analysis: SUCCESS")
        return True
        
    except Exception as e:
        print(f"❌ Intent Analysis Error: {e}")
        return False

async def test_content_suggestions():
    """Test content suggestion generation"""
    print("\n💡 Testing Content Suggestions...")
    try:
        shop_data = {
            'name': 'فروشگاه لباس',
            'plan': 'professional',
            'category': 'fashion',
            'products_count': 50
        }
        
        suggestions = await ai_service.generate_content_suggestions(
            shop_data=shop_data,
            target_audience='جوانان'
        )
        
        print("پیشنهادات محتوا:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        
        if len(suggestions) >= 3:
            print("✅ Content Suggestions: SUCCESS")
            return True
        else:
            print("❌ Content Suggestions: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Content Suggestions Error: {e}")
        return False

async def test_quick_replies():
    """Test quick reply generation"""
    print("\n⚡ Testing Quick Replies...")
    try:
        test_message = "مشکل پرداخت دارم"
        
        quick_replies = await ai_service.generate_quick_replies(test_message, 'fa')
        
        print(f"پیام: {test_message}")
        print("پاسخ‌های سریع:")
        for reply in quick_replies:
            print(f"- {reply}")
        
        if len(quick_replies) >= 2:
            print("✅ Quick Replies: SUCCESS")
            return True
        else:
            print("❌ Quick Replies: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Quick Replies Error: {e}")
        return False

async def test_conversation_flow():
    """Test conversation flow and context"""
    print("\n💬 Testing Conversation Flow...")
    try:
        test_user_id = 12349
        
        # Simulate a conversation
        messages = [
            "سلام، میخوام فروشگاه بسازم",
            "پلن حرفه‌ای چیه؟",
            "چطور پرداخت کنم؟",
            "رسید رو کجا بفرستم؟"
        ]
        
        for message in messages:
            response = await ai_service.get_ai_response(
                user_id=test_user_id,
                message=message,
                user_language='fa'
            )
            print(f"کاربر: {message}")
            print(f"AI: {response[:100]}...")
            print("---")
        
        print("✅ Conversation Flow: SUCCESS")
        return True
        
    except Exception as e:
        print(f"❌ Conversation Flow Error: {e}")
        return False

async def test_feature_explanation():
    """Test feature explanation capability"""
    print("\n📚 Testing Feature Explanation...")
    try:
        feature = "سیستم معرفی"
        
        explanation = await ai_service.get_feature_explanation(feature, 'fa')
        
        print(f"ویژگی: {feature}")
        print(f"توضیح: {explanation[:200]}...")
        
        if "معرفی" in explanation and len(explanation) > 100:
            print("✅ Feature Explanation: SUCCESS")
            return True
        else:
            print("❌ Feature Explanation: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Feature Explanation Error: {e}")
        return False

async def run_comprehensive_ai_tests():
    """Run all AI tests"""
    print("🤖 CodeRoot AI Integration Test Suite")
    print("=====================================")
    print(f"🔗 AI Base URL: {Config.AI_BASE_URL}")
    print(f"🤖 AI Model: {Config.AI_MODEL}")
    print(f"📊 Max Tokens: {Config.AI_MAX_TOKENS}")
    print(f"🌡️ Temperature: {Config.AI_TEMPERATURE}")
    print("=====================================\n")
    
    test_results = {}
    
    # Run all tests
    test_functions = [
        ("Connection Test", test_ai_connection),
        ("Persian Support", test_persian_support),
        ("English Support", test_english_support),
        ("Arabic Support", test_arabic_support),
        ("Shop Support", test_shop_specific_support),
        ("Admin Assistance", test_admin_assistance),
        ("Intent Analysis", test_user_intent_analysis),
        ("Content Suggestions", test_content_suggestions),
        ("Quick Replies", test_quick_replies),
        ("Conversation Flow", test_conversation_flow),
        ("Feature Explanation", test_feature_explanation)
    ]
    
    for test_name, test_func in test_functions:
        try:
            result = await test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name}: FAILED with error: {e}")
            test_results[test_name] = False
        
        # Small delay between tests
        await asyncio.sleep(1)
    
    # Summary
    print("\n" + "="*50)
    print("🏁 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! AI is fully trained and ready!")
    elif passed >= total * 0.8:
        print("🌟 Most tests passed! AI is well-trained!")
    elif passed >= total * 0.6:
        print("⚠️ Some issues detected. AI needs minor adjustments.")
    else:
        print("🚨 Multiple failures. AI needs significant work.")
    
    return test_results

if __name__ == "__main__":
    try:
        results = asyncio.run(run_comprehensive_ai_tests())
        
        # Save test results
        with open('ai_test_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'config': {
                    'ai_enabled': Config.AI_ENABLED,
                    'ai_base_url': Config.AI_BASE_URL,
                    'ai_model': Config.AI_MODEL,
                    'ai_max_tokens': Config.AI_MAX_TOKENS,
                    'ai_temperature': Config.AI_TEMPERATURE
                },
                'results': results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Test results saved to: ai_test_results.json")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error during testing: {e}")
        import traceback
        traceback.print_exc()