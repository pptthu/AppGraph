from src.domain.models.graph import Graph
import json
import os

class GraphService:
    @staticmethod
    def create_graph_from_json(json_data):
        """Chuyển JSON từ FE thành Object Graph"""
        graph = Graph()
        # Giả sử FE gửi: { "nodes": [{"id": "A"}, ...], "edges": [{"source": "A", "target": "B", "weight": 5}] }
        
        nodes = json_data.get("nodes", [])
        edges = json_data.get("edges", [])

        for node in nodes:
            graph.add_node(node.get("id"))
        
        for edge in edges:
            u = edge.get("source")
            v = edge.get("target")
            w = edge.get("weight", 1)
            graph.add_edge(u, v, w)
            
        return graph

    @staticmethod
    def save_graph_to_file(json_data, filename="graph_data.json"):
        """Lưu đồ thị xuống file (Yêu cầu chức năng số 2)"""
        try:
            with open(filename, 'w') as f:
                json.dump(json_data, f)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False