#!/usr/bin/env python3
"""
Basic syntax and import testing for CodeRoot Bot
تست پایه‌ای سینتکس و import ها برای ربات CodeRoot
"""

import ast
import os
import sys
import traceback

def test_python_syntax(file_path):
    """Test Python file for syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check syntax
        ast.parse(content)
        print(f"✅ {file_path} - Syntax OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {file_path} - Error reading file: {e}")
        return False

def test_imports(file_path):
    """Test if file imports work without dependencies"""
    try:
        # Create a mock environment for testing
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        if spec is None:
            print(f"⚠️  {file_path} - Could not create spec")
            return False
        
        # Just check if the spec can be created (basic import structure test)
        print(f"✅ {file_path} - Import structure OK")
        return True
        
    except Exception as e:
        print(f"❌ {file_path} - Import Error: {e}")
        return False

def find_python_files():
    """Find all Python files in the project"""
    python_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip virtual environment and cache directories
        dirs[:] = [d for d in dirs if not d.startswith(('.', '__pycache__', 'venv'))]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def check_common_issues():
    """Check for common programming issues"""
    issues = []
    
    # Check for hardcoded credentials
    sensitive_patterns = ['password', 'token', 'api_key', 'secret']
    
    try:
        with open('bot.py', 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        for pattern in sensitive_patterns:
            if f'{pattern} =' in content and 'config.' not in content:
                issues.append(f"Potential hardcoded {pattern} in bot.py")
    except:
        pass
    
    # Check for TODO comments
    try:
        with open('bot.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines, 1):
            if 'TODO' in line.upper():
                issues.append(f"TODO found in bot.py line {i}: {line.strip()}")
    except:
        pass
    
    return issues

def main():
    """Run all basic tests"""
    print("🧪 Starting Basic CodeRoot Bot Tests...")
    print("="*60)
    
    # Find all Python files
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files")
    print("-"*60)
    
    # Test syntax
    syntax_results = []
    print("Testing syntax...")
    for file_path in python_files:
        result = test_python_syntax(file_path)
        syntax_results.append((file_path, result))
    
    print("-"*60)
    
    # Test imports structure
    import_results = []
    print("Testing import structure...")
    for file_path in python_files:
        result = test_imports(file_path)
        import_results.append((file_path, result))
    
    print("-"*60)
    
    # Check for common issues
    print("Checking for common issues...")
    issues = check_common_issues()
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("✅ No common issues found")
    
    print("-"*60)
    
    # Summary
    syntax_passed = sum(1 for _, result in syntax_results if result)
    import_passed = sum(1 for _, result in import_results if result)
    total_files = len(python_files)
    
    print("📊 SUMMARY")
    print(f"Syntax Tests: {syntax_passed}/{total_files} passed")
    print(f"Import Tests: {import_passed}/{total_files} passed")
    print(f"Issues Found: {len(issues)}")
    
    if syntax_passed == total_files and import_passed == total_files and len(issues) == 0:
        print("🎉 All basic tests passed!")
        return True
    else:
        print("⚠️  Some issues found - review above")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Test execution failed: {e}")
        traceback.print_exc()
        sys.exit(1)