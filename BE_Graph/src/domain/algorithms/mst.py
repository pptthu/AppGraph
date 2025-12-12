import heapq

# =======================================================
# 1. THUẬT TOÁN PRIM
# =======================================================
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
    
    # Helper: Hiển thị trạng thái Heap (Priority Queue)
    def get_heap_visual():
        # Hiển thị tối đa 5 phần tử đầu của Heap: "w: u-v"
        return [f"{w}: {u}-{v}" for w, u, v in min_heap[:5]]
    
    # Bắt đầu từ start_node
    for neighbor, weight in adj[start_node]:
        heapq.heappush(min_heap, (weight, start_node, neighbor))
    
    visited.add(start_node)
    
    steps.append({
        "description": f"Khởi tạo Prim từ đỉnh {start_node}. Thêm các cạnh kề vào hàng đợi ưu tiên.",
        "visitedNodes": list(visited),
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": get_heap_visual() # <--- Trả về Heap
    })

    # 3. Vòng lặp chính
    while min_heap:
        if len(visited) == len(nodes):
            break

        # Snapshot Heap TRƯỚC khi pop để hiển thị cho người dùng thấy có gì trong đó
        current_structure = get_heap_visual()

        weight, u, v = heapq.heappop(min_heap)

        if v in visited:
            continue

        visited.add(v)
        mst_edges.append({"source": u, "target": v})

        steps.append({
            "description": f"Chọn cạnh ({u}, {v}) trọng số {weight} nhỏ nhất trong hàng đợi.",
            "visitedNodes": list(visited),
            "currentNodeId": v,
            "selectedEdges": list(mst_edges),
            "structure": current_structure # <--- Hiển thị Heap tại thời điểm xét
        })

        for next_node, w in adj[v]:
            if next_node not in visited:
                heapq.heappush(min_heap, (w, v, next_node))

    # Bước kết thúc
    steps.append({
        "description": f"Hoàn tất Prim. Tổng số cạnh: {len(mst_edges)}.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": list(mst_edges),
        "structure": [] # Heap rỗng hoặc đã xong
    })

    return steps


# =======================================================
# 2. THUẬT TOÁN KRUSKAL
# =======================================================
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
    
    # Helper: Hiển thị danh sách cạnh đang chờ xét (Sorted List)
    def get_list_visual(current_idx):
        # Lấy các cạnh từ vị trí hiện tại trở đi (tối đa 5 cạnh)
        remaining = sorted_edges[current_idx:]
        return [f"{e['w']}: {e['u']}-{e['v']}" for e in remaining[:5]]
    
    steps.append({
        "description": "Sắp xếp tất cả các cạnh theo trọng số tăng dần.",
        "visitedNodes": [],
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": get_list_visual(0) # <--- Trả về danh sách đã sort
    })

    # 2. Khởi tạo DSU (Union-Find)
    parent = {node['id']: node['id'] for node in nodes}
    
    def find(i):
        if parent[i] == i:
            return i
        return find(parent[i])

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    # 3. Duyệt qua các cạnh đã sắp xếp
    for idx, edge in enumerate(sorted_edges):
        u, v, w = edge['u'], edge['v'], edge['w']
        
        # Lấy danh sách cạnh còn lại (từ idx hiện tại)
        current_structure = get_list_visual(idx)
        
        if union(u, v):
            mst_edges.append({"source": u, "target": v})
            
            visited_visual = list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges]))

            steps.append({
                "description": f"Xét cạnh ({u}, {v}) trọng số {w}: Không tạo chu trình -> CHỌN.",
                "visitedNodes": visited_visual,
                "currentNodeId": None, 
                "selectedEdges": list(mst_edges),
                "structure": current_structure # <--- Cập nhật structure
            })
        else:
             steps.append({
                "description": f"Xét cạnh ({u}, {v}) trọng số {w}: Tạo chu trình -> BỎ QUA.",
                "visitedNodes": list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges])),
                "currentNodeId": None,
                "selectedEdges": list(mst_edges),
                "structure": current_structure # <--- Cập nhật structure
            })

    # Bước kết thúc
    steps.append({
        "description": f"Hoàn tất Kruskal. Cây khung gồm {len(mst_edges)} cạnh.",
        "visitedNodes": list(set([e['source'] for e in mst_edges] + [e['target'] for e in mst_edges])),
        "currentNodeId": None,
        "selectedEdges": list(mst_edges),
        "structure": []
    })

    return steps