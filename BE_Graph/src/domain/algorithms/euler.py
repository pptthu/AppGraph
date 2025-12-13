import copy

# ==========================================
# 1. HÀM PHỤ TRỢ (KIỂM TRA & CHECK CẦU)
# ==========================================

def get_euler_status(nodes, edges, is_directed):
    if not nodes: return None, None, "Đồ thị rỗng."
    
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

    start_node = str(nodes[0]['id']) 
    
    if not is_directed:
        odd_nodes = [nid for nid, deg in degree.items() if deg % 2 != 0]
        if len(odd_nodes) == 0:
            for nid, deg in degree.items():
                if deg > 0: return "CIRCUIT", nid, None
            return "CIRCUIT", start_node, None 
        elif len(odd_nodes) == 2:
            return "PATH", odd_nodes[0], None 
        else:
            return None, None, f"Có {len(odd_nodes)} đỉnh bậc lẻ. Đồ thị Euler chỉ cho phép 0 hoặc 2 đỉnh bậc lẻ."

    else:
        start_nodes = []
        end_nodes = []
        imbalanced = 0
        
        for nid in [str(n['id']) for n in nodes]:
            diff = out_degree[nid] - in_degree[nid]
            if diff == 1:
                start_nodes.append(nid)
            elif diff == -1:
                end_nodes.append(nid)
            elif diff != 0:
                imbalanced += 1
        
        if imbalanced == 0 and len(start_nodes) == 0 and len(end_nodes) == 0:
            for nid in [str(n['id']) for n in nodes]:
                if out_degree[nid] > 0: return "CIRCUIT", nid, None
            return "CIRCUIT", start_node, None
            
        elif len(start_nodes) == 1 and len(end_nodes) == 1 and imbalanced == 0:
            return "PATH", start_nodes[0], None
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
# 2. THUẬT TOÁN FLEURY (FIX FULL KEYS)
# ==========================================

def run_fleury(nodes, edges, is_directed=False):
    steps = []
    
    # Kiểm tra điều kiện
    euler_type, start_node, error = get_euler_status(nodes, edges, is_directed)
    
    if error:
        steps.append({
            "description": "Lỗi", 
            "log": f"❌ {error}", 
            "error": True,
            "visitedNodes": [], "selectedEdges": [] # <--- Luôn trả về mảng rỗng để FE không crash
        })
        return steps
        
    # Bước 1: Khởi tạo
    steps.append({
        "description": "Khởi tạo Fleury",
        "log": f"✅ Đồ thị thỏa mãn ({euler_type}). Bắt đầu từ {start_node}",
        "visitedNodes": [start_node],
        "currentNodeId": start_node,
        "selectedEdges": [], # <--- Thêm mảng rỗng
        "pathFound": [start_node]
    })

    adj = {str(n['id']): [] for n in nodes}
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        if not is_directed: adj[v].append(u)

    path = [start_node]
    curr = start_node
    total_edges = len(edges)
    edges_traversed = 0

    # Bước 2: Vòng lặp
    while edges_traversed < total_edges:
        if not adj[curr]: break 

        next_v = -1
        neighbors = adj[curr]
        
        if len(neighbors) == 1:
            next_v = neighbors[0]
        else:
            for v in neighbors:
                if not is_directed:
                    if not is_bridge(curr, v, adj):
                        next_v = v
                        break
                else:
                    next_v = v
                    break
            if next_v == -1: next_v = neighbors[0]

        adj[curr].remove(next_v)
        if not is_directed: adj[next_v].remove(curr)
        edges_traversed += 1
        
        steps.append({
            "description": "Chọn cạnh tiếp theo",
            "log": f"Đi từ {curr} -> {next_v}" + (" (Là cầu)" if len(neighbors)>1 and next_v == neighbors[0] else ""),
            "visitedNodes": [curr, next_v],
            "selectedEdges": [{"source": curr, "target": next_v}],
            "currentNodeId": next_v,
            "pathFound": copy.deepcopy(path + [next_v])
        })
        
        curr = next_v
        path.append(curr)

    # Bước 3: Hoàn thành
    steps.append({
        "description": "Hoàn thành",
        "log": f"🏁 Kết quả Fleury: {' -> '.join(path)}",
        "pathFound": path,
        "visitedNodes": path,
        "selectedEdges": [], # <--- Thêm mảng rỗng
        "currentNodeId": None
    })
    return steps

# ==========================================
# 3. THUẬT TOÁN HIERHOLZER (FIX FULL KEYS)
# ==========================================

def run_hierholzer(nodes, edges, is_directed=False):
    steps = []
    
    euler_type, start_node, error = get_euler_status(nodes, edges, is_directed)
    if error:
        steps.append({
            "description": "Lỗi", "log": f"❌ {error}", "error": True,
            "visitedNodes": [], "selectedEdges": [] # <--- Fix crash
        })
        return steps

    # Bước 1: Khởi tạo
    steps.append({
        "description": "Khởi tạo Hierholzer",
        "log": f"✅ Bắt đầu Hierholzer từ {start_node}",
        "visitedNodes": [start_node],
        "currentNodeId": start_node,
        "selectedEdges": [], # <--- Fix crash
        "pathFound": []
    })

    adj = {str(n['id']): [] for n in nodes}
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        if not is_directed: adj[v].append(u)

    path = []
    stack = [start_node]
    
    # Bước 2: Vòng lặp
    while stack:
        u = stack[-1]
        
        if adj[u]: 
            v = adj[u].pop(0) 
            if not is_directed:
                if u in adj[v]: adj[v].remove(u)
            stack.append(v)
            
            steps.append({
                "description": "Duyệt DFS",
                "log": f"Đi tiếp {u} -> {v}",
                "visitedNodes": [u, v],
                "selectedEdges": [{"source": u, "target": v}],
                "currentNodeId": v,
                "pathFound": list(reversed(path))
            })
        else:
            finished_node = stack.pop()
            path.append(finished_node)
            
            steps.append({
                "description": "Backtrack (Quay lui)",
                "log": f"Đỉnh {finished_node} hết cạnh -> Thêm vào kết quả.",
                "visitedNodes": [finished_node],
                "currentNodeId": finished_node,
                "pathFound": list(reversed(path)),
                "selectedEdges": [] # <--- Fix crash (Quan trọng: bước này không có cạnh nào được chọn)
            })

    final_path = list(reversed(path))
    
    # Bước 3: Kết thúc
    if len(final_path) - 1 < len(edges):
         steps.append({
            "description": "Cảnh báo",
            "log": "⚠️ Đồ thị không liên thông hoàn toàn (Có cạnh bị cô lập).",
            "error": True,
            "visitedNodes": [], "selectedEdges": [] # <--- Fix crash
        })
    else:
        steps.append({
            "description": "Hoàn thành",
            "log": f"🏁 Chu trình Euler: {' -> '.join(final_path)}",
            "pathFound": final_path,
            "visitedNodes": final_path,
            "selectedEdges": [], # <--- Fix crash
            "currentNodeId": None
        })

    return steps