import React, { useRef } from 'react';
import { 
  MousePointer2, PlusCircle, BetweenHorizonalStart, Trash2, Type, 
  Save, ArrowLeftRight, ArrowRight, Eraser 
} from 'lucide-react';
import { ToolMode } from '../types';

interface ToolbarProps {
  isDirected: boolean;
  setIsDirected: (val: boolean) => void;
  currentTool: ToolMode;
  setTool: (tool: ToolMode) => void;
  onClear: () => void;
  onRandom: () => void;
  onSave: () => void;
  onClearWeights: () => void;
  isWeightDisabled: boolean; // <-- KHAI BÁO PROP MỚI
}

export const Toolbar: React.FC<ToolbarProps> = ({
  isDirected,
  setIsDirected,
  currentTool,
  setTool,
  onClear,
  onRandom,
  onSave,
  onClearWeights,
  isWeightDisabled // <-- LẤY PROP RA
}) => {
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const tools = [
    { mode: ToolMode.SELECT, icon: <MousePointer2 size={20} />, label: "Chọn/Di chuyển" },
    { mode: ToolMode.ADD_NODE, icon: <PlusCircle size={20} />, label: "Thêm Đỉnh" },
    { mode: ToolMode.ADD_EDGE, icon: <BetweenHorizonalStart size={20} />, label: "Thêm Cạnh" },
    
    // Nút Sửa Trọng Số - Tự động Disable nếu không cần
    { 
      mode: ToolMode.EDIT_WEIGHT, 
      icon: <Type size={20} />, 
      label: isWeightDisabled ? "Không dùng trọng số" : "Sửa Trọng Số",
      disabled: isWeightDisabled 
    },
    
    { mode: ToolMode.DELETE, icon: <Trash2 size={20} />, label: "Xóa" },
  ];

  return (
    <div className="w-16 flex flex-col items-center bg-white border-r border-slate-200 py-4 gap-4 z-20 shadow-sm h-full">
      <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-xl mb-4">G</div>
      
      <div className="flex flex-col gap-2 w-full px-2">
        <button 
          onClick={() => setIsDirected(!isDirected)}
          className={`p-2 rounded-lg transition-colors flex flex-col items-center justify-center text-xs font-medium gap-1 ${isDirected ? 'bg-indigo-50 text-indigo-700' : 'bg-slate-50 text-slate-600 hover:bg-slate-100'}`}
          title={isDirected ? "Đồ thị Có hướng" : "Đồ thị Vô hướng"}
        >
          {isDirected ? <ArrowRight size={20} /> : <ArrowLeftRight size={20} />}
          <span className="scale-75">{isDirected ? "Có hướng" : "Vô hướng"}</span>
        </button>
      </div>
      <div className="w-8 h-px bg-slate-200"></div>

      <div className="flex flex-col gap-3 w-full px-2">
        {tools.map((tool) => (
          <button
            key={tool.mode}
            onClick={() => !tool.disabled && setTool(tool.mode)} // Chặn click nếu disabled
            disabled={tool.disabled} // Thuộc tính HTML disabled
            className={`p-2 rounded-lg transition-all group relative 
              ${currentTool === tool.mode ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-500 hover:bg-slate-100'}
              ${tool.disabled ? 'opacity-30 cursor-not-allowed bg-slate-100 text-slate-300' : ''} // Style mờ đi
            `}
          >
            {tool.icon}
            <span className="absolute left-14 top-1/2 -translate-y-1/2 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50">
              {tool.label}
            </span>
          </button>
        ))}
      </div>

      <div className="w-8 h-px bg-slate-200 mt-auto"></div>

      <div className="flex flex-col gap-2 w-full px-2 mb-2">
        {/* Chỉ hiện nút Xóa Trọng Số nếu ĐANG DÙNG trọng số */}
        {!isWeightDisabled && (
          <button 
              onClick={onClearWeights} 
              className="p-2 text-orange-500 hover:bg-orange-50 rounded-lg" 
              title="Đặt lại Trọng số (Về 0)"
          >
            <Eraser size={20} />
          </button>
        )}

        <button onClick={onClear} className="p-2 text-red-500 hover:bg-red-50 rounded-lg" title="Xóa tất cả">
          <Trash2 size={20} />
        </button>
      </div>

      <div className="flex flex-col gap-2 w-full px-2">
        <button onClick={onSave} className="p-2 text-slate-500 hover:bg-slate-100 rounded-lg" title="Lưu đồ thị (JSON)">
          <Save size={20} />
        </button>
      </div>
    </div>
  );
};