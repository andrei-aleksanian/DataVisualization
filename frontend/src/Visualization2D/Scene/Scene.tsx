import { Data2DColored, Data3DColored } from '../../types/Data';

export interface PointProps {
  x: number;
  y: number;
  z: number;
  color: string;
}

export const Point = ({ x, y, z, color }: PointProps) => (
  <mesh position={[x, y, z]} rotation={[Math.PI * 0.5, 0, 0]}>
    <cylinderBufferGeometry attach="geometry" args={[0.5, 0.5, 0.15, 32]} />
    <meshStandardMaterial attach="material" color={color} />
  </mesh>
);

export interface SceneProps {
  data: Data2DColored | Data3DColored;
}

export default function Scene({ data: { colors, points } }: SceneProps) {
  return (
    <>
      <ambientLight color="#fff" intensity={1.0} />
      {points.map((p, i) => (
        <Point x={p[0]} y={p[1]} z={p[2]} color={`#${colors[i]}`} key={`${p[0]}${p[1]}${p[2]}`} />
      ))}
    </>
  );
}
