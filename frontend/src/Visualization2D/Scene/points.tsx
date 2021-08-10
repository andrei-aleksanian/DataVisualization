export interface PointProps {
  x: number;
  y: number;
  z: number;
  color: string;
}

export const Point2D = ({ x, y, z, color }: PointProps) => (
  <mesh position={[x, y, z]} rotation={[Math.PI * 0.5, 0, 0]}>
    <cylinderBufferGeometry attach="geometry" args={[0.5, 0.5, 0.15, 32]} />
    <meshStandardMaterial attach="material" color={color} />
  </mesh>
);

export const Point3D = ({ x, y, z, color }: PointProps) => (
  <mesh position={[x, y, z]}>
    <sphereBufferGeometry attach="geometry" args={[0.5, 16, 16]} />
    <meshStandardMaterial attach="material" color={color} />
  </mesh>
);
