import os
import sys 
from src.create_app import create_app
from src.cors import setup_cors 

# Khởi tạo ứng dụng
app = create_app()

# ==================================================
# 2. GỌI HÀM CẤU HÌNH CORS NGAY TẠI ĐÂY 
# ==================================================
print(">>> DANG CAI DAT CORS", file=sys.stdout)
setup_cors(app)
print(">>> DA CAI DAT CORS XONG!", file=sys.stdout)
# ==================================================

if __name__ == "__main__":
    # Lấy cổng từ biến môi trường
    port = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    
    # Chạy server
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))