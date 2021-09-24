import React, { useState } from 'react';
// import { ThreeEvent } from '@react-three/fiber';
import { Html } from '@react-three/drei';

export interface PointProps {
  x: number;
  y: number;
  z: number;
  color: string;
  radius: number;
  dimension2D: boolean;
  isPreservation: boolean;
}

const Point = ({ x, y, z, color, radius, dimension2D, isPreservation }: PointProps) => {
  const [hovered, setHover] = useState(false);
  const click = () => {
    setHover((prev) => !prev);
  };

  return (
    <mesh position={[x, y, z]} rotation={[Math.PI / 2, 0, 0]} onPointerDown={click}>
      {hovered && isPreservation && (
        <Html>
          <div
            onClick={() => click()}
            style={{
              backgroundColor: color,
              width: '20px',
              height: '20px',
              display: 'block',
              borderRadius: '5px',
              marginTop: '10px',
            }}
          />
        </Html>
      )}
      {dimension2D ? (
        <cylinderBufferGeometry attach="geometry" args={[radius, radius, 0.15, 32]} />
      ) : (
        <sphereBufferGeometry attach="geometry" args={[radius, 16, 16]} />
      )}
      <meshStandardMaterial attach="material" color={isPreservation && !hovered ? '#AAAAAA' : color} />
    </mesh>
  );
};

export default Point;
