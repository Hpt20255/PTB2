# 🧮 GPTB2 - Giải Phương Trình Bậc 2

**Ứng dụng web hoàn chỉnh để giải phương trình bậc 2 với React + Flask + MySQL + Docker**

---

## ⚡ **CHẠY NGAY - 1 LỆNH DUY NHẤT**

```bash
# Cách 1: Sử dụng script (Khuyến nghị)
./start.sh

# Cách 2: Docker Compose
docker compose up

# Cách 3: Background mode
docker compose up -d
```

**🎉 Truy cập: http://localhost:3000**

---

## 📋 **YÊU CẦU HỆ THỐNG**

### ✅ **Chỉ cần:**
- Docker (20.0+)
- Docker Compose (2.0+)

### ❌ **KHÔNG cần cài đặt:**
- Node.js, Python, MySQL, Nginx

---

## 🎯 **TÍNH NĂNG**

✅ **Giải phương trình bậc 2** (ax² + bx + c = 0)  
✅ **Hiển thị bước giải chi tiết**  
✅ **Lưu lịch sử phương trình**  
✅ **CRUD operations** (Tạo, Đọc, Sửa, Xóa)  
✅ **Responsive UI** với React TypeScript  
✅ **RESTful API** với Flask  
✅ **Database persistence** với MySQL  
✅ **Docker containerization**  

---

## 🏗️ **KIẾN TRÚC**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   React + TS    │◄──►│   Flask + API   │◄──►│   MySQL 8.0     │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📁 **CẤU TRÚC DỰ ÁN**

```
GPTB2/
├── 🚀 start.sh                     # Quick start script
├── 📖 QUICK_START.md               # Hướng dẫn nhanh
├── 📖 USAGE.md                     # Hướng dẫn chi tiết
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

## 🧮 **CÁCH SỬ DỤNG**

### **1. Khởi động ứng dụng:**
```bash
./start.sh
```

### **2. Giải phương trình:**
1. Mở http://localhost:3000
2. Nhập hệ số a, b, c
3. Click "Giải Phương Trình"
4. Xem kết quả và bước giải

### **3. Quản lý lịch sử:**
1. Click tab "Lịch Sử"
2. Xem, sửa, xóa phương trình

---

## 🔧 **API ENDPOINTS**

```bash
# Health check
GET /ping

# Tạo phương trình
POST /api/equation
{"a": 1, "b": -3, "c": 2}

# Lấy tất cả phương trình
GET /api/equation

# Cập nhật phương trình
PUT /api/equation/{id}

# Xóa phương trình
DELETE /api/equation/{id}
```

---

## 🧪 **TESTING**

```bash
# Test toàn bộ hệ thống
python test_docker_compose.py

# Test API
curl http://localhost:5000/ping

# Test giải phương trình
curl -X POST http://localhost:5000/api/equation \
  -H "Content-Type: application/json" \
  -d '{"a": 1, "b": -3, "c": 2}'
```

---

## 🛑 **DỪNG ỨNG DỤNG**

```bash
# Dừng containers
docker compose down

# Dừng và xóa dữ liệu
docker compose down -v
```

---

## 🐛 **TROUBLESHOOTING**

### **Port đã sử dụng:**
```bash
sudo kill -9 $(lsof -t -i:3000)
sudo kill -9 $(lsof -t -i:5000)
```

### **Docker issues:**
```bash
docker compose up --build
docker system prune -a
```

### **Xem logs:**
```bash
docker compose logs -f
```

---

## 📚 **TÀI LIỆU**

- **QUICK_START.md**: Hướng dẫn nhanh
- **USAGE.md**: Hướng dẫn chi tiết
- **backend/api_endpoints_summary.md**: API documentation
- **TASK_*_COMPLETION_REPORT.md**: Task reports

---

## 🎯 **VÍ DỤ SỬ DỤNG**

### **Hai nghiệm phân biệt:**
```
Input: a=1, b=-3, c=2
Output: x1 = 2.0, x2 = 1.0
```

### **Nghiệm kép:**
```
Input: a=1, b=-2, c=1
Output: x = 1.0 (nghiệm kép)
```

### **Vô nghiệm:**
```
Input: a=1, b=1, c=1
Output: Vô nghiệm thực
```

---

**🚀 Chỉ cần `./start.sh` và bạn đã có ứng dụng hoàn chỉnh! 🧮**