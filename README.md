# 🧮 GPTB2 - Ứng Dụng Giải Phương Trình Bậc 2

**Ứng dụng web hoàn chỉnh để giải phương trình bậc 2 với React + Flask + MySQL + Docker**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?logo=flask)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com/)

---

## 🚀 **CHẠY NGAY BẰNG 1 LỆNH DUY NHẤT**

```bash
# Clone repository
git clone https://github.com/Hpt20255/PTB2.git
cd PTB2/GPTB2

# Chạy toàn bộ ứng dụng (MySQL + Backend + Frontend)
docker compose up
```

**🎉 Xong! Truy cập http://localhost:3000 để sử dụng ứng dụng**

---

## 📋 **TÍNH NĂNG CHÍNH**

### ✅ **Giải Phương Trình Bậc 2**
- Nhập hệ số a, b, c
- Tính nghiệm tự động (nghiệm thực, nghiệm phức, vô nghiệm)
- Hiển thị bước giải chi tiết
- Validation đầu vào thông minh

### ✅ **Quản Lý Lịch Sử**
- Lưu trữ tất cả phương trình đã giải
- Xem danh sách lịch sử dạng bảng
- Chỉnh sửa và tính lại nghiệm
- Xóa phương trình không cần thiết

### ✅ **Giao Diện Hiện Đại**
- React TypeScript với UI responsive
- Real-time validation và feedback
- Dark/Light theme support
- Mobile-friendly design

### ✅ **API RESTful Hoàn Chỉnh**
- POST /api/equation - Tạo và giải phương trình mới
- GET /api/equation - Lấy danh sách tất cả phương trình
- PUT /api/equation/{id} - Cập nhật phương trình
- DELETE /api/equation/{id} - Xóa phương trình

---

## 🏗️ **KIẾN TRÚC HỆ THỐNG**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   React + TS    │◄──►│   Flask + API   │◄──►│   MySQL 8.0     │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🐳 **Docker Containers:**
- **Frontend**: React app served by Nginx
- **Backend**: Flask API with SQLAlchemy ORM
- **Database**: MySQL 8.0 with persistent storage
- **Network**: Custom Docker network for service communication

---

## 📦 **YÊU CẦU HỆ THỐNG**

### **Chỉ cần Docker:**
- ✅ **Docker** (version 20.0+)
- ✅ **Docker Compose** (version 2.0+)

### **Không cần cài đặt:**
- ❌ Node.js
- ❌ Python
- ❌ MySQL
- ❌ Nginx

**Tất cả dependencies đã được đóng gói trong Docker containers!**

---

## 🎯 **HƯỚNG DẪN SỬ DỤNG**

### **1. Clone Repository**
```bash
git clone https://github.com/Hpt20255/PTB2.git
cd PTB2/GPTB2
```

### **2. Chạy Ứng Dụng**
```bash
# Chạy tất cả services
docker compose up

# Hoặc chạy trong background
docker compose up -d
```

### **3. Truy Cập Ứng Dụng**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/ping

### **4. Sử Dụng Ứng Dụng**
1. Nhập hệ số a, b, c vào form
2. Click "Giải Phương Trình"
3. Xem kết quả và bước giải
4. Phương trình được lưu tự động vào lịch sử
5. Quản lý lịch sử trong tab "Lịch Sử"

### **5. Dừng Ứng Dụng**
```bash
# Dừng containers
docker compose down

# Dừng và xóa volumes (xóa dữ liệu)
docker compose down -v
```

---

## 🧪 **TESTING & DEVELOPMENT**

### **Chạy Tests**
```bash
# Test toàn bộ hệ thống
python test_docker_compose.py

# Test debug mode
python test_debug_mode.py

# Test environment variables
python test_env_variables.py
```

### **Development Mode**
```bash
# Chạy với debug mode
DEBUG=true docker compose up

# Xem logs real-time
docker compose logs -f

# Rebuild containers
docker compose up --build
```

### **API Testing**
```bash
# Test API endpoints
curl -X GET http://localhost:5000/ping
curl -X POST http://localhost:5000/api/equation \
  -H "Content-Type: application/json" \
  -d '{"a": 1, "b": -3, "c": 2}'
```

---

## 📁 **CẤU TRÚC DỰ ÁN**

```
GPTB2/
├── 🐳 docker-compose.yaml          # Docker orchestration
├── 📄 .env                         # Environment variables
├── 📁 backend/                     # Flask API
│   ├── 🐍 app.py                   # Main Flask application
│   ├── 🗃️ models.py                # Database models
│   ├── 🐳 Dockerfile               # Backend container
│   ├── 📋 requirements.txt         # Python dependencies
│   └── 📄 .env                     # Backend environment
├── 📁 frontend/                    # React application
│   ├── 📁 src/                     # React source code
│   ├── 🐳 Dockerfile               # Frontend container
│   ├── 📦 package.json             # Node dependencies
│   └── 📄 .env                     # Frontend environment
├── 📁 mysql/                       # Database setup
│   └── 📁 init/                    # Database initialization
└── 📁 test_*.py                    # Testing suites
```

---

## 🔧 **CONFIGURATION**

### **Environment Variables**
```bash
# Database Configuration
DB_HOST=mysql
DB_PORT=3306
DB_NAME=gptb2_db
DB_USER=root
DB_PASSWORD=gptb2_secure_password_2024

# Application Configuration
DEBUG=true
PORT=5000
FRONTEND_PORT=3000

# Security
SECRET_KEY=gptb2-production-secret-key-change-in-production
```

### **Ports**
- **Frontend**: 3000
- **Backend**: 5000
- **MySQL**: 3306 (internal only)

### **Volumes**
- **MySQL Data**: Persistent storage for database
- **Backend Logs**: Application logs storage

---

## 🐛 **TROUBLESHOOTING**

### **Common Issues:**

#### **Port Already in Use**
```bash
# Check ports
netstat -tulpn | grep :3000
netstat -tulpn | grep :5000

# Kill processes
sudo kill -9 $(lsof -t -i:3000)
sudo kill -9 $(lsof -t -i:5000)
```

#### **Docker Issues**
```bash
# Restart Docker
sudo systemctl restart docker

# Clean Docker
docker system prune -a

# Rebuild containers
docker compose up --build --force-recreate
```

#### **Database Connection Issues**
```bash
# Check MySQL container
docker compose logs mysql

# Reset database
docker compose down -v
docker compose up
```

### **Debug Mode**
```bash
# Enable debug logging
DEBUG=true docker compose up

# Check container logs
docker compose logs backend
docker compose logs frontend
docker compose logs mysql
```

---

## 📚 **API DOCUMENTATION**

### **Endpoints:**

#### **Health Check**
```http
GET /ping
Response: {"message": "pong", "debug_mode": true}
```

#### **Create Equation**
```http
POST /api/equation
Content-Type: application/json

{
  "a": 1,
  "b": -3,
  "c": 2
}

Response: {
  "id": 1,
  "a": 1,
  "b": -3,
  "c": 2,
  "solution": "x1 = 2.0, x2 = 1.0"
}
```

#### **Get All Equations**
```http
GET /api/equation
Response: [
  {
    "id": 1,
    "a": 1,
    "b": -3,
    "c": 2,
    "solution": "x1 = 2.0, x2 = 1.0"
  }
]
```

#### **Update Equation**
```http
PUT /api/equation/1
Content-Type: application/json

{
  "a": 2,
  "b": -4,
  "c": 2
}
```

#### **Delete Equation**
```http
DELETE /api/equation/1
Response: {"message": "Equation deleted successfully"}
```

---

## 🤝 **CONTRIBUTING**

### **Development Setup**
```bash
# Clone repository
git clone https://github.com/Hpt20255/PTB2.git
cd PTB2/GPTB2

# Start development environment
docker compose up --build

# Make changes and test
python test_docker_compose.py
```

### **Code Style**
- **Backend**: Python PEP 8, Flask best practices
- **Frontend**: TypeScript, React hooks, ESLint
- **Docker**: Multi-stage builds, security best practices

---

## 📄 **LICENSE**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **AUTHOR**

**Hpt20255**
- GitHub: [@Hpt20255](https://github.com/Hpt20255)
- Repository: [PTB2](https://github.com/Hpt20255/PTB2)

---

## 🎉 **ACKNOWLEDGMENTS**

- React team for the amazing frontend framework
- Flask team for the lightweight Python web framework
- Docker team for containerization technology
- MySQL team for the reliable database system

---

**🚀 Happy Coding! Enjoy solving quadratic equations! 🧮**