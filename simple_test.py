#!/usr/bin/env python3
"""
Simple test for demo version structure
تست ساده برای ساختار نسخه دمو
"""

import os
from pathlib import Path

def test_file_structure():
    """Test if all required files exist"""
    print("📁 بررسی ساختار فایل‌های نسخه دمو...")
    
    required_files = [
        'bot_demo.py',
        'database_mock.py',
        'config.py',
        'utils.py',
        'handlers/user_handlers.py', 
        'handlers/admin_handlers.py',
        'requirements.txt',
        'Dockerfile.liara',
        'liara.json',
        'DEPLOY_LIARA.md',
        'README_DEMO.md'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 نتیجه:")
    print(f"✅ موجود: {len(existing_files)}")
    print(f"❌ ناموجود: {len(missing_files)}")
    
    if missing_files:
        print(f"\n❌ فایل‌های ناقص:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("🎉 تمام فایل‌های مورد نیاز موجود است!")
    return True

def test_syntax():
    """Test Python syntax of main files"""
    print("\n🔍 بررسی syntax فایل‌های اصلی...")
    
    main_files = [
        'bot_demo.py',
        'database_mock.py',
        'config.py',
        'utils.py'
    ]
    
    import ast
    
    for file_path in main_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
                print(f"✅ {file_path}: syntax صحیح")
            except SyntaxError as e:
                print(f"❌ {file_path}: خطای syntax - {e}")
                return False
            except Exception as e:
                print(f"⚠️ {file_path}: خطا در بررسی - {e}")
        else:
            print(f"❌ {file_path}: فایل موجود نیست")
            return False
    
    print("✅ syntax تمام فایل‌ها صحیح است!")
    return True

def test_dockerfile():
    """Test Dockerfile.liara exists and has basic structure"""
    print("\n🐳 بررسی Dockerfile.liara...")
    
    dockerfile_path = Path("Dockerfile.liara")
    if not dockerfile_path.exists():
        print("❌ Dockerfile.liara موجود نیست")
        return False
    
    with open(dockerfile_path, 'r') as f:
        content = f.read()
    
    required_instructions = ['FROM', 'WORKDIR', 'COPY', 'RUN', 'CMD']
    missing_instructions = []
    
    for instruction in required_instructions:
        if instruction not in content:
            missing_instructions.append(instruction)
        else:
            print(f"✅ {instruction} موجود است")
    
    if missing_instructions:
        print(f"❌ دستورات ناقص در Dockerfile: {missing_instructions}")
        return False
    
    print("✅ Dockerfile.liara ساختار صحیح دارد!")
    return True

def test_liara_config():
    """Test liara.json configuration"""
    print("\n⚙️ بررسی liara.json...")
    
    config_path = Path("liara.json")
    if not config_path.exists():
        print("❌ liara.json موجود نیست")
        return False
    
    try:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        required_keys = ['platform', 'app']
        for key in required_keys:
            if key in config:
                print(f"✅ {key}: {config[key]}")
            else:
                print(f"❌ {key} در تنظیمات موجود نیست")
                return False
        
        print("✅ liara.json ساختار صحیح دارد!")
        return True
        
    except json.JSONDecodeError:
        print("❌ liara.json فرمت نامعتبر دارد")
        return False

def main():
    """Run all simple tests"""
    print("🎭 تست‌های ساده نسخه دمو CodeRoot")
    print("=" * 50)
    
    tests = [
        ("بررسی ساختار فایل‌ها", test_file_structure),
        ("بررسی syntax فایل‌ها", test_syntax),
        ("بررسی Dockerfile", test_dockerfile),
        ("بررسی تنظیمات Liara", test_liara_config)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ خطا در {test_name}: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 نتایج:")
    print(f"✅ موفق: {passed}")
    print(f"❌ ناموفق: {failed}")
    
    if failed == 0:
        print("\n🎉 نسخه دمو آماده است!")
        print("🚀 دستورات بعدی:")
        print("   1. تنظیم متغیرهای محیطی در Liara")
        print("   2. دپلویمنت: liara deploy --app coderoot-demo")
        print("   3. مشاهده لاگ‌ها: liara app:logs --app coderoot-demo")
    else:
        print("\n⚠️ برخی مشکلات وجود دارد. لطفاً برطرف کنید.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)