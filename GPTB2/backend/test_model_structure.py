#!/usr/bin/env python3
"""
Test script để kiểm tra cấu trúc model và SQL generation
"""
import os
from dotenv import load_dotenv
from flask import Flask
from models import db, Equation
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Create Flask app for testing
app = Flask(__name__)

# Use SQLite for testing (không cần MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

print("=== TESTING MODEL STRUCTURE ===")

try:
    with app.app_context():
        # Create tables in SQLite
        db.create_all()
        print("✅ Tables created successfully in SQLite")
        
        # Check table structure
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✅ Tables created: {tables}")
        
        if 'equations' in tables:
            columns = inspector.get_columns('equations')
            print("✅ Equation table columns:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
        
        # Test model functionality
        print("\n=== TESTING MODEL FUNCTIONALITY ===")
        
        # Test different equation types
        test_cases = [
            {'a': 1, 'b': -5, 'c': 6, 'expected': 'two_real'},
            {'a': 1, 'b': -4, 'c': 4, 'expected': 'one_real'},
            {'a': 1, 'b': 0, 'c': 1, 'expected': 'complex'},
            {'a': 0, 'b': 2, 'c': -4, 'expected': 'linear'},
            {'a': 0, 'b': 0, 'c': 0, 'expected': 'infinite'},
            {'a': 0, 'b': 0, 'c': 5, 'expected': 'none'},
        ]
        
        for i, case in enumerate(test_cases, 1):
            eq = Equation(case['a'], case['b'], case['c'])
            print(f"✅ Test {i}: {eq.a}x² + {eq.b}x + {eq.c} = 0")
            print(f"   Solution: {eq.solution}")
            print(f"   Type: {eq.solution_type} (expected: {case['expected']})")
            print(f"   Discriminant: {eq.discriminant}")
            
            # Test database operations
            db.session.add(eq)
            db.session.commit()
            print(f"   ✅ Saved to database with ID: {eq.id}")
        
        # Test querying
        print(f"\n✅ Total equations in database: {Equation.query.count()}")
        
        # Test to_dict method
        first_eq = Equation.query.first()
        eq_dict = first_eq.to_dict()
        print(f"✅ to_dict() method works: {eq_dict['equation_string']}")
        
        print("\n=== MODEL STRUCTURE TEST COMPLETED ===")
        
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("=================================")