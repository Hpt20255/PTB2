#!/usr/bin/env python3
"""
Test script cho API POST /api/equation
"""
import requests
import json
import time
import subprocess
import os
import signal

def start_flask_server():
    """Start Flask server in background"""
    print("Starting Flask server...")
    process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='/workspace/TetsPTB2/GPTB2/backend'
    )
    time.sleep(3)  # Wait for server to start
    return process

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("=== TESTING API POST /api/equation ===")
    
    # Test cases
    test_cases = [
        {
            'name': 'Two real roots',
            'data': {'a': 1, 'b': -5, 'c': 6},
            'expected_type': 'two_real'
        },
        {
            'name': 'One repeated root',
            'data': {'a': 1, 'b': -4, 'c': 4},
            'expected_type': 'one_real'
        },
        {
            'name': 'Complex roots',
            'data': {'a': 1, 'b': 0, 'c': 1},
            'expected_type': 'complex'
        },
        {
            'name': 'Linear equation',
            'data': {'a': 0, 'b': 2, 'c': -4},
            'expected_type': 'linear'
        }
    ]
    
    # Test valid requests
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {case['name']} ---")
        try:
            response = requests.post(
                f"{base_url}/api/equation",
                json=case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"✅ SUCCESS: {data['message']}")
                print(f"   Equation: {data['data']['equation_string']}")
                print(f"   Solution: {data['data']['solution']}")
                print(f"   Type: {data['data']['solution_type']} (expected: {case['expected_type']})")
                print(f"   Status: {data['status']}")
            else:
                print(f"❌ FAILED: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    # Test invalid requests
    print(f"\n=== TESTING VALIDATION ===")
    
    invalid_cases = [
        {
            'name': 'Missing field',
            'data': {'a': 1, 'b': 2},  # missing 'c'
            'expected_status': 400
        },
        {
            'name': 'Invalid data type',
            'data': {'a': 'invalid', 'b': 2, 'c': 3},
            'expected_status': 400
        },
        {
            'name': 'Empty request',
            'data': {},
            'expected_status': 400
        }
    ]
    
    for i, case in enumerate(invalid_cases, 1):
        print(f"\n--- Invalid Test {i}: {case['name']} ---")
        try:
            response = requests.post(
                f"{base_url}/api/equation",
                json=case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == case['expected_status']:
                data = response.json()
                print(f"✅ VALIDATION SUCCESS: {data['message']}")
            else:
                print(f"❌ UNEXPECTED STATUS: Expected {case['expected_status']}, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    # Test GET endpoints
    print(f"\n=== TESTING GET ENDPOINTS ===")
    
    try:
        # Test GET all equations
        response = requests.get(f"{base_url}/api/equation", timeout=5)
        print(f"\nGET /api/equation - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: {data['message']}")
            print(f"   Count: {data.get('count', 0)} equations")
        else:
            print(f"❌ FAILED: {response.text}")
            
        # Test GET specific equation (if any exist)
        if response.status_code == 200 and data.get('count', 0) > 0:
            first_eq_id = data['data'][0]['id']
            response = requests.get(f"{base_url}/api/equation/{first_eq_id}", timeout=5)
            print(f"\nGET /api/equation/{first_eq_id} - Status: {response.status_code}")
            
            if response.status_code == 200:
                eq_data = response.json()
                print(f"✅ SUCCESS: {eq_data['message']}")
                print(f"   Equation: {eq_data['data']['equation_string']}")
            else:
                print(f"❌ FAILED: {response.text}")
                
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    server_process = None
    try:
        # Start Flask server
        server_process = start_flask_server()
        
        # Test API endpoints
        test_api_endpoints()
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        
    finally:
        # Clean up server process
        if server_process:
            print(f"\nStopping Flask server...")
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")
        
    print("\n=== API TESTING COMPLETED ===")