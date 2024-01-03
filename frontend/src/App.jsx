import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
 
import 'reactflow/dist/style.css';
 
const initialNodes = [
  { id: '1', position: { x: 300, y: 0 }, data: { label: 'Chiller' } },
  { id: '2', position: { x: 0, y: 100 }, data: { label: 'Heat Exchanger' } },
  { id: '3', position: { x: 200, y: 100 }, data: { label: 'Heat Exchanger' } },
  { id: '4', position: { x: 400, y: 100 }, data: { label: 'Heat Exchanger' } },
  { id: '5', position: { x: 600, y: 100 }, data: { label: 'Heat Exchanger' } },
];
const initialEdges = [{ id: 'e1-2', source: '1', target: '2' },
                      { id: 'e1-3', source: '1', target: '3' },
                      { id: 'e1-4', source: '1', target: '4' },
                      { id: 'e1-5', source: '1', target: '5' },
                      { id: 'e1-6', source: '1', target: '6' },
                      { id: 'e1-7', source: '1', target: '7' },];
 
export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
 
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );
 
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}