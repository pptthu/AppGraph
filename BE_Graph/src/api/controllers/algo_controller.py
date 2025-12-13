from flask import Blueprint, request, jsonify
import sys

# 1. IMPORT CÁC THUẬT TOÁN
from src.domain.algorithms.basic import run_bfs, run_dfs, run_dijkstra, check_bipartite
from src.domain.algorithms.mst import run_prim, run_kruskal
from src.domain.algorithms.flow import run_ford_fulkerson
# Nếu bạn đã thêm Euler thì bỏ comment dòng dưới:
# from src.domain.algorithms.euler import run_hierholzer

algo_bp = Blueprint('algo', __name__)

@algo_bp.route('/solve', methods=['POST'])
def solve_algorithm():
    try:
        data = request.json
        
        # --- 1. LOGGING DEBUG (IN RA CONSOLE RENDER) ---
        print("\n----- NHẬN REQUEST MỚI -----", file=sys.stdout)
        print(f"Algorithm: {data.get('algorithm')}", file=sys.stdout)
        
        # --- 2. LẤY DỮ LIỆU TỪ REQUEST ---
        algo_type = data.get('algorithm')
        
        # Lấy thông tin đồ thị
        graph = data.get('graph', {})
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        is_directed = graph.get('isDirected', False)

        # Log số lượng node/edge để kiểm tra data
        print(f"Nodes count: {len(nodes)}", file=sys.stdout)
        print(f"Edges count: {len(edges)}", file=sys.stdout)

        # --- 3. ÉP KIỂU DỮ LIỆU (FIX LỖI ID SỐ VÀ CHỮ) ---
        # Chuyển startNode/endNode về string (nếu có)
        start_node = str(data.get('startNode')) if data.get('startNode') is not None else None
        end_node = str(data.get('endNode')) if data.get('endNode') is not None else None
        
        print(f"Start: {start_node}, End: {end_node}", file=sys.stdout)

        # Chuyển toàn bộ ID trong Nodes về string
        for n in nodes: 
            n['id'] = str(n['id'])
            
        # Chuyển toàn bộ Source/Target trong Edges về string
        for e in edges:
            e['source'] = str(e['source'])
            e['target'] = str(e['target'])
            
        # --- 4. ĐIỀU HƯỚNG XỬ LÝ ---
        steps = []

        # --- NHÓM 1: CƠ BẢN ---
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
            steps = check_bipartite(nodes, edges, start_node, end_node, is_directed)

        # --- NHÓM 2: CÂY KHUNG (MST) ---
        elif algo_type == 'PRIM':
             steps = run_prim(nodes, edges, start_node, is_directed)
             
        elif algo_type == 'KRUSKAL':
             steps = run_kruskal(nodes, edges, is_directed)

        # --- NHÓM 3: LUỒNG (FLOW) ---
        elif algo_type == 'FORD_FULKERSON':
             if not start_node or not end_node:
                 return jsonify({'success': False, 'message': "Cần chọn đỉnh nguồn (Source) và đỉnh đích (Sink)"}), 400
             steps = run_ford_fulkerson(nodes, edges, start_node, end_node, True)

        # --- NHÓM 4: EULER (NẾU CÓ) ---
        elif algo_type == 'HIERHOLZER' or algo_type == 'FLEURY':
             # steps = run_hierholzer(nodes, edges, is_directed)
             pass # Bỏ pass và dùng dòng trên khi đã có file euler.py

        else:
            return jsonify({'success': False, 'message': f"Thuật toán {algo_type} chưa được hỗ trợ"}), 400

        # --- 5. TRẢ VỀ KẾT QUẢ ---
        print(f"-> KẾT QUẢ: Tìm thấy {len(steps)} bước chạy.", file=sys.stdout)
        print("----------------------------\n", file=sys.stdout)
        
        return jsonify({
            'success': True,
            'steps': steps
        })

    except Exception as e:
        print(f"!!! LỖI SERVER: {str(e)}", file=sys.stdout)
        return jsonify({'success': False, 'message': str(e)}), 500