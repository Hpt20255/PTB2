#!/usr/bin/env python3
"""
Test API POST /api/equation với SQLite database
"""
import os
import sys
import tempfile
from flask import Flask
from models import db, Equation

# Override environment for SQLite testing
os.environ['DB_HOST'] = 'sqlite'

# Import app after setting environment
sys.path.insert(0, '/workspace/TetsPTB2/GPTB2/backend')
from app import app

def test_api_with_sqlite():
    """Test API với SQLite database"""
    
    # Configure app for testing with SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            # Create tables
            db.create_all()
            print("✅ SQLite tables created")
            
            print("\n=== TESTING POST /api/equation WITH DATABASE ===")
            
            # Test cases
            test_cases = [
                {'a': 1, 'b': -5, 'c': 6, 'name': 'Two real roots'},
                {'a': 1, 'b': -4, 'c': 4, 'name': 'One repeated root'},
                {'a': 1, 'b': 0, 'c': 1, 'name': 'Complex roots'},
                {'a': 0, 'b': 2, 'c': -4, 'name': 'Linear equation'},
            ]
            
            created_ids = []
            
            for i, case in enumerate(test_cases, 1):
                print(f"\n--- Test {i}: {case['name']} ---")
                
                response = client.post('/api/equation', 
                                     json=case,
                                     content_type='application/json')
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 201:
                    data = response.get_json()
                    print(f"✅ SUCCESS: {data['message']}")
                    print(f"   ID: {data['data']['id']}")
                    print(f"   Equation: {data['data']['equation_string']}")
                    print(f"   Solution: {data['data']['solution']}")
                    print(f"   Status: {data['status']}")
                    created_ids.append(data['data']['id'])
                else:
                    print(f"❌ FAILED: {response.get_json()}")
            
            # Test GET all equations
            print(f"\n=== TESTING GET /api/equation ===")
            response = client.get('/api/equation')
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ SUCCESS: {data['message']}")
                print(f"   Count: {data['count']} equations")
                
                for eq in data['data']:
                    print(f"   - ID {eq['id']}: {eq['equation_string']} → {eq['solution']}")
            else:
                print(f"❌ FAILED: {response.get_json()}")
            
            # Test GET specific equation
            if created_ids:
                test_id = created_ids[0]
                print(f"\n=== TESTING GET /api/equation/{test_id} ===")
                response = client.get(f'/api/equation/{test_id}')
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"✅ SUCCESS: {data['message']}")
                    print(f"   Equation: {data['data']['equation_string']}")
                    print(f"   Solution: {data['data']['solution']}")
                else:
                    print(f"❌ FAILED: {response.get_json()}")
            
            # Test validation
            print(f"\n=== TESTING VALIDATION ===")
            
            # Missing field
            response = client.post('/api/equation', 
                                 json={'a': 1, 'b': 2},
                                 content_type='application/json')
            print(f"Missing field - Status: {response.status_code}")
            if response.status_code == 400:
                print(f"✅ VALIDATION SUCCESS: {response.get_json()['message']}")
            
            # Invalid data type
            response = client.post('/api/equation', 
                                 json={'a': 'invalid', 'b': 2, 'c': 3},
                                 content_type='application/json')
            print(f"Invalid type - Status: {response.status_code}")
            if response.status_code == 400:
                print(f"✅ VALIDATION SUCCESS: {response.get_json()['message']}")
            
            print(f"\n=== DATABASE VERIFICATION ===")
            # Verify database directly
            equations = Equation.query.all()
            print(f"✅ Total equations in database: {len(equations)}")
            
            for eq in equations:
                print(f"   - {eq}")

if __name__ == "__main__":
    test_api_with_sqlite()
    print("\n=== API TESTING WITH DATABASE COMPLETED ===")