import React, { useState, useEffect } from 'react';
import { Toolbar } from './components/Toolbar';
import { ControlPanel } from './components/ControlPanel';
import { DataView } from './components/DataView';
import { GraphCanvas } from './components/GraphCanvas';
import {
  Node, Edge, ToolMode, AlgorithmType,
  NodeState, EdgeState, LogEntry, AlgorithmStep
} from './types';
import { runAlgorithm } from './src/services/api';

const App: React.FC = () => {
  // ==========================================================
  // 1. KHAI BÁO STATE
  // ==========================================================
  
  // State cho Modal Sửa Trọng Số
  const [editingEdge, setEditingEdge] = useState<Edge | null>(null);
  const [weightInput, setWeightInput] = useState("");

  // --- Graph State ---
  const [nodes, setNodes] = useState<Node[]>([]); // <-- Sửa thành mảng rỗng []
  const [edges, setEdges] = useState<Edge[]>([]);
  const [isDirected, setIsDirected] = useState(false);

  // --- UI State ---
  const [currentTool, setTool] = useState<ToolMode>(ToolMode.SELECT);

  // --- Algorithm Selection State ---
  const [selectedAlgo, setSelectedAlgo] = useState<AlgorithmType>(AlgorithmType.NONE);
  const [startNode, setStartNode] = useState<string | null>(null);
  const [endNode, setEndNode] = useState<string | null>(null);

  // --- Algorithm Execution State ---
  const [hasStarted, setHasStarted] = useState(false);
  const [steps, setSteps] = useState<AlgorithmStep[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(5);

  // --- Data View State ---
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [stack, setStack] = useState<string[]>([]);
  const [queue, setQueue] = useState<string[]>([]);

  // ==========================================================
  // 2. CÁC HÀM XỬ LÝ (ACTIONS)
  // ==========================================================

  const addLog = (message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info') => {
    setLogs(prev => [...prev, { id: Date.now(), step: prev.length + 1, message, type }]);
  };

  const handleReset = () => {
    setHasStarted(false);
    setSteps([]);
    setCurrentStepIndex(0);
    setIsPlaying(false);
    setStack([]);
    setQueue([]);
    setNodes(nds => nds.map(n => ({ ...n, state: NodeState.DEFAULT })));
    setEdges(eds => eds.map(e => ({ ...e, state: EdgeState.DEFAULT })));
    addLog("Đã thiết lập lại trạng thái.", 'info');
  };

  const handleClear = () => {
    handleReset();
    setNodes([]);
    setEdges([]);
    setLogs([]);
    setStartNode(null);
    setEndNode(null);
    setSelectedAlgo(AlgorithmType.NONE);
  };

  const handleRandom = () => {
    handleClear();
    const newNodes: Node[] = [];
    const newEdges: Edge[] = [];
    const rows = 3;
    const cols = 4;
    let charCode = 65; // 'A'

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const id = String.fromCharCode(charCode++);
        newNodes.push({
          id,
          x: 150 + c * 150 + Math.random() * 20,
          y: 100 + r * 150 + Math.random() * 20,
          state: NodeState.DEFAULT
        });
      }
    }

    newNodes.forEach((n, i) => {
      if (i + 1 < newNodes.length && (i + 1) % cols !== 0 && Math.random() > 0.3) {
        newEdges.push({
          id: `e-${n.id}-${newNodes[i + 1].id}`,
          source: n.id,
          target: newNodes[i + 1].id,
          weight: Math.floor(Math.random() * 10) + 1,
          state: EdgeState.DEFAULT
        });
      }
      if (i + cols < newNodes.length && Math.random() > 0.3) {
        newEdges.push({
          id: `e-${n.id}-${newNodes[i + cols].id}`,
          source: n.id,
          target: newNodes[i + cols].id,
          weight: Math.floor(Math.random() * 10) + 1,
          state: EdgeState.DEFAULT
        });
      }
    });

    setNodes(newNodes);
    setEdges(newEdges);
    addLog("Đã tạo đồ thị ngẫu nhiên.", 'success');
  };

  // Hàm xóa (Node hoặc Edge)
  const handleDelete = (type: 'node' | 'edge', id: string) => {
    if (type === 'node') {
      setNodes(nodes.filter(n => n.id !== id));
      setEdges(edges.filter(e => e.source !== id && e.target !== id));
      if (startNode === id) setStartNode(null);
      if (endNode === id) setEndNode(null);
    } else {
      setEdges(edges.filter(e => e.id !== id));
    }
  };

  // Hàm xử lý Click vào Cạnh
  const handleEdgeClick = (edge: Edge) => {
    if (currentTool === ToolMode.DELETE) {
      handleDelete('edge', edge.id);
    }
    else if (currentTool === ToolMode.EDIT_WEIGHT) {
      setEditingEdge(edge);
      setWeightInput(edge.weight.toString());
    }
  };

  // Hàm Lưu Trọng Số (cho Modal)
  const saveWeight = () => {
    if (editingEdge) {
      const num = parseFloat(weightInput);
      if (!isNaN(num)) {
        setEdges(prev => prev.map(e => e.id === editingEdge.id ? { ...e, weight: num } : e));
        addLog(`Đã đổi trọng số cạnh ${editingEdge.source}-${editingEdge.target} thành ${num}`, 'info');
        setEditingEdge(null);
      } else {
        alert("Vui lòng nhập số hợp lệ!");
      }
    }
  };

  // --- Xử lý Lưu File ---
  const handleSaveGraph = () => {
    const graphData = {
      nodes: nodes.map(n => ({ ...n, state: NodeState.DEFAULT })), // Reset trạng thái màu khi lưu
      edges: edges.map(e => ({ ...e, state: EdgeState.DEFAULT })),
      isDirected
    };

    const jsonString = JSON.stringify(graphData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const href = URL.createObjectURL(blob);

    // Tạo thẻ a ảo để kích hoạt tải xuống
    const link = document.createElement('a');
    link.href = href;
    link.download = `graph-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(href);

    addLog("Đã lưu đồ thị thành công.", 'success');
  };

  // ==========================================================
  // 3. LOGIC CHẠY MÔ PHỎNG
  // ==========================================================

  const handleRunSimulation = async () => {
    // 1. Kiểm tra Ràng buộc
    if (isDirected && (selectedAlgo === AlgorithmType.PRIM || selectedAlgo === AlgorithmType.KRUSKAL)) {
      return;
    }
    // Lỗi: Ford-Fulkerson chạy trên Vô hướng (MỚI THÊM)
    if (!isDirected && selectedAlgo === AlgorithmType.FORD_FULKERSON) {
      return; // Chặn
    }

    try {
      // --- GỌI API TỪ BACKEND ---
      addLog(`Đang gửi yêu cầu thuật toán ${selectedAlgo} lên server...`, 'info');

      const realSteps = await runAlgorithm(
        selectedAlgo,
        nodes,
        edges,
        isDirected,
        startNode || undefined,
        endNode || undefined
      );

      if (realSteps && realSteps.length > 0) {
        setSteps(realSteps);
        setHasStarted(true);
        setCurrentStepIndex(0);
        setIsPlaying(true);
        addLog(`Thành công! Đã nhận ${realSteps.length} bước xử lý.`, 'success');
      } else {
        addLog("Thuật toán chạy xong nhưng không trả về bước nào (có thể do đồ thị rỗng hoặc lỗi logic).", 'warning');
      }

    } catch (error: any) {
      console.error("Lỗi gọi API:", error);
      // Hiển thị lỗi chi tiết từ Backend nếu có
      const errorMessage = error.response?.data?.message || error.message || "Lỗi không xác định";
      addLog(`Lỗi Server: ${errorMessage}`, 'error');
    }
  };

  // ==========================================================
  // 4. EFFECTS
  // ==========================================================

  // Effect 1: Chỉ phụ trách việc tăng bước nhảy (Timer)
  useEffect(() => {
    let interval: any;
    if (isPlaying && hasStarted) {
      interval = setInterval(() => {
        setCurrentStepIndex(prev => {
          // Nếu chưa đến cuối thì tăng, đến cuối rồi thì giữ nguyên
          return prev < steps.length - 1 ? prev + 1 : prev;
        });
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [isPlaying, hasStarted, steps.length]);

  // Effect 2: Phụ trách kiểm tra khi nào thì Dừng và Log (Chỉ chạy khi index thay đổi)
  useEffect(() => {
    if (hasStarted && steps.length > 0 && currentStepIndex === steps.length - 1 && isPlaying) {
      setIsPlaying(false); // Dừng chạy
      addLog("Mô phỏng hoàn tất.", 'success'); // Ghi log 1 lần duy nhất
    }
  }, [currentStepIndex, hasStarted, steps.length, isPlaying]);

  // Effect cập nhật màu sắc Đồ thị VÀ Cấu trúc dữ liệu
  useEffect(() => {
    if (!hasStarted || steps.length === 0) return;

    const currentStep = steps[currentStepIndex];

    // 1. Cập nhật màu Node
    setNodes(nds => nds.map(n => {
      let newState = NodeState.DEFAULT;
      if (currentStep.visitedNodes.includes(n.id)) {
        newState = NodeState.VISITED;
      }
      if (n.id === currentStep.currentNodeId) {
        newState = NodeState.PROCESSING;
      }
      return { ...n, state: newState };
    }));

    // 2. Cập nhật màu Edge
    setEdges(eds => eds.map(e => {
      const isSelected = currentStep.selectedEdges.some(se =>
        (se.source === e.source && se.target === e.target) ||
        (!isDirected && se.source === e.target && se.target === e.source)
      );

      return {
        ...e,
        state: isSelected ? EdgeState.TRAVERSED : EdgeState.DEFAULT
      };
    }));

    // 3. CẬP NHẬT CẤU TRÚC DỮ LIỆU (QUAN TRỌNG: Đã thêm mới)
    // Backend gửi về field "structure", ta cần đẩy nó vào state queue hoặc stack
    if (currentStep.structure) {
      if (selectedAlgo === AlgorithmType.DFS) {
        setStack(currentStep.structure);
        setQueue([]);
      } else {
        // Tất cả thuật toán khác (BFS, Prim, Kruskal, Ford...) đều dùng state 'queue' để hiển thị
        setQueue(currentStep.structure);
        setStack([]);
      }
    } else {
      setStack([]);
      setQueue([]);
    }

  }, [currentStepIndex, hasStarted, steps, isDirected, selectedAlgo]);

  // ==========================================================
  // 5. CÁC HÀM VẼ ĐỒ THỊ (NODE, EDGE)
  // ==========================================================

  const handleNodeAdd = (x: number, y: number) => {
    const newId = String.fromCharCode(65 + nodes.length);
    setNodes([...nodes, { id: newId, x, y, state: NodeState.DEFAULT }]);
  };

  const handleEdgeAdd = (sourceId: string, targetId: string) => {
    if (sourceId === targetId) return;
    if (edges.some(e => e.source === sourceId && e.target === targetId)) return;
    setEdges([...edges, {
      id: `e-${sourceId}-${targetId}`,
      source: sourceId,
      target: targetId,
      weight: 1,
      state: EdgeState.DEFAULT
    }]);
  };

  const handleNodeMove = (id: string, x: number, y: number) => {
    setNodes(nodes.map(n => n.id === id ? { ...n, x, y } : n));
  };

  // ==========================================================
  // 6. RENDER
  // ==========================================================

  return (
    <div className="flex h-screen w-screen bg-slate-100 text-slate-900 overflow-hidden font-sans">
      <Toolbar
        isDirected={isDirected}
        setIsDirected={setIsDirected}
        currentTool={currentTool}
        setTool={setTool}
        onClear={handleClear}
        onRandom={handleRandom}
        // Truyền 2 hàm mới
        onSave={handleSaveGraph}
      />

      <div className="flex-1 flex flex-col h-full relative">
        <div className="flex-1 flex relative">
          <GraphCanvas
            nodes={nodes}
            edges={edges}
            isDirected={isDirected}
            currentTool={currentTool}
            onNodeAdd={handleNodeAdd}
            onNodeSelect={(id) => console.log('select', id)}
            onNodeMove={handleNodeMove}
            onEdgeAdd={handleEdgeAdd}
            onDelete={(type, id) => handleDelete(type, id)} // Sửa ở đây để gọi đúng hàm
            onEdgeClick={handleEdgeClick}
          />
        </div>

        <DataView
          nodes={nodes}
          edges={edges}
          isDirected={isDirected}
          logs={logs}
          stack={stack}
          queue={queue}
          currentAlgo={selectedAlgo}
        />
      </div>

      <ControlPanel
        nodes={nodes}
        edges={edges}
        isDirected={isDirected}
        selectedAlgo={selectedAlgo}
        setAlgorithm={setSelectedAlgo}
        startNode={startNode}
        setStartNode={setStartNode}
        endNode={endNode}
        setEndNode={setEndNode}
        hasStarted={hasStarted}
        onRunSimulation={handleRunSimulation}
        steps={steps}
        currentStepIndex={currentStepIndex}
        setCurrentStepIndex={setCurrentStepIndex}
        isPlaying={isPlaying}
        setIsPlaying={setIsPlaying}
        onReset={handleReset}
      />

      {/* MODAL SỬA TRỌNG SỐ */}
      {editingEdge && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-80 animate-in fade-in zoom-in duration-200">
            <h3 className="text-lg font-bold mb-4 text-slate-800">Sửa Trọng Số</h3>
            <p className="text-sm text-slate-600 mb-2">
              Cạnh: <span className="font-bold">{editingEdge.source}</span> - <span className="font-bold">{editingEdge.target}</span>
            </p>
            <input
              type="number"
              value={weightInput}
              onChange={(e) => setWeightInput(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded mb-4 focus:ring-2 focus:ring-indigo-500 outline-none"
              autoFocus
              onKeyDown={(e) => e.key === 'Enter' && saveWeight()}
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setEditingEdge(null)}
                className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded font-medium"
              >
                Hủy
              </button>
              <button
                onClick={saveWeight}
                className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 font-medium"
              >
                Lưu
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;