import { Data3D, Data2D } from '../../types/Data';

export interface PointProps {
  x: number;
  y: number;
  z: number;
}

export const Point = ({ x, y, z }: PointProps) => (
  <mesh position={[x, y, z]} rotation={[Math.PI * 0.5, 0, 0]}>
    <cylinderBufferGeometry attach="geometry" args={[0.5, 0.5, 0.15, 32]} />
    <meshStandardMaterial attach="material" color="blue" />
  </mesh>
);

export interface SceneProps {
  data: Data2D | Data3D;
}

export default function Scene({ data }: SceneProps) {
  return (
    <>
      <ambientLight color="#fff" intensity={1.0} />
      {data.points.map((p) => (
        <Point x={p[0]} y={p[1]} z={p[2]} key={`${p[0]}${p[1]}${p[2]}`} />
      ))}
    </>
  );
}
