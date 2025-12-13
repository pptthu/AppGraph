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

// --- HÀM HELPER: Kiểm tra thuật toán có cần trọng số không ---
const isWeightedAlgorithm = (algo: AlgorithmType) => {
  return [
    AlgorithmType.DIJKSTRA,
    AlgorithmType.PRIM,
    AlgorithmType.KRUSKAL,
    AlgorithmType.FORD_FULKERSON
  ].includes(algo);
};

const App: React.FC = () => {
  // State definitions
  const [editingEdge, setEditingEdge] = useState<Edge | null>(null);
  const [weightInput, setWeightInput] = useState("");
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [isDirected, setIsDirected] = useState(false);
  const [currentTool, setTool] = useState<ToolMode>(ToolMode.SELECT);
  const [selectedAlgo, setSelectedAlgo] = useState<AlgorithmType>(AlgorithmType.NONE);
  const [startNode, setStartNode] = useState<string | null>(null);
  const [endNode, setEndNode] = useState<string | null>(null);
  const [hasStarted, setHasStarted] = useState(false);
  const [steps, setSteps] = useState<AlgorithmStep[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(5);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [stack, setStack] = useState<string[]>([]);
  const [queue, setQueue] = useState<string[]>([]);

  // Actions
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
    let charCode = 65; 

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

  // --- LOGIC TỰ ĐỘNG XỬ LÝ KHI ĐỔI THUẬT TOÁN ---
  useEffect(() => {
    if (selectedAlgo === AlgorithmType.NONE) return;

    const needsWeight = isWeightedAlgorithm(selectedAlgo);

    if (!needsWeight) {
        // Tự động xóa trọng số (về 0)
        setEdges(eds => eds.map(e => ({ ...e, weight: 0 })));
        
        if (currentTool === ToolMode.EDIT_WEIGHT) {
            setTool(ToolMode.SELECT);
        }
        addLog(`Thuật toán ${selectedAlgo} không dùng trọng số. Đã ẩn trọng số & khóa chức năng sửa.`, 'warning');
    }
  }, [selectedAlgo]);

  const handleEdgeClick = (edge: Edge) => {
    if (currentTool === ToolMode.DELETE) {
      handleDelete('edge', edge.id);
    }
    else if (currentTool === ToolMode.EDIT_WEIGHT) {
      if (selectedAlgo !== AlgorithmType.NONE && !isWeightedAlgorithm(selectedAlgo)) {
          alert(`Thuật toán ${selectedAlgo} không hỗ trợ trọng số!`);
          setTool(ToolMode.SELECT);
          return;
      }
      setEditingEdge(edge);
      setWeightInput(edge.weight.toString());
    }
  };

  // --- HÀM SỬA TRỌNG SỐ (ĐÃ THÊM VALIDATE SỐ ÂM) ---
  const saveWeight = () => {
    if (editingEdge) {
      const num = parseFloat(weightInput);
      
      if (isNaN(num)) {
        alert("Vui lòng nhập số hợp lệ!");
        return;
      }

      const isNegative = num < 0;

      // Validate Dijkstra
      if (selectedAlgo === AlgorithmType.DIJKSTRA && isNegative) {
          alert("Lỗi: Dijkstra không hỗ trợ trọng số âm! Vui lòng nhập số >= 0.");
          return;
      }

      // Validate Ford-Fulkerson
      if (selectedAlgo === AlgorithmType.FORD_FULKERSON && isNegative) {
          alert("Lỗi: Dung lượng luồng (Capacity) không được âm! Vui lòng nhập số >= 0.");
          return;
      }

      setEdges(prev => prev.map(e => e.id === editingEdge.id ? { ...e, weight: num } : e));
      addLog(`Đã đổi trọng số cạnh ${editingEdge.source}-${editingEdge.target} thành ${num}`, 'info');
      setEditingEdge(null);
    }
  };

  const handleSaveGraph = () => {
    const graphData = {
      nodes: nodes.map(n => ({ ...n, state: NodeState.DEFAULT })), 
      edges: edges.map(e => ({ ...e, state: EdgeState.DEFAULT })),
      isDirected
    };
    const jsonString = JSON.stringify(graphData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = `graph-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(href);
    addLog("Đã lưu đồ thị thành công.", 'success');
  };

  const handleClearWeights = () => {
      setEdges(eds => eds.map(e => ({ ...e, weight: 0 }))); 
      addLog("Đã xóa trọng số (về 0) cho đồ thị không trọng số.", 'info');
  };

  const handleRunSimulation = async () => {
    if (isDirected && (selectedAlgo === AlgorithmType.PRIM || selectedAlgo === AlgorithmType.KRUSKAL)) return;
    if (!isDirected && selectedAlgo === AlgorithmType.FORD_FULKERSON) return; 

    try {
      addLog(`Đang gửi yêu cầu thuật toán ${selectedAlgo} lên server...`, 'info');
      const realSteps = await runAlgorithm(selectedAlgo, nodes, edges, isDirected, startNode || undefined, endNode || undefined);

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
      const errorMessage = error.response?.data?.message || error.message || "Lỗi không xác định";
      addLog(`Lỗi Server: ${errorMessage}`, 'error');
    }
  };

  // Effects
  useEffect(() => {
    let interval: any;
    if (isPlaying && hasStarted) {
      interval = setInterval(() => {
        setCurrentStepIndex(prev => { return prev < steps.length - 1 ? prev + 1 : prev; });
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [isPlaying, hasStarted, steps.length]);

  useEffect(() => {
    if (hasStarted && steps.length > 0 && currentStepIndex === steps.length - 1 && isPlaying) {
      setIsPlaying(false);
      addLog("Mô phỏng hoàn tất.", 'success'); 
    }
  }, [currentStepIndex, hasStarted, steps.length, isPlaying]);

  useEffect(() => {
    if (!hasStarted || steps.length === 0) return;
    const currentStep = steps[currentStepIndex];
    setNodes(nds => nds.map(n => {
      let newState = NodeState.DEFAULT;
      if (currentStep.visitedNodes.includes(n.id)) newState = NodeState.VISITED;
      if (n.id === currentStep.currentNodeId) newState = NodeState.PROCESSING;
      return { ...n, state: newState };
    }));
    setEdges(eds => eds.map(e => {
      const isSelected = currentStep.selectedEdges.some(se =>
        (se.source === e.source && se.target === e.target) ||
        (!isDirected && se.source === e.target && se.target === e.source)
      );
      return { ...e, state: isSelected ? EdgeState.TRAVERSED : EdgeState.DEFAULT };
    }));
    if (currentStep.structure) {
      if (selectedAlgo === AlgorithmType.DFS) {
        setStack(currentStep.structure); setQueue([]);
      } else {
        setQueue(currentStep.structure); setStack([]);
      }
    } else {
      setStack([]); setQueue([]);
    }
    // --- 4. CẬP NHẬT LOG 
    // Logic: Nếu bước hiện tại có log và log đó chưa được ghi, hãy ghi vào bảng
    if (currentStep.log) {
        setLogs(prevLogs => {
            // Kiểm tra xem log cuối cùng có trùng nội dung không để tránh spam
            const lastLog = prevLogs[prevLogs.length - 1];
            if (lastLog && lastLog.message === currentStep.log) {
                return prevLogs;
            }
            
            // Thêm log mới vào danh sách
            return [...prevLogs, {
                id: Date.now(),
                step: currentStepIndex + 1,
                message: currentStep.log,
                type: currentStep.error ? 'error' : 'info' // Nếu backend báo error=True thì hiện màu đỏ
            }];
        });
    }

  }, [currentStepIndex, hasStarted, steps, isDirected, selectedAlgo]);

  const handleNodeMove = (id: string, x: number, y: number) => {
    setNodes(nodes.map(n => n.id === id ? { ...n, x, y } : n));
  };

  const handleNodeAdd = (x: number, y: number) => {
    const newId = String.fromCharCode(65 + nodes.length);
    setNodes([...nodes, { id: newId, x, y, state: NodeState.DEFAULT }]);
  };

  const isWeightDisabled = selectedAlgo !== AlgorithmType.NONE && !isWeightedAlgorithm(selectedAlgo);

  const handleEdgeAdd = (sourceId: string, targetId: string) => {
    if (sourceId === targetId) return;
    if (edges.some(e => 
        (e.source === sourceId && e.target === targetId) ||
        (!isDirected && e.source === targetId && e.target === sourceId)
    )) return;
    
    const defaultWeight = isWeightDisabled ? 0 : 1;
    setEdges([...edges, { id: `e-${sourceId}-${targetId}`, source: sourceId, target: targetId, weight: defaultWeight, state: EdgeState.DEFAULT }]);
  };

  return (
    <div className="flex h-screen w-screen bg-slate-100 text-slate-900 overflow-hidden font-sans">
      <Toolbar
        isDirected={isDirected}
        setIsDirected={setIsDirected}
        currentTool={currentTool}
        setTool={setTool}
        onClear={handleClear}
        onRandom={handleRandom}
        onSave={handleSaveGraph}
        onClearWeights={handleClearWeights}
        isWeightDisabled={isWeightDisabled} 
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
            onDelete={(type, id) => handleDelete(type, id)}
            onEdgeClick={handleEdgeClick}
          />
        </div>
        <DataView nodes={nodes} edges={edges} isDirected={isDirected} logs={logs} stack={stack} queue={queue} currentAlgo={selectedAlgo} />
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

      {editingEdge && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-80 animate-in fade-in zoom-in duration-200">
            <h3 className="text-lg font-bold mb-4 text-slate-800">Sửa Trọng Số</h3>
            <p className="text-sm text-slate-600 mb-2">Cạnh: <span className="font-bold">{editingEdge.source}</span> - <span className="font-bold">{editingEdge.target}</span></p>
            <input type="number" value={weightInput} onChange={(e) => setWeightInput(e.target.value)} className="w-full p-2 border border-slate-300 rounded mb-4 focus:ring-2 focus:ring-indigo-500 outline-none" autoFocus onKeyDown={(e) => e.key === 'Enter' && saveWeight()} />
            <div className="flex justify-end gap-2">
              <button onClick={() => setEditingEdge(null)} className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded font-medium">Hủy</button>
              <button onClick={saveWeight} className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 font-medium">Lưu</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default App;