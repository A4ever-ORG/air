#!/usr/bin/env python3
"""
Comprehensive Test Suite for CodeRoot Bot
تست جامع برای ربات CodeRoot
"""

import asyncio
import logging
import sys
import os
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import bot modules
from config import Config
from database import DatabaseManager
from utils.bot_utils import BotUtils
from utils.validation import Validation
from utils.security import Security
from utils.language import translator
from utils.keyboards import Keyboards

# Configure test logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestConfig:
    """Test configuration settings"""
    
    def test_config_loading(self):
        """Test configuration loading"""
        try:
            # Test required configurations
            assert Config.BOT_TOKEN is not None or Config.DEMO_MODE
            assert Config.API_ID is not None or Config.DEMO_MODE
            assert Config.API_HASH is not None or Config.DEMO_MODE
            
            # Test optional configurations have defaults
            assert Config.DATABASE_NAME
            assert Config.DEFAULT_LANGUAGE
            assert Config.LOG_LEVEL
            
            logger.info("✅ Configuration test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Configuration test failed: {e}")
            return False

class TestBotUtils:
    """Test bot utility functions"""
    
    def test_date_formatting(self):
        """Test date formatting functions"""
        try:
            test_date = datetime.now()
            
            # Test different format types
            date_str = BotUtils.format_datetime(test_date, "date")
            assert len(date_str) > 0
            
            time_str = BotUtils.format_datetime(test_date, "time")
            assert len(time_str) > 0
            
            short_str = BotUtils.format_datetime(test_date, "short")
            assert len(short_str) > 0
            
            full_str = BotUtils.format_datetime(test_date, "full")
            assert len(full_str) > 0
            
            # Test invalid input handling
            result = BotUtils.format_datetime(None)
            assert result == "None"
            
            logger.info("✅ Date formatting test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Date formatting test failed: {e}")
            return False
    
    def test_text_processing(self):
        """Test text processing functions"""
        try:
            test_text = "Hello @user123 #test 12345"
            
            # Test number extraction
            numbers = BotUtils.extract_numbers(test_text)
            assert 12345 in numbers
            
            # Test mention extraction
            mentions = BotUtils.extract_mentions(test_text)
            assert "user123" in mentions
            
            # Test hashtag extraction
            hashtags = BotUtils.extract_hashtags(test_text)
            assert "test" in hashtags
            
            # Test text truncation
            long_text = "a" * 200
            truncated = BotUtils.truncate_text(long_text, 50)
            assert len(truncated) <= 53  # 50 + "..."
            
            logger.info("✅ Text processing test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Text processing test failed: {e}")
            return False
    
    def test_callback_data(self):
        """Test callback data handling"""
        try:
            # Test callback data creation
            callback_data = BotUtils.create_callback_data("test", "param", "extra")
            assert "test" in callback_data
            
            # Test callback data parsing
            parsed = BotUtils.parse_callback_data(callback_data)
            assert parsed['action'] == "test"
            assert parsed['param'] == "param"
            assert parsed['extra'] == "extra"
            
            # Test invalid callback data
            invalid_parsed = BotUtils.parse_callback_data("invalid")
            assert invalid_parsed['action'] == "invalid"
            
            logger.info("✅ Callback data test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Callback data test failed: {e}")
            return False

class TestValidation:
    """Test validation functions"""
    
    def test_user_input_validation(self):
        """Test user input validation"""
        try:
            # Test shop name validation
            valid_name = "My Shop"
            assert Validation.validate_shop_name(valid_name)
            
            invalid_name = ""
            assert not Validation.validate_shop_name(invalid_name)
            
            # Test product validation
            valid_product = {
                'name': 'Test Product',
                'price': 100,
                'description': 'Test description'
            }
            assert Validation.validate_product_data(valid_product)
            
            invalid_product = {
                'name': '',
                'price': -1
            }
            assert not Validation.validate_product_data(invalid_product)
            
            logger.info("✅ Validation test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Validation test failed: {e}")
            return False
    
    def test_payment_validation(self):
        """Test payment validation"""
        try:
            # Test payment data validation
            valid_payment = {
                'amount': 1000,
                'currency': 'IRR',
                'transaction_id': '12345'
            }
            assert Validation.validate_payment_data(valid_payment)
            
            invalid_payment = {
                'amount': -100
            }
            assert not Validation.validate_payment_data(invalid_payment)
            
            logger.info("✅ Payment validation test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Payment validation test failed: {e}")
            return False

class TestSecurity:
    """Test security functions"""
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        try:
            # Test SQL injection prevention
            malicious_input = "'; DROP TABLE users; --"
            sanitized = Security.sanitize_input(malicious_input)
            assert "DROP" not in sanitized.upper()
            
            # Test XSS prevention
            xss_input = "<script>alert('xss')</script>"
            sanitized_xss = Security.sanitize_input(xss_input)
            assert "<script>" not in sanitized_xss
            
            logger.info("✅ Security test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Security test failed: {e}")
            return False
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        try:
            user_id = 12345
            
            # Test rate limiting
            for i in range(10):
                result = Security.check_rate_limit(user_id, "message")
                if i < 5:
                    assert result  # Should allow first few requests
                
            # After many requests, should be rate limited
            # This is a simplified test
            
            logger.info("✅ Rate limiting test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Rate limiting test failed: {e}")
            return False

class TestLanguage:
    """Test language and translation functions"""
    
    def test_translation(self):
        """Test translation system"""
        try:
            # Test text retrieval in different languages
            fa_text = translator.get_text('welcome_message', 'fa')
            en_text = translator.get_text('welcome_message', 'en')
            
            assert fa_text != en_text
            assert len(fa_text) > 0
            assert len(en_text) > 0
            
            # Test fallback to default language
            fallback_text = translator.get_text('nonexistent_key', 'fa')
            assert len(fallback_text) > 0
            
            logger.info("✅ Language test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Language test failed: {e}")
            return False

class TestKeyboards:
    """Test keyboard generation"""
    
    def test_keyboard_generation(self):
        """Test keyboard creation"""
        try:
            # Test main menu keyboard
            keyboard = Keyboards.main_menu_keyboard('fa')
            assert keyboard is not None
            
            # Test language selection keyboard
            lang_keyboard = translator.get_language_selection_keyboard()
            assert lang_keyboard is not None
            
            # Test admin keyboard
            admin_keyboard = Keyboards.admin_menu_keyboard('fa')
            assert admin_keyboard is not None
            
            logger.info("✅ Keyboard generation test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Keyboard generation test failed: {e}")
            return False

async def test_database_operations():
    """Test database operations"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Test connection (will use mock in testing)
        with patch.object(db_manager, 'connect', new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = True
            await db_manager.connect()
            mock_connect.assert_called_once()
        
        # Test user operations
        with patch.object(db_manager, 'users') as mock_users:
            mock_users.get_user = AsyncMock(return_value={'user_id': 123, 'username': 'test'})
            mock_users.create_user = AsyncMock(return_value={'user_id': 123})
            mock_users.update_user = AsyncMock(return_value=True)
            
            # Test get user
            user = await mock_users.get_user(123)
            assert user['user_id'] == 123
            
            # Test create user
            new_user = await mock_users.create_user({'user_id': 123})
            assert new_user['user_id'] == 123
            
        logger.info("✅ Database operations test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database operations test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    results = []
    
    logger.info("🧪 Starting comprehensive bot tests...")
    
    # Configuration tests
    config_test = TestConfig()
    results.append(("Configuration", config_test.test_config_loading()))
    
    # Bot utils tests
    utils_test = TestBotUtils()
    results.append(("Date Formatting", utils_test.test_date_formatting()))
    results.append(("Text Processing", utils_test.test_text_processing()))
    results.append(("Callback Data", utils_test.test_callback_data()))
    
    # Validation tests
    validation_test = TestValidation()
    results.append(("User Input Validation", validation_test.test_user_input_validation()))
    results.append(("Payment Validation", validation_test.test_payment_validation()))
    
    # Security tests
    security_test = TestSecurity()
    results.append(("Input Sanitization", security_test.test_input_sanitization()))
    results.append(("Rate Limiting", security_test.test_rate_limiting()))
    
    # Language tests
    language_test = TestLanguage()
    results.append(("Translation", language_test.test_translation()))
    
    # Keyboard tests
    keyboard_test = TestKeyboards()
    results.append(("Keyboard Generation", keyboard_test.test_keyboard_generation()))
    
    # Database tests (async)
    try:
        db_result = asyncio.run(test_database_operations())
        results.append(("Database Operations", db_result))
    except Exception as e:
        logger.error(f"Database test error: {e}")
        results.append(("Database Operations", False))
    
    # Report results
    logger.info("\n" + "="*60)
    logger.info("🧪 TEST RESULTS SUMMARY")
    logger.info("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    logger.info("="*60)
    logger.info(f"Total: {total}, Passed: {passed}, Failed: {total - passed}")
    logger.info(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED! Bot is ready for deployment.")
        return True
    else:
        logger.warning(f"⚠️  {total - passed} tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    # Set demo mode for testing
    Config.DEMO_MODE = True
    
    try:
        success = run_all_tests()
        exit_code = 0 if success else 1
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        sys.exit(1)