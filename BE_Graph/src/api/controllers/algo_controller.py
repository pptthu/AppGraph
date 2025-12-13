from flask import Blueprint, request, jsonify
import sys

# IMPORT CÁC THUẬT TOÁN
from src.domain.algorithms.basic import run_bfs, run_dfs, run_dijkstra, check_bipartite
from src.domain.algorithms.mst import run_prim, run_kruskal
from src.domain.algorithms.flow import run_ford_fulkerson
# Import thuật toán Euler mới
from src.domain.algorithms.euler import run_fleury, run_hierholzer
# from src.domain.algorithms.euler import run_hierholzer # Bỏ comment nếu đã có file

algo_bp = Blueprint('algo', __name__)

@algo_bp.route('/solve', methods=['POST'])
def solve_algorithm():
    try:
        data = request.json
        
        # --- LOG DEBUG ---
        print("\n========== REQUEST MỚI ==========", file=sys.stdout)
        print(f"Algorithm: {data.get('algorithm')}", file=sys.stdout)
        
        algo_type = data.get('algorithm')
        graph = data.get('graph', {})
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        is_directed = graph.get('isDirected', False)

        # Log dữ liệu thô ban đầu
        print(f"Nodes count: {len(nodes)}", file=sys.stdout)
        print(f"Edges count: {len(edges)}", file=sys.stdout)

        # --- QUAN TRỌNG: CHUẨN HÓA DỮ LIỆU ---
        
        # 1. Ép kiểu Start/End về string
        start_node = str(data.get('startNode')) if data.get('startNode') is not None else None
        end_node = str(data.get('endNode')) if data.get('endNode') is not None else None
        print(f"Start: {start_node} | End: {end_node}", file=sys.stdout)

        # 2. Ép kiểu Nodes ID về string
        for n in nodes: 
            n['id'] = str(n['id'])

        # 3. Ép kiểu Edges và QUAN TRỌNG NHẤT: XỬ LÝ TRỌNG SỐ
        for e in edges:
            e['source'] = str(e['source'])
            e['target'] = str(e['target'])
            
            # Lấy giá trị trọng số từ Frontend (nó có thể tên là 'weight', 'label', hoặc 'value')
            raw_weight = e.get('weight') or e.get('label') or e.get('value') or 1
            
            try:
                # Ép về số thực
                val = float(raw_weight)
            except:
                val = 1.0
            
            # Gán vào cả 'weight' (cho Dijkstra/Prim) và 'capacity' (cho Flow)
            e['weight'] = val
            e['capacity'] = val 

        # --- ĐIỀU HƯỚNG THUẬT TOÁN ---
        steps = []

        if algo_type == 'BFS':
            if not start_node: return jsonify({'success': False, 'message': "Thiếu nút bắt đầu"}), 400
            steps = run_bfs(nodes, edges, start_node, end_node, is_directed)
            
        elif algo_type == 'DFS':
            if not start_node: return jsonify({'success': False, 'message': "Thiếu nút bắt đầu"}), 400
            steps = run_dfs(nodes, edges, start_node, end_node, is_directed)
            
        elif algo_type == 'DIJKSTRA':
            if not start_node or not end_node: return jsonify({'success': False, 'message': "Thiếu nút đầu/cuối"}), 400
            steps = run_dijkstra(nodes, edges, start_node, end_node, is_directed)
            
        elif algo_type == 'BIPARTITE':
            steps = check_bipartite(nodes, edges, start_node, end_node, is_directed)

        elif algo_type == 'PRIM':
             steps = run_prim(nodes, edges, start_node, is_directed)
             
        elif algo_type == 'KRUSKAL':
             steps = run_kruskal(nodes, edges, is_directed)

        elif algo_type == 'FORD_FULKERSON':
             if not start_node or not end_node: return jsonify({'success': False, 'message': "Thiếu nút đầu/cuối"}), 400
             # Flow luôn cần đồ thị có hướng
             steps = run_ford_fulkerson(nodes, edges, start_node, end_node, True)

        elif algo_type == 'FLEURY':
             steps = run_fleury(nodes, edges, is_directed, start_node)

        elif algo_type == 'HIERHOLZER':
             steps = run_hierholzer(nodes, edges, is_directed, start_node)

        else:
            return jsonify({'success': False, 'message': "Thuật toán không hỗ trợ"}), 400

        # --- LOG KẾT QUẢ ---
        print(f"-> KẾT QUẢ: {len(steps)} bước.", file=sys.stdout)
        print("=================================\n", file=sys.stdout)
        
        return jsonify({'success': True, 'steps': steps})

    except Exception as e:
        print(f"!!! LỖI SERVER: {str(e)}", file=sys.stdout)
        return jsonify({'success': False, 'message': str(e)}), 500