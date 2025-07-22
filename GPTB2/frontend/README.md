# GPTB2 Frontend - React TypeScript

## 🎯 Task 2.1: Form nhập hệ số a, b, c

### ✅ Hoàn thành
- ✅ React app với TypeScript
- ✅ Form nhập hệ số a, b, c
- ✅ Validation đầy đủ (required fields, data types)
- ✅ API integration với Flask backend
- ✅ Hiển thị kết quả phương trình
- ✅ Error handling và notifications
- ✅ Responsive design với gradient background

## 🚀 Features

### 📝 Form Input
- **Hệ số a (x²)**: Input với validation số
- **Hệ số b (x)**: Input với validation số  
- **Hệ số c (hằng số)**: Input với validation số
- **Submit button**: Gọi API POST với loading state
- **Clear button**: Reset form

### 🔒 Validation
- **Required fields**: Tất cả hệ số bắt buộc
- **Data type**: Chỉ chấp nhận số (int/float)
- **Real-time validation**: Hiển thị lỗi ngay khi nhập
- **Form submission**: Validate trước khi gọi API

### 🌐 API Integration
- **Axios client**: HTTP requests với interceptors
- **Error handling**: Network errors, API errors
- **Loading states**: Visual feedback khi gọi API
- **Response processing**: Parse và hiển thị kết quả

### 🎨 UI/UX
- **Modern design**: Gradient background, glass morphism
- **Responsive**: Mobile-friendly layout
- **Notifications**: Success/error messages với auto-dismiss
- **Real-time feedback**: API status, equation history

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   └── EquationForm.tsx # Main form component
│   ├── services/
│   │   └── api.ts          # API service layer
│   ├── types.ts            # TypeScript definitions
│   ├── index.tsx           # React entry point
│   ├── index.css           # Global styles
│   └── App.tsx             # Main app component
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── .env                    # Environment variables
└── test_frontend_api.js    # Integration tests
```

## 🔧 Environment Variables

```bash
REACT_APP_API_URL=http://localhost:5000  # Backend API URL
REACT_APP_DEBUG=true                     # Debug mode
PORT=3000                                # Frontend port
```

## 🚀 Running the App

### Development Mode
```bash
npm start
```
- Runs on http://localhost:3000
- Hot reload enabled
- Development build

### Production Build
```bash
npm run build
```
- Creates optimized production build
- Static files in `build/` directory

## 🧪 Testing

### API Integration Test
```bash
node test_frontend_api.js
```

**Test Results:**
```
✅ Backend API: Running and functional
✅ Frontend Server: Running and serving content  
✅ API Integration: Ready for React app
✅ Equation Solving: Working (with/without database)
✅ Validation: Working correctly
✅ Task 2.1: Form nhập a,b,c → API POST ✅ READY
```

### Manual Testing
1. **Form Validation**:
   - Try submitting empty fields → Should show validation errors
   - Enter non-numeric values → Should show type errors
   - Enter valid numbers → Should submit successfully

2. **API Integration**:
   - Submit equation → Should call POST /api/equation
   - Check network tab → Should see API requests/responses
   - Verify results → Should display equation and solution

3. **UI/UX**:
   - Responsive design → Test on different screen sizes
   - Loading states → Should show spinner during API calls
   - Notifications → Should show success/error messages

## 📊 API Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /ping | Check API connection |
| POST | /api/equation | Create and solve equation |

## 🎯 Example Usage

### Input Form
```
Hệ số a (x²): 1
Hệ số b (x):  -5  
Hệ số c (hằng số): 6
```

### API Request
```json
POST /api/equation
{
  "a": 1,
  "b": -5,
  "c": 6
}
```

### API Response
```json
{
  "message": "Equation created and solved successfully",
  "status": "success",
  "data": {
    "id": 1,
    "equation_string": "1.0x² + -5.0x + 6.0 = 0",
    "solution": "x₁ = 3.000000, x₂ = 2.000000",
    "solution_type": "two_real",
    "discriminant": 1.0
  }
}
```

### UI Display
```
✅ Kết quả:
📝 Phương trình: 1.0x² + -5.0x + 6.0 = 0
🎯 Nghiệm: x₁ = 3.000000, x₂ = 2.000000
📊 Loại nghiệm: two_real | Δ = 1.0 | ID: 1
```

## 🔄 Next Steps (Task 2.2)
- ✅ Task 2.1: Form nhập hệ số ✅ COMPLETED
- 🎯 Task 2.2: Hiển thị kết quả (enhanced)
- 🎯 Task 2.3: Danh sách phương trình đã lưu

## 🛠️ Technologies Used
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **CSS3** - Styling with gradients
- **Node.js** - Development environment