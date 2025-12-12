import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Cấu hình cơ bản cho ứng dụng Flask."""
    # Chế độ môi trường 
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    # Bật/Tắt chế độ debug 
    DEBUG = (FLASK_ENV == "development")
    # Khóa bí mật 
    SECRET_KEY = os.getenv("SECRET_KEY", "graph_project_secret_key")
    
    # Cấu hình CORS (React gọi API)
    # Cho phép FE (chạy ở localhost:3000) truy cập BE
    CORS_ORIGINS = ["http://localhost:3000"]
    CORS_SUPPORTS_CREDENTIALS = True