import os
from flask import Flask
from src.config import Config
from src.cors import setup_cors
from src.api.routes import register_routes


def create_app():
    """Tạo và cấu hình một instance của ứng dụng Flask."""
    
    # Khởi tạo Flask
    app = Flask(__name__)
    
    # Load cấu hình từ lớp Config
    app.config.from_object(Config)

    # 1. Thiết lập CORS
    setup_cors(app)
    
    # 2. Đăng ký Routes (API Endpoints)
    register_routes(app)
    
    # Ghi log đơn giản khi debug được bật
    if app.debug:
        print(f"Flask App running in {app.config['FLASK_ENV']} mode.")
        print(f"CORS allowed origins: {app.config['CORS_ORIGINS']}")

    return app