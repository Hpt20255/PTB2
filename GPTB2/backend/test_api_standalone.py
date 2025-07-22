#!/usr/bin/env python3
"""
Standalone test cho API POST /api/equation với SQLite
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
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
    
    # Enable CORS
    CORS(app)
    
    @app.route('/api/equation', methods=['POST'])
    def create_equation():
        """Create new equation and solve it"""
        try:
            if not request.is_json:
                return jsonify({
                    'message': 'Content-Type must be application/json',
                    'status': 'error'
                }), 400
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['a', 'b', 'c']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    'message': f'Missing required fields: {", ".join(missing_fields)}',
                    'status': 'error',
                    'required_fields': required_fields
                }), 400
            
            # Validate field types and convert to float
            try:
                a = float(data['a'])
                b = float(data['b'])
                c = float(data['c'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'message': 'Coefficients a, b, c must be valid numbers',
                    'status': 'error',
                    'error': str(e)
                }), 400
            
            # Create and solve equation
            equation = Equation(a=a, b=b, c=c)
            
            # Save to database
            try:
                db.session.add(equation)
                db.session.commit()
                
                return jsonify({
                    'message': 'Equation created and solved successfully',
                    'status': 'success',
                    'data': equation.to_dict()
                }), 201
                
            except Exception as db_error:
                db.session.rollback()
                return jsonify({
                    'message': 'Equation solved but database save failed',
                    'status': 'partial_success',
                    'data': equation.to_dict(),
                    'database_error': str(db_error)
                }), 200
                
        except Exception as e:
            return jsonify({
                'message': 'Failed to create equation',
                'status': 'error',
                'error': str(e)
            }), 500
    
    @app.route('/api/equation', methods=['GET'])
    def get_all_equations():
        """Get all equations from database"""
        try:
            equations = Equation.query.order_by(Equation.created_at.desc()).all()
            
            return jsonify({
                'message': f'Retrieved {len(equations)} equations',
                'status': 'success',
                'count': len(equations),
                'data': [eq.to_dict() for eq in equations]
            })
            
        except Exception as e:
            return jsonify({
                'message': 'Failed to retrieve equations',
                'status': 'error',
                'error': str(e)
            }), 500
    
    @app.route('/api/equation/<int:equation_id>', methods=['GET'])
    def get_equation(equation_id):
        """Get specific equation by ID"""
        try:
            equation = Equation.query.get(equation_id)
            
            if not equation:
                return jsonify({
                    'message': f'Equation with ID {equation_id} not found',
                    'status': 'error'
                }), 404
            
            return jsonify({
                'message': 'Equation retrieved successfully',
                'status': 'success',
                'data': equation.to_dict()
            })
            
        except Exception as e:
            return jsonify({
                'message': 'Failed to retrieve equation',
                'status': 'error',
                'error': str(e)
            }), 500
    
    return app

def test_api_complete():
    """Test all API functionality"""
    app = create_test_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Create tables
            db.create_all()
            print("✅ SQLite database and tables created")
            
            print("\n=== TESTING POST /api/equation ===")
            
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
                    print(f"   Type: {data['data']['solution_type']}")
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
            
            # Test 404
            response = client.get('/api/equation/999')
            print(f"Not found - Status: {response.status_code}")
            if response.status_code == 404:
                print(f"✅ 404 SUCCESS: {response.get_json()['message']}")
            
            print(f"\n=== DATABASE VERIFICATION ===")
            # Verify database directly
            equations = Equation.query.all()
            print(f"✅ Total equations in database: {len(equations)}")
            
            for eq in equations:
                print(f"   - {eq}")

if __name__ == "__main__":
    test_api_complete()
    print("\n=== COMPLETE API TESTING FINISHED ===")