import heapq

# =======================================================
# 1. THUẬT TOÁN PRIM (ĐÃ THÊM KEY: structure)
# =======================================================

# Helper: Hiển thị trạng thái Heap (Priority Queue)
def get_prim_heap_visual(min_heap):
    # Lấy các cạnh trong heap, sắp xếp lại để hiển thị (w, u, v)
    temp = sorted(min_heap, key=lambda x: x[0])
    # Format: "w: u-v"
    return [f"{int(w)}: {u}-{v}" for w, u, v in temp]

def run_prim(nodes, edges, start_node, is_directed=False):
    steps = []
    
    # 1. Chuyển đổi dữ liệu sang Danh sách kề
    adj = {node['id']: [] for node in nodes}
    for e in edges:
        u, v, w = e['source'], e['target'], float(e.get('weight', 1))
        adj[u].append((v, w))
        adj[v].append((u, w)) 

    # 2. Khởi tạo
    if not start_node:
        start_node = nodes[0]['id']
        
    mst_edges = []      
    visited = set()     
    min_heap = []       
    
    # Bắt đầu từ start_node
    for neighbor, weight in adj[start_node]:
        heapq.heappush(min_heap, (weight, start_node, neighbor))
    
    visited.add(start_node)
    
    steps.append({
        "description": f"Khởi tạo Prim từ đỉnh {start_node}. Thêm các cạnh kề vào hàng đợi ưu tiên.",
        "visitedNodes": list(visited),
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": get_prim_heap_visual(min_heap) # <-- ĐÃ THÊM
    })

    # 3. Vòng lặp chính
    while min_heap:
        if len(visited) == len(nodes):
            break

        weight, u, v = heapq.heappop(min_heap)

        if v in visited:
            # Cạnh bị loại do tạo chu trình (nối vào đỉnh đã xét)
            continue

        visited.add(v)
        mst_edges.append({"source": u, "target": v})

        steps.append({
            "description": f"Chọn cạnh ({u}, {v}) trọng số {weight} nhỏ nhất trong hàng đợi.",
            "visitedNodes": list(visited),
            "currentNodeId": v,
            "selectedEdges": list(mst_edges),
            "structure": get_prim_heap_visual(min_heap) # <-- ĐÃ THÊM
        })

        for next_node, w in adj[v]:
            if next_node not in visited:
                # Đẩy cạnh mới vào heap
                heapq.heappush(min_heap, (w, v, next_node))

    # Bước kết thúc
    steps.append({
        "description": f"Hoàn tất Prim. Tổng số cạnh: {len(mst_edges)}.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": list(mst_edges),
        "structure": get_prim_heap_visual(min_heap) # <-- ĐÃ THÊM (Heap rỗng)
    })

    return steps


# =======================================================
# 2. THUẬT TOÁN KRUSKAL (ĐÃ THÊM KEY: structure)
# =======================================================

# Helper: Hiển thị danh sách cạnh đang chờ xét (Sorted List)
def get_kruskal_list_visual(sorted_edges, current_idx):
    # Chỉ hiển thị 5 cạnh đầu tiên chưa xét
    remaining = sorted_edges[current_idx:]
    # Format: "w: u-v"
    return [f"{int(e['w'])}: {e['u']}-{e['v']}" for e in remaining[:5]]


def run_kruskal(nodes, edges, is_directed=False):
    steps = []
    mst_edges = []
    
    # 1. Chuẩn bị danh sách cạnh và sắp xếp
    unique_edges = []
    seen_edges = set()
    
    for e in edges:
        u, v, w = e['source'], e['target'], float(e.get('weight', 1))
        edge_key = tuple(sorted((u, v)))
        if edge_key not in seen_edges:
            unique_edges.append({'u': u, 'v': v, 'w': w})
            seen_edges.add(edge_key)
            
    # Sắp xếp tăng dần theo trọng số
    sorted_edges = sorted(unique_edges, key=lambda x: x['w'])
    
    steps.append({
        "description": "Sắp xếp tất cả các cạnh theo trọng số tăng dần.",
        "visitedNodes": [],
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": get_kruskal_list_visual(sorted_edges, 0) # <-- ĐÃ THÊM
    })

    # 2. Khởi tạo DSU (Union-Find)
    parent = {node['id']: node['id'] for node in nodes}
    
    def find(i):
        if parent[i] == i:
            return i
        # Path compression (tối ưu)
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            # Union by rank/size (tối ưu)
            parent[root_i] = root_j
            return True
        return False

    # 3. Duyệt qua các cạnh đã sắp xếp
    for idx, edge in enumerate(sorted_edges):
        u, v, w = edge['u'], edge['v'], edge['w']
        
        current_structure = get_kruskal_list_visual(sorted_edges, idx + 1)
        
        if union(u, v):
            mst_edges.append({"source": u, "target": v})
            
            visited_visual = list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges]))

            steps.append({
                "description": f"Xét cạnh ({u}, {v}) trọng số {w}: Không tạo chu trình -> CHỌN.",
                "visitedNodes": visited_visual,
                "currentNodeId": None, 
                "selectedEdges": list(mst_edges),
                "structure": current_structure # <-- ĐÃ THÊM
            })
        else:
             steps.append({
                "description": f"Xét cạnh ({u}, {v}) trọng số {w}: Tạo chu trình -> BỎ QUA.",
                "visitedNodes": list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges])),
                "currentNodeId": None,
                "selectedEdges": list(mst_edges),
                "structure": current_structure # <-- ĐÃ THÊM
            })

    # Bước kết thúc
    steps.append({
        "description": f"Hoàn tất Kruskal. Cây khung gồm {len(mst_edges)} cạnh.",
        "visitedNodes": list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges])),
        "currentNodeId": None,
        "selectedEdges": list(mst_edges),
        "structure": [] # <--- ĐÃ THÊM (Danh sách rỗng)
    })

    return steps