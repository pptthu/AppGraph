from collections import deque
import math

# --- HÀM BỔ TRỢ: Tạo danh sách kề từ dữ liệu thô ---
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
# 1. BFS (DUYỆT CHIỀU RỘNG)
# =======================================================
def run_bfs(nodes, edges, start_node, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    
    queue = deque([start_node])
    visited = [start_node] 
    
    # Bước 1: Khởi tạo (u, v chưa tồn tại ở đây -> selectedEdges rỗng)
    steps.append({
        "description": f"Khởi tạo BFS: Đưa {start_node} vào hàng đợi",
        "visitedNodes": list(visited),
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": list(queue)
    })

    while queue:
        current_structure = list(queue)
        u = queue.popleft()
        
        # Bước 2: Lấy ra khỏi hàng đợi
        steps.append({
            "description": f"Đang xét đỉnh {u} (Lấy ra khỏi Queue)",
            "visitedNodes": list(visited),
            "currentNodeId": u,
            "selectedEdges": [],
            "structure": current_structure
        })

        for item in adj.get(u, []):
            v = item['neighbor']
            if v not in visited:
                visited.append(v)
                queue.append(v)
                
                # Bước 3: Thăm láng giềng (u và v đã tồn tại -> tô màu cạnh u-v)
                steps.append({
                    "description": f"  -> Thăm đỉnh kề {v}, thêm vào Queue",
                    "visitedNodes": list(visited),
                    "currentNodeId": u,
                    "selectedEdges": [{"source": u, "target": v}],
                    "structure": list(queue)
                })

    steps.append({
        "description": "Hàng đợi rỗng. Hoàn tất BFS.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": []
    })
    
    return steps

# =======================================================
# 2. DFS (DUYỆT CHIỀU SÂU)
# =======================================================
def run_dfs(nodes, edges, start_node, end_node=None, is_directed=False):
    steps = []
    adj = build_adjacency_list(nodes, edges, is_directed)
    
    stack = [start_node]
    visited = [] 
    
    # Bước 1: Khởi tạo (u, v chưa có -> selectedEdges rỗng)
    steps.append({
        "description": f"Khởi tạo DFS: Đưa {start_node} vào Stack",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": list(stack)
    })

    while stack:
        current_structure = list(stack)
        u = stack.pop()
        
        if u not in visited:
            visited.append(u)
            
            # Bước 2: Thăm đỉnh
            steps.append({
                "description": f"Thăm đỉnh {u} (Lấy ra khỏi Stack)",
                "visitedNodes": list(visited),
                "currentNodeId": u,
                "selectedEdges": [],
                "structure": current_structure
            })

            neighbors = list(reversed(adj.get(u, [])))
            
            for item in neighbors:
                v = item['neighbor']
                if v not in visited:
                    stack.append(v)
                    # Bước 3: Đẩy vào stack (u và v đã có -> tô màu cạnh u-v)
                    steps.append({
                        "description": f"  -> Đẩy đỉnh kề {v} vào Stack",
                        "visitedNodes": list(visited),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(stack)
                    })

    steps.append({
        "description": "Stack rỗng. Hoàn tất DFS.",
        "visitedNodes": list(visited),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": []
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

    # Helper để tạo string hiển thị Priority Queue giả lập: ["A: 0", "B: inf", ...]
    def get_pq_visual():
        # Lấy các đỉnh chưa thăm, sắp xếp theo khoảng cách
        pq = sorted([(n, dist[n]) for n in unvisited], key=lambda x: x[1])
        # Chỉ lấy những đỉnh có khoảng cách < inf để hiển thị cho gọn
        return [f"{n}:{d}" for n, d in pq if d != float('inf')]
    
    # Bước 1: Khởi tạo (u, v chưa có -> selectedEdges rỗng)
    steps.append({
        "description": f"Khởi tạo: Khoảng cách tại {start_node} = 0, các đỉnh khác = ∞",
        "visitedNodes": [],
        "currentNodeId": start_node,
        "selectedEdges": [],
        "structure": get_pq_visual()
    })

    while unvisited:
        u = min(unvisited, key=lambda node: dist[node])
        
        if dist[u] == float('inf'):
            break 
            
        unvisited.remove(u)
        visited_visual.append(u)

        # Bước 2: Chọn đỉnh xét
        steps.append({
            "description": f"Chọn đỉnh {u} (dist={dist[u]}) để xét",
            "visitedNodes": list(visited_visual),
            "currentNodeId": u,
            "selectedEdges": [],
            "structure": get_pq_visual()
        })

        if u == end_node:
            steps.append({
                "description": f"Đã đến đích {end_node}!",
                "visitedNodes": list(visited_visual),
                "currentNodeId": u,
                "selectedEdges": [],
                
            })
            break

        for item in adj.get(u, []):
            v = item['neighbor']
            weight = float(item['weight'])
            
            if v in unvisited:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    # Bước 3: Cập nhật khoảng cách (u và v đã có -> tô màu cạnh)
                    steps.append({
                        "description": f"  -> Cập nhật {v}: dist giảm xuống {new_dist}",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": get_pq_visual()
                    })

    # --- TRUY VẾT ĐƯỜNG ĐI ---
    path_edges = []
    if dist[end_node] != float('inf'):
        curr = end_node
        while parent[curr] is not None:
            prev = parent[curr]
            path_edges.append({"source": prev, "target": curr})
            curr = prev
        
        steps.append({
            "description": f"Hoàn tất! Tổng trọng số = {dist[end_node]}",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": path_edges 
        })
    else:
        steps.append({
            "description": f"Không tìm thấy đường đi từ {start_node} đến {end_node}",
            "visitedNodes": list(visited_visual),
            "currentNodeId": None,
            "selectedEdges": []
        })

    return steps

# =======================================================
# 4. KIỂM TRA ĐỒ THỊ 2 PHÍA (BIPARTITE)
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
            "description": f"Bắt đầu kiểm tra từ {start_node_id}. Gán màu ĐỎ (0)",
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
                        "description": f"  -> Đỉnh kề {v} chưa tô: Gán màu {color_name} ({colors[v]})",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": u,
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": list(queue)
                    })
                elif colors[v] == colors[u]:
                    steps.append({
                        "description": f"PHÁT HIỆN MÂU THUẪN! Đỉnh {u} và {v} cùng màu.",
                        "visitedNodes": list(visited_visual),
                        "currentNodeId": v, 
                        "selectedEdges": [{"source": u, "target": v}],
                        "structure": [] # Queue rỗng khi dừng
                    })
                    return steps 

    steps.append({
        "description": "Đã duyệt xong. ĐÂY LÀ đồ thị 2 phía hợp lệ.",
        "visitedNodes": list(visited_visual),
        "currentNodeId": None,
        "selectedEdges": [],
        "structure": [] # Queue rỗng khi xong
    })
    
    return steps