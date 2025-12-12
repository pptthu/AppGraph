from flask import Flask
from flask_cors import CORS
from src.config import Config

def setup_cors(app: Flask):
    """Thiết lập CORS để cho phép Frontend giao tiếp với Backend."""
    # Lấy danh sách origin từ Config
    origins = app.config.get("CORS_ORIGINS", ["*"])
    
    CORS(
        app,
        resources={r"/*": {"origins": origins}},
        supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", True)
    )