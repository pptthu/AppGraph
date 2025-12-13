import heapq

# =======================================================
# 0. HÀM KIỂM TRA LIÊN THÔNG 
# =======================================================
def check_connectivity(nodes, edges):
    if not nodes: return True
    if not edges and len(nodes) > 1: return False 
    
    # Xây dựng danh sách kề (Vô hướng)
    adj = {str(n['id']): [] for n in nodes}
    relevant_nodes = set()
    
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        adj[u].append(v)
        adj[v].append(u)
        relevant_nodes.add(u)
        relevant_nodes.add(v)
        
    if len(relevant_nodes) < len(nodes) and len(nodes) > 1:
        return False

    start_node = nodes[0]['id']
    visited = {start_node}
    queue = [start_node]
    
    while queue:
        u = queue.pop(0)
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
                
    return len(visited) == len(nodes)

# =======================================================
# 1. THUẬT TOÁN PRIM 
# =======================================================

def get_prim_heap_visual(min_heap):
    # Sắp xếp heap để hiển thị cho user dễ hiểu
    temp = sorted(min_heap, key=lambda x: x[0])
    return [f"{float(w)}: {u}-{v}" for w, u, v in temp]

def run_prim(nodes, edges, start_node, is_directed=False):
    steps = []
    
    # 1. Kiểm tra ràng buộc
    if is_directed:
        steps.append({
            "description": "Cảnh báo hướng",
            "log": "⚠️ Đồ thị có hướng -> Chuyển về vô hướng để chạy MST.",
            "visitedNodes": [], "selectedEdges": [], "structure": []
        })

    if not check_connectivity(nodes, edges):
        steps.append({
            "description": "Lỗi: Không liên thông", 
            "log": "❌ Đồ thị không liên thông! Không thể tìm cây khung.",
            "error": True,
            "visitedNodes": [], "selectedEdges": [], "structure": []
        })
        return steps

    # 2. Chuẩn bị dữ liệu 
    adj = {str(n['id']): [] for n in nodes}
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        # Ép kiểu float ngay tại đây để tránh lỗi so sánh chuỗi
        try:
            w = float(e.get('weight', 1))
        except:
            w = 1.0
            
        adj[u].append((v, w))
        adj[v].append((u, w))

    if not start_node:
        start_node = str(nodes[0]['id'])
    else:
        start_node = str(start_node)
        
    mst_edges = []      
    visited = set()     
    min_heap = []       
    total_weight = 0.0 # <-- Biến tích lũy trọng số
    
    # Khởi tạo từ đỉnh bắt đầu
    for neighbor, weight in adj[start_node]:
        heapq.heappush(min_heap, (weight, start_node, neighbor))
    
    visited.add(start_node)
    
    steps.append({
        "description": f"Bắt đầu từ {start_node}",
        "log": f"🏁 Khởi tạo Prim từ đỉnh {start_node}. Tổng trọng số = 0.",
        "visitedNodes": list(visited),
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": get_prim_heap_visual(min_heap)
    })

    # 3. Vòng lặp chính
    while min_heap:
        if len(visited) == len(nodes):
            break

        weight, u, v = heapq.heappop(min_heap)

        if v in visited:
            continue

        visited.add(v)
        mst_edges.append({"source": u, "target": v})
        total_weight += weight # <-- Cộng dồn trọng số

        steps.append({
            "description": f"Chọn ({u}, {v}) | w={weight}",
            "log": f"⚡ Chọn cạnh {u}-{v} (min={weight}). Tổng trọng số hiện tại: {total_weight}",
            "visitedNodes": list(visited),
            "currentNodeId": v,
            "selectedEdges": list(mst_edges),
            "structure": get_prim_heap_visual(min_heap)
        })

        for next_node, w in adj[v]:
            if next_node not in visited:
                heapq.heappush(min_heap, (w, v, next_node))

    # 4. Kết thúc
    steps.append({
        "description": f"Hoàn tất. Tổng trọng số = {total_weight}",
        "log": f"✅ Cây khung hoàn thành. TỔNG TRỌNG SỐ = {total_weight}. Số cạnh: {len(mst_edges)}.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": list(mst_edges),
        "structure": [] 
    })

    return steps


# =======================================================
# 2. THUẬT TOÁN KRUSKAL 
# =======================================================

def get_kruskal_list_visual(sorted_edges, current_idx):
    remaining = sorted_edges[current_idx:]
    return [f"{float(e['w'])}: {e['u']}-{e['v']}" for e in remaining[:6]]

def run_kruskal(nodes, edges, is_directed=False):
    steps = []
    
    if is_directed:
        steps.append({
            "description": "Cảnh báo hướng",
            "log": "⚠️ Cảnh báo: Đồ thị có hướng -> Chuyển về vô hướng.",
            "visitedNodes": [], "selectedEdges": [], "structure": []
        })

    if not check_connectivity(nodes, edges):
        steps.append({
            "description": "Lỗi: Không liên thông", 
            "log": "❌ Đồ thị không liên thông! Không thể tìm MST.",
            "error": True,
            "visitedNodes": [], "selectedEdges": [], "structure": []
        })
        return steps

    mst_edges = []
    total_weight = 0.0 # <-- Biến tích lũy
    
    # 1. Chuẩn bị dữ liệu
    unique_edges = []
    seen_edges = set()
    
    for e in edges:
        u, v = str(e['source']), str(e['target'])
        # ÉP KIỂU FLOAT ĐỂ SORT 
        try:
            w = float(e.get('weight', 1))
        except:
            w = 1.0
        
        edge_key = tuple(sorted((u, v)))
        if edge_key not in seen_edges:
            unique_edges.append({'u': u, 'v': v, 'w': w})
            seen_edges.add(edge_key)
            
    # Sắp xếp: Số thực sẽ so sánh đúng 
    sorted_edges = sorted(unique_edges, key=lambda x: x['w'])
    
    steps.append({
        "description": "Sắp xếp cạnh tăng dần",
        "log": f"📋 Đã sắp xếp {len(sorted_edges)} cạnh theo trọng số.",
        "visitedNodes": [],
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": get_kruskal_list_visual(sorted_edges, 0)
    })

    # 2. DSU
    parent = {str(n['id']): str(n['id']) for n in nodes}
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    # 3. Duyệt cạnh
    for idx, edge in enumerate(sorted_edges):
        u, v, w = edge['u'], edge['v'], edge['w']
        current_structure = get_kruskal_list_visual(sorted_edges, idx + 1)
        current_nodes = list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges]))

        if union(u, v):
            mst_edges.append({"source": u, "target": v})
            total_weight += w #  Cộng trọng số
            
            current_nodes = list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges]))

            steps.append({
                "description": f"Chọn ({u}, {v}) | w={w}",
                "log": f"⚡ Chọn cạnh {u}-{v} (w={w}). Tổng trọng số: {total_weight}",
                "visitedNodes": current_nodes,
                "currentNodeId": None, 
                "selectedEdges": list(mst_edges),
                "structure": current_structure
            })
        else:
             steps.append({
                "description": f"Bỏ qua ({u}, {v}) | w={w}",
                "log": f"⚠️ Bỏ qua cạnh {u}-{v} (Tạo chu trình).",
                "visitedNodes": current_nodes,
                "currentNodeId": None,
                "selectedEdges": list(mst_edges),
                "structure": current_structure
            })
            
        if len(mst_edges) == len(nodes) - 1:
            break

    # 4. Kết thúc
    final_nodes = list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges]))
    steps.append({
        "description": f"Hoàn tất. Tổng trọng số = {total_weight}",
        "log": f"✅ Cây khung hoàn thành. TỔNG TRỌNG SỐ = {total_weight}",
        "visitedNodes": final_nodes,
        "currentNodeId": None,
        "selectedEdges": list(mst_edges),
        "structure": [] 
    })

    return steps