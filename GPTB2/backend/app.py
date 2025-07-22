import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

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

# Initialize SQLAlchemy
db = SQLAlchemy(app)

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

if __name__ == '__main__':
    # Test database connection on startup
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
    
    print("=====================================\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    )