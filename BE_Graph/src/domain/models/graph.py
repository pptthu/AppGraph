class Graph:
    def __init__(self):
        # Dùng dictionary để lưu danh sách kề: {node: {neighbor: weight}}
        self.adj_list = {} 
        self.is_directed = False

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = {}

    def add_edge(self, u, v, weight=1):
        self.add_node(u)
        self.add_node(v)
        self.adj_list[u][v] = weight
        if not self.is_directed:
            self.adj_list[v][u] = weight

    def from_matrix(self, matrix):
        # TODO: Người 1 viết code chuyển từ Ma trận kề -> Danh sách kề tại đây
        pass

    def to_edge_list(self):
        # TODO: Người 1 viết code trả về danh sách cạnh
        pass