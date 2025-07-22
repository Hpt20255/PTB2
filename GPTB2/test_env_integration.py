#!/usr/bin/env python3
"""
Integration test to verify environment variables work with Flask and React
"""
import os
import sys
import time
import requests
import subprocess
from dotenv import load_dotenv

def test_backend_with_env():
    """Test backend with environment variables"""
    print("\n🔧 TESTING BACKEND WITH ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    # Load backend environment
    load_dotenv('backend/.env', override=True)
    
    # Print loaded environment variables
    print("📋 Loaded Backend Environment Variables:")
    backend_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'FLASK_ENV', 'PORT', 'LOG_LEVEL']
    for var in backend_vars:
        value = os.getenv(var)
        if value:
            display_value = '*' * len(value) if 'PASSWORD' in var else value
            print(f"   ✅ {var}: {display_value}")
    
    # Test if backend can start with these variables
    print("\n🚀 Starting Backend Server...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen(
            ['python', 'app.py'],
            cwd='backend',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ.copy()
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test ping endpoint
        try:
            response = requests.get('http://localhost:5000/ping', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Backend Response: {data.get('message', 'No message')}")
                print(f"   ✅ Status: {data.get('status', 'Unknown')}")
                print(f"   ✅ Database Configured: {data.get('database_configured', False)}")
                backend_success = True
            else:
                print(f"   ❌ Backend returned status code: {response.status_code}")
                backend_success = False
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Backend connection failed: {e}")
            backend_success = False
        
        # Stop backend
        backend_process.terminate()
        backend_process.wait(timeout=5)
        
    except Exception as e:
        print(f"   ❌ Backend startup failed: {e}")
        backend_success = False
    
    return backend_success

def test_frontend_env():
    """Test frontend environment variables"""
    print("\n⚛️  TESTING FRONTEND ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    # Load frontend environment
    load_dotenv('frontend/.env', override=True)
    
    # Print loaded React environment variables
    print("📋 Loaded Frontend Environment Variables:")
    frontend_vars = [
        'REACT_APP_API_URL', 'REACT_APP_DEBUG', 'REACT_APP_ENV', 
        'PORT', 'HOST', 'REACT_APP_THEME', 'REACT_APP_LANGUAGE'
    ]
    
    for var in frontend_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Check if package.json exists
    if os.path.exists('frontend/package.json'):
        print("   ✅ package.json found")
        
        # Check if node_modules exists
        if os.path.exists('frontend/node_modules'):
            print("   ✅ node_modules found")
            frontend_ready = True
        else:
            print("   ⚠️  node_modules not found - run 'npm install' first")
            frontend_ready = False
    else:
        print("   ❌ package.json not found")
        frontend_ready = False
    
    return frontend_ready

def test_docker_compose_env():
    """Test Docker Compose environment variables"""
    print("\n🐳 TESTING DOCKER COMPOSE ENVIRONMENT")
    print("=" * 60)
    
    # Load main environment
    load_dotenv('.env', override=True)
    
    # Print Docker Compose variables
    print("📋 Docker Compose Environment Variables:")
    docker_vars = [
        'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
        'DEBUG', 'PORT', 'FRONTEND_PORT', 'SECRET_KEY'
    ]
    
    for var in docker_vars:
        value = os.getenv(var)
        if value:
            display_value = '*' * len(value) if 'PASSWORD' in var or 'SECRET' in var else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Check if docker-compose.yaml exists
    if os.path.exists('docker-compose.yaml'):
        print("   ✅ docker-compose.yaml found")
        docker_ready = True
    else:
        print("   ❌ docker-compose.yaml not found")
        docker_ready = False
    
    return docker_ready

def main():
    """Main integration test function"""
    print("🧪 GPTB2 Environment Integration Test Suite")
    print("=" * 60)
    
    # Change to project directory
    os.chdir('/workspace/TetsPTB2/GPTB2')
    
    # Run tests
    backend_success = test_backend_with_env()
    frontend_ready = test_frontend_env()
    docker_ready = test_docker_compose_env()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 INTEGRATION TEST SUMMARY")
    print(f"{'='*60}")
    print(f"🔧 Backend Environment: {'✅ PASS' if backend_success else '❌ FAIL'}")
    print(f"⚛️  Frontend Environment: {'✅ READY' if frontend_ready else '❌ NOT READY'}")
    print(f"🐳 Docker Environment: {'✅ READY' if docker_ready else '❌ NOT READY'}")
    
    # Overall status
    if backend_success and frontend_ready and docker_ready:
        print("\n🎉 All environment configurations are working correctly!")
        print("✅ Task 3.1 - Environment Variables Configuration: COMPLETED")
        return 0
    else:
        print("\n⚠️  Some environment configurations need attention.")
        if not backend_success:
            print("   - Backend environment needs fixing")
        if not frontend_ready:
            print("   - Frontend environment needs setup")
        if not docker_ready:
            print("   - Docker environment needs configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())