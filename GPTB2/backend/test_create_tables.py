#!/usr/bin/env python3
"""
Test script để kiểm tra db.create_all() và model Equation
"""
import os
from dotenv import load_dotenv
from flask import Flask
from models import db, Equation

# Load environment variables
load_dotenv()

# Create Flask app for testing
app = Flask(__name__)

# Override DB_HOST for local testing (if needed)
# os.environ['DB_HOST'] = 'localhost'

DB_HOST = os.getenv('DB_HOST', 'mysql')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'gptb2_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'rootpassword')

# Configure SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

print("=== TESTING DB.CREATE_ALL() ===")
print(f"Database URL: mysql+pymysql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    with app.app_context():
        # Test db.create_all()
        print("Attempting to create tables...")
        db.create_all()
        print("✅ db.create_all() executed successfully")
        
        # Test model creation
        print("\nTesting Equation model:")
        test_equations = [
            Equation(a=1, b=-5, c=6),   # Two real roots
            Equation(a=1, b=-4, c=4),   # One repeated root  
            Equation(a=1, b=0, c=1),    # Complex roots
            Equation(a=0, b=2, c=-4),   # Linear equation
        ]
        
        for i, eq in enumerate(test_equations, 1):
            print(f"✅ Equation {i}: {eq}")
            print(f"   Solution: {eq.solution}")
            print(f"   Type: {eq.solution_type}")
            
        # Test database insertion (if connected)
        try:
            print("\nTesting database insertion...")
            sample_eq = Equation(a=2, b=-7, c=3)  # 2x² - 7x + 3 = 0
            db.session.add(sample_eq)
            db.session.commit()
            print(f"✅ Successfully inserted: {sample_eq}")
            
            # Query back
            retrieved = Equation.query.first()
            print(f"✅ Successfully retrieved: {retrieved}")
            
        except Exception as e:
            print(f"❌ Database insertion failed: {str(e)}")
            print("Note: This is expected if MySQL is not running")
            
except Exception as e:
    print(f"❌ db.create_all() failed: {str(e)}")
    print("Note: This is expected if MySQL is not running")

print("=================================")