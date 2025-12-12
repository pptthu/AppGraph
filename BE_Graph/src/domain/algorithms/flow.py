from collections import deque

def run_ford_fulkerson(nodes, edges, start_node, end_node, is_directed=True):
    """
    Thuật toán Ford-Fulkerson (Edmonds-Karp implementation).
    Có hỗ trợ visualize cấu trúc dữ liệu (Queue).
    """
    steps = []
    
    # 1. Khởi tạo cấu trúc dữ liệu
    capacity = {n['id']: {} for n in nodes}
    for n_id in capacity:
        for m_id in capacity:
            capacity[n_id][m_id] = 0
            
    for e in edges:
        u, v, w = e['source'], e['target'], float(e.get('weight', 0))
        capacity[u][v] = w
        if not is_directed:
            capacity[v][u] = w

    parent = {n['id']: None for n in nodes}
    max_flow = 0
    
    steps.append({
        "description": f"Khởi tạo: Tìm luồng cực đại từ {start_node} đến {end_node}.",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": [] # Queue ban đầu rỗng
    })

    # 2. Vòng lặp chính
    while True:
        for n in nodes: parent[n['id']] = None
        queue = deque([start_node])
        parent[start_node] = start_node
        
        path_found = False
        
        # --- BẮT ĐẦU BFS (Visual hóa Queue tại đây) ---
        while queue:
            # Snapshot Queue trước khi pop (nếu muốn hiện chi tiết)
            
            u = queue.popleft()
            
            if u == end_node:
                path_found = True
                break
            
            for v in capacity.keys():
                if parent[v] is None and capacity[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
                    
                    # --- THÊM: Ghi lại trạng thái Queue ---
                    steps.append({
                        "description": f"BFS tìm đường tăng luồng: Từ {u}, thêm {v} vào hàng đợi",
                        "visitedNodes": [], 
                        "currentNodeId": u, # Đang xét u
                        "selectedEdges": [{"source": u, "target": v}], # Tô màu cạnh đang xét
                        "structure": list(queue) # Gửi Queue về FE
                    })
        
        if not path_found:
            break

        # 3. Truy vết và cập nhật luồng
        path_flow = float('inf')
        v = end_node
        path_edges = [] 
        path_nodes = [end_node]
        
        while v != start_node:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            path_edges.append({"source": u, "target": v})
            path_nodes.append(u)
            v = u
        
        path_nodes.reverse()

        steps.append({
            "description": f"Tìm thấy đường tăng: {' -> '.join(path_nodes)}. Flow += {path_flow}",
            "visitedNodes": list(path_nodes),
            "currentNodeId": end_node,
            "selectedEdges": list(path_edges),
            "structure": [] # Lúc này Queue đã dùng xong cho đợt tìm này
        })

        # 4. Cập nhật đồ thị thặng dư
        max_flow += path_flow
        v = end_node
        while v != start_node:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = u
            
        steps.append({
            "description": f"Cập nhật đồ thị thặng dư. Tổng luồng = {max_flow}.",
            "visitedNodes": [],
            "currentNodeId": start_node,
            "selectedEdges": [],
            "structure": []
        })

    # Kết thúc
    steps.append({
        "description": f"Hoàn tất. LUỒNG CỰC ĐẠI = {max_flow}",
        "visitedNodes": [],
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": []
    })

    return steps