import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Equation

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'gptb2_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'rootpassword')

# Print database configuration for testing
print("=== DATABASE CONFIGURATION ===")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {'*' * len(DB_PASSWORD) if DB_PASSWORD else 'None'}")
print("================================")

# Configure SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize SQLAlchemy with app
db.init_app(app)

@app.route('/ping', methods=['GET'])
def ping():
    """Basic health check endpoint"""
    return jsonify({
        'message': 'pong',
        'status': 'success',
        'database_configured': True
    })

@app.route('/test-db', methods=['GET'])
def test_database_connection():
    """Test database connection endpoint"""
    try:
        # Test database connection
        with db.engine.connect() as connection:
            result = connection.execute(db.text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
        return jsonify({
            'message': 'Database connection successful',
            'status': 'success',
            'test_query_result': test_value,
            'database_url': f"mysql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        })
    except Exception as e:
        return jsonify({
            'message': 'Database connection failed',
            'status': 'error',
            'error': str(e),
            'database_url': f"mysql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        }), 500

@app.route('/create-tables', methods=['POST'])
def create_tables():
    """Create all database tables"""
    try:
        with app.app_context():
            db.create_all()
            
            # Test creating a sample equation
            sample_equation = Equation(a=1, b=-5, c=6)  # x² - 5x + 6 = 0
            
            return jsonify({
                'message': 'Database tables created successfully',
                'status': 'success',
                'sample_equation': {
                    'equation': f"{sample_equation.a}x² + {sample_equation.b}x + {sample_equation.c} = 0",
                    'solution': sample_equation.solution,
                    'solution_type': sample_equation.solution_type,
                    'discriminant': sample_equation.discriminant
                },
                'tables_created': ['equations']
            })
    except Exception as e:
        return jsonify({
            'message': 'Failed to create database tables',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/test-equation', methods=['GET'])
def test_equation_model():
    """Test Equation model functionality"""
    try:
        # Test different types of equations
        test_cases = [
            {'a': 1, 'b': -5, 'c': 6, 'description': 'Two real roots'},      # (x-2)(x-3) = 0
            {'a': 1, 'b': -4, 'c': 4, 'description': 'One repeated root'},   # (x-2)² = 0  
            {'a': 1, 'b': 0, 'c': 1, 'description': 'Complex roots'},        # x² + 1 = 0
            {'a': 0, 'b': 2, 'c': -4, 'description': 'Linear equation'},     # 2x - 4 = 0
        ]
        
        results = []
        for case in test_cases:
            eq = Equation(case['a'], case['b'], case['c'])
            results.append({
                'description': case['description'],
                'equation': f"{eq.a}x² + {eq.b}x + {eq.c} = 0",
                'solution': eq.solution,
                'solution_type': eq.solution_type,
                'discriminant': eq.discriminant
            })
        
        return jsonify({
            'message': 'Equation model test completed',
            'status': 'success',
            'test_results': results
        })
    except Exception as e:
        return jsonify({
            'message': 'Equation model test failed',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/equation', methods=['POST'])
def create_equation():
    """
    Create new equation and solve it
    Expected JSON: {"a": float, "b": float, "c": float}
    """
    try:
        # Validate request content type
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
            # Return equation data even if database save fails
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

@app.route('/api/equation/<int:equation_id>', methods=['PUT'])
def update_equation(equation_id):
    """
    Update existing equation with new coefficients and re-solve
    Expected JSON: {"a": float, "b": float, "c": float}
    """
    try:
        # Find existing equation
        equation = Equation.query.get(equation_id)
        
        if not equation:
            return jsonify({
                'message': f'Equation with ID {equation_id} not found',
                'status': 'error'
            }), 404
        
        # Validate request content type
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
            new_a = float(data['a'])
            new_b = float(data['b'])
            new_c = float(data['c'])
        except (ValueError, TypeError) as e:
            return jsonify({
                'message': 'Coefficients a, b, c must be valid numbers',
                'status': 'error',
                'error': str(e)
            }), 400
        
        # Store old values for response
        old_values = {
            'a': equation.a,
            'b': equation.b,
            'c': equation.c,
            'solution': equation.solution,
            'solution_type': equation.solution_type
        }
        
        # Update coefficients and re-solve
        equation.a = new_a
        equation.b = new_b
        equation.c = new_c
        equation.solve_equation()  # Re-calculate solution
        
        # Save to database
        try:
            db.session.commit()
            
            return jsonify({
                'message': 'Equation updated and re-solved successfully',
                'status': 'success',
                'data': equation.to_dict(),
                'previous_values': {
                    'equation_string': f"{old_values['a']}x² + {old_values['b']}x + {old_values['c']} = 0",
                    'solution': old_values['solution'],
                    'solution_type': old_values['solution_type']
                }
            }), 200
            
        except Exception as db_error:
            db.session.rollback()
            return jsonify({
                'message': 'Equation updated but database save failed',
                'status': 'partial_success',
                'data': equation.to_dict(),
                'database_error': str(db_error)
            }), 200
            
    except Exception as e:
        return jsonify({
            'message': 'Failed to update equation',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/equation/<int:equation_id>', methods=['DELETE'])
def delete_equation(equation_id):
    """Delete equation by ID"""
    try:
        # Find existing equation
        equation = Equation.query.get(equation_id)
        
        if not equation:
            return jsonify({
                'message': f'Equation with ID {equation_id} not found',
                'status': 'error'
            }), 404
        
        # Store equation data for response before deletion
        equation_data = equation.to_dict()
        
        # Delete from database
        try:
            db.session.delete(equation)
            db.session.commit()
            
            return jsonify({
                'message': f'Equation with ID {equation_id} deleted successfully',
                'status': 'success',
                'deleted_equation': equation_data
            }), 200
            
        except Exception as db_error:
            db.session.rollback()
            return jsonify({
                'message': 'Failed to delete equation from database',
                'status': 'error',
                'error': str(db_error)
            }), 500
            
    except Exception as e:
        return jsonify({
            'message': 'Failed to delete equation',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/equations/bulk', methods=['POST'])
def create_bulk_equations():
    """
    Create multiple equations at once
    Expected JSON: {"equations": [{"a": float, "b": float, "c": float}, ...]}
    """
    try:
        if not request.is_json:
            return jsonify({
                'message': 'Content-Type must be application/json',
                'status': 'error'
            }), 400
        
        data = request.get_json()
        
        if 'equations' not in data or not isinstance(data['equations'], list):
            return jsonify({
                'message': 'Request must contain "equations" array',
                'status': 'error'
            }), 400
        
        if len(data['equations']) == 0:
            return jsonify({
                'message': 'Equations array cannot be empty',
                'status': 'error'
            }), 400
        
        if len(data['equations']) > 50:  # Limit bulk operations
            return jsonify({
                'message': 'Maximum 50 equations allowed per bulk operation',
                'status': 'error'
            }), 400
        
        created_equations = []
        errors = []
        
        for i, eq_data in enumerate(data['equations']):
            try:
                # Validate each equation
                required_fields = ['a', 'b', 'c']
                missing_fields = [field for field in required_fields if field not in eq_data]
                
                if missing_fields:
                    errors.append({
                        'index': i,
                        'error': f'Missing required fields: {", ".join(missing_fields)}'
                    })
                    continue
                
                # Convert to float
                a = float(eq_data['a'])
                b = float(eq_data['b'])
                c = float(eq_data['c'])
                
                # Create equation
                equation = Equation(a=a, b=b, c=c)
                db.session.add(equation)
                created_equations.append(equation)
                
            except (ValueError, TypeError) as e:
                errors.append({
                    'index': i,
                    'error': f'Invalid coefficients: {str(e)}'
                })
            except Exception as e:
                errors.append({
                    'index': i,
                    'error': str(e)
                })
        
        # Commit all valid equations
        try:
            if created_equations:
                db.session.commit()
                
            return jsonify({
                'message': f'Bulk operation completed: {len(created_equations)} created, {len(errors)} errors',
                'status': 'success' if len(errors) == 0 else 'partial_success',
                'created_count': len(created_equations),
                'error_count': len(errors),
                'created_equations': [eq.to_dict() for eq in created_equations],
                'errors': errors
            }), 201 if len(errors) == 0 else 200
            
        except Exception as db_error:
            db.session.rollback()
            return jsonify({
                'message': 'Bulk operation failed during database save',
                'status': 'error',
                'error': str(db_error)
            }), 500
            
    except Exception as e:
        return jsonify({
            'message': 'Bulk operation failed',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/equations/stats', methods=['GET'])
def get_equation_stats():
    """Get statistics about equations in database"""
    try:
        total_count = Equation.query.count()
        
        if total_count == 0:
            return jsonify({
                'message': 'No equations found in database',
                'status': 'success',
                'stats': {
                    'total_equations': 0,
                    'by_solution_type': {},
                    'latest_equation': None
                }
            })
        
        # Count by solution type
        from sqlalchemy import func
        solution_type_counts = db.session.query(
            Equation.solution_type,
            func.count(Equation.id)
        ).group_by(Equation.solution_type).all()
        
        by_solution_type = {solution_type: count for solution_type, count in solution_type_counts}
        
        # Get latest equation
        latest_equation = Equation.query.order_by(Equation.created_at.desc()).first()
        
        return jsonify({
            'message': f'Retrieved statistics for {total_count} equations',
            'status': 'success',
            'stats': {
                'total_equations': total_count,
                'by_solution_type': by_solution_type,
                'latest_equation': latest_equation.to_dict() if latest_equation else None
            }
        })
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve equation statistics',
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Test database connection and model on startup
    print("\n=== TESTING DATABASE CONNECTION ===")
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 'Database connection successful!' as message"))
                message = result.fetchone()[0]
                print(f"✅ SUCCESS: {message}")
    except Exception as e:
        print(f"❌ ERROR: Database connection failed - {str(e)}")
        print("Note: This is expected if MySQL is not running yet")
    
    print("\n=== TESTING EQUATION MODEL ===")
    try:
        with app.app_context():
            # Test equation model without database
            test_eq = Equation(a=1, b=-5, c=6)  # x² - 5x + 6 = 0
            print(f"✅ Model created: {test_eq}")
            print(f"✅ Solution: {test_eq.solution}")
            print(f"✅ Solution type: {test_eq.solution_type}")
            print(f"✅ Discriminant: {test_eq.discriminant}")
    except Exception as e:
        print(f"❌ ERROR: Model test failed - {str(e)}")
    
    print("=====================================\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    )