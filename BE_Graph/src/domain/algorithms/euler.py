import copy

# ==========================================
# 1. HÀM PHỤ TRỢ (KIỂM TRA & CHECK CẦU)
# ==========================================

# (Giữ nguyên get_euler_status, is_bridge, count_reachable)
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
# 2. THUẬT TOÁN FLEURY (FIX LỖI CÚ PHÁP & LOG)
# ==========================================

def run_fleury(nodes, edges, is_directed=False):
    steps = []
    
    euler_type, start_node, error = get_euler_status(nodes, edges, is_directed)
    
    if error:
        steps.append({
            "description": "Lỗi", 
            "log": f"❌ {error}", 
            "error": True,
            "visitedNodes": [], "selectedEdges": []
        })
        return steps
        
    # Bước 1: Khởi tạo
    path = [start_node]
    steps.append({
        "description": f"Bắt đầu Fleury: {euler_type} thỏa mãn. Bắt đầu từ {start_node}",
        "log": f"✅ Đồ thị thỏa mãn ({euler_type}).",
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

    # Bước 2: Vòng lặp
    while edges_traversed < total_edges:
        if not adj[curr]: break 

        next_v = -1
        neighbors = adj[curr]
        
        # KHỞI TẠO BIẾN TRƯỚC VÒNG LẶP/KIỂM TRA
        is_bridge_edge = False
        
        if len(neighbors) == 1:
            # Trường hợp 1: Chỉ còn 1 cạnh, phải đi
            next_v = neighbors[0]
            is_bridge_edge = True 
        else:
            # Trường hợp 2: Có nhiều hơn 1 cạnh
            if not is_directed:
                # 2a. Ưu tiên cạnh KHÔNG phải cầu (non-bridge)
                for v in neighbors:
                    if not is_bridge(curr, v, adj):
                        next_v = v
                        is_bridge_edge = False
                        break
            
            # 2b. Nếu là đồ thị có hướng HOẶC (vẫn là vô hướng & không tìm thấy non-bridge)
            if next_v == -1: 
                next_v = neighbors[0] # Chọn cạnh đầu tiên (chắc chắn là cầu hoặc là lựa chọn duy nhất)
                is_bridge_edge = True
        
        # --- THỰC HIỆN BƯỚC ĐI ---
        adj[curr].remove(next_v)
        if not is_directed: adj[next_v].remove(curr)
        edges_traversed += 1
        
        path.append(next_v) 
        
        log_detail = "Áp dụng Quy tắc Fleury: Chọn cạnh KHÔNG là cầu."
        if is_bridge_edge:
             log_detail = "Buộc phải đi qua cầu (hoặc chỉ còn 1 đường, hoặc đồ thị có hướng)."
        
        steps.append({
            "description": f"Xét tại {curr}. Chọn cạnh {curr} -> {next_v}. ({'Cầu' if is_bridge_edge else 'Không cầu'})",
            "log": f"Đi: {curr} -> {next_v}. {log_detail}",
            "visitedNodes": [curr, next_v],
            "selectedEdges": [{"source": curr, "target": next_v}],
            "currentNodeId": next_v,
            "pathFound": copy.deepcopy(path),
            "structure": copy.deepcopy(path) 
        })
        
        curr = next_v

    # Bước 3: Hoàn thành
    steps.append({
        "description": "Hoàn thành duyệt",
        "log": f"🏁 CHU TRÌNH EULER: {' -> '.join(path)}. Hoàn thành tất cả {total_edges} cạnh.",
        "pathFound": path,
        "visitedNodes": path,
        "selectedEdges": [], 
        "currentNodeId": None,
        "structure": path
    })
    return steps

# ==========================================
# 3. THUẬT TOÁN HIERHOLZER (FIX LOG & STRUCTURE)
# ==========================================

def run_hierholzer(nodes, edges, is_directed=False):
    steps = []
    
    euler_type, start_node, error = get_euler_status(nodes, edges, is_directed)
    if error:
        steps.append({
            "description": "Lỗi", "log": f"❌ {error}", "error": True,
            "visitedNodes": [], "selectedEdges": []
        })
        return steps

    # Bước 1: Khởi tạo
    steps.append({
        "description": "Khởi tạo Hierholzer",
        "log": f"✅ Bắt đầu Hierholzer (dùng Stack) từ {start_node}",
        "visitedNodes": [start_node],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "pathFound": [],
        "structure": [start_node] 
    })

    adj = {str(n['id']): [] for n in nodes}
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        if not is_directed: adj[v].append(u)

    circuit = [] 
    stack = [start_node]
    
    # Bước 2: Vòng lặp (DFS)
    while stack:
        u = stack[-1] 
        
        if adj.get(u): 
            v = adj[u].pop(0) 
            
            if not is_directed:
                if u in adj[v]: adj[v].remove(u)
            
            stack.append(v) 
            
            steps.append({
                "description": f"Duyệt sâu: {u} -> {v}. Đẩy {v} vào Stack.",
                "log": f"Tiếp tục DFS. Cạnh {u}-{v} được chọn.",
                "visitedNodes": [u, v],
                "selectedEdges": [{"source": u, "target": v}],
                "currentNodeId": v,
                "pathFound": list(reversed(circuit)) + stack,
                "structure": list(stack) 
            })
        else:
            finished_node = stack.pop()
            circuit.append(finished_node)
            
            steps.append({
                "description": f"Backtrack: Đỉnh {finished_node} hết cạnh. Đưa vào Chu trình.",
                "log": f"Quay lui, nối chu trình con vào {finished_node}.",
                "visitedNodes": [finished_node],
                "currentNodeId": stack[-1] if stack else None,
                "pathFound": list(reversed(circuit)),
                "selectedEdges": [],
                "structure": list(stack) 
            })

    final_path = list(reversed(circuit))
    
    # Bước 3: Kết thúc
    if len(final_path) - 1 < len(edges):
         steps.append({
            "description": "Cảnh báo",
            "log": "⚠️ Đồ thị không liên thông hoàn toàn (Có cạnh bị cô lập).",
            "error": True,
            "visitedNodes": [], "selectedEdges": []
        })
    else:
        steps.append({
            "description": "Hoàn thành",
            "log": f"🏁 CHU TRÌNH EULER: {' -> '.join(final_path)}. Tổng số cạnh: {len(edges)}.",
            "pathFound": final_path,
            "visitedNodes": final_path,
            "selectedEdges": [], 
            "currentNodeId": None,
            "structure": []
        })

    return steps