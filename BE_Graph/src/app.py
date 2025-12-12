import os
from src.create_app import create_app

# Khởi tạo ứng dụng
app = create_app()

if __name__ == "__main__":
    import os
    # Lấy cổng từ biến môi trường
    port = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    
    # Chạy server, host 0.0.0.0 để có thể truy cập từ mạng ngoài 
    # Debug = True: Server sẽ tự động reload khi có thay đổi code
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))