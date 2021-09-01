import { useRef } from 'react';

export interface PointProps {
  x: number;
  y: number;
  z: number;
  color: string;
  radius: number;
  dimension2D: boolean;
}

const Point = ({ x, y, z, color, radius, dimension2D }: PointProps) => {
  const pointsGroup = useRef();

  return (
    <group ref={pointsGroup}>
      <mesh position={[x, y, z]} rotation={[Math.PI / 2, 0, 0]}>
        {dimension2D ? (
          <cylinderBufferGeometry attach="geometry" args={[radius, radius, 0.15, 32]} />
        ) : (
          <sphereBufferGeometry attach="geometry" args={[radius, 16, 16]} />
        )}
        <meshStandardMaterial attach="material" color={color} />
      </mesh>
    </group>
  );
};

export default Point;
