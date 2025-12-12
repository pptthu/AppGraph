from flask import Flask
from flask_cors import CORS

def setup_cors(app: Flask):
    """
    Thiết lập CORS: Cho phép TẤT CẢ các nguồn truy cập.
    Dùng cấu hình này để đảm bảo Frontend trên Render/Netlify không bị chặn.
    """
    # Force cho phép tất cả (*) bất kể config là gì
    CORS(
        app,
        resources={r"/*": {"origins": "*"}}, 
        supports_credentials=True
    )