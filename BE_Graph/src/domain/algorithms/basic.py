from collections import deque

# --- HÀM BỔ TRỢ: Tạo danh sách kề ---
def build_adjacency_list(nodes, edges, is_directed):
    adj = {node['id']: [] for node in nodes}
    for e in edges:
        source, target, weight = e['source'], e['target'], e.get('weight', 1)
        
        # Thêm cạnh xuôi
        if source in adj:
            adj[source].append({'neighbor': target, 'weight': weight})
        
        # Nếu vô hướng, thêm cạnh ngược
        if not is_directed and target in adj:
            adj[target].append({'neighbor': source, 'weight': weight})
            
    # Sắp xếp để duyệt thứ tự ổn định (A->B->C)
    for node_id in adj:
        adj[node_id].sort(key=lambda x: x['neighbor'])
        
    return adj

# =======================================================
# 1. BFS (DUYỆT CHIỀU RỘNG) - ĐÃ DÙNG KEY: structure
# =======================================================
def run_bfs(nodes, edges, start_node, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    
    queue = deque([start_node])
    visited = [start_node] 
    
    steps.append({
        "description": f"Bắt đầu BFS từ {start_node}. Đưa {start_node} vào hàng đợi.",
        "visitedNodes": list(visited),
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": list(queue) # <-- Dùng key 'structure'
    })

    while queue:
        u = queue.popleft()
        
        steps.append({
            "description": f"Lấy {u} ra khỏi hàng đợi để xét.",
            "visitedNodes": list(visited),
            "currentNodeId": u,
            "selectedEdges": [],
            "structure": list(queue) # <-- Dùng key 'structure'
        })

        for item in adj.get(u, []):
            v = item['neighbor']
            if v not in visited:
                visited.append(v)
                queue.append(v)
                
                steps.append({
                    "description": f"  -> Tìm thấy {v} (kề {u}), đưa vào hàng đợi.",
                    "visitedNodes": list(visited),
                    "currentNodeId": u,
                    "selectedEdges": [{"source": u, "target": v}],
                    "structure": list(queue) # <-- Dùng key 'structure'
                })

    steps.append({
        "description": "Hàng đợi rỗng. Hoàn tất thuật toán BFS.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": list(queue) # <-- Dùng key 'structure' (là mảng rỗng)
    })
    
    return steps

# =======================================================
# 2. DFS (DUYỆT CHIỀU SÂU) - ĐÃ DÙNG KEY: structure
# =======================================================
def run_dfs(nodes, edges, start_node, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    
    stack = [start_node]
    visited = [] 
    
    steps.append({
        "description": f"Bắt đầu DFS từ {start_node}. Đưa {start_node} vào Stack.",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": list(stack) # <-- Dùng key 'structure'
    })

    while stack:
        u = stack.pop()
        
        if u not in visited:
            visited.append(u)
            
            steps.append({
                "description": f"Lấy {u} ra khỏi Stack để thăm.",
                "visitedNodes": list(visited),
                "currentNodeId": u,
                "selectedEdges": [],
                "structure": list(stack) # <-- Dùng key 'structure'
            })

            # Đảo ngược để khi push vào stack, phần tử nhỏ hơn sẽ ở trên cùng (LIFO)
            neighbors = list(reversed(adj.get(u, [])))
            
            for item in neighbors:
                v = item['neighbor']
                if v not in visited:
                    stack.append(v)
                    steps.append({
                        "description": f"  -> Đẩy {v} (kề {u}) vào Stack chờ duyệt.",
                        "visitedNodes": list(visited),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(stack) # <-- Dùng key 'structure'
                    })

    steps.append({
        "description": "Stack rỗng. Hoàn tất thuật toán DFS.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": list(stack) # <-- Dùng key 'structure' (là mảng rỗng)
    })
    
    return steps

# =======================================================
# 3. DIJKSTRA (ĐƯỜNG ĐI NGẮN NHẤT)
# =======================================================
def run_dijkstra(nodes, edges, start_node, end_node, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    
    dist = {node['id']: float('inf') for node in nodes}
    parent = {node['id']: None for node in nodes}
    dist[start_node] = 0
    
    unvisited = set(node['id'] for node in nodes)
    visited_visual = []

    # Helper để tạo Priority Queue visual (Không phải Queue thật)
    def get_pq_visual(current_unvisited):
        pq = sorted([(n, dist[n]) for n in current_unvisited], key=lambda x: x[1])
        return [f"{n}:{int(d) if d != float('inf') else 'inf'}" for n, d in pq]

    steps.append({
        "description": f"Khởi tạo: Khoảng cách tại {start_node} = 0, các đỉnh khác = ∞.",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": get_pq_visual(unvisited) # <-- Dùng key 'structure'
    })

    while unvisited:
        u = min(unvisited, key=lambda node: dist[node])
        
        if dist[u] == float('inf'):
            break 
            
        unvisited.remove(u)
        visited_visual.append(u)

        steps.append({
            "description": f"Chọn đỉnh {u} có khoảng cách nhỏ nhất ({dist[u]}) để xét.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": u,
            "selectedEdges": [],
            "structure": get_pq_visual(unvisited) # <-- Dùng key 'structure'
        })

        if u == end_node:
            break

        for item in adj.get(u, []):
            v = item['neighbor']
            weight = float(item['weight'])
            
            if v in unvisited:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    steps.append({
                        "description": f"  -> Cập nhật {v}: KC mới = {dist[u]} + {weight} = {new_dist}.",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": get_pq_visual(unvisited) # <-- Dùng key 'structure'
                    })

    # --- TRUY VẾT ĐƯỜNG ĐI ---
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
            "description": f"Tìm thấy đường đi ngắn nhất: {path_str}. Tổng trọng số = {dist[end_node]}.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": path_edges,
            "pathFound": path_nodes,
            "structure": get_pq_visual(unvisited) # <-- Dùng key 'structure'
        })
    else:
        steps.append({
            "description": f"Không tìm thấy đường đi từ {start_node} đến {end_node}.",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": [],
            "structure": get_pq_visual(unvisited) # <-- Dùng key 'structure'
        })

    return steps

# =======================================================
# 4. KIỂM TRA ĐỒ THỊ 2 PHÍA (BIPARTITE) - ĐÃ DÙNG KEY: structure
# =======================================================
def check_bipartite(nodes, edges, start_node=None, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, False) 
    
    colors = {} 
    visited_visual = []
    
    for node in nodes:
        start_node_id = node['id']
        if start_node_id in colors:
            continue
            
        queue = deque([start_node_id])
        colors[start_node_id] = 0
        visited_visual.append(start_node_id)
        
        steps.append({
            "description": f"Xét thành phần liên thông mới từ {start_node_id}. Gán màu ĐỎ (0).",
            "visitedNodes": list(visited_visual),
            "currentNodeId": start_node_id,
            "selectedEdges": [],
            "structure": list(queue) # <-- Dùng key 'structure'
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
                        "description": f"  -> Tô màu đỉnh kề {v} là {color_name} (Ngược màu với {u}).",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(queue) # <-- Dùng key 'structure'
                    })
                elif colors[v] == colors[u]:
                    steps.append({
                        "description": f"❌ MÂU THUẪN: Đỉnh {u} và {v} kề nhau nhưng cùng màu! Không phải đồ thị 2 phía.",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": v, 
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(queue) # <-- Dùng key 'structure'
                    })
                    return steps 

    steps.append({
        "description": "✅ Đã duyệt xong toàn bộ. Không có mâu thuẫn. ĐÂY LÀ ĐỒ THỊ 2 PHÍA.",
        "visitedNodes": list(visited_visual),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": list(queue) # <-- Dùng key 'structure'
    })
    
    return steps