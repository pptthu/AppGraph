// src/constants.ts
import { AlgorithmType, NodeState, EdgeState } from './types';

export const COLORS = {
  [NodeState.DEFAULT]: 'fill-slate-100 stroke-slate-400',
  [NodeState.PROCESSING]: 'fill-yellow-200 stroke-yellow-500', // Đang xét
  [NodeState.COMMITTED]: 'fill-green-200 stroke-green-500',    // Đã duyệt xong/Kết quả
  [NodeState.VISITED]: 'fill-blue-100 stroke-blue-400',        // Đã nằm trong hàng đợi/ngăn xếp
};

export const EDGE_COLORS = {
  [EdgeState.DEFAULT]: 'stroke-slate-400',
  [EdgeState.TRAVERSED]: 'stroke-green-500', // Cạnh thuộc đường đi/Cây khung/Luồng
  [EdgeState.REJECTED]: 'stroke-red-300',    // Cạnh bị loại (nếu cần)
  [EdgeState.WARNING]: 'stroke-orange-400',  // Cạnh gây chu trình (Kruskal) hoặc mâu thuẫn màu
};

export const ALGORITHMS = [
  // Option mặc định
  { value: 'NONE', label: '-- Chọn thuật toán --' },
  
  // Phần Cơ bản (Thịnh làm)
  { value: 'BFS', label: 'Duyệt theo chiều rộng (BFS)' },
  { value: 'DFS', label: 'Duyệt theo chiều sâu (DFS)' },
  { value: 'DIJKSTRA', label: 'Đường đi ngắn nhất (Dijkstra)' },
  { value: 'BIPARTITE', label: 'Kiểm tra đồ thị hai phía (Bipartite)' },

  // Phần Nâng cao (Linh làm & Leader làm)
  { value: 'PRIM', label: 'Cây khung nhỏ nhất (Prim)' },
  { value: 'KRUSKAL', label: 'Cây khung nhỏ nhất (Kruskal)' },
  { value: 'FORD_FULKERSON', label: 'Luồng cực đại (Ford-Fulkerson)' },
  
  // Phần Bonus (Làm sau)
  { value: 'FLEURY', label: 'Chu trình Euler (Fleury)' },
  { value: 'HIERHOLZER', label: 'Chu trình Euler (Hierholzer)' },
];

