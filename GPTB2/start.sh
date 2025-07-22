#!/bin/bash

# GPTB2 - Quick Start Script
# Chạy ứng dụng giải phương trình bậc 2 với 1 lệnh duy nhất

echo "🧮 GPTB2 - Ứng Dụng Giải Phương Trình Bậc 2"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker chưa được cài đặt!"
    echo "📥 Vui lòng cài đặt Docker từ: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose chưa được cài đặt!"
    echo "📥 Vui lòng cài đặt Docker Compose từ: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker đã được cài đặt"
echo "✅ Docker Compose đã sẵn sàng"
echo ""

# Check if ports are available
echo "🔍 Kiểm tra ports..."

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 3000 đang được sử dụng"
    echo "💡 Dừng process đang sử dụng port 3000 hoặc chạy: sudo kill -9 \$(lsof -t -i:3000)"
    read -p "Tiếp tục? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5000 đang được sử dụng"
    echo "💡 Dừng process đang sử dụng port 5000 hoặc chạy: sudo kill -9 \$(lsof -t -i:5000)"
    read -p "Tiếp tục? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Ports 3000 và 5000 sẵn sàng"
echo ""

# Start the application
echo "🚀 Đang khởi động ứng dụng GPTB2..."
echo "📦 Pulling và building Docker images..."
echo ""

# Use docker compose or docker-compose based on availability
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

# Start services
$DOCKER_COMPOSE_CMD up --build -d

# Check if services started successfully
echo ""
echo "⏳ Đang kiểm tra trạng thái services..."
sleep 10

# Check MySQL
if $DOCKER_COMPOSE_CMD ps mysql | grep -q "Up"; then
    echo "✅ MySQL Database: Running"
else
    echo "❌ MySQL Database: Failed to start"
    echo "📋 Logs:"
    $DOCKER_COMPOSE_CMD logs mysql
    exit 1
fi

# Check Backend
if $DOCKER_COMPOSE_CMD ps backend | grep -q "Up"; then
    echo "✅ Backend API: Running"
else
    echo "❌ Backend API: Failed to start"
    echo "📋 Logs:"
    $DOCKER_COMPOSE_CMD logs backend
    exit 1
fi

# Check Frontend
if $DOCKER_COMPOSE_CMD ps frontend | grep -q "Up"; then
    echo "✅ Frontend App: Running"
else
    echo "❌ Frontend App: Failed to start"
    echo "📋 Logs:"
    $DOCKER_COMPOSE_CMD logs frontend
    exit 1
fi

echo ""
echo "🎉 ỨNG DỤNG ĐÃ KHỞI ĐỘNG THÀNH CÔNG!"
echo "=============================================="
echo ""
echo "🌐 Truy cập ứng dụng:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:5000"
echo "   API Test:  http://localhost:5000/ping"
echo ""
echo "🧮 Cách sử dụng:"
echo "   1. Mở http://localhost:3000"
echo "   2. Nhập hệ số a, b, c"
echo "   3. Click 'Giải Phương Trình'"
echo "   4. Xem kết quả và lịch sử"
echo ""
echo "🛑 Để dừng ứng dụng:"
echo "   $DOCKER_COMPOSE_CMD down"
echo ""
echo "📋 Xem logs:"
echo "   $DOCKER_COMPOSE_CMD logs -f"
echo ""

# Test API endpoint
echo "🧪 Testing API..."
sleep 5

if curl -s http://localhost:5000/ping > /dev/null; then
    echo "✅ API Health Check: OK"
    
    # Test equation solving
    RESPONSE=$(curl -s -X POST http://localhost:5000/api/equation \
        -H "Content-Type: application/json" \
        -d '{"a": 1, "b": -3, "c": 2}' 2>/dev/null)
    
    if [[ $? -eq 0 ]] && [[ -n "$RESPONSE" ]]; then
        echo "✅ Equation Solving: OK"
        echo "📊 Test Result: $RESPONSE"
    else
        echo "⚠️  Equation API: Có thể chưa sẵn sàng (đang khởi động)"
    fi
else
    echo "⚠️  API Health Check: Có thể chưa sẵn sàng (đang khởi động)"
fi

echo ""
echo "🎯 ỨNG DỤNG SẴN SÀNG SỬ DỤNG!"
echo "🚀 Happy Coding! Enjoy solving quadratic equations! 🧮"

# Keep script running to show logs (optional)
read -p "Xem logs real-time? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📋 Showing logs (Ctrl+C để thoát)..."
    $DOCKER_COMPOSE_CMD logs -f
fi