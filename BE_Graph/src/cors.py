from flask import Flask
from flask_cors import CORS
import sys

def setup_cors(app: Flask):
    """
    Thiết lập CORS: Cho phép TẤT CẢ các nguồn truy cập.
    """
    # --- THÊM DÒNG NÀY ĐỂ SOI LOG ---
    print("!!! KICH HOAT CORS MOI - CHO PHEP TAT CA (ALLOW ALL) !!!", file=sys.stdout)
    # --------------------------------
    
    CORS(
        app,
        resources={r"/*": {"origins": "*"}}, 
        supports_credentials=True
    )