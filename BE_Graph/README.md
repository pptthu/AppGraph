# 🐍 Backend: Ứng dụng Trực quan hóa Thuật toán Đồ thị

Đây là Backend (API) cho bài tập lớn môn Cấu trúc rời rạc, được xây dựng bằng **Flask (Python)** theo kiến trúc phân lớp (Layered Architecture).

## 🛠️ 1. Cài đặt và Chạy dự án

### Bước 1: Clone dự án
```bash
git clone https://github.com/pptthu/BE_Graph.git
cd BE_Graph
```
### Bước 2: Tạo môi trường ảo 
```bash
python -m venv .venv
```
### Bước 3: Kích hoạt môi trường 
``` bash
.\.venv\Scripts\Activate
```
### Bước 4: Cài đặt thư viện 
``` bash 
pip install -r requirements.txt
```

### Bước 5: Cấu hình, tạo file .env tại thư mục gốc (BE_Graph)
``` bash 
FLASK_ENV=development
SECRET_KEY=graph_project_secret_key
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```
### Bước 6: Chạy server 
``` bash 
python -m src.app

nhấn http://127.0.0.1:8000
```

# Cấu trúc 
``` bash
BE_Graph/
├── src/
│   ├── api/                  # Giao tiếp với bên ngoài (Frontend)
│   │   ├── controllers/      # Nhận Request, trả về Response
│   │   │   ├── algo_controller.py   # API chạy thuật toán (BFS, Prim...)
│   │   │   └── graph_controller.py  # API xử lý dữ liệu đồ thị
│   │   ├── schemas/          # Định dạng dữ liệu (Validation)
│   │   │   └── graph_schema.py
│   │   └── routes.py         # Đăng ký đường dẫn API (Routes)
│   │
│   ├── domain/               # Logic nghiệp vụ cốt lõi (Core)
│   │   ├── algorithms/       # Các thuật toán đồ thị
│   │   │   ├── basic.py      # BFS, DFS, Dijkstra
│   │   │   ├── euler.py      # Fleury, Hierholzer
│   │   │   ├── flow.py       # Ford-Fulkerson
│   │   │   └── mst.py        # Prim, Kruskal
│   │   └── models/
│   │       └── graph.py      # Cấu trúc dữ liệu Graph (Class)
│   │
│   ├── services/             # Lớp trung gian (Logic ứng dụng)
│   │   ├── algo_service.py   # Gọi thuật toán và xử lý kết quả
│   │   └── graph_service.py  # Chuyển đổi dữ liệu JSON <-> Graph
│   │
│   ├── app.py                # File cấu hình chính
│   ├── config.py             # Load biến môi trường
│   ├── cors.py               # Cấu hình CORS
│   └── create_app.py         # Hàm khởi tạo Flask App
│
├── .env                      # Biến môi trường (Không up lên Git)
├── .gitignore                # File loại bỏ (ignore) của Git
└── requirements.txt          # Danh sách thư viện
```
# Vai trò 
``` bash
Thành phần,Vai trò,Nhiệm vụ cụ thể
Controller,Tiếp tân,"Nhận yêu cầu từ React, gọi Service, và trả kết quả JSON. Không chứa logic tính toán phức tạp."
Service,Quản lý,"Nhận dữ liệu từ Controller, chuyển đổi format, gọi đúng thuật toán trong Domain để xử lý."
Domain,Chuyên gia,"Chứa các class và hàm thuật toán thuần túy. Đây là nơi chứa logic ""thông minh"" nhất của đồ án."
```
# Danh sách API 
``` bash
Chức năng,Method,Endpoint
Nhập dữ liệu đồ thị,POST,/api/v1/graph/data
Lưu đồ thị xuống file,POST,/api/v1/graph/save
Chạy thuật toán BFS,POST,/api/v1/algo/bfs
Chạy thuật toán Prim,POST,/api/v1/algo/mst/prim
Chạy luồng cực đại,POST,/api/v1/algo/flow/max
```