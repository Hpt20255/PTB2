# 📖 HƯỚNG DẪN SỬ DỤNG - GPTB2

**Hướng dẫn chi tiết cách sử dụng ứng dụng giải phương trình bậc 2**

---

## 🚀 **KHỞI ĐỘNG ỨNG DỤNG**

### **Cách 1: Sử dụng Script (Khuyến nghị)**
```bash
# Chạy script tự động
./start.sh
```

### **Cách 2: Docker Compose**
```bash
# Chạy manual
docker compose up

# Hoặc chạy background
docker compose up -d
```

### **Cách 3: Step by Step**
```bash
# 1. Clone repository
git clone https://github.com/Hpt20255/PTB2.git
cd PTB2/GPTB2

# 2. Start services
docker compose up --build

# 3. Truy cập http://localhost:3000
```

---

## 🌐 **TRUY CẬP ỨNG DỤNG**

### **URLs:**
- **🎨 Frontend**: http://localhost:3000
- **🔧 Backend API**: http://localhost:5000
- **💓 Health Check**: http://localhost:5000/ping

### **Kiểm tra hoạt động:**
```bash
# Test API
curl http://localhost:5000/ping

# Test giải phương trình
curl -X POST http://localhost:5000/api/equation \
  -H "Content-Type: application/json" \
  -d '{"a": 1, "b": -3, "c": 2}'
```

---

## 🧮 **SỬ DỤNG GIAO DIỆN WEB**

### **1. Giải Phương Trình Mới**

#### **Bước 1: Nhập hệ số**
- Mở http://localhost:3000
- Nhập hệ số **a** (khác 0)
- Nhập hệ số **b**
- Nhập hệ số **c**

#### **Bước 2: Giải phương trình**
- Click nút **"Giải Phương Trình"**
- Xem kết quả hiển thị ngay lập tức

#### **Bước 3: Xem bước giải**
- Kết quả hiển thị đầy đủ:
  - Phương trình dạng chuẩn
  - Discriminant (Δ)
  - Loại nghiệm
  - Nghiệm cụ thể

### **2. Quản Lý Lịch Sử**

#### **Xem lịch sử:**
- Click tab **"Lịch Sử"**
- Xem danh sách tất cả phương trình đã giải
- Thông tin hiển thị: ID, a, b, c, nghiệm

#### **Chỉnh sửa phương trình:**
- Click nút **"Sửa"** trên dòng muốn chỉnh sửa
- Thay đổi hệ số a, b, c
- Click **"Cập nhật"** để tính lại nghiệm

#### **Xóa phương trình:**
- Click nút **"Xóa"** trên dòng muốn xóa
- Xác nhận xóa trong dialog

---

## 🔧 **SỬ DỤNG API**

### **1. Health Check**
```bash
GET /ping

# Response:
{
  "message": "pong",
  "debug_mode": true,
  "debug_info": {
    "timestamp": "2024-07-22T23:30:00",
    "environment": "development"
  }
}
```

### **2. Tạo và Giải Phương Trình**
```bash
POST /api/equation
Content-Type: application/json

{
  "a": 1,
  "b": -3,
  "c": 2
}

# Response:
{
  "id": 1,
  "a": 1.0,
  "b": -3.0,
  "c": 2.0,
  "solution": "x1 = 2.0, x2 = 1.0"
}
```

### **3. Lấy Tất Cả Phương Trình**
```bash
GET /api/equation

# Response:
[
  {
    "id": 1,
    "a": 1.0,
    "b": -3.0,
    "c": 2.0,
    "solution": "x1 = 2.0, x2 = 1.0"
  },
  {
    "id": 2,
    "a": 1.0,
    "b": 0.0,
    "c": -4.0,
    "solution": "x1 = 2.0, x2 = -2.0"
  }
]
```

### **4. Cập Nhật Phương Trình**
```bash
PUT /api/equation/1
Content-Type: application/json

{
  "a": 2,
  "b": -4,
  "c": 2
}

# Response:
{
  "id": 1,
  "a": 2.0,
  "b": -4.0,
  "c": 2.0,
  "solution": "x = 1.0 (nghiệm kép)"
}
```

### **5. Xóa Phương Trình**
```bash
DELETE /api/equation/1

# Response:
{
  "message": "Equation deleted successfully"
}
```

---

## 📊 **CÁC LOẠI NGHIỆM**

### **1. Hai nghiệm phân biệt (Δ > 0)**
```
Phương trình: x² - 3x + 2 = 0
Δ = 9 - 8 = 1 > 0
Nghiệm: x1 = 2.0, x2 = 1.0
```

### **2. Nghiệm kép (Δ = 0)**
```
Phương trình: x² - 2x + 1 = 0
Δ = 4 - 4 = 0
Nghiệm: x = 1.0 (nghiệm kép)
```

### **3. Vô nghiệm thực (Δ < 0)**
```
Phương trình: x² + x + 1 = 0
Δ = 1 - 4 = -3 < 0
Nghiệm: Vô nghiệm thực
```

### **4. Phương trình bậc nhất (a = 0)**
```
Phương trình: 0x² + 2x + 1 = 0 → 2x + 1 = 0
Nghiệm: x = -0.5
```

---

## 🎨 **TÍNH NĂNG GIAO DIỆN**

### **Responsive Design:**
- ✅ Desktop: Layout 2 cột
- ✅ Tablet: Layout responsive
- ✅ Mobile: Layout 1 cột

### **Real-time Validation:**
- ✅ Kiểm tra a ≠ 0
- ✅ Kiểm tra định dạng số
- ✅ Hiển thị lỗi ngay lập tức

### **Debug Mode:**
- ✅ Banner debug khi DEBUG=true
- ✅ Console logging
- ✅ Enhanced error messages

### **User Experience:**
- ✅ Loading states
- ✅ Success/Error notifications
- ✅ Smooth animations
- ✅ Intuitive navigation

---

## 🧪 **TESTING**

### **Frontend Testing:**
```bash
# Mở browser developer tools
# Console sẽ hiển thị debug logs khi DEBUG=true

# Test cases:
1. a=1, b=-3, c=2 → x1=2.0, x2=1.0
2. a=1, b=-2, c=1 → x=1.0 (nghiệm kép)
3. a=1, b=1, c=1 → Vô nghiệm thực
4. a=0, b=2, c=1 → x=-0.5 (bậc nhất)
```

### **API Testing:**
```bash
# Test với curl
curl -X POST http://localhost:5000/api/equation \
  -H "Content-Type: application/json" \
  -d '{"a": 1, "b": -3, "c": 2}'

# Test với Postman
# Import collection từ backend/api_endpoints_summary.md
```

### **Database Testing:**
```bash
# Kiểm tra MySQL container
docker compose exec mysql mysql -u root -p gptb2_db

# Xem dữ liệu
SELECT * FROM equation;
```

---

## 🛑 **DỪNG ỨNG DỤNG**

### **Dừng containers:**
```bash
# Dừng nhưng giữ dữ liệu
docker compose down

# Dừng và xóa volumes (xóa dữ liệu)
docker compose down -v

# Dừng và xóa images
docker compose down --rmi all
```

### **Clean up:**
```bash
# Xóa tất cả containers, networks, volumes
docker system prune -a

# Xóa chỉ volumes
docker volume prune
```

---

## 🐛 **TROUBLESHOOTING**

### **Lỗi thường gặp:**

#### **Port đã sử dụng:**
```bash
# Kiểm tra process sử dụng port
lsof -i :3000
lsof -i :5000

# Kill process
sudo kill -9 $(lsof -t -i:3000)
sudo kill -9 $(lsof -t -i:5000)
```

#### **Docker issues:**
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Rebuild containers
docker compose up --build --force-recreate

# Check container status
docker compose ps
docker compose logs
```

#### **Database connection:**
```bash
# Check MySQL logs
docker compose logs mysql

# Reset database
docker compose down -v
docker compose up
```

#### **Frontend không load:**
```bash
# Check frontend logs
docker compose logs frontend

# Rebuild frontend
docker compose up --build frontend
```

#### **API không response:**
```bash
# Check backend logs
docker compose logs backend

# Test API directly
curl http://localhost:5000/ping
```

---

## 📋 **LOGS & MONITORING**

### **Xem logs:**
```bash
# Tất cả services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs frontend
docker compose logs mysql

# Follow logs real-time
docker compose logs -f

# Logs với timestamp
docker compose logs -t
```

### **Monitor resources:**
```bash
# Container stats
docker stats

# Disk usage
docker system df

# Network info
docker network ls
docker network inspect gptb2_gptb2-network
```

---

## 🔧 **DEVELOPMENT MODE**

### **Enable debug:**
```bash
# Set debug mode
DEBUG=true docker compose up

# Check debug features:
# - Frontend: Debug banner hiển thị
# - Backend: Enhanced logging
# - API: Debug info trong response
```

### **Hot reload:**
```bash
# Frontend: Automatic reload khi code thay đổi
# Backend: Restart container để reload code

# Rebuild specific service
docker compose up --build backend
docker compose up --build frontend
```

---

## 📚 **TÀI LIỆU THAM KHẢO**

- **README.md**: Tổng quan dự án
- **QUICK_START.md**: Hướng dẫn nhanh
- **API Documentation**: backend/api_endpoints_summary.md
- **Task Reports**: TASK_*_COMPLETION_REPORT.md
- **Environment Guide**: ENVIRONMENT.md

---

**🎯 Chúc bạn sử dụng ứng dụng hiệu quả! 🧮**