export interface PointProps {
  x: number;
  y: number;
  z: number;
  color: string;
  radius: number;
  dimension2D: boolean;
}

const Point = ({ x, y, z, color, radius, dimension2D }: PointProps) => (
  <mesh position={[x, y, z]}>
    {dimension2D ? (
      <cylinderBufferGeometry attach="geometry" args={[radius, radius, 0.15, 32]} />
    ) : (
      <sphereBufferGeometry attach="geometry" args={[radius, 16, 16]} />
    )}
    <meshStandardMaterial attach="material" color={color} />
  </mesh>
);

export default Point;
