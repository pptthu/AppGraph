from flask import Blueprint, request, jsonify

# 1. IMPORT NHÓM CƠ BẢN (Basic)
# Đảm bảo file src/domain/algorithms/basic.py đã tồn tại và đúng logic
from src.domain.algorithms.basic import run_bfs, run_dfs, run_dijkstra, check_bipartite

# 2. IMPORT NHÓM CÂY KHUNG (MST)
# Đảm bảo file src/domain/algorithms/mst.py đã tồn tại và đúng logic
from src.domain.algorithms.mst import run_prim, run_kruskal

# 3. IMPORT NHÓM LUỒNG (Flow)
# Đảm bảo file src/domain/algorithms/flow.py đã tồn tại và đúng logic
from src.domain.algorithms.flow import run_ford_fulkerson

algo_bp = Blueprint('algo', __name__)

@algo_bp.route('/solve', methods=['POST'])
def solve_algorithm():
    try:
        data = request.json
        
        # Lấy tham số từ Frontend
        algo_type = data.get('algorithm') 
        start_node = data.get('startNode')
        end_node = data.get('endNode')
        
        # Lấy dữ liệu đồ thị
        graph = data.get('graph', {})
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        is_directed = graph.get('isDirected', False)

        steps = []

        # ==========================================
        # ĐIỀU HƯỚNG XỬ LÝ CÁC THUẬT TOÁN
        # ==========================================

        # --- NHÓM 1: THUẬT TOÁN CƠ BẢN ---
        if algo_type == 'BFS':
            if not start_node:
                return jsonify({'success': False, 'message': "Vui lòng chọn nút bắt đầu cho BFS"}), 400
            steps = run_bfs(nodes, edges, start_node, end_node, is_directed)
            
        elif algo_type == 'DFS':
            if not start_node:
                return jsonify({'success': False, 'message': "Vui lòng chọn nút bắt đầu cho DFS"}), 400
            steps = run_dfs(nodes, edges, start_node, end_node, is_directed)
            
        elif algo_type == 'DIJKSTRA':
            if not start_node or not end_node:
                return jsonify({'success': False, 'message': "Vui lòng chọn nút bắt đầu và nút đích cho Dijkstra"}), 400
            steps = run_dijkstra(nodes, edges, start_node, end_node, is_directed)
            
        elif algo_type == 'BIPARTITE':
            # Bipartite tự động duyệt qua các thành phần liên thông, không bắt buộc start_node từ FE
            steps = check_bipartite(nodes, edges, start_node, end_node, is_directed)

        # --- NHÓM 2: CÂY KHUNG CỰC TIỂU (MST) ---
        elif algo_type == 'PRIM':
             # Prim nên có điểm bắt đầu để visualize đẹp hơn
             # Nếu start_node null, hàm run_prim của bạn Linh nên tự xử lý (lấy node đầu tiên)
             steps = run_prim(nodes, edges, start_node, is_directed)
             
        elif algo_type == 'KRUSKAL':
             # Kruskal hoạt động trên toàn bộ danh sách cạnh, không cần điểm bắt đầu
             steps = run_kruskal(nodes, edges, is_directed)

        # --- NHÓM 3: LUỒNG CỰC ĐẠI (FLOW) ---
        elif algo_type == 'FORD_FULKERSON':
             if not start_node or not end_node:
                 return jsonify({'success': False, 'message': "Cần chọn đỉnh nguồn (Source) và đỉnh đích (Sink)"}), 400
             # Ford-Fulkerson luôn chạy trên đồ thị có hướng (ép is_directed=True để xử lý đúng logic ma trận kề)
             steps = run_ford_fulkerson(nodes, edges, start_node, end_node, is_directed=True)
            
        else:
            return jsonify({'success': False, 'message': f"Thuật toán {algo_type} chưa được hỗ trợ"}), 400

        # Trả về kết quả thành công cho Frontend
        return jsonify({
            'success': True,
            'steps': steps
        })

    except Exception as e:
        # Ghi log lỗi ra terminal server để debug
        print(f"Server Error: {str(e)}") 
        return jsonify({'success': False, 'message': str(e)}), 500