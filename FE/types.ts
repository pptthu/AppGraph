// Định nghĩa kiểu dữ liệu cho một bước mô phỏng thuật toán
export interface AlgorithmStep {
  description: string;
  visitedNodes: string[];   // Các nút đã duyệt xong (Màu Xanh - VISITED)
  currentNodeId?: string;   // Nút đang xét hiện tại (Màu Vàng - PROCESSING) <--- THÊM DÒNG NÀY
  selectedEdges: string[]; //selectedEdges: { source: string; target: string }[];
  structure?: string[];
}


export interface Node {
  id: string;
  x: number;
  y: number;
  state: NodeState;
}

export interface Edge {
  id: string;
  source: string; // Node ID
  target: string; // Node ID
  weight: number;
  flow?: number; // For Max Flow
  capacity?: number; // For Max Flow
  state: EdgeState;
}

export enum NodeState {
  DEFAULT = 'default',
  PROCESSING = 'processing',
  COMMITTED = 'committed',
  VISITED = 'visited'
}

export enum EdgeState {
  DEFAULT = 'default',
  TRAVERSED = 'traversed', // Part of path
  REJECTED = 'rejected', // Cycle or invalid
  WARNING = 'warning', // Bridge
}

export enum ToolMode {
  SELECT = 'SELECT',
  ADD_NODE = 'ADD_NODE',
  ADD_EDGE = 'ADD_EDGE',
  DELETE = 'DELETE',
  EDIT_WEIGHT = 'EDIT_WEIGHT'
}

// Đã bổ sung KRUSKAL và HIERHOLZER để khớp với constants.ts
export enum AlgorithmType {
  NONE = 'NONE',
  DIJKSTRA = 'DIJKSTRA',
  BFS = 'BFS',
  DFS = 'DFS',
  PRIM = 'PRIM',
  KRUSKAL = 'KRUSKAL',
  FORD_FULKERSON = 'FORD_FULKERSON',
  FLEURY = 'FLEURY',
  HIERHOLZER = 'HIERHOLZER',
  BIPARTITE = 'BIPARTITE'
}

export interface LogEntry {
  id: number;
  step: number;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
}

// Cấu trúc lưu trữ từng bước chạy (Snapshot) để làm Animation
export interface AlgorithmFrame {
  description: string;
  nodes: Record<string, NodeState>; // Trạng thái của các đỉnh tại bước này
  edges: Record<string, EdgeState>; // Trạng thái của các cạnh tại bước này
  stack?: string[]; // IDs cho DFS
  queue?: string[]; // IDs cho BFS
  mst?: string[]; // Edge IDs cho Prim/Kruskal
  log: string;
}