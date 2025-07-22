#!/usr/bin/env python3
"""
Test script để kiểm tra SQLAlchemy configuration với localhost MySQL
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Override DB_HOST for local testing
os.environ['DB_HOST'] = 'localhost'

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'gptb2_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'rootpassword')

print("=== TESTING SQLALCHEMY CONNECTION ===")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")

# Create SQLAlchemy engine
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"DATABASE_URL: mysql+pymysql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(DATABASE_URL)
    print("\n✅ SQLAlchemy engine created successfully")
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'SQLAlchemy connection successful!' as message"))
        message = result.fetchone()[0]
        print(f"✅ {message}")
        
        # Test basic query
        result = connection.execute(text("SELECT VERSION() as version"))
        version = result.fetchone()[0]
        print(f"✅ MySQL Version: {version}")
        
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    print("Note: This is expected if MySQL is not installed/running locally")

print("=====================================")