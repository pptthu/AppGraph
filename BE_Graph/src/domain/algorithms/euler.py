import copy

# ==========================================
# 1. HÀM PHỤ TRỢ (KIỂM TRA & CHECK CẦU & LIÊN THÔNG)
# ==========================================

def check_connectivity(nodes, edges, is_directed):
    if not nodes: return True
    if not edges: return True
    
    relevant_nodes = set()
    adj = {str(n['id']): [] for n in nodes}
    
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        if not is_directed:
            adj[v].append(u)
        else:
            adj[v].append(u) 
            
        relevant_nodes.add(u)
        relevant_nodes.add(v)
        
    if not relevant_nodes: return True
    
    start = list(relevant_nodes)[0]
    visited = {start}
    queue = [start]
    
    while queue:
        u = queue.pop(0)
        for v in adj[u]:
            if v in relevant_nodes and v not in visited:
                visited.add(v)
                queue.append(v)
                
    if len(visited) != len(relevant_nodes):
        return False
        
    return True

def get_euler_status(nodes, edges, is_directed, user_start_node=None):
    if not nodes: return None, None, "Đồ thị rỗng."
    
    if not check_connectivity(nodes, edges, is_directed):
        return None, None, "Đồ thị không liên thông (Bị chia cắt thành nhiều cụm cạnh rời nhau)."

    adj = {str(n['id']): [] for n in nodes}
    in_degree = {str(n['id']): 0 for n in nodes}
    out_degree = {str(n['id']): 0 for n in nodes}
    degree = {str(n['id']): 0 for n in nodes}

    for e in edges:
        u, v = str(e['source']), str(e['target'])
        if is_directed:
            out_degree[u] += 1
            in_degree[v] += 1
        else:
            degree[u] += 1
            degree[v] += 1

    if not is_directed:
        odd_nodes = [nid for nid, deg in degree.items() if deg % 2 != 0]
        if len(odd_nodes) == 0:
            start = user_start_node if user_start_node and degree.get(user_start_node, 0) > 0 else str(nodes[0]['id'])
            for nid, deg in degree.items():
                if deg > 0 and not user_start_node: 
                    start = nid
                    break
            return "CIRCUIT", start, None
        elif len(odd_nodes) == 2:
            if user_start_node and user_start_node not in odd_nodes:
                return None, None, f"Đây là Đường đi Euler. Bạn BẮT BUỘC phải chọn xuất phát từ 1 trong 2 đỉnh bậc lẻ: {odd_nodes}."
            start = user_start_node if user_start_node else odd_nodes[0]
            return "PATH", start, None
        else:
            return None, None, f"Có {len(odd_nodes)} đỉnh bậc lẻ. Đồ thị Euler chỉ cho phép 0 hoặc 2 đỉnh bậc lẻ."
    else:
        start_nodes = []
        end_nodes = []
        imbalanced = 0
        for nid in [str(n['id']) for n in nodes]:
            diff = out_degree[nid] - in_degree[nid]
            if diff == 1: start_nodes.append(nid)
            elif diff == -1: end_nodes.append(nid)
            elif diff != 0: imbalanced += 1
        
        if imbalanced == 0 and len(start_nodes) == 0 and len(end_nodes) == 0:
            start = user_start_node if user_start_node and out_degree.get(user_start_node, 0) > 0 else str(nodes[0]['id'])
            for nid in [str(n['id']) for n in nodes]:
                if out_degree[nid] > 0 and not user_start_node: 
                    start = nid
                    break
            return "CIRCUIT", start, None
        elif len(start_nodes) == 1 and len(end_nodes) == 1 and imbalanced == 0:
            required_start = start_nodes[0]
            if user_start_node and user_start_node != required_start:
                 return None, None, f"Với đồ thị có hướng này, bạn BẮT BUỘC phải xuất phát từ đỉnh: {required_start}."
            return "PATH", required_start, None
        else:
            return None, None, "Vi phạm điều kiện cân bằng In/Out degree của Euler có hướng."

def is_bridge(u, v, adj):
    count1 = count_reachable(u, adj)
    adj[u].remove(v)
    adj[v].remove(u)
    count2 = count_reachable(u, adj)
    adj[u].append(v)
    adj[v].append(u)
    return count1 > count2

def count_reachable(u, adj):
    visited = set()
    queue = [u]
    visited.add(u)
    count = 0
    while queue:
        curr = queue.pop(0)
        count += 1
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return count

# ==========================================
# 2. THUẬT TOÁN FLEURY 
# ==========================================

def run_fleury(nodes, edges, is_directed=False, user_start_node=None):
    steps = []
    
    euler_type, start_node, error = get_euler_status(nodes, edges, is_directed, user_start_node)
    
    if error:
        steps.append({
            "description": "Lỗi Euler", 
            "log": f"❌ {error}", 
            "error": True,
            "visitedNodes": [], "selectedEdges": []
        })
        return steps
        
    path = [start_node]
    steps.append({
        "description": f"Bắt đầu Fleury ({euler_type}) từ {start_node}",
        "log": f"✅ Điều kiện thỏa mãn. Dạng: {euler_type}. Xuất phát: {start_node}",
        "visitedNodes": [start_node],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "pathFound": [start_node],
        "structure": [start_node] 
    })

    adj = {str(n['id']): [] for n in nodes}
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        if not is_directed: adj[v].append(u)

    curr = start_node
    total_edges = len(edges)
    edges_traversed = 0

    while edges_traversed < total_edges:
        if not adj[curr]: break 

        next_v = -1
        neighbors = adj[curr]
        is_bridge_edge = False
        forced_msg = ""
        
        if len(neighbors) == 1:
            next_v = neighbors[0]
            is_bridge_edge = True
            forced_msg = "Chỉ còn 1 cạnh (Cầu), bắt buộc phải đi."
        else:
            if not is_directed:
                for v in neighbors:
                    if not is_bridge(curr, v, adj):
                        next_v = v
                        is_bridge_edge = False
                        break
            
            if next_v == -1: 
                next_v = neighbors[0]
                is_bridge_edge = True
                forced_msg = "Tất cả lựa chọn đều là cầu -> Chọn đại 1 cái."
        
        adj[curr].remove(next_v)
        if not is_directed: adj[next_v].remove(curr)
        edges_traversed += 1
        
        path.append(next_v) 
        
        # LOG 
        log_detail = "Chọn cạnh an toàn (không phải cầu)."
        if is_bridge_edge:
             log_detail = forced_msg if forced_msg else "Buộc phải đi qua cầu."
        
        steps.append({
            "description": f"Đi: {curr} -> {next_v}. ({'Cầu' if is_bridge_edge else 'OK'})",
            "log": f"Chọn cạnh {curr}-{next_v}. {log_detail}",
            "visitedNodes": [curr, next_v],
            "selectedEdges": [{"source": curr, "target": next_v}],
            "currentNodeId": next_v,
            "pathFound": copy.deepcopy(path),
            "structure": copy.deepcopy(path) 
        })
        
        curr = next_v

    steps.append({
        "description": "Hoàn thành",
        "log": f"🏁 KẾT QUẢ: {' -> '.join(path)}. Đã đi hết {total_edges} cạnh.",
        "pathFound": path,
        "visitedNodes": path,
        "selectedEdges": [], 
        "currentNodeId": None,
        "structure": path
    })
    return steps

# ==========================================
# 3. THUẬT TOÁN HIERHOLZER 
# ==========================================

def run_hierholzer(nodes, edges, is_directed=False, user_start_node=None):
    steps = []
    
    euler_type, start_node, error = get_euler_status(nodes, edges, is_directed, user_start_node)
    
    if error:
        steps.append({
            "description": "Lỗi Euler", "log": f"❌ {error}", "error": True,
            "visitedNodes": [], "selectedEdges": []
        })
        return steps

    steps.append({
        "description": f"Bắt đầu Hierholzer ({euler_type})",
        "log": f"✅ Thỏa mãn {euler_type}. Stack khởi tạo: [{start_node}]",
        "visitedNodes": [start_node],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "pathFound": [],
        "structure": [start_node] 
    })

    # Dùng bản sao danh sách kề để xóa cạnh dần
    adj = {str(n['id']): [] for n in nodes}
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        if not is_directed: adj[v].append(u)

    # Sort để thứ tự duyệt ổn định 
    for u in adj: adj[u].sort()

    circuit = [] 
    stack = [start_node]
    
    # --- LOGIC
    while stack:
        u = stack[-1] 
        
        if adj.get(u): 
            # Còn cạnh để đi -> DFS Forward
            v = adj[u].pop(0) 
            
            if not is_directed:
                if u in adj[v]: adj[v].remove(u)
            
            stack.append(v) 
            
            steps.append({
                "description": f"DFS: {u} -> {v}",
                "log": f"Đi tiếp {u}->{v}. Stack: {stack}",
                "visitedNodes": [u, v],
                "selectedEdges": [{"source": u, "target": v}],
                "currentNodeId": v,
                "pathFound": list(reversed(circuit)) + stack,
                "structure": list(stack) 
            })
        else:
            # Hết cạnh -> Backtrack
            finished_node = stack.pop()
            circuit.append(finished_node)
            
            # Ghi log Backtrack cho TẤT CẢ các đỉnh (bao gồm đỉnh trung gian)
            
            current_stack_top = stack[-1] if stack else None
            
            steps.append({
                "description": f"Backtrack: {finished_node}",
                "log": f"Đỉnh {finished_node} hết cạnh -> Quay lui về {current_stack_top}. Thêm {finished_node} vào Chu trình.",
                "visitedNodes": [finished_node],
                "currentNodeId": current_stack_top,
                "pathFound": list(reversed(circuit)), # Hiển thị chu trình đang hình thành
                "selectedEdges": [],
                "structure": list(stack) 
            })

    final_path = list(reversed(circuit))
    
    if len(final_path) - 1 < len(edges):
         steps.append({
            "description": "Cảnh báo Lỗi: Đồ thị không liên thông",
            "log": "⚠️ Đồ thị không liên thông hoàn toàn (Có cạnh bị cô lập).",
            "error": True,
            "visitedNodes": [], "selectedEdges": []
        })
    else:
        steps.append({
            "description": "Hoàn thành",
            "log": f"🏁 KẾT QUẢ: {' -> '.join(final_path)}",
            "pathFound": final_path,
            "visitedNodes": final_path,
            "selectedEdges": [], 
            "currentNodeId": None,
            "structure": []
        })

    return steps