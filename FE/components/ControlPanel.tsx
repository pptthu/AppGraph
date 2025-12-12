import React from 'react';
import { AlgorithmType, Node, AlgorithmStep } from '../types';
import { ALGORITHMS } from '../constants';

import { AlertCircle } from 'lucide-react'; 

interface ControlPanelProps {
  nodes: Node[];
  selectedAlgo: AlgorithmType;
  setAlgorithm: (algo: AlgorithmType) => void;
  startNode: string | null;
  setStartNode: (id: string) => void;
  endNode: string | null;
  setEndNode: (id: string) => void;

  // --- Props quan trọng ---
  isDirected: boolean; 
  hasStarted: boolean;
  onRunSimulation: () => void;
  steps: AlgorithmStep[];
  currentStepIndex: number;
  setCurrentStepIndex: (idx: number) => void;
  isPlaying: boolean;
  setIsPlaying: (val: boolean) => void;
  onReset: () => void;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  nodes,
  selectedAlgo,
  setAlgorithm,
  startNode,
  setStartNode,
  endNode,
  setEndNode,
  isDirected, 
  hasStarted,
  onRunSimulation,
  steps,
  currentStepIndex,
  setCurrentStepIndex,
  isPlaying,
  setIsPlaying,
  onReset
}) => {

  // --- Hàm kiểm tra lỗi logic (Validation) ---
  const getValidationError = (): string | null => {
    // 1. Prim & Kruskal chỉ chạy trên Vô Hướng
    if (isDirected && (selectedAlgo === AlgorithmType.PRIM || selectedAlgo === AlgorithmType.KRUSKAL)) {
      return "Thuật toán này chỉ hỗ trợ Đồ thị Vô hướng.";
    }
    // 2. Ford-Fulkerson & Fleury/Hierholzer (thường) chạy trên Có hướng hoặc có luật riêng
    // Ở đây ta chặn Ford-Fulkerson trên Vô hướng
    if (!isDirected && selectedAlgo === AlgorithmType.FORD_FULKERSON) {
      return "Thuật toán này chỉ hỗ trợ Đồ thị Có hướng.";
    }
    return null;
  };

  const validationError = getValidationError();

  return (
    <div className="w-80 bg-white border-l border-slate-200 flex flex-col shadow-lg z-20 h-full">
      <div className="p-4 border-b border-slate-200 bg-slate-50">
        <h2 className="font-bold text-slate-800 text-lg">THUẬT TOÁN</h2>
      </div>

      <div className="p-4 flex flex-col gap-6 overflow-y-auto flex-1">
        {/* 1. Chọn Thuật toán */}
        <div className="flex flex-col gap-2">
          <select 
            className="w-full p-2.5 bg-slate-700 text-white rounded-md text-sm font-medium outline-none"
            value={selectedAlgo}
            onChange={(e) => {
              setAlgorithm(e.target.value as AlgorithmType);
              onReset();
            }}
          >
            <option value={AlgorithmType.NONE}>-- Chọn thuật toán --</option>
            {ALGORITHMS.filter(a => a.value !== AlgorithmType.NONE).map(algo => (
              <option key={algo.value} value={algo.value}>{algo.label}</option>
            ))}
          </select>
        </div>

        {/* 2. Chọn Nút (Ẩn nếu có lỗi hoặc không cần thiết) */}
        {!validationError && selectedAlgo !== AlgorithmType.NONE && (
          <div className="flex flex-col gap-4">
             {(selectedAlgo !== AlgorithmType.BIPARTITE && selectedAlgo !== AlgorithmType.KRUSKAL) && (
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-slate-700">Nút bắt đầu:</label>
                <select 
                  className="w-32 p-1.5 border border-slate-300 rounded text-sm bg-white"
                  value={startNode || ''}
                  onChange={(e) => setStartNode(e.target.value)}
                  disabled={hasStarted}
                >
                  <option value="">Chọn...</option>
                  {nodes.map(n => <option key={n.id} value={n.id}>{n.id}</option>)}
                </select>
              </div>
            )}
            
            {(selectedAlgo === AlgorithmType.DIJKSTRA || selectedAlgo === AlgorithmType.FORD_FULKERSON) && (
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-slate-700">Nút đích:</label>
                <select 
                  className="w-32 p-1.5 border border-slate-300 rounded text-sm bg-white"
                  value={endNode || ''}
                  onChange={(e) => setEndNode(e.target.value)}
                  disabled={hasStarted}
                >
                  <option value="">Chọn...</option>
                  {nodes.map(n => <option key={n.id} value={n.id}>{n.id}</option>)}
                </select>
              </div>
            )}
          </div>
        )}

        {/* KHU VỰC ĐIỀU KHIỂN */}
        <div className="mt-2">
          {/* NẾU CÓ LỖI -> HIỆN THÔNG BÁO ĐỎ */}
          {validationError ? (
            <div className="bg-red-50 border border-red-200 text-red-600 p-3 rounded-lg text-sm flex items-start gap-2 animate-in fade-in zoom-in">
              <AlertCircle size={18} className="shrink-0 mt-0.5" />
              <span>{validationError}</span>
            </div>
          ) : (
            // NẾU KHÔNG CÓ LỖI -> HIỆN NÚT CHẠY
            <>
              {!hasStarted ? (
                selectedAlgo !== AlgorithmType.NONE && (
                  <button 
                    onClick={onRunSimulation}
                    disabled={
                      (!startNode && selectedAlgo !== AlgorithmType.BIPARTITE && selectedAlgo !== AlgorithmType.KRUSKAL) ||
                      (!endNode && (selectedAlgo === AlgorithmType.DIJKSTRA || selectedAlgo === AlgorithmType.FORD_FULKERSON))
                    }
                    className={`w-full py-3 rounded shadow-md transition-colors font-bold text-white
                      ${
                        ((!startNode && selectedAlgo !== AlgorithmType.BIPARTITE && selectedAlgo !== AlgorithmType.KRUSKAL) ||
                        (!endNode && (selectedAlgo === AlgorithmType.DIJKSTRA || selectedAlgo === AlgorithmType.FORD_FULKERSON)))
                          ? 'bg-slate-300 cursor-not-allowed text-slate-500' 
                          : 'bg-[#E68A00] hover:bg-[#cc7a00]'
                      }`}
                  >
                    Chạy Mô Phỏng
                  </button>
                )
              ) : (
                // ĐANG CHẠY -> HIỆN SLIDER
                <div className="bg-slate-50 p-4 rounded border border-slate-200">
                    <div className="flex justify-between items-end mb-2">
                        <span className="text-sm font-bold text-slate-700">
                            Bước: {currentStepIndex + 1}/{steps.length}
                        </span>
                        <button 
                            onClick={() => setIsPlaying(!isPlaying)} 
                            className="text-blue-600 font-bold text-sm hover:underline"
                        >
                            {isPlaying ? 'Tạm dừng' : 'Tiếp tục'}
                        </button>
                    </div>
                    <input 
                        type="range" 
                        min="0" 
                        max={Math.max(0, steps.length - 1)} 
                        value={currentStepIndex} 
                        onChange={(e) => {
                            setCurrentStepIndex(Number(e.target.value));
                            setIsPlaying(false);
                        }}
                        className="w-full h-2 bg-slate-300 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                    <div className="mt-4 p-3 bg-white border border-slate-200 rounded text-sm text-slate-800 min-h-[3.5rem] flex items-center">
                        {steps[currentStepIndex]?.description || "Hoàn tất."}
                    </div>
                    <div className="mt-2 text-right">
                       <button onClick={onReset} className="text-xs text-red-500 hover:underline">
                          Thiết lập lại (Reset)
                       </button>
                    </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};