#!/usr/bin/env python3
"""
Test script to verify all dependencies are working correctly before deployment.
This script should run without errors on Liara platform.
"""

import sys
import importlib

# List of critical modules to test
CRITICAL_MODULES = [
    'pyrogram',
    'tgcrypto', 
    'pymongo',
    'motor',
    'redis',
    'dotenv',
    'aiofiles',
    'aiohttp',
    'jdatetime',
    'bcrypt',
    'cryptography',
    'PIL',  # Pillow
    'qrcode',
    'schedule',
    'apscheduler',
    'pandas',
    'openpyxl',
    'httpx',
    'pydantic',
    'openai'
]

def test_imports():
    """Test importing all critical modules."""
    print("🧪 Testing CodeRoot Bot Dependencies...")
    print("=" * 50)
    
    failed_imports = []
    
    for module in CRITICAL_MODULES:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"⚠️  {module} - ERROR: {e}")
            failed_imports.append(module)
    
    print("=" * 50)
    
    if failed_imports:
        print(f"❌ FAILED: {len(failed_imports)} modules failed to import:")
        for module in failed_imports:
            print(f"   - {module}")
        return False
    else:
        print("✅ ALL DEPENDENCIES OK - Ready for deployment!")
        return True

def test_openai_version():
    """Test specific OpenAI version."""
    try:
        import openai
        print(f"🤖 OpenAI version: {openai.__version__}")
        
        # Test if we can create a client
        from openai import OpenAI
        client = OpenAI(api_key="test-key", base_url="https://api.openai.com/v1")
        print("✅ OpenAI client creation - OK")
        return True
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

def test_bot_imports():
    """Test bot-specific imports."""
    try:
        from config import Config
        print("✅ Config import - OK")
        
        from database import DatabaseManager
        print("✅ Database import - OK")
        
        return True
    except Exception as e:
        print(f"❌ Bot imports failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CodeRoot Bot Deployment Test")
    print(f"🐍 Python version: {sys.version}")
    print()
    
    # Test 1: Module imports
    imports_ok = test_imports()
    print()
    
    # Test 2: OpenAI specific test
    openai_ok = test_openai_version()
    print()
    
    # Test 3: Bot imports
    bot_ok = test_bot_imports()
    print()
    
    # Final result
    if imports_ok and openai_ok and bot_ok:
        print("🎉 ALL TESTS PASSED - READY FOR LIARA DEPLOYMENT!")
        sys.exit(0)
    else:
        print("💥 SOME TESTS FAILED - FIX BEFORE DEPLOYMENT")
        sys.exit(1)