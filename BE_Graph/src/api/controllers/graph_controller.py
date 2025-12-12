from flask import Blueprint, jsonify, request

# Định nghĩa Blueprint cho các route liên quan đến đồ thị
graph_bp = Blueprint('graph', __name__)

@graph_bp.route('/data', methods=['POST'])
def receive_graph_data():
    """
    API nhận dữ liệu đồ thị từ Frontend.
    Đồ thị có thể là vô hướng/có hướng, có trọng số/không trọng số.
    """
    # Lấy dữ liệu JSON từ request
    data = request.json
    
    # Kiểm tra dữ liệu (Ví dụ: phải có nodes và edges)
    if not data or 'nodes' not in data or 'edges' not in data:
        return jsonify({"error": "Dữ liệu đồ thị không hợp lệ."}), 400

    # TODO: Ở đây, bạn sẽ gọi hàm trong src/services/graph_service.py 
    # để lưu trữ đồ thị (trong bộ nhớ) và trả về trạng thái thành công.
    
    # Ví dụ trả về:
    return jsonify({
        "message": "Đồ thị đã được nhận thành công!", 
        "num_nodes": len(data['nodes'])
    }), 200

# TODO: Thêm các route khác ở đây:
# - @graph_bp.route('/run/bfs', methods=['POST'])
# - @graph_bp.route('/run/prim', methods=['POST'])
# - ...