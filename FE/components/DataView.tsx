import React, { useState } from 'react';
import { Node, Edge, LogEntry, AlgorithmType } from '../types';

interface DataViewProps {
  nodes: Node[];
  edges: Edge[];
  isDirected: boolean; 
  logs: LogEntry[];
  stack: string[];
  queue: string[];
  currentAlgo: string;
}

// Hàm helper lấy tên cấu trúc dữ liệu dựa trên thuật toán
const getStructureName = (algo: string) => {
  switch (algo) {
    case AlgorithmType.DFS: return 'Ngăn xếp (Stack - LIFO)';
    case AlgorithmType.BFS: 
    case AlgorithmType.BIPARTITE: 
    case AlgorithmType.FORD_FULKERSON: return 'Hàng đợi (Queue - FIFO)';
    case AlgorithmType.DIJKSTRA: 
    case AlgorithmType.PRIM: return 'Hàng đợi ưu tiên (Priority Queue - Min Heap)';
    case AlgorithmType.KRUSKAL: return 'Danh sách cạnh (Sorted List)';
    default: return 'Cấu trúc dữ liệu';
  }
};

export const DataView: React.FC<DataViewProps> = ({ nodes, edges, isDirected, logs, stack, queue, currentAlgo }) => {
  const [activeTab, setActiveTab] = useState<'representation' | 'structures' | 'logs'>('representation');

  // Xác định dữ liệu nào để hiển thị (DFS dùng stack, còn lại dùng queue như đã quy ước ở App.tsx)
  const currentStructureData = currentAlgo === AlgorithmType.DFS ? stack : queue;

  return (
    <div className="h-64 bg-white border-t border-slate-200 flex flex-col shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-10">
      {/* Tabs Header */}
      <div className="flex border-b border-slate-200 bg-slate-50 px-4">
        <button 
          onClick={() => setActiveTab('representation')}
          className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${activeTab === 'representation' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          Biểu diễn Đồ thị
        </button>
        <button 
          onClick={() => setActiveTab('structures')}
          className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${activeTab === 'structures' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          Cấu trúc Dữ liệu
        </button>
        <button 
          onClick={() => setActiveTab('logs')}
          className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${activeTab === 'logs' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          Nhật ký Thực thi
        </button>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-auto p-0 bg-slate-50/50">
        
        {/* TAB 1: Representation (chia 3 cột) */}
        {activeTab === 'representation' && (
          <div className="flex h-full">
            
            {/* CỘT 1: MA TRẬN KỀ */}
            <div className="w-1/3 p-4 border-r border-slate-200 overflow-auto">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">MA TRẬN KỀ</h3>
              <table className="w-full text-center text-sm border-collapse">
                <thead>
                  <tr>
                    <th className="p-1"></th>
                    {nodes.map(n => <th key={n.id} className="p-1 text-slate-600 font-medium bg-slate-100 border border-slate-200">{n.id}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {nodes.map(source => (
                    <tr key={source.id}>
                      <td className="p-1 text-slate-600 font-medium bg-slate-100 border border-slate-200">{source.id}</td>
                      {nodes.map(target => {
                        // Tìm cạnh (nếu vô hướng thì tìm cả 2 chiều)
                        const edge = edges.find(e => 
                            (e.source === source.id && e.target === target.id) || 
                            (!isDirected && e.source === target.id && e.target === source.id)
                        );
                        const weight = edge ? edge.weight : (source.id === target.id ? 0 : '∞');
                        return (
                          <td key={`${source.id}-${target.id}`} className="p-1 border border-slate-200 bg-white">
                             <span className={weight !== '∞' && weight !== 0 ? 'font-bold text-indigo-600' : 'text-slate-300'}>
                               {weight}
                             </span>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            {/* CỘT 2: DANH SÁCH KỀ */}
            <div className="w-1/3 p-4 border-r border-slate-200 overflow-auto">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">DANH SÁCH KỀ</h3>
              <div className="flex flex-col gap-2">
                {nodes.map(n => {
                   // Tìm các đỉnh kề
                   const neighbors = edges.filter(e => 
                       e.source === n.id || (!isDirected && e.target === n.id)
                   ).map(e => ({
                       target: e.source === n.id ? e.target : e.source,
                       weight: e.weight
                   }));

                   return (
                     <div key={n.id} className="flex items-center gap-2 text-sm">
                       <div className="w-8 h-8 rounded bg-slate-200 flex items-center justify-center font-bold text-slate-700 shrink-0">{n.id}</div>
                       <div className="text-slate-400">→</div>
                       {neighbors.length === 0 ? <span className="text-slate-400 italic">Trống</span> : (
                         <div className="flex flex-wrap gap-2">
                           {neighbors.map((neighbor, idx) => (
                             <div key={idx} className="px-2 py-1 bg-white border border-slate-300 rounded shadow-sm">
                               {neighbor.target} <span className="text-xs text-slate-400 ml-1">({neighbor.weight})</span>
                             </div>
                           ))}
                         </div>
                       )}
                     </div>
                   )
                })}
              </div>
            </div>

            {/* CỘT 3: DANH SÁCH CẠNH */}
            <div className="w-1/3 p-4 overflow-auto bg-slate-100/50">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">DANH SÁCH CẠNH</h3>
                <div className="grid grid-cols-1 gap-2">
                    {edges.length === 0 && <span className="text-slate-400 italic text-sm">Chưa có cạnh nào</span>}
                    {edges.map(e => (
                        <div key={e.id} className="flex items-center justify-between bg-white p-2 rounded border border-slate-200 shadow-sm text-sm">
                            <div className="flex items-center gap-2 font-mono">
                                <span className="font-bold text-slate-700">{e.source}</span>
                                <span className="text-slate-400 text-xs">
                                    {isDirected ? '──▶' : '───'}
                                </span>
                                <span className="font-bold text-slate-700">{e.target}</span>
                            </div>
                            <div className="text-xs bg-slate-100 px-2 py-1 rounded text-slate-600">
                                w: <span className="font-bold text-indigo-600">{e.weight}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

          </div>
        )}

        {/* TAB 2: Data Structures  */}
        {activeTab === 'structures' && (
          <div className="flex h-full p-6 gap-8 items-start">
             <div className="flex flex-col gap-2 w-full">
                {/* Tiêu đề động dựa theo thuật toán */}
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                  {getStructureName(currentAlgo)}
                </h3>
                
                <div className="h-24 w-full bg-white border border-slate-300 rounded-lg p-4 flex items-center gap-2 overflow-x-auto shadow-inner">
                   {currentStructureData.length === 0 && (
                     <span className="text-slate-400 text-sm italic w-full text-center">Rỗng</span>
                   )}
                   {currentStructureData.map((itemId, idx) => (
                      <div key={idx} className="min-w-[40px] px-3 h-10 bg-yellow-100 border border-yellow-400 text-yellow-800 rounded flex items-center justify-center font-bold shadow-sm whitespace-nowrap animate-in fade-in zoom-in duration-300">
                        {itemId}
                      </div>
                   ))}
                </div>
                
                <p className="text-xs text-slate-400 mt-1">
                  {currentAlgo === AlgorithmType.DFS 
                    ? 'Phần tử được thêm và lấy ra từ cùng một phía (LIFO).' 
                    : 'Dữ liệu được xử lý theo thứ tự hoặc độ ưu tiên.'}
                </p>
             </div>
          </div>
        )}

        {/* TAB 3: Logs */}
        {activeTab === 'logs' && (
          <div className="h-full p-2 font-mono text-sm overflow-auto bg-slate-900 text-slate-300">
             {logs.length === 0 && <div className="text-slate-600 p-2">Đang chờ thuật toán bắt đầu...</div>}
             {logs.map((log) => (
               <div key={log.id} className={`p-1 border-b border-slate-800 flex gap-3 ${
                 log.type === 'error' ? 'text-red-400' : 
                 log.type === 'success' ? 'text-green-400' :
                 log.type === 'warning' ? 'text-orange-400' : 'text-slate-300'
               }`}>
                 <span className="text-slate-500 w-8 shrink-0">#{log.step}</span>
                 <span>{log.message}</span>
               </div>
             ))}
             <div className="h-4"></div> 
          </div>
        )}
      </div>
    </div>
  );
};