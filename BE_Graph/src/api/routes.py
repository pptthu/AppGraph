from flask import Flask
from src.api.controllers.algo_controller import algo_bp

def register_routes(app: Flask):
    """
    Hàm này được gọi bên create_app.py để đăng ký các Blueprint
    """
    # Đăng ký Blueprint với prefix /api
    # Các route sẽ là: /api/solve
    app.register_blueprint(algo_bp, url_prefix='/api')