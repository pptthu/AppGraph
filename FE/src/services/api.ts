import axios from 'axios';
import { Node, Edge, AlgorithmType } from '../../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

export const runAlgorithm = async (
  algo: AlgorithmType,
  nodes: Node[],
  edges: Edge[],
  isDirected: boolean,
  startNode?: string,
  endNode?: string
) => {
  try {
    const response = await axios.post(`${API_URL}/solve`, {
      algorithm: algo,
      graph: { nodes, edges, isDirected },
      startNode,
      endNode
    });
    return response.data.steps; 
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};