import os
import sys # <--- Thêm cái này để in Log
from src.create_app import create_app
# 1. IMPORT HÀM SETUP_CORS TỪ FILE BẠN VỪA TẠO
# (Giả sử file đó bạn lưu là src/cors.py)
from src.cors import setup_cors 

# Khởi tạo ứng dụng
app = create_app()

# ==================================================
# 2. GỌI HÀM CẤU HÌNH CORS NGAY TẠI ĐÂY (BẮT BUỘC)
# ==================================================
print(">>> DANG CAI DAT CORS (FORCE ALLOW ALL)...", file=sys.stdout)
setup_cors(app)
print(">>> DA CAI DAT CORS XONG!", file=sys.stdout)
# ==================================================

if __name__ == "__main__":
    # Lấy cổng từ biến môi trường
    port = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    
    # Chạy server
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))