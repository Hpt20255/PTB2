# ⚡ QUICK START - GPTB2

**Chạy ứng dụng giải phương trình bậc 2 chỉ với 1 lệnh!**

---

## 🚀 **CHẠY NGAY - 1 LỆNH DUY NHẤT**

```bash
docker compose up
```

**🎉 Xong! Truy cập http://localhost:3000**

---

## 📋 **ĐIỀU KIỆN TIÊN QUYẾT**

### ✅ **Chỉ cần Docker:**
- Docker (version 20.0+)
- Docker Compose (version 2.0+)

### ❌ **KHÔNG cần cài đặt:**
- Node.js
- Python
- MySQL
- Nginx

---

## 🎯 **HƯỚNG DẪN CHI TIẾT**

### **Bước 1: Clone Repository**
```bash
git clone https://github.com/Hpt20255/PTB2.git
cd PTB2/GPTB2
```

### **Bước 2: Chạy Ứng Dụng**
```bash
# Chạy tất cả services (MySQL + Backend + Frontend)
docker compose up

# Hoặc chạy trong background
docker compose up -d
```

### **Bước 3: Sử Dụng**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/ping

---

## 🧮 **CÁCH SỬ DỤNG ỨNG DỤNG**

### **1. Giải Phương Trình**
1. Mở http://localhost:3000
2. Nhập hệ số a, b, c
3. Click "Giải Phương Trình"
4. Xem kết quả và bước giải

### **2. Quản Lý Lịch Sử**
1. Click tab "Lịch Sử"
2. Xem tất cả phương trình đã giải
3. Chỉnh sửa hoặc xóa phương trình

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

### **Lỗi Port đã sử dụng:**
```bash
# Kill processes sử dụng port 3000 và 5000
sudo kill -9 $(lsof -t -i:3000)
sudo kill -9 $(lsof -t -i:5000)
```

### **Lỗi Docker:**
```bash
# Restart Docker
sudo systemctl restart docker

# Rebuild containers
docker compose up --build
```

### **Xem logs:**
```bash
# Xem logs tất cả services
docker compose logs

# Xem logs specific service
docker compose logs backend
docker compose logs frontend
docker compose logs mysql
```

---

## 📊 **KIỂM TRA HOẠT ĐỘNG**

### **Test API:**
```bash
# Health check
curl http://localhost:5000/ping

# Test giải phương trình
curl -X POST http://localhost:5000/api/equation \
  -H "Content-Type: application/json" \
  -d '{"a": 1, "b": -3, "c": 2}'
```

### **Test Frontend:**
- Truy cập http://localhost:3000
- Nhập a=1, b=-3, c=2
- Kết quả: x1 = 2.0, x2 = 1.0

---

## 🎯 **TÍNH NĂNG CHÍNH**

✅ **Giải phương trình bậc 2** (ax² + bx + c = 0)  
✅ **Hiển thị bước giải chi tiết**  
✅ **Lưu lịch sử phương trình**  
✅ **CRUD operations** (Create, Read, Update, Delete)  
✅ **Responsive UI** với React TypeScript  
✅ **RESTful API** với Flask  
✅ **Database persistence** với MySQL  

---

## 🏗️ **KIẾN TRÚC**

```
Frontend (React) ←→ Backend (Flask) ←→ Database (MySQL)
    Port 3000           Port 5000          Port 3306
```

---

**🚀 Chỉ cần `docker compose up` và bạn đã có ứng dụng hoàn chỉnh!**