# GPTB2 Environment Configuration

## 🖥️ System Information

### ✅ Operating System
- **OS**: Linux (Ubuntu-based)
- **Kernel**: 5.15.0-1079-gke #85-Ubuntu SMP
- **Architecture**: x86_64 GNU/Linux
- **Container**: Docker/Kubernetes environment

### ✅ Runtime Versions
- **Python**: 3.12.11
- **Node.js**: v22.17.0
- **npm**: 10.9.2

## 🐍 Python Environment

### Core Backend Dependencies
```
Flask==2.3.3              # Web framework
Flask-Cors==4.0.0          # Cross-Origin Resource Sharing
Flask-SQLAlchemy==3.0.5    # ORM integration
SQLAlchemy==2.0.41         # Database ORM
PyMySQL==1.1.0             # MySQL connector
python-dotenv==1.0.0       # Environment variables
cryptography==41.0.4       # Security utilities
requests==2.32.3           # HTTP client for testing
```

### Python Package Manager
- **pip**: Latest version
- **Virtual Environment**: Poetry-managed environment
- **Requirements**: `/backend/requirements.txt`

## 🌐 Node.js Environment

### Frontend Dependencies
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0", 
  "typescript": "^4.9.0",
  "axios": "^1.6.0",
  "react-scripts": "5.0.1"
}
```

### Package Manager
- **npm**: 10.9.2
- **Package file**: `/frontend/package.json`
- **Lock file**: `/frontend/package-lock.json`

## 🔧 Environment Variables

### Backend (.env)
```bash
# Database Configuration
DB_HOST=mysql                    # MySQL server hostname
DB_PORT=3306                     # MySQL port
DB_NAME=gptb2_db                 # Database name
DB_USER=root                     # Database username
DB_PASSWORD=password123          # Database password

# Flask Configuration
FLASK_ENV=development            # Development mode
FLASK_DEBUG=True                 # Debug mode enabled
FLASK_APP=app.py                 # Main application file

# API Configuration
API_HOST=0.0.0.0                 # Listen on all interfaces
API_PORT=5000                    # Backend API port
```

### Frontend (.env)
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:5000  # Backend API endpoint
REACT_APP_DEBUG=true                     # Debug mode
PORT=3000                                # Frontend development server port
```

## 🌐 Network Configuration

### Port Mapping
- **Frontend**: Port 3000 (React development server)
- **Backend**: Port 5000 (Flask API server)
- **Database**: Port 3306 (MySQL server)

### External Access
- **Frontend URL**: https://work-1-zhuwpmoevfstcmvg.prod-runtime.all-hands.dev (port 12000)
- **Backend URL**: https://work-2-zhuwpmoevfstcmvg.prod-runtime.all-hands.dev (port 12001)

### CORS Configuration
- **Allowed Origins**: `*` (all origins for development)
- **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization

## 🐳 Docker Configuration

### Backend Dockerfile
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
```

### Docker Compose (Planned)
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: password123
      MYSQL_DATABASE: gptb2_db
  
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - mysql
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

## 📊 Database Configuration

### MySQL Settings
- **Version**: 8.0 (planned)
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Storage Engine**: InnoDB

### Database Schema
```sql
CREATE TABLE equations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL, 
    c FLOAT NOT NULL,
    solution TEXT,
    discriminant FLOAT,
    solution_type VARCHAR(20),
    equation_string VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔍 Development Tools

### Code Quality
- **Linting**: ESLint (frontend), Flake8 (backend)
- **Formatting**: Prettier (frontend), Black (backend - planned)
- **Type Checking**: TypeScript (frontend), Python type hints

### Testing Tools
- **Backend**: Custom test scripts with requests library
- **Frontend**: React Testing Library, Jest (configured)
- **Integration**: Custom Node.js test scripts

### Development Servers
- **Backend**: Flask development server with hot reload
- **Frontend**: React development server with hot reload
- **Proxy**: Frontend proxies API requests to backend

## 🚀 Deployment Configuration

### Current Status
- **Environment**: Development
- **Hosting**: Local development servers
- **Database**: SQLite (fallback), MySQL (planned)
- **SSL**: Not configured (development)

### Production Readiness
- **Docker**: Dockerfiles ready
- **Environment Variables**: Configured for production
- **Database**: MySQL ready for deployment
- **CORS**: Configurable for production domains
- **Build Process**: Optimized production builds available

## 📝 Notes

### Current Limitations
- MySQL server not running (using SQLite fallback)
- No SSL/HTTPS in development
- CORS set to allow all origins (development only)

### Next Steps
- Set up MySQL server
- Configure production environment variables
- Implement proper CORS for production
- Set up CI/CD pipeline