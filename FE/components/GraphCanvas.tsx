import React, { useRef, useState } from 'react';
import { Node, Edge, ToolMode, NodeState, EdgeState } from '../types';
import { COLORS, EDGE_COLORS } from '../constants';

interface GraphCanvasProps {
  nodes: Node[];
  edges: Edge[];
  isDirected: boolean;
  currentTool: ToolMode;
  onNodeAdd: (x: number, y: number) => void;
  onNodeSelect: (id: string) => void;
  onNodeMove: (id: string, x: number, y: number) => void;
  onEdgeAdd: (sourceId: string, targetId: string) => void;
  onDelete: (type: 'node' | 'edge', id: string) => void;
   onEdgeClick: (edge: Edge) => void;
}

export const GraphCanvas: React.FC<GraphCanvasProps> = ({
  nodes,
  edges,
  isDirected,
  currentTool,
  onNodeAdd,
  onNodeSelect,
  onNodeMove,
  onEdgeAdd,
  onDelete,
  onEdgeClick
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [draggingNode, setDraggingNode] = useState<string | null>(null);
  const [tempEdgeStart, setTempEdgeStart] = useState<{id: string, x: number, y: number} | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Get SVG coordinates
  const getMousePos = (e: React.MouseEvent) => {
    if (!svgRef.current) return { x: 0, y: 0 };
    const CTM = svgRef.current.getScreenCTM();
    if (!CTM) return { x: 0, y: 0 };
    return {
      x: (e.clientX - CTM.e) / CTM.a,
      y: (e.clientY - CTM.f) / CTM.d
    };
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    const { x, y } = getMousePos(e);
    // Background click
    if (e.target === svgRef.current) {
        if (currentTool === ToolMode.ADD_NODE) {
            onNodeAdd(x, y);
        } else if (currentTool === ToolMode.SELECT) {
             // Deselect or Box select logic here
        }
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    const { x, y } = getMousePos(e);
    setMousePos({ x, y });
    
    if (draggingNode && currentTool === ToolMode.SELECT) {
      onNodeMove(draggingNode, x, y);
    }
  };

  const handleMouseUp = () => {
  setDraggingNode(null); // Ngắt trạng thái kéo
  setTempEdgeStart(null); // Ngắt trạng thái nối dây
};

  const onNodeMouseDown = (e: React.MouseEvent, node: Node) => {
     e.stopPropagation();
     if (currentTool === ToolMode.SELECT) {
         setDraggingNode(node.id);
     } else if (currentTool === ToolMode.ADD_EDGE) {
         setTempEdgeStart({ id: node.id, x: node.x, y: node.y });
     } else if (currentTool === ToolMode.DELETE) {
         onDelete('node', node.id);
     }
  };

  const onNodeMouseUp = (e: React.MouseEvent, node: Node) => {
      e.stopPropagation();
      if (currentTool === ToolMode.ADD_EDGE && tempEdgeStart && tempEdgeStart.id !== node.id) {
          onEdgeAdd(tempEdgeStart.id, node.id);
          setTempEdgeStart(null);
      }
  };

  return (
    <div className="flex-1 bg-slate-50 relative overflow-hidden select-none cursor-crosshair">
       {/* Grid Background Pattern */}
       <div 
         className="absolute inset-0 opacity-10 pointer-events-none" 
         style={{ backgroundImage: 'radial-gradient(#475569 1px, transparent 1px)', backgroundSize: '20px 20px' }}
       ></div>

       <svg
         ref={svgRef}
         className="w-full h-full block"
         onMouseDown={handleMouseDown}
         onMouseMove={handleMouseMove}
         onMouseUp={handleMouseUp}
         onMouseLeave={handleMouseUp}
       >
         {/* Arrow Marker Definition */}
         <defs>
           <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
             <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
           </marker>
           <marker id="arrowhead-traversed" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
             <polygon points="0 0, 10 3.5, 0 7" fill="#22c55e" />
           </marker>
         </defs>

         {/* Edges */}
         {edges.map(edge => {
             const startNode = nodes.find(n => n.id === edge.source);
             const endNode = nodes.find(n => n.id === edge.target);
             if (!startNode || !endNode) return null;

             const isTraversed = edge.state === EdgeState.TRAVERSED;
             const markerEnd = isDirected ? (isTraversed ? "url(#arrowhead-traversed)" : "url(#arrowhead)") : undefined;
             const colorClass = EDGE_COLORS[edge.state] || EDGE_COLORS[EdgeState.DEFAULT];

             // Calculate midpoint for text
             const midX = (startNode.x + endNode.x) / 2;
             const midY = (startNode.y + endNode.y) / 2;

             return (
               <g key={edge.id} onClick={(e) => {
                  e.stopPropagation(); 
                  onEdgeClick(edge);
                  }}
                  className="cursor-pointer"
                  >
                  <line 
                    x1={startNode.x} y1={startNode.y}
                    x2={endNode.x} y2={endNode.y}
                    className={`stroke-2 cursor-pointer transition-all duration-300 ${colorClass} hover:stroke-[3px] hover:stroke-indigo-400`}
                    markerEnd={markerEnd}
                  />
                  {/* Edge Weight Background */}
                  <circle cx={midX} cy={midY} r="8" fill="white" stroke="#e2e8f0" strokeWidth="1" />
                  {/* Edge Weight Text */}
                  <text 
                    x={midX} y={midY} 
                    dy="3" 
                    textAnchor="middle" 
                    className="text-[10px] font-bold fill-slate-600 pointer-events-none select-none"
                  >
                    {edge.weight}
                  </text>
               </g>
             );
         })}

         {/* Temp Edge Drawing */}
         {tempEdgeStart && (
             <line 
                x1={tempEdgeStart.x} y1={tempEdgeStart.y}
                x2={mousePos.x} y2={mousePos.y}
                className="stroke-2 stroke-indigo-400 stroke-dashed"
                strokeDasharray="5,5"
             />
         )}

         {/* Nodes */}
         {nodes.map(node => {
            const colorClass = COLORS[node.state] || COLORS[NodeState.DEFAULT];
            return (
              <g 
                key={node.id} 
                transform={`translate(${node.x}, ${node.y})`}
                onMouseDown={(e) => onNodeMouseDown(e, node)}
                onMouseUp={(e) => onNodeMouseUp(e, node)}
                className="cursor-pointer transition-all duration-300"
              >
                {/* Outer Glow for Processing */}
                {node.state === NodeState.PROCESSING && (
                    <circle r="25" className="fill-yellow-100 animate-pulse opacity-50" />
                )}
                {/* Main Node Circle */}
                <circle 
                  r="18" 
                  className={`stroke-2 ${colorClass} transition-colors duration-300 hover:shadow-lg`}
                />
                {/* Node ID Text */}
                <text 
                  dy="4" 
                  textAnchor="middle" 
                  className="text-xs font-bold fill-slate-700 pointer-events-none select-none"
                >
                  {node.id}
                </text>
              </g>
            );
         })}
       </svg>

       {/* Hint Overlay */}
       <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm p-2 rounded border border-slate-200 shadow-sm text-xs text-slate-500 pointer-events-none">
          Công cụ: <span className="font-bold text-indigo-600">{currentTool}</span>
       </div>
    </div>
  );
};