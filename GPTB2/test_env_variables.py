#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""
import os
import sys
from dotenv import load_dotenv

def test_env_file(env_file_path, description):
    """Test loading environment variables from a specific .env file"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING: {description}")
    print(f"📁 File: {env_file_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(env_file_path):
        print(f"❌ ERROR: File {env_file_path} does not exist!")
        return False
    
    # Clear existing environment variables
    env_vars_to_clear = [
        'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
        'DEBUG', 'PORT', 'FRONTEND_PORT', 'SECRET_KEY', 'CORS_ORIGINS',
        'LOG_LEVEL', 'FLASK_ENV', 'REACT_APP_API_URL', 'REACT_APP_DEBUG'
    ]
    
    for var in env_vars_to_clear:
        if var in os.environ:
            del os.environ[var]
    
    # Load the specific .env file
    load_dotenv(env_file_path, override=True)
    
    # Test database variables
    print("\n🗄️  DATABASE CONFIGURATION:")
    db_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    for var in db_vars:
        value = os.getenv(var)
        if value:
            display_value = '*' * len(value) if 'PASSWORD' in var else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Test application variables
    print("\n🚀 APPLICATION CONFIGURATION:")
    app_vars = ['DEBUG', 'PORT', 'FRONTEND_PORT', 'SECRET_KEY', 'FLASK_ENV']
    for var in app_vars:
        value = os.getenv(var)
        if value:
            display_value = '*' * len(value) if 'SECRET' in var else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Test network variables
    print("\n🌐 NETWORK CONFIGURATION:")
    network_vars = ['CORS_ORIGINS', 'LOG_LEVEL']
    for var in network_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Test React variables (if present)
    react_vars = ['REACT_APP_API_URL', 'REACT_APP_DEBUG', 'REACT_APP_ENV']
    react_found = False
    for var in react_vars:
        value = os.getenv(var)
        if value:
            if not react_found:
                print("\n⚛️  REACT CONFIGURATION:")
                react_found = True
            print(f"   ✅ {var}: {value}")
    
    return True

def main():
    """Main test function"""
    print("🧪 GPTB2 Environment Variables Test Suite")
    print("=" * 60)
    
    # Test different environment files
    env_files = [
        (".env", "Main Environment (Docker Compose)"),
        ("backend/.env", "Backend Development Environment"),
        ("frontend/.env", "Frontend Development Environment"),
        (".env.production", "Production Environment"),
        ("backend/.env.production", "Backend Production Environment"),
        ("frontend/.env.production", "Frontend Production Environment"),
        (".env.testing", "Testing Environment"),
        (".env.example", "Example Environment Template")
    ]
    
    success_count = 0
    total_count = len(env_files)
    
    for env_file, description in env_files:
        if test_env_file(env_file, description):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful tests: {success_count}/{total_count}")
    print(f"❌ Failed tests: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All environment files are properly configured!")
        return 0
    else:
        print("⚠️  Some environment files have issues. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())