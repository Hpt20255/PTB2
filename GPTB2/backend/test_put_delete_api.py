#!/usr/bin/env python3
"""
Test script cho API PUT và DELETE operations
"""
import os
from flask import Flask
from models import db, Equation

def create_test_app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    
    # Configure for SQLite testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    # Initialize database
    db.init_app(app)
    
    # Import routes after app configuration
    from app import (create_equation, get_all_equations, get_equation, 
                     update_equation, delete_equation, create_bulk_equations, 
                     get_equation_stats)
    
    # Register routes manually
    app.add_url_rule('/api/equation', 'create_equation', create_equation, methods=['POST'])
    app.add_url_rule('/api/equation', 'get_all_equations', get_all_equations, methods=['GET'])
    app.add_url_rule('/api/equation/<int:equation_id>', 'get_equation', get_equation, methods=['GET'])
    app.add_url_rule('/api/equation/<int:equation_id>', 'update_equation', update_equation, methods=['PUT'])
    app.add_url_rule('/api/equation/<int:equation_id>', 'delete_equation', delete_equation, methods=['DELETE'])
    app.add_url_rule('/api/equations/bulk', 'create_bulk_equations', create_bulk_equations, methods=['POST'])
    app.add_url_rule('/api/equations/stats', 'get_equation_stats', get_equation_stats, methods=['GET'])
    
    return app

def test_complete_crud_operations():
    """Test complete CRUD operations including PUT and DELETE"""
    app = create_test_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Create tables
            db.create_all()
            print("✅ SQLite database and tables created")
            
            print("\n=== STEP 1: CREATE INITIAL EQUATIONS ===")
            
            # Create some initial equations
            initial_equations = [
                {'a': 1, 'b': -5, 'c': 6, 'name': 'Two real roots'},
                {'a': 1, 'b': -4, 'c': 4, 'name': 'One repeated root'},
                {'a': 1, 'b': 0, 'c': 1, 'name': 'Complex roots'},
            ]
            
            created_ids = []
            
            for i, eq_data in enumerate(initial_equations, 1):
                print(f"\n--- Creating Equation {i}: {eq_data['name']} ---")
                
                response = client.post('/api/equation', 
                                     json=eq_data,
                                     content_type='application/json')
                
                if response.status_code == 201:
                    data = response.get_json()
                    print(f"✅ Created ID {data['data']['id']}: {data['data']['equation_string']}")
                    print(f"   Solution: {data['data']['solution']}")
                    created_ids.append(data['data']['id'])
                else:
                    print(f"❌ Failed to create: {response.get_json()}")
            
            print(f"\n✅ Created {len(created_ids)} equations: IDs {created_ids}")
            
            print("\n=== STEP 2: TEST PUT API (UPDATE EQUATIONS) ===")
            
            if created_ids:
                # Test updating first equation
                update_id = created_ids[0]
                print(f"\n--- Testing PUT /api/equation/{update_id} ---")
                
                # Update to different coefficients
                update_data = {'a': 2, 'b': -7, 'c': 3}  # 2x² - 7x + 3 = 0
                
                response = client.put(f'/api/equation/{update_id}',
                                    json=update_data,
                                    content_type='application/json')
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"✅ UPDATE SUCCESS: {data['message']}")
                    print(f"   Previous: {data['previous_values']['equation_string']}")
                    print(f"   Previous Solution: {data['previous_values']['solution']}")
                    print(f"   New: {data['data']['equation_string']}")
                    print(f"   New Solution: {data['data']['solution']}")
                    print(f"   New Type: {data['data']['solution_type']}")
                else:
                    print(f"❌ UPDATE FAILED: {response.get_json()}")
                
                # Test updating non-existent equation
                print(f"\n--- Testing PUT /api/equation/999 (non-existent) ---")
                response = client.put('/api/equation/999',
                                    json={'a': 1, 'b': 2, 'c': 3},
                                    content_type='application/json')
                
                print(f"Status Code: {response.status_code}")
                if response.status_code == 404:
                    print(f"✅ 404 SUCCESS: {response.get_json()['message']}")
                
                # Test PUT validation
                print(f"\n--- Testing PUT validation (missing field) ---")
                response = client.put(f'/api/equation/{update_id}',
                                    json={'a': 1, 'b': 2},  # missing 'c'
                                    content_type='application/json')
                
                print(f"Status Code: {response.status_code}")
                if response.status_code == 400:
                    print(f"✅ VALIDATION SUCCESS: {response.get_json()['message']}")
            
            print("\n=== STEP 3: TEST DELETE API ===")
            
            if len(created_ids) >= 2:
                # Test deleting second equation
                delete_id = created_ids[1]
                print(f"\n--- Testing DELETE /api/equation/{delete_id} ---")
                
                response = client.delete(f'/api/equation/{delete_id}')
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"✅ DELETE SUCCESS: {data['message']}")
                    print(f"   Deleted: {data['deleted_equation']['equation_string']}")
                    print(f"   Solution was: {data['deleted_equation']['solution']}")
                else:
                    print(f"❌ DELETE FAILED: {response.get_json()}")
                
                # Verify deletion by trying to GET the deleted equation
                print(f"\n--- Verifying deletion: GET /api/equation/{delete_id} ---")
                response = client.get(f'/api/equation/{delete_id}')
                
                print(f"Status Code: {response.status_code}")
                if response.status_code == 404:
                    print(f"✅ DELETION VERIFIED: {response.get_json()['message']}")
                
                # Test deleting non-existent equation
                print(f"\n--- Testing DELETE /api/equation/999 (non-existent) ---")
                response = client.delete('/api/equation/999')
                
                print(f"Status Code: {response.status_code}")
                if response.status_code == 404:
                    print(f"✅ 404 SUCCESS: {response.get_json()['message']}")
            
            print("\n=== STEP 4: TEST BULK OPERATIONS ===")
            
            # Test bulk create
            print(f"\n--- Testing POST /api/equations/bulk ---")
            bulk_data = {
                'equations': [
                    {'a': 3, 'b': -12, 'c': 9},   # 3x² - 12x + 9 = 0
                    {'a': 0, 'b': 5, 'c': -10},   # 5x - 10 = 0
                    {'a': 1, 'b': 1, 'c': 1},     # x² + x + 1 = 0 (complex)
                ]
            }
            
            response = client.post('/api/equations/bulk',
                                 json=bulk_data,
                                 content_type='application/json')
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                data = response.get_json()
                print(f"✅ BULK CREATE SUCCESS: {data['message']}")
                print(f"   Created: {data['created_count']} equations")
                print(f"   Errors: {data['error_count']}")
                
                for eq in data['created_equations']:
                    print(f"   - ID {eq['id']}: {eq['equation_string']} → {eq['solution']}")
            else:
                print(f"❌ BULK CREATE FAILED: {response.get_json()}")
            
            print("\n=== STEP 5: TEST STATISTICS API ===")
            
            # Test stats
            print(f"\n--- Testing GET /api/equations/stats ---")
            response = client.get('/api/equations/stats')
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ STATS SUCCESS: {data['message']}")
                print(f"   Total equations: {data['stats']['total_equations']}")
                print(f"   By solution type: {data['stats']['by_solution_type']}")
                if data['stats']['latest_equation']:
                    print(f"   Latest: {data['stats']['latest_equation']['equation_string']}")
            else:
                print(f"❌ STATS FAILED: {response.get_json()}")
            
            print("\n=== STEP 6: FINAL VERIFICATION ===")
            
            # Get all remaining equations
            response = client.get('/api/equation')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ FINAL COUNT: {data['count']} equations remaining")
                
                for eq in data['data']:
                    print(f"   - ID {eq['id']}: {eq['equation_string']} → {eq['solution']}")
            else:
                print(f"❌ FINAL VERIFICATION FAILED: {response.get_json()}")

if __name__ == "__main__":
    test_complete_crud_operations()
    print("\n=== COMPLETE CRUD TESTING FINISHED ===")