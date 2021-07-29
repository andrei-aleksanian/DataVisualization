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
        <Point {...p} key={`${p.x}${p.y}${p.z}`} />
      ))}
    </>
  );
}
