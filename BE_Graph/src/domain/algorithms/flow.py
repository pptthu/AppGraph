from collections import deque
import copy

def run_ford_fulkerson(nodes, edges, start_node_id, end_node_id, is_directed=True):
    steps = []

    # --- 1. KIỂM TRA DỮ LIỆU ĐẦU VÀO ---
    for e in edges:
        val = float(e.get('capacity', e.get('weight', 1)))
        if val < 0:
            steps.append({
                "description": "Lỗi: Trọng số âm!", # Hiển thị ngắn gọn ở hộp điều khiển
                "log": "❌ Ford-Fulkerson không hỗ trợ dung lượng âm!",
                "error": True,
                "visitedNodes": [],
                "currentNodeId": None,
                "selectedEdges": [],
                "structure": []
            })
            return steps
    
    # --- 2. KHỞI TẠO ---
    graph = {str(n['id']): [] for n in nodes}
    capacity = {}
    current_flow = {} 

    for edge in edges:
        u, v = str(edge['source']), str(edge['target'])
        cap = float(edge.get('capacity', edge.get('weight', 1)))
        
        graph[u].append(v)
        capacity[(u, v)] = cap
        current_flow[(u, v)] = 0
        
        if v not in graph: graph[v] = []
        graph[v].append(u)
        
        if (v, u) not in capacity: capacity[(v, u)] = 0 
        if (v, u) not in current_flow: current_flow[(v, u)] = 0

    # --- 3. HÀM BFS ---
    def bfs(s, t, parent):
        visited = {n: False for n in graph}
        queue = deque([s])
        visited[s] = True
        parent[s] = -1
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                residual = capacity.get((u, v), 0) - current_flow.get((u, v), 0)
                if not visited[v] and residual > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t: return True
        return False

    # --- 4. BẮT ĐẦU THUẬT TOÁN ---
    max_flow = 0
    
    steps.append({
        "description": "Khởi tạo: Tất cả luồng = 0",
        "log": f"🏁 Khởi tạo. Nguồn: {start_node_id}, Đích: {end_node_id}.",
        "visitedNodes": [start_node_id, end_node_id],
        "selectedEdges": [],
        "currentNodeId": start_node_id,
        "structure": []
    })

    parent = {}
    path_counter = 0 # Đếm số đường tìm thấy

    while bfs(start_node_id, end_node_id, parent):
        path_counter += 1
        path_flow = float('Inf')
        s = end_node_id
        path_nodes = [end_node_id]
        
        # 4a. Truy vết ngược
        while s != start_node_id:
            p = parent[s]
            residual = capacity[(p, s)] - current_flow[(p, s)]
            path_flow = min(path_flow, residual)
            path_nodes.append(p)
            s = p
        
        path_nodes.reverse()
        path_str = " -> ".join(path_nodes) # VD: "A -> B -> D"

        # 4b. Cập nhật luồng
        s = end_node_id
        highlight_edges = []
        
        while s != start_node_id:
            p = parent[s]
            current_flow[(p, s)] += path_flow
            current_flow[(s, p)] -= path_flow
            
            # Label trên cạnh: Flow/Capacity (VD: 3/5)
            info = f"{int(current_flow[(p,s)])}/{int(capacity[(p,s)])}"
            highlight_edges.append({"source": p, "target": s, "label": info})
            s = p

        max_flow += path_flow
        
        # --- 4c. TỐI ƯU HIỂN THỊ (QUAN TRỌNG) ---
        # Đưa thông tin chi tiết vào `description` vì Web chỉ hiển thị cái này
        step_desc = f"#{path_counter}. Tăng {path_flow}: {path_str}"
        
        steps.append({
            "description": step_desc, # <--- Dòng này sẽ hiện rõ ràng trên Web
            "log": f"⚡ Tìm thấy đường: {path_str} (Tăng {path_flow})",
            "visitedNodes": path_nodes,
            "selectedEdges": highlight_edges,
            "pathFound": path_nodes,
            "currentNodeId": end_node_id,
            "structure": [] 
        })

    # --- 5. KẾT THÚC ---
    steps.append({
        "description": f"Hoàn thành. Tổng luồng cực đại = {max_flow}", # <--- Hiện kết quả cuối cùng
        "log": f"✅ Tổng luồng cực đại = {max_flow}",
        "visitedNodes": [], 
        "selectedEdges": [],
        "currentNodeId": None,
        "structure": []
    })
    
    return steps