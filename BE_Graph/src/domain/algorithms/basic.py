from collections import deque
import heapq

# --- HÀM BỔ TRỢ ---
def build_adjacency_list(nodes, edges, is_directed):
    adj = {str(node['id']): [] for node in nodes}
    for e in edges:
        source = str(e['source'])
        target = str(e['target'])
        try:
            weight = float(e.get('weight', 1))
        except:
            weight = 1.0

        if source in adj:
            adj[source].append({'neighbor': target, 'weight': weight})
        
        if not is_directed:
            if target in adj:
                adj[target].append({'neighbor': source, 'weight': weight})
                
    # Sắp xếp alpha-beta để thứ tự duyệt ổn định, dễ theo dõi
    for node_id in adj:
        adj[node_id].sort(key=lambda x: x['neighbor'])
        
    return adj

# =======================================================
# 1. BFS (DUYỆT CHIỀU RỘNG) - CÓ THỨ TỰ DUYỆT
# =======================================================
def run_bfs(nodes, edges, start_node, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    start_node = str(start_node)
    
    queue = deque([start_node])
    visited = [start_node] 
    
    steps.append({
        "description": f"Bắt đầu BFS từ {start_node}.",
        "log": f"🏁 Khởi tạo hàng đợi: [{start_node}]",
        "visitedNodes": list(visited),
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": list(queue)
    })

    while queue:
        u = queue.popleft()
        
        steps.append({
            "description": f"Lấy {u} ra khỏi hàng đợi.",
            "log": f"Đang xét đỉnh {u}. Hàng đợi: {list(queue)}",
            "visitedNodes": list(visited),
            "currentNodeId": u,
            "selectedEdges": [],
            "structure": list(queue)
        })

        if str(end_node) and u == str(end_node):
            path_str = " -> ".join(visited)
            steps.append({
                "description": f"Đã tìm thấy đích {u}! Thứ tự: {path_str}",
                "log": f"✅ Tìm thấy đích {u}. Dừng thuật toán.",
                "visitedNodes": list(visited),
                "currentNodeId": u,
                "selectedEdges": [],
                "structure": list(queue)
            })
            return steps

        for item in adj.get(u, []):
            v = item['neighbor']
            if v not in visited:
                visited.append(v)
                queue.append(v)
                steps.append({
                    "description": f"-> Thăm {v} (kề {u}).",
                    "log": f"Thêm {v} vào hàng đợi.",
                    "visitedNodes": list(visited),
                    "currentNodeId": u,
                    "selectedEdges": [{"source": u, "target": v}],
                    "structure": list(queue)
                })

    # --- TỔNG KẾT RÕ RÀNG ---
    traversal_order = " -> ".join(visited)
    steps.append({
        "description": f"Hoàn thành BFS. Thứ tự duyệt: {traversal_order}",
        "log": f"✅ Duyệt xong. Tổng số đỉnh đã thăm: {len(visited)}.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": list(queue)
    })
    return steps

# =======================================================
# 2. DFS (DUYỆT CHIỀU SÂU) - CÓ THỨ TỰ DUYỆT
# =======================================================
def run_dfs(nodes, edges, start_node, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    start_node = str(start_node)
    
    stack = [start_node]
    visited = [] 
    
    steps.append({
        "description": f"Bắt đầu DFS từ {start_node}.",
        "log": f"🏁 Khởi tạo Stack: [{start_node}]",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": list(stack)
    })

    while stack:
        u = stack.pop()
        
        if u not in visited:
            visited.append(u)
            
            steps.append({
                "description": f"Lấy {u} khỏi Stack để duyệt.",
                "log": f"Đang xét đỉnh {u}. Stack: {stack}",
                "visitedNodes": list(visited),
                "currentNodeId": u,
                "selectedEdges": [],
                "structure": list(stack)
            })

            if str(end_node) and u == str(end_node):
                path_str = " -> ".join(visited)
                steps.append({
                    "description": f"Đã tìm thấy đích {u}! Thứ tự: {path_str}",
                    "log": f"✅ Tìm thấy đích {u}. Dừng thuật toán.",
                    "visitedNodes": list(visited),
                    "currentNodeId": u,
                    "selectedEdges": [],
                    "structure": list(stack)
                })
                return steps

            # Đảo ngược danh sách kề để khi push vào stack, phần tử nhỏ hơn sẽ được pop ra trước
            neighbors = list(reversed(adj.get(u, [])))
            
            for item in neighbors:
                v = item['neighbor']
                if v not in visited:
                    stack.append(v)
                    steps.append({
                        "description": f"-> Đẩy {v} vào Stack.",
                        "log": f"Phát hiện {v} kề {u}. Thêm vào Stack.",
                        "visitedNodes": list(visited),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(stack)
                    })

    # --- TỔNG KẾT RÕ RÀNG ---
    traversal_order = " -> ".join(visited)
    steps.append({
        "description": f"Hoàn thành DFS. Thứ tự duyệt: {traversal_order}",
        "log": f"✅ Duyệt xong. Tổng số đỉnh đã thăm: {len(visited)}.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": list(stack)
    })
    return steps

# =======================================================
# 3. DIJKSTRA (ĐƯỜNG ĐI NGẮN NHẤT)
# =======================================================
def run_dijkstra(nodes, edges, start_node, end_node, is_directed=False):
    steps = []
    
    # Check trọng số âm
    for e in edges:
        try:
            w = float(e.get('weight', 0))
        except:
            w = 0
        if w < 0:
            steps.append({
                "description": "Lỗi Dữ Liệu",
                "log": "❌ Dijkstra không hỗ trợ trọng số âm! Vui lòng sửa lại.",
                "error": True,
                "visitedNodes": [],
                "currentNodeId": None,
                "selectedEdges": [],
                "structure": ["ERROR"]
            })
            return steps

    start_node = str(start_node)
    end_node = str(end_node)
    adj = build_adjacency_list(nodes, edges, is_directed)
    
    dist = {str(node['id']): float('inf') for node in nodes}
    parent = {str(node['id']): None for node in nodes}
    dist[start_node] = 0
    
    unvisited = set(str(node['id']) for node in nodes)
    visited_visual = []

    def get_pq_visual(current_unvisited):
        pq = sorted([(n, dist[n]) for n in current_unvisited], key=lambda x: x[1])
        return [f"{n}:{int(d) if d != float('inf') else 'inf'}" for n, d in pq]

    steps.append({
        "description": f"Khởi tạo: {start_node}=0, còn lại=∞.",
        "log": f"🏁 Bắt đầu tìm đường từ {start_node}.",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": get_pq_visual(unvisited)
    })

    while unvisited:
        u = min(unvisited, key=lambda node: dist[node])
        
        if dist[u] == float('inf'):
            break 
            
        unvisited.remove(u)
        visited_visual.append(u)

        steps.append({
            "description": f"Chọn {u} (dist={dist[u]}) nhỏ nhất.",
            "log": f"⚡ Xét đỉnh {u} có khoảng cách nhỏ nhất.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": u,
            "selectedEdges": [],
            "structure": get_pq_visual(unvisited)
        })

        if u == end_node:
            break

        for item in adj.get(u, []):
            v = item['neighbor']
            weight = item['weight']
            
            if v in unvisited:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    steps.append({
                        "description": f"Cập nhật {v}: {dist[u]} + {weight} = {new_dist}.",
                        "log": f"-> Cập nhật {v} (Cost: {new_dist}).",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": get_pq_visual(unvisited)
                    })

    # Truy vết
    path_edges = []
    path_nodes = [] 
    if dist[end_node] != float('inf'):
        curr = end_node
        path_nodes.append(curr)
        while parent[curr] is not None:
            prev = parent[curr]
            path_edges.append({"source": prev, "target": curr})
            curr = prev
            path_nodes.append(curr)
        path_nodes.reverse()
        path_str = " -> ".join(path_nodes)
        
        steps.append({
            "description": f"Hoàn tất. Đường đi: {path_str}",
            "log": f"✅ Tổng trọng số = {dist[end_node]}.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": path_edges,
            "pathFound": path_nodes,
            "structure": get_pq_visual(unvisited)
        })
    else:
        steps.append({
            "description": f"Không tìm thấy đường đi đến {end_node}.",
            "log": "❌ Không có đường đi.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": [],
            "structure": get_pq_visual(unvisited)
        })
        
    return steps

# =======================================================
# 4. KIỂM TRA 2 PHÍA
# =======================================================
def check_bipartite(nodes, edges, start_node=None, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed=False) 
    colors = {} 
    visited_visual = []
    
    is_bipartite = True

    for node in nodes:
        start_node_id = str(node['id'])
        if start_node_id in colors: continue
        
        queue = deque([start_node_id])
        colors[start_node_id] = 0
        visited_visual.append(start_node_id)
        
        steps.append({
            "description": f"Xét thành phần mới từ {start_node_id}.",
            "log": f"Gán màu ĐỎ (0) cho {start_node_id}.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": start_node_id,
            "selectedEdges": [],
            "structure": list(queue)
        })
        
        while queue:
            u = queue.popleft()
            for item in adj.get(u, []):
                v = item['neighbor']
                if v not in colors:
                    colors[v] = 1 - colors[u] 
                    visited_visual.append(v)
                    queue.append(v)
                    color_name = "XANH" if colors[v] == 1 else "ĐỎ"
                    steps.append({
                        "description": f"Tô màu {v} là {color_name}.",
                        "log": f"-> {u} nối {v} -> Tô {v} màu {color_name}.",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(queue)
                    })
                elif colors[v] == colors[u]:
                    is_bipartite = False
                    steps.append({
                        "description": f"Mâu thuẫn tại {u}-{v}!",
                        "log": f"❌ {u} và {v} cùng màu -> KHÔNG PHẢI 2 PHÍA.",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": v, 
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(queue)
                    })
                    return steps 

    if is_bipartite:
        steps.append({
            "description": "Hoàn tất: Đồ thị 2 Phía.",
            "log": "✅ Không có mâu thuẫn màu.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": [],
            "structure": list(queue)
        })
    return steps