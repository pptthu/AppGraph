from collections import deque
import copy

def run_ford_fulkerson(nodes, edges, start_node_id, end_node_id, is_directed=True):
    steps = []

    # --- CHECK AN TOÀN: SỐ ÂM ---
    for e in edges:
        if float(e.get('capacity', e.get('weight', 1))) < 0:
            steps.append({
                "description": "Lỗi Dữ Liệu",
                "log": "❌ Ford-Fulkerson không hỗ trợ dung lượng âm! Vui lòng sửa lại.",
                "error": True,
                "visitedNodes": [],
                "currentNodeId": None,
                "selectedEdges": [],
                "structure": []
            })
            return steps
    
    # 1. Cấu trúc dữ liệu
    graph = {str(n['id']): [] for n in nodes}
    capacity = {}
    current_flow = {} 

    # Khởi tạo đồ thị
    for edge in edges:
        u, v = str(edge['source']), str(edge['target'])
        cap = float(edge.get('capacity', edge.get('weight', 1)))
        
        # Cạnh thuận
        graph[u].append(v)
        capacity[(u, v)] = cap
        current_flow[(u, v)] = 0
        
        # Cạnh nghịch
        if v not in graph: graph[v] = []
        graph[v].append(u)
        if (v, u) not in capacity:
            capacity[(v, u)] = 0 
        current_flow[(v, u)] = 0

    # Hàm BFS
    def bfs(s, t, parent):
        visited = {n: False for n in graph}
        queue = [s]
        visited[s] = True
        parent[s] = -1
        
        while queue:
            u = queue.pop(0)
            for v in graph[u]:
                residual = capacity.get((u, v), 0) - current_flow.get((u, v), 0)
                if not visited[v] and residual > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t: return True
        return False

    # 2. Bắt đầu thuật toán
    max_flow = 0
    steps.append({
        "description": "Khởi tạo",
        "log": f"Bắt đầu tìm luồng cực đại từ {start_node_id} -> {end_node_id}",
        "visitedNodes": [start_node_id, end_node_id],
        "selectedEdges": [],
        "currentNodeId": start_node_id,
        "structure": []
    })

    parent = {}
    while bfs(start_node_id, end_node_id, parent):
        path_flow = float('Inf')
        s = end_node_id
        path_nodes = [end_node_id]
        
        while s != start_node_id:
            p = parent[s]
            residual = capacity[(p, s)] - current_flow[(p, s)]
            path_flow = min(path_flow, residual)
            path_nodes.append(p)
            s = p
        path_nodes.reverse()

        # Cập nhật flow
        s = end_node_id
        highlight_edges = []
        while s != start_node_id:
            p = parent[s]
            current_flow[(p, s)] += path_flow
            current_flow[(s, p)] -= path_flow
            
            info = f"{int(current_flow[(p,s)])}/{int(capacity[(p,s)])}"
            highlight_edges.append({"source": p, "target": s, "label": info})
            s = p

        max_flow += path_flow
        
        steps.append({
            "description": f"Tìm thấy đường tăng luồng (Flow +{path_flow})",
            "log": f"Đường đi: {'->'.join(path_nodes)} | Tăng thêm: {path_flow} | Tổng luồng: {max_flow}",
            "visitedNodes": path_nodes,
            "selectedEdges": highlight_edges,
            "pathFound": path_nodes,
            "currentNodeId": end_node_id,
            "structure": []
        })

    # Kết thúc
    steps.append({
        "description": "Hoàn thành",
        "log": f"✅ TỔNG LUỒNG CỰC ĐẠI = {max_flow}",
        "visitedNodes": [], 
        "selectedEdges": [],
        "currentNodeId": None,
        "structure": []
    })
    
    return steps